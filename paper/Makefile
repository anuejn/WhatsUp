all: view
view: pdf
	evince main.pdf
pdf:
	pandoc --smart --toc --template=template.tex *.md -o main.pdf
