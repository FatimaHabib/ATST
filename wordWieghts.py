import spacy
import json
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from pathlib import Path
stopwords = list(STOP_WORDS)
listWieghts=[]

#with open("Dic5_list.json", "r") as f:
           #B = json.load(f)
           #for Dic in B:
               #word_wieghts= {}
               #maximum_frequency = max(Dic.values()) #calculate the maximum word frequency 
               #for word in Dic.keys():  
                       #word_wieghts[word]= (Dic[word]/maximum_frequency) # the word wieght 
               #listWieghts.append(word_wieghts)
               #print(maximum_frequency )
               #print("-------------------------------------------------------")

#save the list of word wieghts in a jason file 
#with open("wordWieghts.json", "w") as f:
     #json.dump(listWieghts, f)
with open("wordWieghts.json", "r") as f:
     B = json.load(f)
     for Dic in B:
        for key in Dic:
            print (key)
        print("-------------------------------------------------------")
