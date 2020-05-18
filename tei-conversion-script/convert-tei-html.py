#!/usr/bin/env python
# coding: utf-8

import os
import sys

from bs4 import BeautifulSoup
from bs4 import element

import re

def replace_nth(string, sub, wanted, n):
    where = [m.start() for m in re.finditer(sub, string)][n-1]
    before = string[:where]
    after = string[where:]
    after = after.replace(sub, wanted, 1)
    new_string = before + after
    return new_string

try :
    #filename = sys.argv[1]
    filename = "./tei-conversion-script/tei/Ms__1.xml"
    #filename = "./tei-conversion-script/tei/missing_folios_xml_draft_1.xml"

    orig_text = ""
    with open(filename, "rb") as infile:
        orig_text = infile.read().decode('utf-8')
        
        pattern = re.compile(r'(<\/Drop-Capital>(.*?)<rubrication\/>(\2))')
        
        for (phrase, term, _term) in re.findall(pattern, orig_text):
            print(phrase)
            #phrase_fixed = phrase[0:phrase.index('</abbr>')+7]
            phrase_fixed = replace_nth(phrase, term, '', 2)
            print(phrase_fixed,'\n')
            orig_text = orig_text.replace(phrase,phrase_fixed)

    root = BeautifulSoup(orig_text)
except Exception as e:
    print(e)
    print("Provide a TEI file to run this script on.\n Example usage: python3 convert-tei-to-html.py Ms__1.xml")
    exit()

# Map facs_# to proper folio page name
facs_to_folio = {}

for facs in root.find_all('facsimile'):
    facs_to_folio[facs['xml:id']] = facs.find('graphic')['url']

# Preprocess all choice elements
for choice in root.findAll('choice'):
    abbr = str(choice.find('abbr'))
    expan = choice.find('expan').text
    new_choice = BeautifulSoup('<span data-html="true" data-toggle="tooltip" title="<em>' +expan+ '</em>"><mark>' +abbr+ '</mark></span>')
    choice.replace_with(new_choice.span)

# Split the dataset by page
num_files = 0 # Files successfully processed
for p in root.find_all('p'):
    page_str = '<div id="currentPage">'
    # Split the page by lines
    for lb in p.find_all('lb'):
        reading_order = str(int(lb['n'].replace('N','')))
        
        # Append everything under one lb into a string and wrap in a div
        lb_string = '<div readingOrderIndex="'+reading_order+'">'
        
        # Walk through the contents of this line until the next line is found
        for sib in lb.next_siblings:
            if type(sib) == element.Tag:
                if sib.has_attr('n'):
                    break
            lb_string += str(sib)
        lb_string += '</div>'
        page_str += lb_string
    page_str += '</div>'
    # Translate tags to HTML
    page_str = page_str.replace('<rubrication>','<span rubricated="true">')
    page_str = page_str.replace('</rubrication>','</span>')
    page_str = page_str.replace('<Drop-Capital>', '<span dropCap="true">')
    page_str = page_str.replace('</Drop-Capital>', '</span>')
    # In some cases Tranksribus uses lowercase for Drop-Caps
    page_str = page_str.replace('<drop-capital>', '<span dropCap="true">')
    page_str = page_str.replace('</drop-capital>', '</span>')
    page_str = page_str.replace("\n",'')

    # Output newly built page to an html file
    try:
        if p['facs'].find('region') > 0:
            filename = facs_to_folio[p['facs'].split('_')[0].replace('#','') + '_' + p['facs'].split('_')[1]]
        else:
            filename = facs_to_folio[p['facs'].replace('_r1','').replace('_r2','').replace('_r3','').replace('#','')]
    except Exception as e:
        print(p['facs'].replace('_r1','').replace('#','')+ " has a problem")
        continue

    filename_fixed = filename.replace('.JPG','.html').replace('.jpg',
            '.html').replace(' (duo)','').replace(' (bis)','')
    if page_str == '<div id="currentPage"></div>':
        # Skip empty pages
        continue
    with open("./tei-conversion-script/output/" + filename_fixed, "wb") as outfile:
        outfile.write(page_str.encode("utf-8"))
        num_files += 1

print('Finished!')
print(num_files, ' files successfully processed.')