#/bin/sh
cd /home/twl/pyblog/blosxom
/home/twl/bin/j2sdk1.4.1/bin/java -cp /home/twl/pyblog/lib/lucene-1.2/lucene-demos-1.2.jar:/home/twl/pyblog/lib/lucene-1.2/lucene-1.2.jar:/home/twl/pyblog/bin BlosxomIndexer -create -index /home/twl/pyblog/index .