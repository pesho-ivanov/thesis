.DEFAULT_GOAL := pdf

.PHONY: pdf
pdf:
	latexmk -pdf -interaction=nonstopmode -silent main.tex

.PHONY: clean
clean:
	rm -f $(LOGFILES)

