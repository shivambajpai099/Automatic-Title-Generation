import re
import nltk
import collections
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer, WordNetLemmatizer

res = 0
nres = 0
bicount = 0
no = 0
ad = 0
ot = 0
for i in range(102,139):
    print "\n"
    num = i
    name = "txt" + str(i) + ".txt"
    mod = open(name,"r")   #opensfile
    modi = open(name,"r") 
    print "FILE NO: " + str(i)
    stri = mod.read()
    stri = stri.lower()
    start = modi.readline()
    start = start.lower()
   
    start = start.replace('#','')
    start = nltk.word_tokenize(start)
    sr = stri
    ind = stri.find('\n') #deletes the first line (heading)
    stri = stri[ind+1:]
    #print sr.split('\n', 1)[0]  #prints the first line
    print "\n" 
    stri = re.sub(r'https?:\/\/.*[//ml]', '', stri, flags=re.MULTILINE) #removes url
    stri = re.sub(r'www.?.*[//ml]', '', stri, flags=re.MULTILINE) #removes url
    cleanr = re.compile('<.*?>')   #removes html tags
    stri = re.sub(cleanr, '', stri) 
    delim = [',','?','/','//','!','\\','[',']','&','-',':',';','@','...','>','<', '(',')',',','%','+','*','"','.',"'s","’s","s’","isn’t","’",'“',"‘","|"]
    new_s = stri
    for i in delim:  #removes delimiters
        new_s = new_s.replace(i, ' ')
    stri = ' '.join(new_s.split())
    #removes stopwords
    stop_words = set(stopwords.words('english'))
    tokens = nltk.word_tokenize(stri)
    filtered_sentence = []     
    for w in tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    tokens = filtered_sentence
    tok = []
    lemm = WordNetLemmatizer();
    for wo in tokens:
            try:
                tok.append(lemm.lemmatize(wo))
            except UnicodeDecodeError:
                tok.append(wo)
                
    st = []
    for wo in start:
            try:
                st.append(lemm.lemmatize(wo))
            except UnicodeDecodeError:
                st.append(wo)
    toke = nltk.pos_tag(tok)
    noun = []
    adj = []
    for a,b in toke:
        if b =="NN" or b =="NNP" or b == "NNS":
            noun.append(a)
        elif b == "JJ" or b == "JJR" or b == "JJS":
            adj.append(a)
    
    freq = nltk.FreqDist(tok)
    bgss = nltk.bigrams(toke)
    #compute frequency distribution for all the bigrams in the text
    fdist2 = nltk.FreqDist(bgss)
    print "Manual Title:" + ' '.join(st)
    keyword = list(collections.Counter(noun).most_common(4))
    keyword = keyword + list(collections.Counter(adj).most_common(2))
    key = []
    for a,b in keyword:
        key.append(a)
    print "\n"
    fin = []
    
    for a,b in fdist2.most_common(20):
        for k in key:
            if a[0][0] == k or a[1][0] == k:
                fin.append(a)
    count = 0
    loop = 0
    preva = ""
    prevb = ""
    title = []
    freq =  freq.most_common(2)
    for a,b in freq:
        title.append(a)
        if a in st:
            count = count + 1
    for a,b in fin:
        if a[0] != preva and b[0] != prevb and b[1] != 'VBG' and b[1] != 'RB' and b[1]!= 'MD' and b[1] != 'RBR' and a[1] != 'RB' and a[1] != 'VBN':
            title.append(a[0])
            title.append(b[0])
            loop = loop + 1
            preva = a[0]
            prevb = b[0]
            for word in st:
                if a[0] == word:
                    count = count + 1
                    if a[1] == "NN":
                        no = no + 1
                    elif a[1] == "JJ":
                        ad = ad + 1
                    else:
                        ot = ot + 1
                    break
                elif b[0] == word:
                    count = count + 1
                    if a[1] == "NN":
                        no = no + 1
                    elif a[1] == "JJ":
                        ad = ad + 1
                    else:
                        ot = ot + 1
                    break            
            fi = 0
            for word in st:
                if a[0] == word:
                    fi = 1
                    continue
                if b[0] == word:
                    if fi == 1:
                        bicount = bicount + 1
                        print "bigram"
                        break
        if loop == 2:
            break
    title = set(title)
    print "Prediceted Title:" + " ".join(title)
    if count>0:
        res = res+1
        print "RES"
    else:
        nres = nres + 1
        print "NRES"
print "RESULTS"
print "Matched:" + str(res)
print "Bigrams Matched:" + str(bicount)
print "Not matched:" + str(nres)
print "-------------------------"
print "POS Matched:"
print "Noun:" + str(no)
print "Adjectives:" + str(ad)
print "Others:" + str(ot)
