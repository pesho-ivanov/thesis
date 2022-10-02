# Publisher instructions

In this file, we describe how to produce the final version of the paper.

## Build

You can build the paper by running

```sh
latexmk -pdf -interaction=nonstopmode main.tex
```

This will create the file [main.pdf](./main.pdf), which does not include the appendix.

## Reference files

For reference, we already prepared the resulting paper
[main_no_appendix.pdf](./submission/main_no_appendix.pdf) in the directory
[submission](./submission).

The directory [submission](./submission) also contains:

- the [main.bbl](./submission/main.bbl) file created during compilation.
- the full paper [main_full.pdf](./submission/main_full.pdf) (including
  appendix)
- the appendix [main_only_appendix.pdf](./submission/main_only_appendix.pdf)

## Prerequisites

To compile the paper, you need `TeX Live` and `latexmk`.

You can install the prerequisites (on Ubuntu) by running

```sh
sudo apt-get install texlive-full latexmk
```
