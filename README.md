# EvaExam md2csv
A script to convert exam questions in a (specifically structured) Markdown (.md) file to a (specifically structured) CSV file that can be uploaded/imported to the EvaExam questions library.

### Required syntax of the markdown file:
(Texts in curly braces {like this} are placeholders)
```
{GLOBAL OPTIONS}

{DIRECTORY}

{QUESTION}
---
{QUESTION}
---
{QUESTION}
...

{DIRECTORY}

{QUESTION}
...
```

> **GLOBAL OPTIONS**
> ```
> *{QUESTION TYPE}_{OPTION}* {Global value}
> *{QUESTION TYPE}_{OPTION}* {Global value}
> ...
> ```

> **OPTION**  
> `append` — Text to append at the end of the question text, e.g., for kprim questions: "Please state for each of the statements below whether they are true(+) or false(-)."  
> `code` — How to handle code (\`\`\`). Allowed values are `as-is`, `exclude`, `inline-html`, or an  `<images-output-directory>`
>
> Put global options (with a question type prefix) at the top of the document and per-question options (without the prefix) in the lines following the question type.

> **DIRECTORY**
> ```
> # {First/top-most questions library directory, e.g., lecture name}
> ## {Second level directory, e.g., year or semester}
> ### {Third level directory, e.g., topic}
> ...
> ```

> **QUESTION**
> ```
> > {QUESTION TYPE}
> > *{OPTION}* {Per-question value}
> > *{OPTION}* {Per-question value}
> > ...
>
> {Multiline question text}
>
> {ANSWER}
> {ANSWER}
> ...
> ```

> **QUESTION TYPE**
> ```
> kprim | single_choice
> ```

> **ANSWER**  
>> **kprim:**
>> ```
>> - {r | f} {Multiline text of true (r) or false (f) answer}
>> ```
>> Exactly 4 answers required
>
>> **single_choice:**
>> ```
>> - {0 | 1} {Multiline text of right (1) or wrong (0) answer}
>> ```
>> At least 2 answers required
>
> Subsequent lines of a multiline answer must not start with a hyphen (`-`).

> **Comments**
> ```
> ~~~ {Single line comment} ~~~
> ```
>
> ```
> ~~~
> {Multiline comment}
> ~~~
> ```
> Comments must always be whole line comments.  
> Completely sripped from the output.  
> They may be inserted at any point, e.g., to note additional explanations or (filnames of) images that are not supported for import/export directly, but need to be added via the web interface.

> **Math**
> ```
> $$
> a^2 + b^2 = c^2
> $$
> ```
> Completely sripped form the output.  
> Formulas may be inserted at any point, e.g., to note latex formulas that are not supported for import/export directly, but need to be added via the web interface.

> **Additional formatting**  
> *(As opposed to the web interface, the importer seem to allow arbitrary **html tags** in questions and answers. Keep in mind that this may change anytime, so use the following with caution.)*
>
> Questions and answers may include the following markdown formatting:
> ~~~
> ```
> code blocks
> ```
>
> `inline code`
> **bold**
> *italic*
> ~~~

> Horizontal lines via three hyphens (`---`) are skipped during processing and may be inserted at any point, e.g., to visually (in the .md file) separate questions in the same directory.

See [example.md](example.md).

### Run
`> {py | python | python3} md2csv.py example.md`

### Additional notes
See [EvaExam docs](https://help.evasys.de/evaexam/de/user/index.html#Help=&rhsearch=rtf%20kprim&rhhlterm=rtf%20kprim&rhsyns=%20&t=Help%2FHelp_Text%2FHelp_Text-116.htm) for details on the generated CSV file.
