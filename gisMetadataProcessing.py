from lxml import etree
import csv
import os
import pathlib


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
        print('No FAST URI for ' + value + ' - check value in spreadsheet')
        exit()
    else:
        keywordkey.attrib['urn'] = urn


def splitkeywords(fieldname, newkeyword):
    """Split multiple keyword values separated by pipe delimiters."""
    values = row[fieldname].split('|')
    for value in values:
        creatkeyword(value, newkeyword)


def createfile(file, outputfilepath):
    """Create XML file."""
    updatedfile = os.path.join(outputfilepath, filename)
    f = open(updatedfile, 'wb')
    f.write(etree.tostring(file, pretty_print=True))


vocabdict = {'iso': 'ISO 19115 Topic Category', 'fst': 'searchFAST'}

csvfile = 'gis.csv'
outputfilepath = ''


metadatacsv = csv.DictReader(open(csvfile))
for row in metadatacsv:
    newkeywords = etree.Element('keywords')
    for fieldname, value in row.items():
        if fieldname == 'filename':
            filepath = row[fieldname]
            p = pathlib.Path(filepath)
            filename = p.name
            print(filename)
            file = etree.parse(filepath)
            oldkeywords = file.find('idinfo').find('keywords')
            if oldkeywords is not None:
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

    createfile(file, outputfilepath)
