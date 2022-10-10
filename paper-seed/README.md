

# Automatic build of paper

![pipeline status](https://gitlab.inf.ethz.ch/pivanov/astarix-recomb2020-poster/badges/master/pipeline.svg)

On every push, the paper gets built automatically (using continuous integration). To access the most recent builds, go to

- [Full paper](https://gitlab.inf.ethz.ch/pivanov/astarix-recomb2020-poster/-/jobs/artifacts/master/raw/main_full.pdf?job=latex-compile)
- [Without Appendix](https://gitlab.inf.ethz.ch/pivanov/astarix-recomb2020-poster/-/jobs/artifacts/master/raw/main_no_appendix.pdf?job=latex-compile)
- [Only Appendix](https://gitlab.inf.ethz.ch/pivanov/astarix-recomb2020-poster/-/jobs/artifacts/master/raw/main_only_appendix.pdf?job=latex-compile)
- [Abstract](https://gitlab.inf.ethz.ch/pivanov/astarix-recomb2020-poster/-/jobs/artifacts/master/raw/abstract.txt?job=latex-compile), produced by [abstract.py](/paper/lqa-scripts/abstract.py)
- [Advanced builds](https://gitlab.inf.ethz.ch/pivanov/astarix-recomb2020-poster/-/jobs/artifacts/master/browse?job=latex-advanced) (\eg [grayscale version](https://gitlab.inf.ethz.ch/pivanov/astarix-recomb2020-poster/-/jobs/artifacts/master/raw/main_gray.pdf?job=latex-advanced), [overfull marks](https://gitlab.inf.ethz.ch/pivanov/astarix-recomb2020-poster/-/jobs/artifacts/master/raw/main_overfull.pdf?job=latex-advanced))
- Logfiles: [Full latex log](https://gitlab.inf.ethz.ch/pivanov/astarix-recomb2020-poster/-/jobs/artifacts/master/raw/main.log?job=latex-advanced), [Short latex log](https://gitlab.inf.ethz.ch/pivanov/astarix-recomb2020-poster/-/jobs/artifacts/master/raw/main-short.log?job=latex-advanced)
- [Final submission with sources (zip)](https://gitlab.inf.ethz.ch/pivanov/astarix-recomb2020-poster/-/jobs/artifacts/master/raw/submission.zip?job=latex-submission): Must be triggered, as described [here](/paper/README.md#create-submittable-version).

Current LQA issues are listed on the dashboard:

- [LQA dashboard](https://gitlab.inf.ethz.ch/pivanov/astarix-recomb2020-poster/-/jobs/artifacts/master/raw/lqa-dashboard.txt?job=latex-advanced)

To browse older builds and to debug errors:

- Go to [Jobs](https://gitlab.inf.ethz.ch/pivanov/astarix-recomb2020-poster/pipelines)
- Click on the most recent job number (\eg, "#55814")
- Browse through the generated files with the button on the right-hand-side.

## Commands

Use the commands defined in the `headers/` folder to

- abbreviate common words like `\eg`, `w.r.t.`, ...

Use [cleveref](http://tug.ctan.org/tex-archive/macros/latex/contrib/cleveref/cleveref.pdf) to ensure a consistent handling of references:

- Write `\cref` instead of `\ref`

## Capitalization

- All sections, subsections, subsubsections, and paragraphs must be capitalized.
- Capitalization of hyphenated words (inspired by
  https://english.stackexchange.com/questions/460/do-you-capitalize-both-parts-of-a-hyphenated-word-in-a-title):

  - Capitalize only the first word unless later words are proper nouns or
    adjectives. Proper nouns (adjectives) are names used for an individual
    person, place, organization, etc.

# Create submittable version

To create a submittable version, browse to [Pipelines](https://gitlab.inf.ethz.ch/pivanov/astarix-recomb2020-poster/pipelines), select click `Play` on the stage `submission`.

This generates a [special artifact](/paper/README.md#automatic-build-of-paper) for submission.

# Conventions

This template assumes that

- an abstract is in file [/paper/abstract.tex](/paper/abstract.tex)
- all commands and included packages are specified a header file in `/paper/headers`

# Compiling locally

See [here](lqa/doc/README.md) for a documentation of LQA and how to configure the tool.

To run all compilation and test steps, you can use Docker (installation instructions can be found at https://docs.docker.com/install/linux/docker-ce/ubuntu/).
To run the Docker container, run `make docker-run`.

Alternatively, you can follow the installation instructions in the [Dockerfile](../lqa-meta/docker/Dockerfile) to install the necessary prerequisites directly on your system.

## Known Issues

### Pdftk on MacOS

On MacOS the `make split` command can hang when calling `pdftk` (\ie call it but it never returns). This is not a bug by the paper template, but by an often with other tools distributed version of `pdftk`. [This can be fixed by installing a correct version of pdftk](https://stackoverflow.com/questions/39750883/pdftk-hanging-on-macos-sierra) or by running via docker.

### GitLab Issues

- Running CI on GitLab may fail with `no space left on device`. This happens
  when GitLab runners run out of storage (can only be permanently fixed by the
  runner administrator).
- Similarly, GitLab may exhibit an SSL configuration error, indicated by `SSL
  certificate problem: unable to get issuer certificate`.

To fix this, try the following options:

- [simplest option] Run the failing job again
  - Navigate to https://gitlab.inf.ethz.ch/pivanov/astarix-recomb2020-poster/pipelines
  - Rerun the failing job by clicking the `Rerun` button.
- [temporary fix] Navigate to https://gitlab.inf.ethz.ch/pivanov/astarix-recomb2020-poster/pipelines and
press `Clear Runner Caches`.
- [work-around] Specify a specific runner that is not currently out of space:
  - Navigate to
  https://gitlab.inf.ethz.ch/pivanov/astarix-recomb2020-poster/settings/ci_cd
  - "Expand" Runners
  - Pick a runner and look at its tag (avoid the runner that raised the
    exception; its ID is listed in the error message).
  - Add this tag to your .yml file, resulting in a configuration that looks
  something like this:

```yml
.paper:
  [...]
  tags: # only use runners with this tag
    - cpp

latex-compile:
  extends: .paper
[...]
```
