import csv
from dataclasses import dataclass
from enum import Enum
import re
import sys
from typing import List


class Type(Enum):
    kprim = 'kprim'

    def fromString(string):


@dataclass
class Question:
    dir: str = ''
    question: str = ''
    type: Type|None = None
    rfs: str = ''
    answers: List[str]|None = None


if len(sys.argv) < 2:
    print('Questions (.md) file required as argument')
    exit()

filename = sys.argv[1]
with open(filename) as file:
    lines = file.readlines()


questions : List[Question] = [Question()]
current_dir: List[str] = []
current_question: Question = questions[0]

for line_no, line in enumerate(lines):

    def error(msg: str):
        dir = ' # '.join(current_dir)
        print(f'\nERROR: {msg}\nin: {dir}\nline {line_no}: {line}')
        exit()

    if line.startswith('#'):
        if current_question.question != '':
            questions.append(current_question := Question())

        level = re.match(r'#+[^#]', line).end() - 1

        current_dir = current_dir[:level - 1] + [line[level:].strip()]
        current_question.dir = '###'.join(current_dir)

    elif line.startswith('---'):
        questions.append(current_question := Question())
        current_question.dir = '###'.join(current_dir)

    elif current_question.type is None and not line.startswith('>'):
        if current_question.question == '' and line.strip() == '':
            continue
        line = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', line.strip())
        line = re.sub(r'\*([^*]+)\*', r'<i>\1</i>', line.strip())
        current_question.question += line + '<br />'

    elif line.startswith('>'):
        if current_question.question == '':
            error('Question text required before specifying the question type.')
        if current_question.type is not None:
            error('Question type already set.')
        current_question.type = { 'kprim': Type.kprim }[line[1:].strip()]

    else:
        if current_question.type is None:
            error('Question type required before listing answers.')

        if current_question.type == Type.kprim:
            if current_question.answers is None:
                current_question.answers = []
            if line.startswith('-'):
                if len(current_question.answers) >= 4:
                    error('No more than 4 answers allowed.')
                line_tmp = line[1:].strip()
                if line_tmp[0] not in 'rf':
                    error('Answers must start with either `- r ` or `- f `\n       e.g.: `- r This answer is right.` or `- f This answer is false.`')
                current_question.rfs += {'r':'1', 'f':'0'}[line_tmp[0]] + '|'
                current_question.answers.append(line_tmp[1:].strip())
            else:
                current_question.answers[-1]


print(f'Found {len(questions)} questions.\nGenerating `{filename}.csv` ...')

with open(filename + '.csv', 'w', newline='') as csvFile:
    writer = csv.writer(csvFile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for q in questions:
        writer.writerow([
            q.dir,
            8,4,
            q.question,
            '|'.join(q.answers),
            None, None,
            q.rfs + '1',
            1,0,4,2048
        ])