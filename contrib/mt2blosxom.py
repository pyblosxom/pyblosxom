#!/usr/bin/env python

import sys
import time
import os
import re
import random
    
def convert(inputfile, outputdir):    
    input = open(inputfile).read()
    entries = input.split("--------")
    for entry in entries:
        if entry.strip():
            sections = entry.split("----")
            body = sections[1].split(":",1)[1]
            extendedbody = sections[2].split(":",1)[1]
            fields = sections[0].strip().split("\n")
            publish = 0
            for field in fields:
                if field.strip():
                    tag, value = field.split(": ", 1)
                    if tag == "TITLE":
                        title = value.strip()
                    elif tag == "DATE":
                        date = value.strip()
                    elif tag == "STATUS":
                        if value.strip() == "publish":
                            publish = 1

            timestamp = time.mktime(time.strptime(date, "%m/%d/%Y %H:%M:%S %p"))
            outputfile = title.strip()
            if not outputfile: outputfile = body[:20].strip()
            outputfile= "%s/%s" % (outputdir, re.sub(r"[^a-zA-Z0-9]", "_", outputfile))
            if os.path.isfile(outputfile + ".txt") or os.path.isfile(outputfile + ".txt-"):
                outputfile = outputfile + str(random.random()).split(".")[1]
            if publish:
                outputfile = outputfile + ".txt"
            else:
                outputfile = outputfile + ".txt-"

            output = open(outputfile, "w")
            output.write(title+"\n")
            output.write(body)
            output.write(extendedbody)
            output.close()
            # set the modified date on the output file
            os.utime(outputfile, (timestamp, timestamp)) 
if __name__=="__main__":
    try:
        inputfile, outputdir = sys.argv[1:]
    except:
        print """Usage: mt2blosxom mtexportfile datadir
        mtexportfile - File containing exported Movable Type entries
        datadir -  Blosxom directory to put files in"""
	sys.exit(0)

    convert(inputfile, outputdir)

