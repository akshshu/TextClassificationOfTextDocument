import os
import argparse
from nltk.tokenize import word_tokenize
import nltk
import math
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
import operator
tokenizer = RegexpTokenizer(r'\w+')
lemmatizer = WordNetLemmatizer()
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
stop = stopwords.words("english")


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(dest="datapathAdd",
                        help=" datapathAdd")
    parser.add_argument(dest="OutputFileName",
                        help=" Output file name")
    options = parser.parse_args()
    if not options.datapathAdd:
        parser.error("please specify dataset folder name")
    if not options.OutputFileName:
        parser.error("please specify Output filename")
    return options.datapathAdd, options.OutputFileName


datapath, out = get_arguments()

count1 = {}
count2 = {}
globalallWords = []
globalallWords2 = []

docCount = 0
docCount2 = 0

mut_Inf_c1 = {}
mut_Inf_c2 = {}


def compute(className, condprob1, condprob2):
    global tp, fp, fn
    for filename in os.listdir(datapath+"/"+className+"/test"):
        allWords = []
        filtered2 = []
        tokens = []
        with open(os.path.join(datapath+"/"+className+"/test", filename), "r") as file:
            document = file.read()
        tokens = tokenizer.tokenize(document.strip().lower())
        for t in tokens:
            t = str(t).strip()
            if t not in stop:
                filtered2.append(t)
        for dt in range(len(filtered2)):
            a = lemmatizer.lemmatize(filtered2[dt].strip())
            a = lemmatizer.lemmatize(a, pos="a")
            a = lemmatizer.lemmatize(a, pos="v")
            allWords.append(a)
        allWords = list(set(allWords))
        maxval = math.log(priorC1, 2)
        maxval2 = math.log(priorC2, 2)
        for word in allWords:
            try:
                if(condprob1[word]):
                    maxval = maxval+math.log(condprob1[word], 2)
            except Exception:
                maxval = maxval+0
            try:
                if(condprob2[word]):
                    maxval2 = maxval2+math.log(condprob2[word], 2)
            except Exception:
                maxval2 = maxval2+0

        if(maxval >= maxval2):
            tp = tp+1
        else:
            fp = fp+1
            fn = fn+1


def conditonProb(sorted_d, word1count, diWrdCount, tokenCount1):
    condprob1 = {}
    condprob10 = {}
    condprob100 = {}
    condprob1000 = {}
    condprob10000 = {}
    classTop = []
    for key in sorted_d:
        classTop.append(key)
    for key in classTop:
        condprob10000[key] = (word1count[key]+1) / (tokenCount1+diWrdCount)
    classTop = []
    sorted_d = dict(sorted(sorted_d.items(),
                           key=operator.itemgetter(1), reverse=True)[:1000])
    for key in sorted_d:
        classTop.append(key)
    for key in classTop:
        condprob1000[key] = (word1count[key]+1) / (tokenCount1+diWrdCount)
    classTop = []
    sorted_d = dict(sorted(sorted_d.items(),
                           key=operator.itemgetter(1), reverse=True)[:100])
    for key in sorted_d:
        classTop.append(key)
    for key in classTop:
        condprob100[key] = (word1count[key]+1) / (tokenCount1+diWrdCount)
    classTop = []
    sorted_d = dict(sorted(sorted_d.items(),
                           key=operator.itemgetter(1), reverse=True)[:10])
    for key in sorted_d:
        classTop.append(key)
    for key in classTop:
        condprob10[key] = (word1count[key]+1) / (tokenCount1+diWrdCount)
    classTop = []
    sorted_d = dict(sorted(sorted_d.items(),
                           key=operator.itemgetter(1), reverse=True)[:1])
    for key in sorted_d:
        classTop.append(key)
    for key in classTop:
        condprob1[key] = (word1count[key]+1) / (tokenCount1+diWrdCount)
    return condprob1, condprob10, condprob100, condprob1000, condprob10000


def func2():
    global docCount, docCount2
    for filename in os.listdir(datapath + "/class2/train"):
        allWords2 = []
        docCount2 = docCount2+1
        filtered2 = []
        tokens = []
        with open(os.path.join(datapath + "/class2/train", filename), "r") as file:
            document = file.read()
        tokens = tokenizer.tokenize(document.strip().lower())
        for t in tokens:
            t = str(t).strip()
            if t not in stop:
                filtered2.append(t)
        for dt in range(len(filtered2)):
            a = lemmatizer.lemmatize(filtered2[dt].strip())
            a = lemmatizer.lemmatize(a, pos="a")
            a = lemmatizer.lemmatize(a, pos="v")
            allWords2.append(a)
            globalallWords2.append(a)
        allWords2 = list(set(allWords2))
        for a in allWords2:
            try:
                if(count2[a] >= 1):
                    count2[a] = count2[a]+1
            except Exception:
                count2[a] = 1


def func():
    global docCount, docCount2
    for filename in os.listdir(datapath + "/class1/train"):
        allWords = []
        docCount = docCount+1
        filtered2 = []
        tokens = []
        with open(os.path.join(datapath + "/class1/train", filename), "r") as file:
            document = file.read()
        tokens = tokenizer.tokenize(document.strip().lower())
        for t in tokens:
            t = str(t).strip()
            if t not in stop:
                filtered2.append(t)
        for dt in range(len(filtered2)):
            a = lemmatizer.lemmatize(filtered2[dt].strip())
            a = lemmatizer.lemmatize(a, pos="a")
            a = lemmatizer.lemmatize(a, pos="v")
            allWords.append(a)
            globalallWords.append(a)
        allWords = list(set(allWords))
        for a in allWords:
            try:
                if(count1[a] >= 1):
                    count1[a] = count1[a]+1
            except Exception:
                count1[a] = 1


func()
func2()
tokenCount1 = len(globalallWords)
tokenCount2 = len(globalallWords2)
word1count = {}
word2count = {}

for word in globalallWords:
    try:
        if(word1count[word] >= 1):
            word1count[word] = word1count[word]+1
    except Exception:
        word1count[word] = 1
for word in globalallWords2:
    try:
        if(word2count[word] >= 1):
            word2count[word] = word2count[word]+1
    except Exception:
        word2count[word] = 1

allWords = list(set(globalallWords))
diWrdCount = len(allWords)
allWords2 = list(set(globalallWords2))
diWrdCount2 = len(allWords2)

for word in allWords:
    try:
        N11 = count1[word]
        N01 = docCount-N11
    except:
        N11 = 0
        N01 = docCount
    try:
        N10 = count2[word]
        N00 = docCount2-N10
    except:
        N10 = 0
        N00 = docCount2
    total = N00+N01+N10+N11
    if(N11 > 0):
        a = N11*math.log((total*N11)/((N11+N10)*(N01+N11)), 2)
    else:
        a = 0
    if(N01 > 0):
        b = N01*math.log((total*N01)/((N00+N01)*(N01+N11)), 2)
    else:
        b = 0
    if(N10 > 0):
        c = N10*math.log((total*N10)/((N10+N11)*(N10+N00)), 2)
    else:
        c = 0
    if(N00 > 0):
        d = N00*math.log((total*N00)/((N00+N01)*(N10+N00)), 2)
    else:
        d = 0
    if(total != 0):
        mut_Inf_c1[word] = (a+b+c+d)/total
    else:
        mut_Inf_c1[word] = 0
for word in allWords2:
    try:
        N11 = count2[word]
        N01 = docCount2-N11
    except:
        N11 = 0
        N01 = docCount2
    try:
        N10 = count1[word]
        N00 = docCount-N10
    except:
        N10 = 0
        N00 = docCount
    total = N00+N01+N10+N11
    if(N11 > 0):
        a = N11*math.log((total*N11)/((N11+N10)*(N01+N11)), 2)
    else:
        a = 0
    if(N01 > 0):
        b = N01*math.log((total*N01)/((N00+N01)*(N01+N11)), 2)
    else:
        b = 0
    if(N10 > 0):
        c = N10*math.log((total*N10)/((N10+N11)*(N10+N00)), 2)
    else:
        c = 0
    if(N00 > 0):
        d = N00*math.log((total*N00)/((N00+N01)*(N10+N00)), 2)
    else:
        d = 0
    if(total != 0):
        mut_Inf_c2[word] = (a+b+c+d)/total
    else:
        mut_Inf_c2[word] = 0
priorC1 = docCount/(docCount+docCount2)
priorC2 = docCount2/(docCount+docCount2)
sorted_d = dict(sorted(mut_Inf_c1.items(),
                       key=operator.itemgetter(1), reverse=True)[:10000])

sorted_d2 = dict(
    sorted(mut_Inf_c2.items(), key=operator.itemgetter(1), reverse=True)[:10000])


condprob1 = {}
condprob10 = {}
condprob100 = {}
condprob1000 = {}
condprob10000 = {}
condprob2 = {}
condprob20 = {}
condprob200 = {}
condprob2000 = {}
condprob20000 = {}

condprob1, condprob10, condprob100, condprob1000, condprob10000 = conditonProb(
    sorted_d, word1count, diWrdCount, tokenCount1)
condprob2, condprob20, condprob200, condprob2000, condprob20000 = conditonProb(
    sorted_d2, word2count, diWrdCount2, tokenCount2)
tp = 0
fp = 0
fn = 0
outputfile = open(out, "w")
outputfile.write("NumFeature    \t\t1\t\t10\t\t100\t\t1000\t\t10000\n")
compute("class1", condprob1, condprob2)
compute("class2", condprob1, condprob2)
p = tp/(tp+fp)
r = tp/(tp+fn)
f = 2*p*r/(p+r)
outputfile.write("MultinomialNB")
outputfile.write("\t\t" + str(round(f, 2)))
tp = 0
fp = 0
fn = 0
compute("class1", condprob10, condprob20)
compute("class2", condprob10, condprob20)
p = tp/(tp+fp)
r = tp/(tp+fn)
f = 2*p*r/(p+r)
outputfile.write("\t\t" + str(round(f, 2)))

tp = 0
fp = 0
fn = 0
compute("class1", condprob100, condprob200)
compute("class2", condprob100, condprob200)
p = tp/(tp+fp)
r = tp/(tp+fn)
f = 2*p*r/(p+r)
outputfile.write("\t\t" + str(round(f, 2)))

tp = 0
fp = 0
fn = 0
compute("class1", condprob1000, condprob2000)
compute("class2", condprob1000, condprob2000)
p = tp/(tp+fp)
r = tp/(tp+fn)
f = 2*p*r/(p+r)
outputfile.write("\t\t" + str(round(f, 2)))

tp = 0
fp = 0
fn = 0
compute("class1", condprob10000, condprob20000)
compute("class2", condprob10000, condprob20000)
p = tp/(tp+fp)
r = tp/(tp+fn)
f = 2*p*r/(p+r)
outputfile.write("\t\t" + str(round(f, 2)))
