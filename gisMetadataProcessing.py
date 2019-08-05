from bs4 import BeautifulSoup
import csv
import os


def creatkeyword(value):
    """Create keyword element."""
    keywordkey = keywordxml.new_tag(tag + 'key')
    keywordkey.string = value
    if vocab == 'fst':
        getfasturi(value, keywordkey)
    else:
        pass
    keyword.append(keywordkey)


def getfasturi(value, keywordkey):
    """Get URI for FAST term."""
    urn = ''
    fastcsv = csv.DictReader(open('fast.csv'))
    for row in fastcsv:
        if value == row['label']:
            urn = row['uri']
            print(urn)
            break
        else:
            pass
    if urn == '':
        print('No FAST URI - check value in spreadsheet')
        exit()
    else:
        keywordkey['urn'] = urn


def splitkeywords(fieldname):
    """Split multiple keyword values separated by pipe delimiters."""
    values = row[fieldname].split('|')
    for value in values:
        creatkeyword(value)


dir = os.path.dirname(os.path.realpath(__file__))

vocabdict = {'iso': 'ISO 19115 Topic Category', 'fst': 'searchFAST'}

csvfile = 'gis.csv'

metadatacsv = csv.DictReader(open(csvfile))

for row in metadatacsv:
    xml = BeautifulSoup('<keywords></keywords>', 'lxml')
    keywords = xml.find('html').find('body').findChild()
    for fieldname, value in row.items():
        if fieldname == 'filename':
            filename = row[fieldname]
            file = BeautifulSoup(open(filename), 'lxml')
            file = file.find('html').find('body').findChild()
            for metadata in file.findAll('keywords'):
                metadata.decompose()
        else:
            tag = fieldname[:-3]
            vocab = fieldname[-3:]
            keywordxml = BeautifulSoup('<' + tag + '></' + tag + '>', 'lxml')
            keyword = keywordxml.find('html').find('body').findChild()
            tagkt = keywordxml.new_tag(tag + 'kt')
            tagkt.string = vocabdict[vocab]
            keyword.append(tagkt)
            if '|' in row[fieldname]:
                splitkeywords(fieldname)
            else:
                value = row[fieldname]
                creatkeyword(value)
            keywords.append(keyword)

    file.find('idinfo').append(keywords)
    updatedFolder = os.path.join(dir, 'Updated')
    if not os.path.exists(updatedFolder):
        os.makedirs(updatedFolder)
    updatedfile = os.path.join(updatedFolder, filename)
    f = open(updatedfile, 'w')
    f.write(str(file))
