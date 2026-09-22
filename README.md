# Ruto's tranScripter
## For more knowledge start with Artificial Level
---
## This is on development project  

Not a Production line project. Research based project which enables English can be used as Programming.

To Test the Project :- 

\* Download the whole file from github.

\* Extract the zip.

\* Go to the extracted folder.

\* Open a shell and install all python requirements using uv:
```
uv pip install -r requirements.txt
```

---
For anaconda users 

\* Open a shell and install all anaconda requirements 
```
conda env create -f environment.yml
```
---



\* To test working of Ruto's tranScripter their is a same file with the zip called "main.ai".

\* On the shell run this command (For linux users use python3 instead of python)
```
python javs.py main.ai
```

\* To generate the python code use "-p"
```
python javs.py main.ai -p
```

\* To generate log "-l"

```
python javs.py main.ai -l
```
---

\* To generate Env words ** don't use any file
```
python javs.py -envWords
```


## Sample input with String 
```
Store 2 in $v1 then add 3 with $v1 and print the result .
Add 3, 5 and $v1 .
Print the result.
Divide result by 4 and the display result.
Store 2 in $v1, the add 5 with $v1.
Print the string 'i am adding 2 with 5 and the result is ' and result .
Add 5 and 4, then print the string '5 + 4 = ' and result. 
```


# Artificial Level Language

For more information got to Documents folder

Artificial Level Language is an new form of idea which basically understand the natural language in the computer.

\* There are some theory are not explain now as on development.

\* It just an idea which is not presented anywhere.

\* It is on development 
___
___
## Achu's Programming Language
It is not a language, it is set of rules that to flow to make a tranScripter or transCompiler which can define the Artificial Level Language (In simple words to support natural language).

\* As it on development simple explanation is given. 

\* File Extension is ".ai"
___
___
# Ruto's tranScripter
It is the software which is to support the natural language as the input to the computer.

Which it is developed on the basic of the rule, that given by the Achu's Programming Language.

The name JAVS is the combination of first letters of the people which developing the software (or tranScripter).

Developers :-
- J for Julien
- A for Anas
- V for Vishnu
- S for Sayu  

\* All the things that is listed up there are on development and no papers published about it.

---

## Research & Documentation

This project is completed based on **"Artificial Level Language: A Library of Computing Engine for Natural Languages"** (K S Sunil et al., IEEE ICC 2023, DOI: `10.1109/ICCC57789.2023.10165200`) and is maintained at [rutoassistant/Rutos-tranScripter](https://github.com/rutoassistant/Rutos-tranScripter). Forked/cloned from the original [VishnuSuresh2000/JAVS-tranScripter](https://github.com/VishnuSuresh2000/JAVS-tranScripter).

### Core Principles

Environment-based learning follows principles from [[Winograd SHRDLU]] (1971):

| Principle | Implementation |
|-----------|----------------|
| **Procedural Representation** | Knowledge encoded as callable functions (ArithmeticEnv) |
| **Self-Reinforcement Loop** | Parse → Execute → Update based on feedback |
| **Micro-World Constraint** | Current focus: arithmetic operations |
| **Natural Language Interface** | English commands translate to Python |

See [README_ENV.md](README_ENV.md) for detailed principles and future development roadmap.

### Cited Works

1. **Sunil, K. S., et al.** "Artificial Level Language: A Library of Computing Engine for Natural Languages." *IEEE ICC 2023*. DOI: [10.1109/ICCC57789.2023.10165200](https://ieeexplore.ieee.org/document/10165200). — The foundational ALL framework: a tranSMachine with tranScripter and transCompiler that converts natural-language sentences to Python statements.

2. **Thomas, J., Suresh, V., Anas, M., Sajeev, S., & Sunil, K.** "Programming with Natural Languages: A Survey." In *Computer Networks and Inventive Communication Technologies* (Springer, 2021), pp. 767–779. DOI: [10.1007/978-981-16-3728-5_57](https://link.springer.com/chapter/10.1007/978-981-16-3728-5_57). — The natural language survey motivating the ALL approach.

### Presentations

- [Nov 2020 Presentation](Document/presentation-all-nov-2020.md) — Original ALL concept
- [Apr 2021 Presentation](Document/presentation-javs-working-apr-2021.md) — Implementation updates

### Project Documentation

- `CONTEXT.md` — Domain model glossary (language, rules, research foundations)
- `ADR.md` — Architecture Decision Records (index; full ADRs in `docs/adr/`)
- `docs/adr/` — Individual ADR files (0001–0004)
- [Document/README_RESEARCH.md](Document/README_RESEARCH.md) — Research context

### Wiki Index

This project is documented in the [[LLM Wiki]]:
- [[Ruto's tranScripter]] — Transcompiler architecture, known bugs, how to run
- [[Artificial Level Language (ALL) Paper]] — IEEE paper abstract + slideshare pre-presentation content

---
