#!/usr/bin/env python3

#########
# USAGE #
#########
# ./matplotlib-template.py
#
# Requirements
# - matplotlib
# - numpy

###########
# PURPOSE #
###########
# A template that generates nicely formatted matplotlib figures
# - Follows
#   https://inf.ethz.ch/personal/markusp/teaching/guides/guide-presentations.pdf
#   (pages 38-42)

#################
# CONFIGURATION #
#################
# You may need to change the fonts to follow the rest of your document. For a
# list of commonly used fonts based on conference, see ./inkscape-header.tex.

##########
# SCRIPT #
##########

# imports
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np

# font sizes
labelsize=20
ticksize=15

# set fonts
rcParams['pdf.fonttype'] = 42
rcParams['ps.fonttype'] = 42
rcParams['font.family'] = 'sans-serif'

# the following line may result in a warning `Font family ['sans-serif'] not
# found. Falling back to DejaVu Sans.`
# rcParams['font.sans-serif'] = ['Gill Sans MT']

##################
# PREPARE FIGURE #
##################

# prepare figure
f = plt.figure(figsize=[6.4, 3])
ax = plt.gca() # Get current axes instance on the current figure

# set axis labels
plt.xlabel('$x$', fontsize=labelsize)
plt.ylabel('$\\sin(x)$', rotation=0, fontsize=labelsize)
ax.yaxis.set_label_coords(0.01, 1.02)

# add label to figure
ax.text(1.1, 0.2, "$\\sin(x)$", fontsize=labelsize)

# set font size for ticks
plt.setp(ax.get_xticklabels(), fontsize=ticksize)
plt.setp(ax.get_yticklabels(), fontsize=ticksize)

# set background to light gray
ax.yaxis.grid(True, color=(1,1,1))
ax.set_facecolor( (0.97, 0.97, 0.97) )

# remove bounding lines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

#############
# PLOT DATA #
#############

# generate data
x = np.arange(-3, 3, 0.01)
y = np.sin(x)

# plot
plt.plot(x, y, '-')

# automatically adjust subplot params so that the subplot(s) fits in to the
# figure area
f.tight_layout()

###############
# SAVE FIGURE #
###############

# save figure
# plt.show()
plt.savefig('./sin.pdf')
