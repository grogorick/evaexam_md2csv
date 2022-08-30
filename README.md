# EvaExam md2csv
A script to convert exam questions in a (specifically structured) Markdown (.md) file to a (specifically structured) CSV file that can be uploaded/imported to the EvaExam questions library.

### Supported question types:
- kprim
- single_choice

### Required syntax of the markdown file:
(Texts in curly braces {like this} are placeholders)
~~~
*{option}* {value for this option, to be applied for all questions}

# {First/top-most questions library directory, e.g. lecture name}
## {Second level directory, e.g. year/semester. Optional}
### {Third level directory, e.g. first topic. Optional}
{#### ...}

> {question type of first question. Currently supported: kprim}
> *{option}* {per-question value}

{Multiline question text...
 may include <code>CODE</code> and markdown syntax for **bold** and *italic* font style.}

``` {Single line comment} ```

```
{Multiline comment}
```

- {For `kprim` questions, in-/correct answer indicator: r/f} {Multiline text of the first answer.}
- {r/f} {Multiline text of the second answer.}
- {r/f} {Multiline text of the third answer.}
- {r/f} {Multiline text of the fourth answer.}

---

> {question type of next question within the same topic...}

{question text...}

- {For `single_choice` questions, points: 0/1} {Multiline text of the first answer.}
- {r/f} {Multiline text of the second answer.}
- {r/f} {Multiline text of the third answer.}
- {r/f} {Multiline text of the fourth answer.}

---

> {question type...}


### {next topic}

> {question type of first question within the new topic...}

{...}
~~~
See [example.md](example.md).

#### Options (global and per question)
*kprim_append* — Text to append to questions of type kprim, e.g.:  
   Please state for each of the statements below whether they are true(+) or false(-).

Block comments may be inserted at any point with ` ``` `  
e.g. to note latex formulas that are not supported for import/export.

Horizontal lines may be inserted at any point with `---`  
e.g. to separate questions in the same directory.

### Run
`python md2csv.py example.md`

### Additional notes
See [EvaExam docs](https://help.evasys.de/evaexam/de/user/index.html#Help=&rhsearch=rtf%20kprim&rhhlterm=rtf%20kprim&rhsyns=%20&t=Help%2FHelp_Text%2FHelp_Text-116.htm) for details on the generated CSV file.
