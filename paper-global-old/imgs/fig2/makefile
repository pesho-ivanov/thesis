all: sh csh pruning

sh:
	drawio --export --embed-diagram heuristics.drawio -p 1 		-o sh.svg
	drawio --export --embed-diagram heuristics.drawio -g 1..1 	-o sh.pdf
csh:
	drawio --export --embed-diagram heuristics.drawio -p 2 		-o csh.svg
	drawio --export --embed-diagram heuristics.drawio -g 2..2 	-o csh.pdf
pruning:
	drawio --export --embed-diagram heuristics.drawio -p 3 		-o pruning.svg
	drawio --export --embed-diagram heuristics.drawio -g 3..3 	-o pruning.pdf

# Png files are very large and should be avoided.
png:
	drawio --export 				heuristics.drawio -p 1 		-o sh.png --scale 10
	drawio --export 				heuristics.drawio -p 2 		-o csh.png --scale 10
	drawio --export 				heuristics.drawio -p 3 		-o pruning.png --scale 10

# Png files are very large and should be avoided.
png-small:
	drawio --export 				heuristics.drawio -p 1 		-o sh-small.png --scale 3
	drawio --export 				heuristics.drawio -p 2 		-o csh-small.png --scale 3
	drawio --export 				heuristics.drawio -p 3 		-o pruning-small.png --scale 3
