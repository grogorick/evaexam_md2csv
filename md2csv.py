import csv
from dataclasses import dataclass
import re
import sys
from typing import List


@dataclass
class Question:
    dir: str = ''
    question: str = ''
    answers: List[str]|None = None
    rfs: List[str] = []


if len(sys.argv) < 2:
    print('Questions (.md) file required as argument')
    exit()

with open(sys.argv[1]) as file:
    lines = file.readlines()


questions : List[Question] = [Question()]
current_dir: List[str] = []
current_question: Question = questions[0]

for line in lines:
    if line.startswith('#'):
        questions.append(current_question := Question())

        level = re.match(r'#+[^#]', line).end()
        current_dir = current_dir[:level - 1] + [line[level:].strip()]
        current_question.dir = '###'.join(current_dir)

    elif current_question.answers is None and not line.startswith('-'):
        current_question.question += line[1:].strip() + '<br />'

    else:
        if current_question.answers is None:
            current_question.answers = []
        if line.startswith('-'):
            line = line[1:].strip()
            current_question.rfs.append('1' if line[0] == 'r' else ('0' if line[0] == 'f' else None))
            current_question.answers.append(line[1:].strip())


with open(sys.argv[1] + '.csv', 'w', newline='') as csvFile:
    writer = csv.writer(csvFile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for q in questions:
        d, q2, r, a = q
        writer.writerow([
            q.dir,
            8,4,
            q.question + '<br />',
            '<br />|'.join(q.answers) + '<br />',
            None, None,
            '|'.join(q.rfs) + '|1',
            1,0,4,2048
        ])