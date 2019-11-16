import spacy
import json
import string
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from pathlib import Path
stopwords = list(STOP_WORDS)

nlp = spacy.load('en_core_web_sm')
destdir = Path('/home/fatima/Bureau/CorpusTXT5')
files = [p for p in destdir.iterdir() if p.is_file()]
#list of the word frequency of each file 
listDic =[]
for p in files:
  with p.open() as f : 

    contents = f.read() #read the text files
    docx = nlp(contents)
    mytokens = [token.text for token in docx] #tokenize the files 
    word_frequencies = {} #dictoinery the words is the keys thier frequencies are the values are their frequencies
    for word in docx:
       if word.text not in stopwords and word.text not in string.punctuation and word.text!= "\n":
             if word.text not in word_frequencies.keys():
                     word_frequencies[word.text] = 1
             else:
                     word_frequencies[word.text] += 1


    listDic.append(word_frequencies)
#save the list of word frequency in a jason file 
#with open("Dic5_list.json", "w") as f:
    #json.dump(listDic, f)
