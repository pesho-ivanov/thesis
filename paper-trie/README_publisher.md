# Publisher instructions

In this file, we describe how to produce the final version of the paper.

## Build

You can build the paper by running

```sh
make split
```

This will create the paper `/ci-output/main.pdf`, and split it into the main part (`/ci-output/submission.pdf`) and the supplement (`/ci-output/submission_supplement.pdf`).

## Reference files

For reference, we already prepared the resulting paper in the directory `/final_submission`.

The directory `/final_submission` also contains the `.bbl` file created during compilation.

## Prerequisites

To compile the paper, you need `TeX Live` and `latexmk`. To split the paper into the main part and the supplement, you need `pdftk`.

You can install the prerequisites (on Ubuntu) by running

```sh
sudo apt-get install texlive-full latexmk
sudo apt-get install pdftk
```
