#!/usr/bin/env python
"""
Build tuple for country code drop down
"""
inPath="iso3166.txt"
OutPath="new_iso3166.txt"


outfile =open(OutPath, 'w')
line=[]
with open(inPath, 'r') as f:
    for i, l in enumerate(f):
        line=l.split()
        countryname=""
        for j in line[0:len(line)-1]:
            countryname="%s %s" % (countryname, j)
            if countryname[0]==" ":
                countryname=countryname[1:]
        newline="""("%s", "%s"),""" % (line[-1], countryname)
        print newline
        outfile.write(newline)
        outfile.write("\n")
    numlines= i + 1

    


f.close()
outfile.close()