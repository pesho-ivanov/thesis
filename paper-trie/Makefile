#####################
# REQUIRED PACKAGES #
#####################

# For instructions on how to set up your system to run all commands here, see the Dockerfile
# https://hub.docker.com/r/bichselb/latex-plus/~/dockerfile/

##############
# PARAMETERS #
##############

# main
OUTPUTDIR := ci-output
NAME := main
SUBMISSION := submission
SUPPLEMENT := submission_supplement

# special
OVERFULL := $(NAME)_overfull
GRAY := $(NAME)_gray

# submission
SUBMISSIONDIR := final_submission
ZIP := submission.zip

# log
LATEXMKDIR := $(OUTPUTDIR)/latexmk
LOG := $(LATEXMKDIR)/$(NAME).log
SHORTLOG := $(OUTPUTDIR)/$(NAME)-short.log
OVERFULLOUTPUTDIR := $(OUTPUTDIR)/overfull

LOGFILES := *.aux *.bbl *.log *.bcf  *.blg *.lot *.toc *.swp *.gz *.out *.ttt *.fls *.fdb_latexmk

#############
# COMPILING #
#############

# -pdf: generate pdf version
# -interaction=nonstopmode
# -f: force latexmk to continue document processing despite errors, should also use "-interaction=nonstopmode"
# -outdir=FOO: set to directory for the output files
# -logfilewarninglist: give a  list  of  warnings  about  undefined citations and references (unless silent mode is on)
# -silent: run commands with less diagnostic output
LATEXCMD := latexmk -pdf -interaction=nonstopmode -silent
# alternative command enabling shell-escape (requires copying the files to the correct directory afterwards)
# LATEXCMD := latexmk -e '$$pdflatex=q/pdflatex %O -shell-escape %S/' -pdf -interaction=nonstopmode -silent
LATEX := $(LATEXCMD) -outdir=$(LATEXMKDIR) $(NAME).tex
LATEXOVERFULL := $(LATEXCMD) -outdir=$(OVERFULLOUTPUTDIR) $(OVERFULL).tex

##########
# OTHERS #
##########

# determining last page of submission
LASTBODYPAGE := python3 ci-scripts/pages.py --action lastbodypage
LASTREFERENCESPAGE := python3 ci-scripts/pages.py --action lastreferencespage
LASTPAGE := python3 ci-scripts/pages.py --action lastpage
SPLITPAGE := $(LASTREFERENCESPAGE)
# latex code to enable marking overfull areas
OVERFULLFILECONTENT := \def\isoverfull{1} \input{$(NAME).tex}

########
# PDFS #
########

.DEFAULT_GOAL := pdf

.PHONY: pdf
pdf:
	@echo "\n> COMPILING pdf..."
	# clean and run again in case of failure
	$(LATEX) ||  ( make clean &&  $(LATEX) )
	@cp $(LATEXMKDIR)/$(NAME).pdf $(OUTPUTDIR)
	@cp $(LATEXMKDIR)/$(NAME).pdf .

.PHONY: overfull
overfull:
	@echo "\n> COMPILING OVERFULL pdf..."
	echo "$(OVERFULLFILECONTENT)" > $(OVERFULL).tex
	$(LATEXOVERFULL) ||  ( make clean &&  $(LATEXOVERFULL) )
	@cp $(OVERFULLOUTPUTDIR)/$(OVERFULL).pdf $(OUTPUTDIR)
	rm $(OVERFULL).tex # cleanup

# make split: builds the whole paper and splits it into submission and supplementary material
.PHONY: split
split: pdf
	@echo "\n> SPLITTING pdf after page $$($(SPLITPAGE))..."
	@pdftk $(OUTPUTDIR)/$(NAME).pdf cat 1-$$($(SPLITPAGE)) output $(OUTPUTDIR)/$(SUBMISSION).pdf
	@pdftk $(OUTPUTDIR)/$(NAME).pdf cat $$($(SPLITPAGE))-end~$$($(SPLITPAGE)) output $(OUTPUTDIR)/$(SUPPLEMENT).pdf

.PHONY: gray
gray: pdf
	@echo "\n> Producing GRAYSCALE version to $(OUTPUTDIR)/$(GRAY).pdf..."
	gs -sOutputFile=$(OUTPUTDIR)/$(GRAY).pdf -sDEVICE=pdfwrite -sColorConversionStrategy=Gray -dProcessColorModel=/DeviceGray -dCompatibilityLevel=1.4 -qQUIET -dNOPAUSE -dBATCH $(OUTPUTDIR)/$(NAME).pdf

# produce better log files
.PHONY: log
log:
	pplatex -i $(LOG) > $(SHORTLOG)

.PHONY: printlog
printlog: log
	cat $(SHORTLOG)


###############
# CONVENIENCE #
###############

.PHONY: check
check: pdf log
	python3 ci-scripts/checks.py

.PHONY: finalcheck
finalcheck: pdf
	python3 ci-scripts/final_checks.py

.PHONY: all
all: pdf split gray check log overfull

#########
# CLEAN #
#########

.PHONY: clean
clean:
	@echo "\n> CLEANING temporary files..."
	cd $(OUTPUTDIR) && rm -f $(LOGFILES)
	rm -f $(LOGFILES)
	rm -r -f $(LATEXMKDIR) $(OVERFULLOUTPUTDIR)

# make cleanall: remove all produced files
.PHONY: cleanall
cleanall: clean
	@echo "\n> CLEANING PDFs..."
	rm -f *.pdf
	rm -f $(OUTPUTDIR)/*.pdf
	rm -r -f $(SUBMISSIONDIR)

##############
# SUBMISSION #
##############

.PHONY: abstract
abstract:
	python3 ci-scripts/abstract.py

# prepare a submission: produce PDFs and ZIP
.PHONY: submission
submission: split finalcheck
	@echo "\n> PREPARING submission in directory $(OUTPUTDIR)..."
	rm -r -f $(SUBMISSIONDIR)
	mkdir $(SUBMISSIONDIR)
	cp $(OUTPUTDIR)/$(SUBMISSION).pdf $(SUBMISSIONDIR)
	cp $(OUTPUTDIR)/$(SUPPLEMENT).pdf $(SUBMISSIONDIR)
	cp $(LATEXMKDIR)/$(NAME).bbl $(SUBMISSIONDIR)

# zip the whole directory and place the result in /submission
.PHONY: zip
zip: submission
	@echo "\n> ZIPPING directory..."
	@rm -f $(SUBMISSIONDIR)/$(ZIP)
	zip --quiet -r $(SUBMISSIONDIR)/$(ZIP) . -x /.git* /$(OUTPUTDIR)* /$(SUBMISSIONDIR)/*.zip

##########
# DOCKER #
##########

PAPERDIR := $$(pwd)
IMAGE := bichselb/latex-plus:version-2
CONTAINER := latex-plus-container
RUN := sudo docker run \
		-it \
		--name $(CONTAINER) \
		--workdir="/paper" \
		-v $(PAPERDIR):/paper \
		$(IMAGE)


# all commands involving docker use sudo, which is typically required to use docker commands

# launch a docker container using the image, which will provide a shell in the container
.PHONY: docker-run
docker-run: clean-container
	$(RUN)

# remove the created docker container
.PHONY: clean-container
clean-container:
	sudo docker rm /$(CONTAINER) || true

# all above commands, run in docker
.PHONY: docker-run
docker-pdf: clean-container
	$(RUN) make pdf

.PHONY: docker-run
docker-overfull: clean-container
	$(RUN) make overfull

.PHONY: docker-run
docker-split: clean-container
	$(RUN) make split

.PHONY: docker-run
docker-gray: clean-container
	$(RUN) make gray

.PHONY: docker-run
docker-check: clean-container
	$(RUN) make check

.PHONY: docker-run
docker-finalcheck: clean-container
	$(RUN) make finalcheck

.PHONY: docker-run
docker-zip: clean-container
	$(RUN) make zip

