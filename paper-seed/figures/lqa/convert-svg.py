#!/usr/bin/env python3

#########
# USAGE #
#########
# ./convert-svg.py
#
# Requirements
# - inkscape

###########
# PURPOSE #
###########
# Converts all SVGs to PDFs
# - If the filename end with "tex.svg", use tex export (replaces path in 
#   generated "tex" by a relative path)
# - Otherwise, use normal export

import os
import re
import argparse
import subprocess

# determine directory containing this script
script_directory = os.path.dirname(os.path.realpath(__file__))
default_directory = os.path.join(script_directory, '..')


def find_svgs(directory):
	for filename in os.listdir(directory):
		if filename.endswith(".svg"):
			svg = filename
			pdf = re.sub('svg$', 'pdf', svg)

			is_tex_export = svg.endswith('tex.svg')
			yield svg, pdf, is_tex_export


def tex_export(svg, pdf, directory, rel_path):
	export = [
		'inkscape',
		f'--export-pdf={pdf}',
		'--export-latex',
		'--export-area-drawing',
		svg
	]
	subprocess.run(export, cwd=directory)

	replace = [
		'sed',
		'-i',
		f"s|{pdf}|{rel_path}/{pdf}|g",
		f'{pdf}_tex'
	]
	subprocess.run(replace, cwd=directory)


def default_export(svg, pdf, directory):
	export = [
		'inkscape',
		f'--export-pdf={pdf}',
		'--export-area-drawing',
		svg
	]
	subprocess.run(export, cwd=directory)


def export_all(directory, rel_path, force, simulate):
	print('Processing', directory)
	exported = []

	for svg, pdf, is_tex_export in find_svgs(directory):
		print('>', svg, '->', pdf)

		svg_time = os.path.getmtime(os.path.join(directory, svg))
		try:
			pdf_time = os.path.getmtime(os.path.join(directory, pdf))
		except FileNotFoundError:
			pdf_time = 0
		if svg_time < pdf_time and not force:
			print(' ', '(already up to date)')
			continue

		if simulate:
			print(' ', '(skipping export)')
			continue

		exported += [svg]
		if is_tex_export:
			print(' ', '(exporting tex)')
			tex_export(svg, pdf, directory, rel_path)
		else:
			print(' ', '(exporting pdf)')
			default_export(svg, pdf, directory)
	
	return exported


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Convert SVGs to PDFs.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('--directory', default=default_directory, help='Directory to process')
	parser.add_argument('--rel-path', default='./figures', help='Relative path to be used for tex export')
	parser.add_argument('--force', action='store_true', help='Export even if not newer.')
	parser.add_argument('--simulate', action='store_true', help='Only print which files will be exported.')
	args = parser.parse_args()

	exported = export_all(args.directory, args.rel_path, args.force, args.simulate)
	
	print(f"\nEXPORTED {len(exported)} SVGs.")
	for e in exported:
		print('-', e)