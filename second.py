import os
import argparse
from nltk.tokenize import word_tokenize
import nltk
import math
from nltk.corpus import stopwords
from sklearn.datasets import load_iris
from nltk.tokenize import RegexpTokenizer
stop = stopwords.words("english")
tokenizer = RegexpTokenizer(r'\w+')


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

vocab = []
globalTdCount = {}
docCount1 = 0


def func2(className):

    global vocab, globalTdCount, docCount1, check1, check2, tp, fp, fn
    for filename in os.listdir(datapath+"/"+className+"/test"):
        allWords = []
        tokens = []
        docCount1 = docCount1+1
        with open(os.path.join(datapath+"/"+className+"/test", filename), "r") as file:
            document = file.read()
        tokens = tokenizer.tokenize(document.strip().lower())
        for t in tokens:
            t = str(t).strip()
            if t not in stop:
                vocab.append(t)
                allWords.append(t)

        allWords = list(set(allWords))
        for t in allWords:
            try:
                globalTdCount[t] = globalTdCount[t]+1
            except:
                globalTdCount[t] = 1

    vocab = list(set(vocab))
    wrdIndex = {}
    i = 0
    for wrd in vocab:
        wrdIndex[wrd] = i
        i = i+1

    for filename in os.listdir(datapath+"/"+className+"/test"):
        vector = [0]*i
        wrdCount = {}
        tokens = []
        with open(os.path.join(datapath+"/"+className+"/test", filename), "r") as file:
            document = file.read()
        tokens = tokenizer.tokenize(document.strip().lower())
        for t in tokens:
            t = str(t).strip()
            if t not in stop:
                try:
                    wrdCount[t] = wrdCount+1
                except:
                    wrdCount[t] = 1
        for key in wrdCount:
            idft = math.log((docCount1/globalTdCount[key]), 2)
            vector[wrdIndex[key]] = idft*wrdCount[key]
            vector[wrdIndex[key]] = vector[wrdIndex[key]]/docCount1
        pr = [0]*i
        sum1 = 0
        sum2 = 0
        for jp in range(i):
            try:
                pr[jp] = check1[jp]-vector[jp]
            except Exception:
                pr[jp] = vector[jp]
            sum1 = sum1+(pr[jp]*pr[jp])
        sum1 = math.sqrt(sum1)
        pr = [0]*i

        for jp in range(i):
            try:
                pr[jp] = check2[jp]-vector[jp]
            except Exception:
                pr[jp] = vector[jp]
            sum2 = sum2+(pr[jp]*pr[jp])
        sum2 = math.sqrt(sum2)

        if(className == "class1"):
            if(sum1 < sum2):
                tp = tp+1
            else:
                fp = fp+1
                fn = fn+1
        else:
            if(sum1 > sum2):
                tp = tp+1
            else:
                fp = fp+1
                fn = fn+1


def func(className):
    global vocab, globalTdCount, docCount1
    for filename in os.listdir(datapath+"/"+className+"/train"):
        allWords = []
        tokens = []
        docCount1 = docCount1+1
        with open(os.path.join(datapath+"/"+className+"/train", filename), "r") as file:
            document = file.read()
        tokens = tokenizer.tokenize(document.strip().lower())
        for t in tokens:
            t = str(t).strip()
            if t not in stop:
                vocab.append(t)
                allWords.append(t)

        allWords = list(set(allWords))
        for t in allWords:
            try:
                globalTdCount[t] = globalTdCount[t]+1
            except:
                globalTdCount[t] = 1

    vocab = list(set(vocab))
    wrdIndex = {}
    i = 0
    for wrd in vocab:
        wrdIndex[wrd] = i
        i = i+1
    vector = [0]*i
    for filename in os.listdir(datapath+"/"+className+"/train"):
        wrdCount = {}
        tokens = []
        with open(os.path.join(datapath+"/"+className+"/train", filename), "r") as file:
            document = file.read()
        tokens = tokenizer.tokenize(document.strip().lower())
        for t in tokens:
            t = str(t).strip()
            if t not in stop:
                try:
                    wrdCount[t] = wrdCount+1
                except:
                    wrdCount[t] = 1
        for key in wrdCount:
            idft = math.log((docCount1/globalTdCount[key]), 2)
            vector[wrdIndex[key]] = vector[wrdIndex[key]] + \
                idft*wrdCount[key]
            vector[wrdIndex[key]] = vector[wrdIndex[key]]/docCount1
    return vector


check1 = func("class1")
vocab = []
globalTdCount = {}
docCount1 = 0
check2 = func("class2")
vocab = []
globalTdCount = {}
docCount1 = 0
tp = 0
fp = 0
fn = 0
func2("class1")
vocab = []
globalTdCount = {}
docCount1 = 0
func2("class2")
p = tp/(tp+fp)
r = tp/(tp+fn)
f = 2*p*r/(p+r)
with open(out, "w") as put:
    put.write(str(f))
