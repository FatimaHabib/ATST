# -*- coding: utf-8 -*-
"""
@author: Kroxyl
"""

### Libraries 

import nltk
import os
#import re

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
#from nltk.stem import WordNetLemmatizer 
from nltk.tokenize import word_tokenize, sent_tokenize


### FUNCTIONS 

# Create a dictionary table with frequency (without stopwords) // return the frequency of each word in a dictionary
def dictionary_table(article):
    
    # Removing stop words
    stop_words = set(stopwords.words("english"))
    
    # Tokenization
    wordtokenize = nltk.word_tokenize(articleRaw)
    
    # Take words to their root form
    # 'Caring' -> Stemming -> 'Car'
    stem = PorterStemmer()
    
    ## Init the Wordnet Lemmatizer -> word to their meaningful base form
    ## 'Caring' -> Lemmatization -> 'Care' 
    #lemmatizer = WordNetLemmatizer()

    # creation of the dictionnary for the word frequency
    frequency_table = dict()
    for word in wordtokenize :
        word = stem.stem(word)
        if word in stop_words :
            continue
        if word in frequency_table :
            frequency_table[word] += 1
        else :
            frequency_table[word] = 1

    return frequency_table

# Calculate the score of each sentence weight (without stopwords) // return a dict of sentence + weight
def sentence_scores_weigth(sentences, frequency_table) -> dict:
    
    #algorithm for scoring a sentence by its words
    sentence_weight = dict()
    
    for sentence in sentences:
        #wordcount_insentence = (len(word_tokenize(sentence)))
        wordcount_insentence_without_stopwords = 0
        for word_weight in frequency_table:
            if word_weight in sentence.lower():
                wordcount_insentence_without_stopwords += 1
                if sentence[:7] in sentence_weight:
                    sentence_weight[sentence[:7]] += frequency_table[word_weight]
                else:
                    sentence_weight[sentence[:7]] = frequency_table[word_weight]
    
        sentence_weight[sentence[:7]] = sentence_weight[sentence[:7]] / wordcount_insentence_without_stopwords
    
    #sentence_scores = sorted(sentence_weight.items(), reverse=True, key= lambda x: x[1])
    #print(sentence_scores)    
    
    return sentence_weight


# Calculate the average score between all the sentences in the article
def average_score_sentences(sentence_scores) -> int:
    
    #calculating the average score for all the sentences
    sum_values = 0 
    for sent in sentence_scores :
        sum_values += sentence_scores[sent]
        
    #getting sentence average value from source text
    average_score = (sum_values / len(sentence_scores))

    return average_score

# Summarization of the article taking sentences with a higher value of sentence weight than the average score
def article_summarization(sentences, sentence_scores, average_score):
    sentence_count = 0 
    summary = "" 
    
    for sentence in sentences :
        if sentence[:7] in sentence_scores and sentence_scores[sentence[:7]] >= (average_score):
            summary += " " + sentence
            sentence_count += 1
    
    return summary



### MAIN FUNCTION 

# Run all the functions to produce the summary of all article in parameter // return a string 
def run_article_summarization(article):
    
    #creating a dictionary for the word frequency table
    frequency_table = (dictionary_table(articleRaw))
    
    #tokenizing the sentences
    sentences = sent_tokenize(article)

    #algorithm for scoring a sentence by the weight of all the words in the sentence 
    sentence_scores = sentence_scores_weigth(sentences, frequency_table)

    #calculation of the average score 
    average_score = average_score_sentences(sentence_scores)
    
    #producing the summary, (we multiply the average_score * 1.5 to get only 20% of the original text maximum)
    article_summary = article_summarization(sentences, sentence_scores, 1.6 * average_score)
    
    #if the average_score multiply is too high, do it normally (will work for all the small text/article)
    if article_summary == "" : 
            article_summary = article_summarization(sentences, sentence_scores, average_score)
    
    return article_summary

### MAIN PYTHON 
 
i = 1
print("START =========================")

#for loop to open every ARTICLE.TXT file in the CHOOSEN PATH, get the summary and create a new txt file to store the SUMMARY.TXT
for x in os.listdir("article/"):
    #open and read the file "x" in our path
    f = open("article/article_"+str(i)+".txt", "r", encoding="utf-8", errors="ignore")
    articleRaw = f.read() 
    f.close()
    
    #run the main function to get the summary from the article.txt
    summary_article = run_article_summarization(articleRaw)
    
    ##print("Here is the summary of the : " + str(x) + "\n")
    ##print(summary_article)
    
    #open (create) a file that will contain the summary we extract from the article.txt
    f = open("summary/summary_"+str(i)+".txt","w", encoding="utf-8")
    f.write(summary_article)
    f.close()
    
    i = i + 1

print("END ===========================")




