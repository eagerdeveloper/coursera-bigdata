#!/usr/bin/env python
import glob
import mincemeat
import re

text_files = glob.glob('hw3data/*')

print 'text_files = ', text_files

print 'Total files = ', len(text_files)

def file_contents(file_name):
    print 'file_name = ', file_name
    f = open(file_name)
    try:
        return f.read()
    finally:
        f.close()

##def split(line):
##    print line
    
datasource = dict((file_name, file_contents(file_name))
              for file_name in text_files)

##print datasource

##data = ["Humpty Dumpty sat on a wall",
##        "Humpty Dumpty had a great fall",
##        "All the King's horses and all the King's men",
##        "Couldn't put Humpty together again",
##        ]
# The data source can be any dictionary-like object
##source = dict(enumerate(datasource))
 
##line = 'books/aw/kimL89/DiederichM89:::Jim Diederich::Jack Milton:::Objects, Messages, and Rules in Database Design.'
##biblio = re.split(':::|::|\n', line)
##print 'BIBLIO: ', biblio

##print "LEN = ", len(biblio)
##authorslist = list(biblio)
##del authorslist[-1]
##del biblio[0]
##print 'BIBLIO: ', biblio
##
##bibliolength = len(biblio)
##print 'BIBLIO LENGTH = ', bibliolength
##
##for name in biblio[:bibliolength-1]:
##    print name, biblio[bibliolength-1]


print "################################"
def mapfn(key, value):
    import re
    for line in value.splitlines():
        biblio = re.split(':::|::|\n',line)
        del biblio[0]
##        print "BIBLIO: ", biblio
        bibliolength = len(biblio)

        for authorname in biblio[:bibliolength-1]:
##            print authorname, biblio[bibliolength-1]
            yield authorname, biblio[bibliolength-1].lower().strip().replace(",", "").replace(".", "").replace("-", "")

def reducefn(key, value):
    import re
    words = dict()
    allStopWords={'about':1, 'above':1, 'after':1, 'again':1, 'against':1, 'all':1, 'am':1, 'an':1, 'and':1, 'any':1, 'are':1, 'arent':1, 'as':1, 'at':1, 'be':1, 'because':1, 'been':1, 'before':1, 'being':1, 'below':1, 'between':1, 'both':1, 'but':1, 'by':1, 'cant':1, 'cannot':1, 'could':1, 'couldnt':1, 'did':1, 'didnt':1, 'do':1, 'does':1, 'doesnt':1, 'doing':1, 'dont':1, 'down':1, 'during':1, 'each':1, 'few':1, 'for':1, 'from':1, 'further':1, 'had':1, 'hadnt':1, 'has':1, 'hasnt':1, 'have':1, 'havent':1, 'having':1, 'he':1, 'hed':1, 'hell':1, 'hes':1, 'her':1, 'here':1, 'heres':1, 'hers':1, 'herself':1, 'him':1, 'himself':1, 'his':1, 'how':1, 'hows':1, 'i':1, 'id':1, 'ill':1, 'im':1, 'ive':1, 'if':1, 'in':1, 'into':1, 'is':1, 'isnt':1, 'it':1, 'its':1, 'its':1, 'itself':1, 'lets':1, 'me':1, 'more':1, 'most':1, 'mustnt':1, 'my':1, 'myself':1, 'no':1, 'nor':1, 'not':1, 'of':1, 'off':1, 'on':1, 'once':1, 'only':1, 'or':1, 'other':1, 'ought':1, 'our':1, 'ours ':1, 'ourselves':1, 'out':1, 'over':1, 'own':1, 'same':1, 'shant':1, 'she':1, 'shed':1, 'shell':1, 'shes':1, 'should':1, 'shouldnt':1, 'so':1, 'some':1, 'such':1, 'than':1, 'that':1, 'thats':1, 'the':1, 'their':1, 'theirs':1, 'them':1, 'themselves':1, 'then':1, 'there':1, 'theres':1, 'these':1, 'they':1, 'theyd':1, 'theyll':1, 'theyre':1, 'theyve':1, 'this':1, 'those':1, 'through':1, 'to':1, 'too':1, 'under':1, 'until':1, 'up':1, 'very':1, 'was':1, 'wasnt':1, 'we':1, 'wed':1, 'well':1, 'were':1, 'weve':1, 'were':1, 'werent':1, 'what':1, 'whats':1, 'when':1, 'whens':1, 'where':1, 'wheres':1, 'which':1, 'while':1, 'who':1, 'whos':1, 'whom':1, 'why':1, 'whys':1, 'with':1, 'wont':1, 'would':1, 'wouldnt':1, 'you':1, 'youd':1, 'youll':1, 'youre':1, 'youve':1, 'your':1, 'yours':1, 'yourself':1, 'yourselves':1}

##    print "\nKEY: ", key, ", VALUE: ", value
    print "\nAUTHOR: ", key, 

    for pub in value:
##        print "PUB: ", pub
        for word in pub.split():
##            print " WORD: ", words.keys()
            if len(word) > 1:
                if word not in allStopWords.keys():
                    if word in words.keys():
                        words[word] = words[word] + 1
                    else:
                        words[word] = 1
##    print "WORDS = ", words
                
    for key, value in sorted(words.iteritems(), key=lambda (k,v): (v,k)):
        print "%s: %s" % (key, value)

##    for k in words.keys():
##        print 'WORDS[', k, ']=', words[k]
##        return k,len(words[k])
##    return key, len(value)


s = mincemeat.Server()
s.datasource = datasource
s.mapfn = mapfn
s.reducefn = reducefn

results = s.run_server(password="changeme")
print results
