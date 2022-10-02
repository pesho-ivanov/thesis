#!/bin/bash
# Prepare a full inkscape header, including custom headers
#
# USAGE: ./combine-headers.sh

# navigate to directory containing script
SCRIPTDIR="$(dirname "$(readlink -f "$0")")"
cd "$SCRIPTDIR"

# relevant files
HEADER=inkscape-header.tex
FULL=inkscape-header-full.tex

########################
# GENERATE FULL HEADER #
########################

# start with default header
cat $HEADER > $FULL

# add custom headers
cat ../../headers/header.tex >> $FULL

# [OPTIONAL] add more headers
# cat ../../headers/lqa/listing.tex >> $FULL