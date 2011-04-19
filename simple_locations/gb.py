#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shapefile
#import pycountry
import zipfile
import os, sys
import tempfile
import slugify
import json



tmpdir="./tmp"

def gbz(f):
    tfile=zipfile.ZipFile(f,'r')
    tempfile.mkdtemp(dir=tmpdir)
    tfile.extractall(tmpdir)
    
def gbs(f):
    nf=[]
    sf = shapefile.Reader(f)
    
    fields = sf.fields
   
    fields=fields[1:]
    for f in fields:
        nf.append(f[0])
    records=sf.records()
    nl=[]
    for r in records:
        nl.append(dict(zip(nf,r)))
        
    for i in nl:
        if i.has_key('HASC_2'):
            split_values = i['HASC_2'].split(".")
            if len(split_values)>=2:
                i.update({'country_code':split_values[0],
                          'subdivision_code': split_values[1]})
                
            if len(split_values)>2:
                i.update({'lev2_code':split_values[2]})
                
        if i.has_key('HASC_1'):
            split_values = i['HASC_1'].split(".")
            if len(split_values)==2:
                i.update({'country_code':split_values[0],
                          'subdivision_code': split_values[1]})
        
        if i.has_key('NAME_0'):
            i.update({'country_name':i['NAME_0'],
                      'country_slug':slugify.slugify(unicode(i['NAME_0']))})
        
        if i.has_key('NAME_1'):
            i.update({'subdivision_name':i['NAME_1'],
                      'subdivision_slug':slugify.slugify(unicode(i['NAME_1']))})
        
        if i.has_key('NAME_2'):
            i.update({'lev2_name':i['NAME_2'],
                      'lev2_slug':slugify.slugify(unicode(i['NAME_2']))})
    
    return nl

if __name__ == "__main__":    
    """
    Accept a single string containing a gadm zip file or a shapefile
    """
    try: 
        f=sys.argv[1]
    except(IndexError):
        print "You must supply a shapefile."
        exit(1)
        
    try:

        r=gbs(f)
        print json.dumps(r[0], indent=4)
    except():
        print "An unexpected error occured. Here is the post-mortem:"
        print sys.exc_info()
