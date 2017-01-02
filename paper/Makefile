dafault: view

view: pdf
	evince main.pdf 2> /dev/null
print: pdf
	lpr main.pdf -o outputorder=reverse

pdf:
	pandoc --smart --toc -N --template=template.tex *.md -o main.pdf

tex:
	pandoc --smart --toc -N --template=template.tex *.md -o main.tex
