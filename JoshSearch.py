import xml.etree.ElementTree as ET
import os
from utility import deaccent


def perseuscount(froot, i, j, inffile, fn):
    """Prints every instance of this articular infinitive construction for Perseus treebanks."""
    idtoheadid = {}
    inflist = []
    verbslistbyid = []
    idtoform = {}
    for body in froot:
        for sentence in body:
            for word in sentence:
                if word.tag == 'word':
                    # Create artheadid{ID:HeadID}
                    idtoheadid[word.get('id')] = word.get('head')
                    # Create a list of every id of an infinitive.
                    if word.get('postag')[4] == 'n':
                        inflist.append(word.get('id'))
                    # Create a dictionary idtoform{ID:form}
                    idtoform[word.get('id')] = word.get('form')
                    if word.get('postag')[0] == 'v':
                        verbslistbyid.append(word.get('id'))

    for body in froot:
        for sentence in body:
            for word in sentence:
                if word.tag == 'word':
                    if deaccent(word.get('lemma')) == 'ο' and word.get('head') in inflist and \
                            word.get('relation') == 'ATR':
                        infinitiveid = word.get('head')
                        mainverbid = idtoheadid[infinitiveid]
                        if mainverbid in verbslistbyid:
                            for infsubj in sentence:
                                if infsubj.tag == 'word':
                                    if infsubj.get('head') == infinitiveid and infsubj.get('relation') == 'SBJ' and\
                                            infsubj.get('postag')[7] == 'a':
                                        for infobj in sentence:
                                            if infobj.tag == 'word':
                                                if infobj.get('postag')[7] == 'a' and infobj.get('head')\
                                                      == infinitiveid and infobj.get('relation') == 'OBJ':
                                                    print(sentence.get('subdoc'), idtoform[mainverbid],
                                                          infsubj.get('form'), '(SUBJ)', word.get('form'),
                                                          idtoform[infinitiveid], infobj.get('form'))
                                                    inffile.writelines([fn, sentence.get('subdoc')])
                                                    if int(word.get('id')) > int(infobj.get('id')):
                                                        print('^^Backwards^^')
                                                        j += 1
                                                    i += 1
                                    if infsubj.get('head') == mainverbid and infsubj.get('relation') == 'OBJ' and\
                                            infsubj.get('postag')[7] == 'a':
                                        for infobj in sentence:
                                            if infobj.tag == 'word':
                                                if infobj.get('postag')[7] == 'a' and infobj.get('head') ==\
                                                        infinitiveid and infobj.get('relation') == 'OBJ':
                                                    print(sentence.get('subdoc'), idtoform[mainverbid],
                                                          infsubj.get('form'), "(OBJ)", word.get('form'),
                                                          idtoform[infinitiveid], infobj.get('form'))
                                                    inffile.writelines([fn, sentence.get('subdoc')])
                                                    if int(word.get('id')) > int(infobj.get('id')):
                                                        print('^^Backwards^^')
                                                        j += 1
                                                    i += 1

    return i, j, inffile


def proielcount(froot, i, j, inffile, fn):
    """Prints every instance of this articular infinitive construction for PROIEL treebanks."""
    idtoheadid = {}
    inflist = []
    verbslistbyid = []
    idtoform = {}

    for source in froot:
        for division in source:
            for sentence in division:
                for token in sentence:
                    if token.tag == 'token' and token.get('empty-token-sort') is None:
                        # Create artheadid{ID:HeadID}
                        idtoheadid[token.get('id')] = token.get('head-id')
                        # Create a list of every id of an infinitive.
                        if token.get('morphology')[3] == 'n':
                            inflist.append(token.get('id'))
                        # Create a dictionary idtoform{ID:form}
                        idtoform[token.get('id')] = token.get('form')
                        if token.get('part-of-speech') == 'V-':
                            verbslistbyid.append(token.get('id'))

    for source in froot:
        for division in source:
            for sentence in division:
                if sentence.tag == 'sentence':
                    for token in sentence:
                        if token.tag == 'token' and token.get('empty-token-sort') is None:
                            if deaccent(token.get('lemma')) == 'ο' and token.get('head-id') in inflist and\
                                    token.get('relation') == 'aux':
                                infinitiveid = token.get('head-id')
                                mainverbid = idtoheadid[infinitiveid]
                                if mainverbid in verbslistbyid:
                                    for infsubj in sentence:
                                        if infsubj.tag == 'token' and infsubj.get('empty-token-sort') is None:
                                            if infsubj.get('morphology')[6] == 'a' and \
                                                    infsubj.get('head-id') == mainverbid and \
                                                    infsubj.get('relation') == 'obj':
                                                for infobj in sentence:
                                                    if infobj.tag == 'token' and infobj.get('empty-token-sort') is None:
                                                        if infobj.get('morphology')[6] == 'a' and \
                                                                infobj.get('head-id') == infinitiveid and \
                                                                infobj.get('relation') == 'obj':
                                                            print(token.get('citation-part'), idtoform[mainverbid],
                                                                  infsubj.get('form'), 'OBJ', token.get('form'),
                                                                  idtoform[token.get('head-id')], infobj.get('form'))
                                                            inffile.writelines([fn, token.get('citation-part')])
                                                            if int(token.get('id')) > int(infobj.get('id')):
                                                                print('^^Backwards!')
                                                                j += 1
                                                            i += 1
                                            if infsubj.get('morphology')[6] == 'a' and \
                                                    infsubj.get('head-id') == infinitiveid and \
                                                    infsubj.get('relation') == 'sub':
                                                for infobj in sentence:
                                                    if infobj.tag == 'token' and infobj.get('empty-token-sort') is None:
                                                        if infobj.get('morphology')[6] == 'a' and \
                                                                infobj.get('head-id') == infinitiveid and \
                                                                infobj.get('relation') == 'obj':
                                                            print(token.get('citation-part'), idtoform[mainverbid],
                                                                  infsubj.get('form'), 'SUB', token.get('form'),
                                                                  idtoform[token.get('head-id')], infobj.get('form'))
                                                            inffile.writelines([fn, token.get('citation-part')])
                                                            if int(token.get('id')) > int(infobj.get('id')):
                                                                print('^^Backwards!')
                                                                j += 1
                                                            i += 1

    return i, j, inffile


os.chdir('/home/chris/Desktop/CustomTB')
indir = os.listdir('/home/chris/Desktop/CustomTB')
infFile = open('/home/chris/Desktop/articularinf.txt', 'w')
infFile.write('Every time an articular infinitive occurs with a head that is an explicit verb and that articular '
              'infinitive also has an explicit accusative subject and accusative object.')
infCount = 0
backwardCount = 0
for file_name in indir:
    if not file_name == 'README.md':
        tb = ET.parse(file_name)
        tbroot = tb.getroot()
        print(file_name)
        if tbroot.tag == 'proiel':
            infCount, backwardCount, infFile = proielcount(tbroot, infCount, backwardCount, infFile, file_name)
        if tbroot.tag == 'treebank':
            infCount, backwardCount, infFile = perseuscount(tbroot, infCount, backwardCount, infFile, file_name)
infFile.close()
print('This construction occurs', infCount, 'times.')
print('The object of the infinitive occurs before the article of the infinitive', backwardCount, 'times.')
