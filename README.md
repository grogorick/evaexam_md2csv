# EvaExam md2csv
A script to convert exam questions in a (specifically structured) Markdown (.md) file to a (specifically structured) CSV file that can be uploaded/importet to the EvaExam questions library.

### Supported question types:
- kprim

### Required syntax of the markdown file:
(Texts in curly braces {like this} are placeholders)
```
kprim_append {Text to append to all questions of type kprim}

# {First/top-most questions library directory, e.g. lecture name}
## {Second level directory, e.g. year/semester. Optional}
### {Third level directory, e.g. first topic. Optional}
{#### ...}

> {question type of first question. Currently supported: kprim}

{Multiline question text...
 may include markdown syntax for **bold** and **italic** font style.}

- {In-/correct answer indicator: r/f} {Multiline text of the first answer.}
- {r/f} {Multiline text of the second answer.}
- {r/f} {Multiline text of the third answer.}
- {r/f} {Multiline text of the fourth answer.}


> {question type of next question within the same topic...}

{...}


### {next topic}

> {question type of first question within the new topic...}

{...}
```
See [example.md](example.md).

### Run
`python md2csv.py example.md`

### Additional notes
See [EvaExam docs](https://help.evasys.de/evaexam/de/user/index.html#Help=&rhsearch=rtf%20kprim&rhhlterm=rtf%20kprim&rhsyns=%20&t=Help%2FHelp_Text%2FHelp_Text-116.htm) for details on the generated CSV file.
