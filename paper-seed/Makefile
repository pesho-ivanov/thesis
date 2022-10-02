# Makefile, allowing to
# - compile
# - test
# - clean
# - run in docker
# For details, see targets defined below
#
# USAGE, for example: make pdf

#####################
# REQUIRED PACKAGES #
#####################

# For instructions on how to set up your system to run all commands here, follow
# https://hub.docker.com/repository/docker/ethsrilab/latex-plus

##############
# PARAMETERS #
##############

# main
OUTPUTDIR := lqa-output
NAME := main

# special
NOAPPENDIX := $(NAME)_no_appendix
FULL := $(NAME)_full
OVERFULL := $(NAME)_overfull
GRAY := $(NAME)_gray
ABSTRACT := $(OUTPUTDIR)/abstract.txt

# submission
SUBMISSIONDIR := submission
ZIP := submission.zip

# log
LATEXMKDIR := $(OUTPUTDIR)/latexmk
LOG := $(OUTPUTDIR)/$(NAME).log
SHORTLOG := $(OUTPUTDIR)/$(NAME)-short.log

LOGFILES := *.aux *.bbl *.log *.bcf  *.blg *.lot *.toc *.swp *.gz *.out *.ttt *.fls *.fdb_latexmk

# scripts

SCRIPTDIR := lqa/scripts

#############
# COMPILING #
#############

LATEX := ./lqa/latex.sh $(NAME).tex $(LATEXMKDIR)

##########
# OTHERS #
##########

NOAPPENDIXCONFIG := headers/config/noappendix.config
SHOWOVERFULLCONFIG := headers/config/showoverfull.config

########
# PDFS #
########

.DEFAULT_GOAL := pdf-full

.PHONY: pdf-full
pdf-full:
	@echo "\n> COMPILING pdf..."
	$(LATEX)
	@cp $(LATEXMKDIR)/$(NAME).pdf $(OUTPUTDIR)/$(FULL).pdf
	@cp $(LATEXMKDIR)/$(NAME).bbl $(OUTPUTDIR)
	@cp $(LATEXMKDIR)/$(NAME).log $(LOG)

.PHONY: pdf-appendix
pdf-appendix: pdf-full
	python3 $(SCRIPTDIR)/pages.py --action appendix

.PHONY: appendix-labels
appendix-labels: pdf-full
	cat lqa/other/appendix-labels-loader-1.tex > appendix-labels-loader.tex
	cat $(LATEXMKDIR)/appendix.aux >> appendix-labels-loader.tex
	cat lqa/other/appendix-labels-loader-2.tex >> appendix-labels-loader.tex

.PHONY: pdf-no-appendix
pdf-no-appendix: appendix-labels
	make clean
	touch $(NOAPPENDIXCONFIG)
	$(LATEX)
	@cp $(LATEXMKDIR)/$(NAME).pdf $(OUTPUTDIR)/$(NOAPPENDIX).pdf
	make clean # cleanup

.PHONY: pdf-overfull
pdf-overfull:
	@echo "\n> COMPILING OVERFULL pdf..."
	make clean
	touch $(SHOWOVERFULLCONFIG)
	$(LATEX)
	@cp $(LATEXMKDIR)/$(NAME).pdf $(OUTPUTDIR)/$(OVERFULL).pdf
	make clean # cleanup

.PHONY: pdf-gray
pdf-gray: pdf-full
	@echo "\n> Producing GRAYSCALE version to $(OUTPUTDIR)/$(GRAY).pdf..."
	gs -sOutputFile=$(OUTPUTDIR)/$(GRAY).pdf -sDEVICE=pdfwrite -sColorConversionStrategy=Gray -dProcessColorModel=/DeviceGray -dCompatibilityLevel=1.4 -qQUIET -dNOPAUSE -dBATCH $(OUTPUTDIR)/$(FULL).pdf

.PHONY: pdf-all
pdf-all: cleanall pdf-appendix pdf-no-appendix pdf-overfull pdf-gray pdf-full

# produce better log files
.PHONY: log
log: pdf-full
	pplatex -i $(LOG) > $(SHORTLOG)


###############
# CONVENIENCE #
###############

.PHONY: check
check: pdf-full log
	python3 $(SCRIPTDIR)/checks.py

.PHONY: all
all: pdf-all check log

#########
# CLEAN #
#########

.PHONY: clean
clean:
	@echo "\n> CLEANING temporary files..."
	rm -f $(LOGFILES) || true
	rm -r -f $(LATEXMKDIR) || true
	rm -r -f $(OUTPUTDIR)/script-logs/*.log* || true
	rm -f headers/config/*.config

# make cleanall: remove all produced files
.PHONY: cleanall
cleanall: clean
	@echo "\n> CLEANING PDFs..."
	rm -f *.pdf || true
	cd $(OUTPUTDIR) && rm -f $(LOGFILES) || true
	rm -f $(OUTPUTDIR)/*.pdf || true
	rm -r -f $(SUBMISSIONDIR) || true
	rm -f appendix-labels-loader.tex
	rm -f $(ABSTRACT)

##############
# SUBMISSION #
##############

.PHONY: abstract
abstract:
	python3 $(SCRIPTDIR)/abstract.py

.PHONY: submission-files
submission-files: cleanall abstract pdf-full pdf-appendix pdf-no-appendix

.PHONY: submission
submission: submission-files check
	@echo "\n> PREPARING submission in directory $(SUBMISSIONDIR)..."
	rm -r -f $(SUBMISSIONDIR)
	mkdir $(SUBMISSIONDIR)
	cp $(OUTPUTDIR)/*.pdf $(SUBMISSIONDIR)
	cp $(ABSTRACT) $(SUBMISSIONDIR)
	cp $(OUTPUTDIR)/*.bbl $(SUBMISSIONDIR)

.PHONY: zip-no-appendix
zip-no-appendix: submission
	@rm -f $(SUBMISSIONDIR)/$(ZIP)
	make pdf-no-appendix # update output, prepare appendix labels
	touch $(NOAPPENDIXCONFIG) # ensure appendix is not included when compiling again
	zip --quiet -r $(SUBMISSIONDIR)/$(ZIP) . -x /.git* /$(OUTPUTDIR)* /$(SUBMISSIONDIR)/*.zip
	make clean

.PHONY: zip-full
zip-full: submission
	@rm -f $(SUBMISSIONDIR)/$(ZIP)
	make pdf-full # update output
	# README_publisher.md is wrong in this case
	zip --quiet -r $(SUBMISSIONDIR)/$(ZIP) . -x /.git* /$(OUTPUTDIR)* /$(SUBMISSIONDIR)/*.zip README_publisher.md

##########
# DOCKER #
##########

DOCKER-CMD := ./lqa/docker.sh


PAPERDIR := $$(pwd)
IMAGE := ethsrilab/latex-plus:version-4.0
CONTAINER := latex-plus-container
RUN := $(DOCKER-CMD) run \
		-it \
		--name $(CONTAINER) \
		--workdir="/paper" \
		-v $(PAPERDIR):/paper \
		$(IMAGE)

# launch a docker container using the image, which will provide a shell in the container
.PHONY: docker-run
docker-run: clean-container
	$(RUN)

# check for updates and remove the created docker container
.PHONY: clean-container
clean-container:
	$(DOCKER-CMD) pull $(IMAGE)
	$(DOCKER-CMD) rm /$(CONTAINER) 2>/dev/null || true

# all above commands, run in docker
.PHONY: docker-all
docker-all: clean-container
	$(RUN) make all

.PHONY: docker-pdf-full
docker-pdf-full: clean-container
	$(RUN) make pdf-full

.PHONY: docker-pdf-appendix
docker-pdf-appendix: clean-container
	$(RUN) make pdf-appendix

.PHONY: docker-pdf-no-appendix
docker-pdf-no-appendix: clean-container
	$(RUN) make pdf-no-appendix

.PHONY: docker-pdf-overfull
docker-pdf-overfull: clean-container
	$(RUN) make pdf-overfull

.PHONY: docker-pdf-gray
docker-pdf-gray: clean-container
	$(RUN) make pdf-gray

.PHONY: docker-pdf-all
docker-pdf-all: clean-container
	$(RUN) make pdf-all

.PHONY: docker-submission
docker-submission: clean-container
	$(RUN) make submission

.PHONY: docker-check
docker-check: clean-container
	$(RUN) make check

.PHONY: docker-zip
docker-zip: clean-container
	$(RUN) make zip
	
.PHONY: docker-abstract
docker-abstract: clean-container
	$(RUN) make abstract

