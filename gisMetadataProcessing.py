from lxml import etree
import csv
import os


def creatkeyword(value, newkeyword):
    """Create keyword element."""
    keywordkey = etree.SubElement(newkeyword, tag + 'key')
    keywordkey.text = value
    if vocab == 'fst':
        getfasturi(value, keywordkey)
    else:
        pass
    newkeyword.append(keywordkey)


def getfasturi(value, keywordkey):
    """Get URI for FAST term."""
    urn = ''
    fastcsv = csv.DictReader(open('fast.csv'))
    for row in fastcsv:
        if value == row['label']:
            urn = row['uri']
            break
        else:
            pass
    if urn == '':
        print('No FAST URI - check value in spreadsheet')
        exit()
    else:
        keywordkey.attrib['urn'] = urn


def splitkeywords(fieldname, newkeyword):
    """Split multiple keyword values separated by pipe delimiters."""
    values = row[fieldname].split('|')
    for value in values:
        creatkeyword(value, newkeyword)


currdir = os.getcwd()

vocabdict = {'iso': 'ISO 19115 Topic Category', 'fst': 'searchFAST'}

csvfile = 'gis.csv'

metadatacsv = csv.DictReader(open(csvfile))

for row in metadatacsv:
    newkeywords = etree.Element('keywords')
    for fieldname, value in row.items():
        if fieldname == 'filename':
            filename = row[fieldname]
            print(filename)
            file = etree.parse(filename)
            oldkeywords = file.find('idinfo').find('keywords')
            oldkeywords.getparent().remove(oldkeywords)

        else:
            tag = fieldname[:-3]
            vocab = fieldname[-3:]
            newkeyword = etree.Element(tag)
            tagkt = etree.SubElement(newkeyword, tag + 'kt')
            tagkt.text = vocabdict[vocab]
            if '|' in row[fieldname]:
                splitkeywords(fieldname, newkeyword)
            else:
                value = row[fieldname]
                creatkeyword(value, newkeyword)
            newkeywords.append(newkeyword)

    idinfo = file.find('idinfo')
    idinfo.append(newkeywords)
    updatedFolder = os.path.join(currdir, 'Updated')
    if not os.path.exists(updatedFolder):
        os.makedirs(updatedFolder)
    updatedfile = os.path.join(updatedFolder, filename)

    f = open(updatedfile, 'wb')
    f.write(etree.tostring(file, pretty_print=True))
