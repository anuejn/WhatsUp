dafault: view

view: pdf
	evince main.pdf 2> /dev/null
print: pdf
	lpr main.pdf -o outputorder=reverse

pdf: code_format
	pandoc --smart --toc -N --listings --bibliography=references.bib --csl=din-1505-2-numeric.csl --filter=pandoc-fignos --template=template.tex --latex-engine=xelatex *.md -o main.pdf

tex: code_format
	pandoc --smart --toc -N --listings --filter pandoc-fignos --template=template.tex *.md -o main.tex

code_format:
	./code_to_md.py > 05_code.md
