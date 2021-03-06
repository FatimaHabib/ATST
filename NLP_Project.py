import pandas as pd
import numpy as np
import tensorflow as tf
import re
from nltk.corpus import stopwords

import nltk
import csv
import time
from tensorflow.python.layers.core import Dense
from tensorflow.python.ops.rnn_cell_impl import _zero_state_tensors
from pathlib import Path
print('TensorFlow Version: {}'.format(tf.__version__))
#clean the texts 

def clean_text(text, remove_stopwords = True):
    '''Remove unwanted characters, stopwords, and format the text to create fewer nulls word embeddings'''
    
    # Convert words to lower case
    text = text.lower()
    
    # Replace contractions with their longer forms 
  
    
    # Format words and remove unwanted characters
    text = re.sub(r'https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
    text = re.sub(r'\<a href', ' ', text)
    text = re.sub(r'&amp;', '', text) 
    text = re.sub(r'[_"\-;%()|+&=*%.,!?:#$@\[\]/]', ' ', text)
    text = re.sub(r'<br />', ' ', text)
    text = re.sub(r'\'', ' ', text)
    
    # Optionally, remove stop words
    if remove_stopwords:
        text = text.split()
        stops = set(stopwords.words("english"))
        text = [w for w in text if not w in stops]
        text = " ".join(text)

    return text

##########################"count words
def count_words(count_dict, text):
    '''Count the number of occurrences of each word in a set of text'''
    for sentence in text:
        for word in sentence.split():
            if word not in count_dict:
                count_dict[word] = 1
            else:
                count_dict[word] += 1
    
###########################"
articles_path = "C:/Users/33660/Downloads/NLP_Corpus/NLP_Corpus/article_txt"
abstracts_path = "C:/Users/33660/Downloads/NLP_Corpus/NLP_Corpus/abstract_txt"

destdir1 = Path(articles_path)
destdir2 = Path(abstracts_path)

articles = [p for p in destdir1.iterdir() if p.is_file()]
abstracts = [p for p in destdir2.iterdir() if p.is_file()]
articles_list = []
abstracts_list = []
for p in articles:
    with p.open('r') as file: 
        content = file.read()
        articles_list.append(content)
print("articles are saved")
for p in abstracts:
    with p.open('r') as file: 
        content = file.read()
        abstracts_list.append(content)   
print("abstracts are saved")
print(len(abstracts_list))
print(len(articles_list))

##################"          
#with open('corpus.csv', 'w') as csvfile:
 #   file_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  #  for i in range(3900):
   #     file_writer.writerow([abstracts_list[i],articles_list[i]])
##################################
clean_abstracts = []   
clean_articles = []
### Clean the abstract and articles

for i in range(3900):
     clean_abstracts.append(clean_text (abstracts_list[i], remove_stopwords=False))
     clean_articles.append(clean_text(articles_list[i]))

    
print(len(clean_abstracts))
print(len(clean_articles))  
##########################
word_counts = {}

count_words(word_counts, clean_abstracts)
count_words(word_counts, clean_articles)
            
print("Size of Vocabulary:", len(word_counts))
################################
# Load Conceptnet Numberbatch's (CN) embeddings, similar to GloVe, but probably better 
# (https://github.com/commonsense/conceptnet-numberbatch)
embeddings_index = {}
with open('numberbatch-en-19.08.txt/numberbatch-en.txt',encoding='utf-8') as f:
    for line in f:
        values = line.split(' ')
        word = values[0]
        embedding = np.asarray(values[1:], dtype='float32')
        embeddings_index[word] = embedding

print('Word embeddings:', len(embeddings_index))
###########################
# Find the number of words that are missing from CN, and are used more than our threshold.
missing_words = 0
threshold = 20

for word, count in word_counts.items():
    if count > threshold:
        if word not in embeddings_index:
            missing_words += 1
            
missing_ratio = round(missing_words/len(word_counts),4)*100
            
print("Number of words missing from CN:", missing_words)
print("Percent of words that are missing from vocabulary: {}%".format(missing_ratio))                
####################################"
# Limit the vocab that we will use to words that appear ≥ threshold or are in GloVe

#dictionary to convert words to integers
vocab_to_int = {} 

value = 0
for word, count in word_counts.items():
    if count >= threshold or word in embeddings_index:
        vocab_to_int[word] = value
        value += 1

# Special tokens that will be added to our vocab
codes = ["<UNK>","<PAD>","<EOS>","<GO>"]   

# Add codes to vocab
for code in codes:
    vocab_to_int[code] = len(vocab_to_int)

# Dictionary to convert integers to words
int_to_vocab = {}
for word, value in vocab_to_int.items():
    int_to_vocab[value] = word

usage_ratio = round(len(vocab_to_int) / len(word_counts),4)*100

print("Total number of unique words:", len(word_counts))
print("Number of words we will use:", len(vocab_to_int))
print("Percent of words we will use: {}%".format(usage_ratio))
############################
# Need to use 300 for embedding dimensions to match CN's vectors.
embedding_dim = 300
nb_words = len(vocab_to_int)

# Create matrix with default values of zero
word_embedding_matrix = np.zeros((nb_words, embedding_dim), dtype=np.float32)
for word, i in vocab_to_int.items():
    if word in embeddings_index:
        word_embedding_matrix[i] = embeddings_index[word]
    else:
        # If word not in CN, create a random embedding for it
        new_embedding = np.array(np.random.uniform(-1.0, 1.0, embedding_dim))
        embeddings_index[word] = new_embedding
        word_embedding_matrix[i] = new_embedding

# Check if value matches len(vocab_to_int)
print(len(word_embedding_matrix))
###############################"
def convert_to_ints(text, word_count, unk_count, eos=False):
    '''Convert words in text to an integer.
       If word is not in vocab_to_int, use UNK's integer.
       Total the number of words and UNKs.
       Add EOS token to the end of texts'''
    ints = []
    for sentence in text:
        sentence_ints = []
        for word in sentence.split():
            word_count += 1
            if word in vocab_to_int:
                sentence_ints.append(vocab_to_int[word])
            else:
                sentence_ints.append(vocab_to_int["<UNK>"])
                unk_count += 1
        if eos:
            sentence_ints.append(vocab_to_int["<EOS>"])
        ints.append(sentence_ints)
    return ints, word_count, unk_count
#############################"
# Apply convert_to_ints to clean_summaries and clean_texts
word_count = 0
unk_count = 0

int_abstracts, word_count, unk_count = convert_to_ints(clean_abstracts, word_count, unk_count)
int_articles, word_count, unk_count = convert_to_ints(clean_articles, word_count, unk_count, eos=True)

unk_percent = round(unk_count/word_count,4)*100

print("Total number of words in headlines:", word_count)
print("Total number of UNKs in headlines:", unk_count)
print("Percent of words that are UNK: {}%".format(unk_percent))
###########################""
def create_lengths(text):
    '''Create a data frame of the sentence lengths from a text'''
    lengths = []
    for sentence in text:
        lengths.append(len(sentence))
    return pd.DataFrame(lengths, columns=['counts'])
#############################""
lengths_abstracts = create_lengths(int_abstracts)
lengths_articles = create_lengths(int_articles)

print("Summaries:")
print(lengths_abstracts.describe())
print()
print("Texts:")
print(lengths_articles.describe())
###############################"# Inspect the length of articls

print(np.percentile(lengths_articles.counts, 90))
print(np.percentile(lengths_articles.counts, 95))
print(np.percentile(lengths_articles.counts, 99))
####################################
###############################"# Inspect the length of abstracts

print(np.percentile(lengths_abstracts.counts, 90))
print(np.percentile(lengths_abstracts.counts, 95))
print(np.percentile(lengths_abstracts.counts, 99))
####################################
def unk_counter(sentence):
    '''Counts the number of time UNK appears in a sentence.'''
    unk_count = 0
    for word in sentence:
        if word == vocab_to_int["<UNK>"]:
            unk_count += 1
    return unk_count
########################"""
# Sort the abstracts and abstracts by the length of the texts, shortest to longest
# Limit the length of abstracts and articles based on the min and max ranges.
# Remove articles that include too many UNKs

sorted_abstracts = []
sorted_articles = []
max_articles_length = 5893
max_abstracts_length = 252
min_length = 2
unk_article_limit = 1
unk_abstract_limit = 0

for length in range(min(lengths_articles.counts), max_articles_length): 
    for count, words in enumerate(int_abstracts):
        if (len(int_abstracts[count]) >= min_length and
            len(int_abstracts[count]) <= max_abstracts_length and
            len(int_articles[count]) >= min_length and
            unk_counter(int_abstracts[count]) <= unk_abstract_limit and
            unk_counter(int_articles[count]) <= unk_article_limit and
            length == len(int_articles[count])
           ):
            sorted_abstracts.append(int_abstracts[count])
            sorted_articles.append(int_articles[count])
        
# Compare lengths to ensure they match
print(len(sorted_abstracts))
print(len(sorted_articles))
###################################Building the model###############################

def model_inputs():
    '''Create palceholders for inputs to the model'''
    
    input_data = tf.placeholder(tf.int32, [None, None], name='input')
    targets = tf.placeholder(tf.int32, [None, None], name='targets')
    lr = tf.placeholder(tf.float32, name='learning_rate')
    keep_prob = tf.placeholder(tf.float32, name='keep_prob')
    abstract_length = tf.placeholder(tf.int32, (None,), name='abstract_length')
    max_abstract_length = tf.reduce_max(abstract_length, name='max_dec_len')
    article_length = tf.placeholder(tf.int32, (None,), name='article_length')

    return input_data, targets, lr, keep_prob, abstract_length, max_abstract_length, article_length

######################################
def process_encoding_input(target_data, vocab_to_int, batch_size):
    '''Remove the last word id from each batch and concat the <GO> to the begining of each batch'''
    
    ending = tf.strided_slice(target_data, [0, 0], [batch_size, -1], [1, 1])
    dec_input = tf.concat([tf.fill([batch_size, 1], vocab_to_int['<GO>']), ending], 1)

    return dec_input
#############################################"
def encoding_layer(rnn_size, sequence_length, num_layers, rnn_inputs, keep_prob):
    '''Create the encoding layer'''
    
    for layer in range(num_layers):
        with tf.variable_scope('encoder_{}'.format(layer)):
            cell_fw = tf.contrib.rnn.LSTMCell(rnn_size,
                                              initializer=tf.random_uniform_initializer(-0.1, 0.1, seed=2))
            cell_fw = tf.contrib.rnn.DropoutWrapper(cell_fw, 
                                                    input_keep_prob = keep_prob)

            cell_bw = tf.contrib.rnn.LSTMCell(rnn_size,
                                              initializer=tf.random_uniform_initializer(-0.1, 0.1, seed=2))
            cell_bw = tf.contrib.rnn.DropoutWrapper(cell_bw, 
                                                    input_keep_prob = keep_prob)

            enc_output, enc_state = tf.nn.bidirectional_dynamic_rnn(cell_fw, 
                                                                    cell_bw, 
                                                                    rnn_inputs,
                                                                    sequence_length,
                                                                    dtype=tf.float32)
    # Join outputs since we are using a bidirectional RNN
    enc_output = tf.concat(enc_output,2)
    
    return enc_output, enc_state
###################################################""decoding
def training_decoding_layer(dec_embed_input, abstract_length, dec_cell, initial_state, output_layer, 
                            vocab_size, max_abstract_length):
    '''Create the training logits'''
    
    training_helper = tf.contrib.seq2seq.TrainingHelper(inputs=dec_embed_input,
                                                        sequence_length=abstract_length,
                                                        time_major=False)

    training_decoder = tf.contrib.seq2seq.BasicDecoder(dec_cell,
                                                       training_helper,
                                                       initial_state,
                                                       output_layer) 

    training_logits, _ , _ = tf.contrib.seq2seq.dynamic_decode(training_decoder,
                                                           output_time_major=False,
                                                           impute_finished=True,
                                                           maximum_iterations=max_abstract_length)
    return training_decoder
###############################################decoding layer
def inference_decoding_layer(embeddings, start_token, end_token, dec_cell, initial_state, output_layer,
                             max_abstract_length, batch_size):
    '''Create the inference logits'''
    
    start_tokens = tf.tile(tf.constant([start_token], dtype=tf.int32), [batch_size], name='start_tokens')
    
    inference_helper = tf.contrib.seq2seq.GreedyEmbeddingHelper(embeddings,
                                                                start_tokens,
                                                                end_token)
                
    inference_decoder = tf.contrib.seq2seq.BasicDecoder(dec_cell,
                                                        inference_helper,
                                                        initial_state,
                                                        output_layer)
                
    inference_logits, _ , _ = tf.contrib.seq2seq.dynamic_decode(inference_decoder,
                                                            output_time_major=False,
                                                            impute_finished=True,
                                                            maximum_iterations=max_abstract_length)
    
    return inference_decoder
####################################################"
def decoding_layer(dec_embed_input, embeddings, enc_output, enc_state, vocab_size, article_length, abstract_length, 
                   max_abstract_length, rnn_size, vocab_to_int, keep_prob, batch_size, num_layers):
    '''Create the decoding cell and attention for the training and inference decoding layers'''
    
    for layer in range(num_layers):
        with tf.variable_scope('decoder_{}'.format(layer)):
            lstm = tf.contrib.rnn.LSTMCell(rnn_size,
                                           initializer=tf.random_uniform_initializer(-0.1, 0.1, seed=2))
            dec_cell = tf.contrib.rnn.DropoutWrapper(lstm, 
                                                     input_keep_prob = keep_prob)
    
    output_layer = Dense(vocab_size,
                         kernel_initializer = tf.truncated_normal_initializer(mean = 0.0, stddev=0.1))
    
    attn_mech = tf.contrib.seq2seq.BahdanauAttention(rnn_size,
                                                  enc_output,
                                                  article_length,
                                                  normalize=False,
                                                  name='BahdanauAttention')

    dec_cell = tf.contrib.seq2seq.AttentionWrapper(dec_cell,
                                                          attn_mech,
                                                          rnn_size)
            
    #initial_state = tf.contrib.seq2seq.AttentionWrapperState(enc_state[0],
    #                                                                _zero_state_tensors(rnn_size, 
    #                                                                                    batch_size, 
    #                                                                                    tf.float32)) 
    initial_state = dec_cell.zero_state(batch_size=batch_size,dtype=tf.float32).clone(cell_state=enc_state[0])

    with tf.variable_scope("decode"):
        training_decoder = training_decoding_layer(dec_embed_input, 
                                                  abstract_length, 
                                                  dec_cell, 
                                                  initial_state,
                                                  output_layer,
                                                  vocab_size, 
                                                  max_abstract_length)
        
        training_logits,_ ,_ = tf.contrib.seq2seq.dynamic_decode(training_decoder,
                                  output_time_major=False,
                                  impute_finished=True,
                                  maximum_iterations=max_abstract_length)
    with tf.variable_scope("decode", reuse=True):
        inference_decoder = inference_decoding_layer(embeddings,  
                                                    vocab_to_int['<GO>'], 
                                                    vocab_to_int['<EOS>'],
                                                    dec_cell, 
                                                    initial_state, 
                                                    output_layer,
                                                    max_abstract_length,
                                                    batch_size)
        
        inference_logits,_ ,_ = tf.contrib.seq2seq.dynamic_decode(inference_decoder,
                                  output_time_major=False,
                                  impute_finished=True,
                                  maximum_iterations=max_abstract_length)

    return training_logits, inference_logits
##################""""
def seq2seq_model(input_data, target_data, keep_prob, text_length, abstract_length, max_abstract_length, 
                  vocab_size, rnn_size, num_layers, vocab_to_int, batch_size):
    '''Use the previous functions to create the training and inference logits'''
    
    # Use Numberbatch's embeddings and the newly created ones as our embeddings
    embeddings = word_embedding_matrix
    
    enc_embed_input = tf.nn.embedding_lookup(embeddings, input_data)
    enc_output, enc_state = encoding_layer(rnn_size, text_length, num_layers, enc_embed_input, keep_prob)
    
    dec_input = process_encoding_input(target_data, vocab_to_int, batch_size)
    dec_embed_input = tf.nn.embedding_lookup(embeddings, dec_input)
    
    training_logits, inference_logits  = decoding_layer(dec_embed_input, 
                                                        embeddings,
                                                        enc_output,
                                                        enc_state, 
                                                        vocab_size, 
                                                        text_length, 
                                                        abstract_length, 
                                                        max_abstract_length,
                                                        rnn_size, 
                                                        vocab_to_int, 
                                                        keep_prob, 
                                                        batch_size,
                                                        num_layers)
    
    return training_logits, inference_logits
############################################"
def pad_sentence_batch(sentence_batch):
    """Pad sentences with <PAD> so that each sentence of a batch has the same length"""
    max_sentence = max([len(sentence) for sentence in sentence_batch])
    return [sentence + [vocab_to_int['<PAD>']] * (max_sentence - len(sentence)) for sentence in sentence_batch]
################################""
def get_batches(abstracts, articles, batch_size):
    """Batch abstracts, articles, and the lengths of their sentences together"""
    for batch_i in range(0, len(articles)//batch_size):
        start_i = batch_i * batch_size
        abstracts_batch = abstracts[start_i:start_i + batch_size]
        articles_batch = articles[start_i:start_i + batch_size]
        pad_abstracts_batch = np.array(pad_sentence_batch(abstracts_batch))
        pad_articles_batch = np.array(pad_sentence_batch(articles_batch))
        
        # Need the lengths for the _lengths parameters
        pad_abstracts_lengths = []
        for abstracts in pad_abstracts_batch:
            pad_abstracts_lengths.append(len(abstracts))
        
        pad_articles_lengths = []
        for article in pad_articles_batch:
            pad_articles_lengths.append(len(article))
        
        yield pad_abstracts_batch, pad_articles_batch, pad_abstracts_lengths, pad_articles_lengths
#######################################################""
# Set the Hyperparameters
epochs = 100
batch_size = 64
rnn_size = 256
num_layers = 2
learning_rate = 0.005
keep_probability = 0.75
##################################################
# Build the graph
train_graph = tf.Graph()
# Set the graph to default to ensure that it is ready for training
with train_graph.as_default():
    
    # Load the model inputs    
    input_data, targets, lr, keep_prob,abstract_length, max_abstract_length, article_length = model_inputs()

    # Create the training and inference logits
    training_logits, inference_logits = seq2seq_model(tf.reverse(input_data, [-1]),
                                                      targets, 
                                                      keep_prob,   
                                                      article_length,
                                                      abstract_length,
                                                      max_abstract_length,
                                                      len(vocab_to_int)+1,
                                                      rnn_size, 
                                                      num_layers, 
                                                      vocab_to_int,
                                                      batch_size)
    
    # Create tensors for the training logits and inference logits
    training_logits = tf.identity(training_logits.rnn_output, 'logits')
    inference_logits = tf.identity(inference_logits.sample_id, name='predictions')
    
    # Create the weights for sequence_loss
    masks = tf.sequence_mask(abstract_length, max_abstract_length, dtype=tf.float32, name='masks')

    with tf.name_scope("optimization"):
        # Loss function
        cost = tf.contrib.seq2seq.sequence_loss(
            training_logits,
            targets,
            masks)

        # Optimizer
        optimizer = tf.train.AdamOptimizer(learning_rate)

        # Gradient Clipping
        gradients = optimizer.compute_gradients(cost)
        capped_gradients = [(tf.clip_by_value(grad, -5., 5.), var) for grad, var in gradients if grad is not None]
        train_op = optimizer.apply_gradients(capped_gradients)
print("Graph is built.")



################################train the model
# Subset the data for training
start = 0
end = start + 3890
sorted_abstracts_short = sorted_abstracts[start:end]
sorted_articles_short = sorted_articles[start:end]
print("The shortest text length:", len(sorted_articles_short[0]))
print("The longest text length:",len(sorted_articles_short[-1]))
###############################""
# Train the Model
learning_rate_decay = 0.95
min_learning_rate = 0.0005
display_step = 20 # Check training loss after every 20 batches
stop_early = 0 
stop = 6 #3 # If the update loss does not decrease in 3 consecutive update checks, stop training
per_epoch = 3 # Make 3 update checks per epoch
update_check = (len(sorted_articles_short)//batch_size//per_epoch)-1

update_loss = 0 
batch_loss = 0
abstract_update_loss = [] # Record the update losses for saving improvements in the model

  
tf.reset_default_graph()
checkpoint = "best_model.ckpt"  #300k sentence
with tf.Session(graph=train_graph) as sess:
    sess.run(tf.global_variables_initializer())
    
    # If we want to continue training a previous session
    # loader = tf.train.import_meta_graph(checkpoint + '.meta')
    # loader.restore(sess, checkpoint)
    #sess.run(tf.local_variables_initializer())

    for epoch_i in range(1, epochs+1):
        update_loss = 0
        batch_loss = 0
        for batch_i, (abstracts_batch, articles_batch, abstracts_lengths, articles_lengths) in enumerate(
                get_batches(sorted_abstracts_short, sorted_articles_short, batch_size)):
            start_time = time.time()
            _, loss = sess.run(
                [train_op, cost],
                {input_data: articles_batch,
                 targets: abstracts_batch,
                 lr: learning_rate,
                 abstract_length: abstracts_lengths,
                 article_length: articles_lengths,
                 keep_prob: keep_probability})

            batch_loss += loss
            update_loss += loss
            end_time = time.time()
            batch_time = end_time - start_time

            if batch_i % display_step == 0 and batch_i > 0:
                print('Epoch {:>3}/{} Batch {:>4}/{} - Loss: {:>6.3f}, Seconds: {:>4.2f}'
                      .format(epoch_i,
                              epochs, 
                              batch_i, 
                              len(sorted_abstracts_short) // batch_size, 
                              batch_loss / display_step, 
                              batch_time*display_step))
                batch_loss = 0
                
                #saver = tf.train.Saver() 
                #saver.save(sess, checkpoint)
                
            if batch_i % update_check == 0 and batch_i > 0:
                print("Average loss for this update:", round(update_loss/update_check,3))
                abstract_update_loss.append(update_loss)
                
              
                  
                # If the update loss is at a new minimum, save the model
                if update_loss <= min(abstract_update_loss):
                    print('New Record!') 
                    stop_early = 0
                    saver = tf.train.Saver() 
                    saver.save(sess, checkpoint)

                else:
                    print("No Improvement.")
                    stop_early += 1
                    if stop_early == stop:
                        break
                update_loss = 0
            
                    
        # Reduce learning rate, but not below its minimum value
        learning_rate *= learning_rate_decay
        if learning_rate < min_learning_rate:
            learning_rate = min_learning_rate
        
        if stop_early == stop:
            print("Stopping Training.")
            break
###################################"*
# ## Making Our Own Summaries

# To see the quality of the summaries that this model can generate, you can either create your own review, or use a review from the dataset. You can set the length of the summary to a fixed value, or use a random value like I have here.


def text_to_seq(text):
    '''Prepare the text for the model'''
    
    text = clean_text(text)
    return [vocab_to_int.get(word, vocab_to_int['<UNK>']) for word in text.split()]



#use article from the dataset

#text = text_to_seq(input_sentence)
random = np.random.randint(0,len(clean_articles))
input_sentence = clean_articles[random]
article = text_to_seq(clean_articles[random])

checkpoint = "./best_model.ckpt"

loaded_graph = tf.Graph()
with tf.Session(graph=loaded_graph) as sess:
    # Load saved model
    loader = tf.train.import_meta_graph(checkpoint + '.meta')
    loader.restore(sess, checkpoint)

    input_data = loaded_graph.get_tensor_by_name('input:0')
    logits = loaded_graph.get_tensor_by_name('predictions:0')
    article_length = loaded_graph.get_tensor_by_name('article_length:0')
    abstract_length = loaded_graph.get_tensor_by_name('abstract_length:0')
    keep_prob = loaded_graph.get_tensor_by_name('keep_prob:0')
    
    #Multiply by batch_size to match the model's input parameters
    answer_logits = sess.run(logits, {input_data: [article]*batch_size, 
                                      abstract_length: [np.random.randint(5,8)], 
                                      article_length: [len(article)]*batch_size,
                                      keep_prob: 1.0})[0] 

# Remove the padding from the tweet
pad = vocab_to_int["<PAD>"] 

print('Original Text:', input_sentence)

print('\nText')
print('  Word Ids:    {}'.format([i for i in article]))
print('  Input Words: {}'.format(" ".join([int_to_vocab[i] for i in article])))

print('\nSummary')
print('  Word Ids:       {}'.format([i for i in answer_logits if i != pad]))
print('  Response Words: {}'.format(" ".join([int_to_vocab[i] for i in answer_logits if i != pad])))


