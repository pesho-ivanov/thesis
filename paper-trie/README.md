<span style="color:red">**TODO: When moving to new repository: Update all occurrences of `pivanov/align-prob`**</span>

# Automatic build of paper

![pipeline status](https://gitlab.inf.ethz.ch/pivanov/align-prob/badges/master/pipeline.svg)

On every push, the paper gets built automatically (using continuous integration). To access the most recent builds, go to

- [Full paper](https://gitlab.inf.ethz.ch/pivanov/align-prob/-/jobs/artifacts/master/raw/main.pdf?job=paper)
- [Submission](https://gitlab.inf.ethz.ch/pivanov/align-prob/-/jobs/artifacts/master/raw/submission.pdf?job=paper)
- [Supplement](https://gitlab.inf.ethz.ch/pivanov/align-prob/-/jobs/artifacts/master/raw/submission_supplement.pdf?job=paper)
- [Abstract](https://gitlab.inf.ethz.ch/pivanov/align-prob/-/jobs/artifacts/master/raw/abstract.txt?job=paper), produced by [abstract.py](/paper/ci-scripts/abstract.py)
- [Advanced builds](https://gitlab.inf.ethz.ch/pivanov/align-prob/-/jobs/artifacts/master/browse?job=advanced) (e.g. [grayscale version](https://gitlab.inf.ethz.ch/pivanov/align-prob/-/jobs/artifacts/master/raw/main_gray.pdf?job=advanced), [overfull marks](https://gitlab.inf.ethz.ch/pivanov/align-prob/-/jobs/artifacts/master/raw/main_overfull.pdf?job=advanced)) 
- [Logfiles](https://gitlab.inf.ethz.ch/pivanov/align-prob/-/jobs/artifacts/master/raw/main.log?job=advanced)
- [Final submission with sources (zip)](https://gitlab.inf.ethz.ch/pivanov/align-prob/-/jobs/artifacts/master/raw/submission.zip?job=submission): Must be triggered, as described [here](/paper/README.md#create-submittable-version).

To browse older builds and to debug errors:
- Go to [Jobs](https://gitlab.inf.ethz.ch/pivanov/align-prob/pipelines)
- Click on the most recent job number (e.g., "#55814")
- Browse through the generated files with the button on the right-hand-side.

## Conventions

A list of conventions for the paper, including terminology and formulas

- ...

## Commands

Use the commands defined in the [header](/paper/header.tex) to

- reference figures, sections, theorems, etc.
- abbreviate common words like `e.g.`, `w.r.t.`, ...


## Spelling

A list of conventions for spelling (e.g. `while loop` not `while-loop`). If Wikipedia has a convention, we try to follow it.

## Capitalization

- All sections, subsections, subsubsections, and paragraphs must be capitalized
- Capitalization of hyphenated words (inspired by https://english.stackexchange.com/questions/460/do-you-capitalize-both-parts-of-a-hyphenated-word-in-a-title):
  - capitalize only the first word unless later words are proper nouns or
    adjectives. Proper nouns (adjectives) are names used for an individual
    person, place, organization, etc.

# Create submittable version

To create a submittable version, browse to [Pipelines](https://gitlab.inf.ethz.ch/pivanov/align-prob/pipelines), select click `Play` on the stage `submission`.

This generates a [special artifact](/paper/README.md#automatic-build-of-paper) for submission, and runs [additional tests](/paper/README.md#final-tests). 


# Tests

## Frequent tests

The automatic build tests some basic properties of the generated paper.

- Check warnings returned by the compiler.
	- To ignore some warnings, edit [acceptable_warnings_list.txt](/paper/ci-scripts/acceptable_warnings_list.txt).
- Check the files for forbidden texts.
	- For the list of forbidden strings, see [forbidden_text_list.txt](/paper/ci-scripts/forbidden_text_list.txt).
- Check the paper does not use Type 3 fonts.
- Check inconsistencies in hyphenation (e.g. `real-world` vs `real world`)

## Final tests

For the final version (to be submitted), the build runs additional checks. These tests must be triggered, as described [here](/paper/README.md#mark-as-ready-for-submission).
- Check the length is below the page limit.
	- Set the pagelimit in [pages.py](/paper/ci-scripts/pages.py).
- Check the paper for todos.

## Fixing errors

All errors come with suggestions on how to fix them. For example:

```
[ERROR]: 1 warnings:
> `./main.bbl:3`    LaTeX Warning: Empty `thebibliography' environment    `log:34`
[SOLUTION]:
> 1) Fix the issues raised by the warnings.
> 2) Add listed warnings to paper/ci-scripts/acceptable_warnings_list.txt.
> 3) Disable the check for warnings by editing paper/ci-scripts/checks.py.
```

# Conventions

This template assumes that
- an abstract is in file [/paper/abstract.tex](/paper/abstract.tex) 
- all commands and included packages are specified in [/paper/header.tex](/paper/header.tex)

# Compiling locally

To run all compilation and test steps, you can use Docker (installation instructions can be found at https://docs.docker.com/install/linux/docker-ce/ubuntu/).
To run the Docker container, run `make docker-run`.

Alternatively, you can follow the installation instructions in the <a href="https://hub.docker.com/r/bichselb/latex-plus/~/dockerfile/">Dockerfile</a> to install the necessary prerequisites directly on your system.

The following commands can all be run in the Docker container. Alternatively, most commands also have a shortcut to run them in Docker. For example, `make docker-check` runs `make check` in the Docker container.

## Build

```sh
make split
```
Performs the following steps:
- compile (`main.tex` to `main.pdf`)
- split into submission (`submission.pdf`) and supplementary material (`submission_supplement.pdf`)

## Other builds

Check the [Makefile](Makefile) for more builds, such as
- `make abstract` (produces `abstract.txt`, a copyable markdown version of the abstract, e.g., for hotcrp)
- `make gray` (producing a grayscale version of the paper)
- `make check` (basic checks)
- `make overfull` (marking places where the paper overlaps its boundaries)
- `make zip` (creating a zipfile to hand in for the camera-ready version)
