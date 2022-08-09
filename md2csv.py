from csv import QUOTE_MINIMAL, writer as csv_writer
from dataclasses import dataclass
from enum import Enum
from io import StringIO
from re import match, sub
from shutil import copyfileobj
from sys import argv
from typing import Dict, List


class Type(Enum):
    kprim = 'kprim'

    @classmethod
    def fromString(cls, string):
        for t in Type:
            if t.value == string:
                return t
        return None


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
with open(filename) as file:
    lines = file.readlines()


questions : List[Question] = []
current_dir: List[str] = []
current_question: Question|None = None
is_comment: bool = False

options = {
    'kprim_append': ''
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
    if line.startswith('```'):
        is_comment = not is_comment
        continue
    elif is_comment:
        # print('==> skip comment line')
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
            # print('==> type ' + current_question.type.name + ' | dir ' + str(current_question.dir))

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
        line = sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', line)
        line = sub(r'\*([^*]+)\*', r'<i>\1</i>', line)
        current_question.question += line
        # print('==> question ' + current_question.question)

    # answers
    else:
        if current_question.type == Type.kprim:
            if current_question.type is None:
                error('Question type required before specifying answers.')
            if '|' in line:
                error('Pipe `|` not allowed in answers.')
            if line.startswith('-'):
                if len(current_question.answers) >= 4:
                    error('No more than 4 answers allowed.')
                line_tmp = line[1:].lstrip()
                if line_tmp[0] not in 'rf':
                    error('Answers must start with either `- r ` or `- f `\n       e.g.: `- r This answer is right.` or `- f This answer is false.`')
                if len(current_question.answers) == 0:
                    current_question.question = current_question.question.strip() + '\n' + current_question.options['kprim_append']
                current_question.rfs += {'r':'1', 'f':'0'}[line_tmp[0]] + '|'
                current_question.answers.append(line_tmp[1:].lstrip())
            else:
                current_question.answers[-1] += line.lstrip()
            # print('==> answer ' + current_question.answers[-1])


print(f'Found {len(questions)} questions.\nRun final checks and convert to CSV ...')

def error(msg: str, question: Question):
    dir = ' / '.join(question.dir)
    print(f'\nERROR: {msg}\nin: {dir}\nin question starting at line {question._line+1}')
    exit()

def remove_trailing_brs(string: str):
    return sub(r'(<br />)+$', '', string)

def newline_to_br(string: str):
    return string.replace('\n', '<br />')

with StringIO() as buffer:
    writer = csv_writer(buffer, delimiter=';', quotechar='"', quoting=QUOTE_MINIMAL)
    for q in questions:
        if q.type == Type.kprim:
            if len(q.answers) < 4:
                error('4 answers required.', q)
            writer.writerow([
                '###'.join(q.dir),
                8,4,
                newline_to_br(q.question.strip()),
                newline_to_br('|'.join([a.strip() for a in q.answers])),
                None, None,
                q.rfs + '1',
                1,0,4,2048
            ])

    print(f'Writing to `{filename}.csv` ...')

    with open(filename + '.csv', 'w', newline='') as csvFile:
        buffer.seek(0)
        copyfileobj(buffer, csvFile)

    print('Finished.')
