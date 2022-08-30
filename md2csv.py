from csv import QUOTE_MINIMAL, writer as csv_writer
from dataclasses import dataclass
from enum import Enum
from io import StringIO
from re import match, sub
from shutil import copyfileobj
from sys import argv
from typing import Callable, Dict, List


class Type(Enum):
    kprim = 'kprim'
    single_choice = 'single_choice'

    @classmethod
    def fromString(cls, string):
        for t in Type:
            if t.value == string:
                return t
        return None

    def num_question_type(self):
        return {
            Type.kprim: 8,
            Type.single_choice: 10
        }[self]

    def num_optional_value(self):
        return {
            Type.kprim: 2048,
            Type.single_choice: None
        }[self]


@dataclass
class Question:
    dir: List[str] = None
    type: Type|None = None
    question: str = ''
    rfs: str = ''
    answers: List[str] = None
    options: Dict = None

    _line: int = 0

    def __init__(self):
        # not allowed to use list (and similar) as default class member value directly
        self.dir = []
        self.answers = []

if len(argv) < 2:
    print('Questions (.md) file required as argument')
    exit()

filename = argv[1]
print(f'Loading `{filename}` ...')
with open(filename, encoding='utf8') as file:
    lines = file.readlines()


questions : List[Question] = []
current_dir: List[str] = []
current_question: Question|None = None
is_comment: bool = False
is_equation: bool = False

options = {
    'kprim_append': '',
    'single_choice_append': ''
}

print('Parsing questions ...')

for line_no, (line, last_line) in enumerate(zip(lines, [''] + lines[:-1])):
    line_empty = line.strip() == ''
    # print(str(line_no+1) + '|\t' + line[:-1])

    def error(msg: str):
        dir = ' / '.join(current_dir)
        print(f'\nERROR: {msg}\nin: {dir}\nline {line_no+1}: {line}')
        exit()

    def parse_option(line: str, question_type: Type|None = None):
        for key in options:
            if question_type is None:
                key_str = f'*{key}*'
            elif key.startswith(question_type.value + '_'):
                key_str = f'*{key[len(question_type.value) + 1:]}*'
            else:
                continue
            if line.startswith(key_str):
                return key, line[len(key_str):].strip()
        return None, None

    # global options at the beginning of the file
    if len(current_dir) == 0 and line.startswith('*'):
        key, value = parse_option(line)
        if key is not None:
            options[key] = value
            # print(f'==> {key}: {value}')
        continue

    # comments
    if line.startswith('~~~'):
        # one-line comment
        if not ( not is_comment and len(line) > 6 and line.rstrip().endswith('~~~') ):
            is_comment = not is_comment
        continue
    elif is_comment:
        # print('==> skip comment line')
        continue

    # equations
    if line.startswith('$$'):
        is_equation = not is_equation
        continue
    elif is_equation:
        # print('==> skip equation line')
        continue

    # horizontal line to separate questions
    elif line.strip() == '---':
        # print('==> skip horizontal line')
        continue

    # empty line
    elif line_empty and current_question is None:
        # print('==> skip empty line')
        continue

    # directory
    elif line.startswith('#'):
        level = match(r'#+[^#]', line).end() - 1
        current_dir = current_dir[:level - 1] + [line[level:].strip()]
        current_question = None
        # print('==> dir ' + str(current_dir))

    # question type
    elif line.startswith('>'):
        if not last_line.startswith('>'):
            questions.append(current_question := Question())
            current_question._line = line_no
            current_question.dir = current_dir.copy()
            current_question.type = Type.fromString(line[1:].strip())
            current_question.options = options.copy()
            # print('==> type ' + current_question.type.name + ' | ' + str(current_question.dir))

        # per question options
        else:
            key, value = parse_option(line[1:].lstrip(), current_question.type)
            if key is not None:
                current_question.options[key] = value
                # print(f'==> {key}: {value}')
                continue

    # empty line
    elif line_empty and current_question.question == '':
        # print('==> skip empty line')
        continue

    # question text
    elif len(current_question.answers) == 0 and not line.startswith('-'):
        current_question.question += line
        # print('==> question ' + current_question.question)

    # answers
    else:
        if current_question.type is None:
            error('Question type required before specifying answers.')
        if '|' in line:
            error('Pipe `|` not allowed in answers.')
        if current_question.type == Type.kprim:
            if line.startswith('-'):
                if len(current_question.answers) >= 4:
                    error('No more than 4 answers allowed.')
                line_tmp = line[1:].lstrip()
                if line_tmp[0] not in 'rf':
                    error('Answers must start with either `- r ` or `- f `\n       e.g.: `- r This answer is right.` or `- f This answer is false.`')
                current_question.rfs += {'r':'1', 'f':'0'}[line_tmp[0]] + '|'
                current_question.answers.append(line_tmp[1:].lstrip())
            else:
                current_question.answers[-1] += line.lstrip()
        if current_question.type == Type.single_choice:
            if line.startswith('-'):
                line_tmp = line[1:].lstrip()
                points = match(r'([0-9]+)\s+(.+)$', line_tmp)
                if points is None:
                    error('Answers must start with their respective points\n       e.g.: `- 1 This answer is right.` or `- 0 This answer is false.`')
                current_question.rfs += points.group(1) + '|'
                current_question.answers.append(points.group(2))
            else:
                current_question.answers[-1] += line.lstrip()
        # print('==> answer ' + current_question.answers[-1])


print(f'Found {len(questions)} questions.\nRun final checks and convert to CSV ...')

def error(msg: str, question: Question):
    dir = ' / '.join(question.dir)
    print(f'\nERROR: {msg}\nin: {dir}\nin question starting at line {question._line+1}')
    exit()

def repeat(string: str, operation: Callable):
    tmp = None
    while string != tmp:
        tmp = string
        string = operation(tmp)
    return string

def prepare_html(string: str):
    code_parts = enumerate(string.split('```'))
    string = ''.join([
            ('<pre><code style="display:inline-block">' + code.replace('<', '&lt;').replace('>', '&gt;').strip() + '</code></pre>')
        if i % 2 else
            code
        for i, code in code_parts])
    ret = ''
    for line in string.split('\n'):
        line = sub(r'`([^`]+)`', r'<code>\1</code>', line)
        line = sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', line)
        line = sub(r'(^|[^\\])\*(((?!\\\*).)+)\*', r'\1<i>\2</i>', line)
        ret += line + '<br>'
    return ret

with StringIO() as buffer:
    writer = csv_writer(buffer, delimiter=';', quotechar='"', quoting=QUOTE_MINIMAL)
    for q in questions:
        if q.type == Type.kprim:
            if len(q.answers) < 4:
                error('4 answers required.', q)
            writer.writerow([
                '###'.join(q.dir),
                q.type.num_question_type(),
                len(q.answers),
                prepare_html(q.question.strip() + '\n\n' + current_question.options['kprim_append']),
                '|'.join([prepare_html(a.strip()) for a in q.answers]),
                None, None,
                q.rfs + '1',
                1,0,0,
                q.type.num_optional_value()
            ])
        if q.type == Type.single_choice:
            if len(q.answers) < 2:
                error('2 answers required.', q)
            writer.writerow([
                '###'.join(q.dir),
                q.type.num_question_type(),
                len(q.answers),
                prepare_html(q.question.strip() + '\n\n' + current_question.options['single_choice_append']),
                '|'.join([prepare_html(a.strip()) for a in q.answers]),
                None, None,
                q.rfs,
                1,0,0,
                q.type.num_optional_value()
            ])

    print(f'Writing to `{filename}.csv` ...')

    with open(filename + '.csv', 'w', newline='', encoding='utf8') as csvFile:
        buffer.seek(0)
        copyfileobj(buffer, csvFile)

    print('Finished.')
