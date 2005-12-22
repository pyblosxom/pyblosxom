docbook:
	echo Creating directory
	-mkdir ./manual

	echo Removing files
	-rm ./manual/*

	echo Compiling docbook files.
	openjade -t sgml \
	     -i html \
	     -d ./mystyle.dsl\#html \
	     /usr/share/sgml/declaration/xml.dcl \
	     ./pyblosxom_manual.docbook

	echo Copying book1.html to index.html.
	cp book1.html index.html
	mv *.html ./manual/

	echo Copying manual_style.css file over.
	cp ./manual_style.css ./manual/

	echo End.

pdf:
	docbook2pdf pyblosxom_manual.docbook
