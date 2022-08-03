import csv
from dataclasses import dataclass
import sys
from typing import List


@dataclass
class Question:
    dir: str
    question: str
    rfs: List[str]
    answers: List[str]


if len(sys.argv) < 2:
    print('Questions (.md) file required as argument')
    exit()

with open(sys.argv[1]) as file:
    lines = file.readlines()


questions : List[Question] = []
dir: List[str] = []

for line in lines:
    if line.startswith('#'):
        if dir:
            questions.append(Question(dir, question, rfs, answers))
        dir = line[1:].strip()
        question = ''
        rfs = []
        answers = []
    if line.startswith('>'):
        question += line[1:].strip() + '<br />'
    if line.startswith('-'):
        line = line[1:].strip()
        rfs.append('1' if line[0] == 'r' else '0')
        answers.append(line[1:].strip())
questions.append(Question(dir, question, rfs, answers))


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