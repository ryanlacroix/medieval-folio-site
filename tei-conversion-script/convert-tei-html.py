#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
import sys

from bs4 import BeautifulSoup
from bs4 import element

from fuzzywuzzy import fuzz
from fuzzywuzzy import process


# In[9]:


try :
    filename = sys.argv[1]
    root = BeautifulSoup(open("./tei/"+filename,
                          encoding="utf-8"),'xml')
except:
    print("Provide a TEI file to run this script on.\n Eg python3 convert-tei-to-html.py Ms__1.xml")
    exit()
#filename = "Ms__1.xml"


# In[201]:


# Map facs_# to proper folio page name
facs_to_folio = {}

for facs in root.find_all('facsimile'):
    facs_to_folio[facs['xml:id']] = facs.find('graphic')['url']
    #print(facs['xml:id'],' ',facs.find('graphic')['url'])


# In[202]:


# Split the dataset by page
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
                # Handle abbreviations
                if sib.name == 'choice':
                    # Handle rubrications inside abbrs
                    if sib.find('rubrication'):
                        inner_rubr = sib.find('rubrication')
                        abbr = str(sib.find('abbr'))
                    else:
                        abbr = sib.find('abbr').text
                        
                    expan = sib.find('expan').text
                    lb_string += '<span data-html="true" data-toggle="tooltip" title="<em>' +expan+ '</em>"><mark>' +abbr+ '</mark></span>'
                    continue
            lb_string += str(sib)
        lb_string += '</div>'
        page_str += lb_string
    page_str += '</div>'
    # Translate tags to HTML
    page_str = page_str.replace('<rubrication>','<span rubricated="true">')
    page_str = page_str.replace('</rubrication>','</span>')
    page_str = page_str.replace('<Drop-Capital>', '<span dropCap="true">')
    page_str = page_str.replace('</Drop-Capital>', '</span>')
    page_str = page_str.replace("\n",'')

    # Output newly built page to an html file
    try:
        #filename = facs_to_folio[p['facs'].replace('_r1','').replace('#','')]
        if p['facs'].find('region') > 0:
            print(p['facs'])
            print(p['facs'].split('_')[0] + '_' + p['facs'].split('_')[1])
            filename = facs_to_folio[p['facs'].split('_')[0].replace('#','') + '_' + p['facs'].split('_')[1]]
        else:
            filename = facs_to_folio[p['facs'].replace('_r1','').replace('_r2','').replace('_r3','').replace('#','')]
        print(filename + ' works')
    except Exception as e:
        #print('Page ' +facs_to_folio[p['facs'].replace('_r1','').replace('#',
        #                    '').split('_region')[0].replace('_r2','').replace('_r3',
        #                                                            '')]+ ' has a problem')
        print(p['facs'].replace('_r1','').replace('#','')+ " has a problem")
        #filename = facs_to_folio[p['facs'].replace('_r1','').replace('_r2','').replace('_r3','').replace('#','')]
        continue

    filename_fixed = filename.replace('.JPG','.html').replace('.jpg',
            '.html').replace(' (duo)','').replace(' (bis)','')
    with open("./output/" + filename_fixed, "wb") as outfile:
        outfile.write(page_str.encode("utf-8"))

    print('--------page successsful--------')

print(facs_to_folio)


# %%
