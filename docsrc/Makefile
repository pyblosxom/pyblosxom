JADE       = openjade
HTMLDOC    = htmldoc
JADECONF   = -t sgml \
		-d ./mystyle.dsl\#html \
		/usr/share/sgml/declaration/xml.dcl \
		./pyblosxom_manual.docbook

HTMLCONF   = --quiet -f ./manual/Pyblosxom_manual.pdf \
		./manual/Pyblosxom_manual.html

all: multiple pdf

directory:
	if [ ! -e ./manual ]; then \
		echo "Creating manual directory"; \
		mkdir ./manual; \
	fi

multiple: directory css
	$(JADE) -i html $(JADECONF)
	echo "Copying book1.html to index.html."
	cp book1.html index.html
	mv *.html ./manual/
	echo "Manual in multiple HTML pages complete."

single: directory css
	echo "Creating single HTML document."
	$(JADE) -V nochunks $(JADECONF) > ./manual/Pyblosxom_manual.html
	echo "Manual in a single HTML page complete."

pdf: single
	echo "Creating PDF"
	$(HTMLDOC) $(HTMLCONF)
	echo "Manual in PDF form complete."

css:
	echo "Copying manual_style.css file over."
	cp ./manual_style.css ./manual/

clean:
	echo "Removing files"
	- rm ./manual/*
	- rm -r ./manual
