dafault: view

view: pdf
	evince main.pdf
print: pdf
	lpr main.pdf -o outputorder=reverse

pdf:
	pandoc --smart --toc --template=template.tex *.md -o main.pdf
