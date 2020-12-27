# MIT License

# Copyright (c) 2020 Shrid Pant

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pickle
import pandas as pd
import numpy as np
import string
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk import pos_tag
from nltk.tokenize import word_tokenize

from keras.models import Model
from keras.layers import Dense, Input, Dropout, LSTM, Activation
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.initializers import glorot_uniform

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
stop_words.update(list(string.punctuation))

def get_simple_pos(tag) :
    if tag.startswith('J') :
        return wordnet.ADJ
    elif tag.startswith('V') :
        return wordnet.VERB
    elif tag.startswith('N') :
        return wordnet.NOUN
    elif tag.startswith('R') :
        return wordnet.ADV
    else:
        return wordnet.NOUN

def init():
    global word_to_index, max_len
    #word_to_index, index_to_word, word_to_vec_map = read_glove_vecs('glove.6B.50d.txt')
    filename = 'src/word_to_index.pkl'
    word_to_index =  pickle.load(open(filename, 'rb')) 
    max_len = 30
    print(len(word_to_index))
    return word_to_index, max_len

def clean_text(review) :
    global max_len 
    words = word_tokenize(review)
    output_words = []
    for word in words :
        if word.lower() not in stop_words :
            pos = pos_tag([word])
            clean_word = lemmatizer.lemmatize(word,pos = get_simple_pos(pos[0][1]))
            output_words.append(clean_word.lower())
    max_len = max(max_len, len(output_words))
    return " ".join(output_words)

def read_glove_vecs(glove_file):
    with open(glove_file, 'r', encoding="utf8") as file:
        word_to_vec_map = {}
        word_to_index = {}
        index_to_word = {}
        index = 0
        for line in file:
            line = line.strip().split()
            curr_word = line[0]
            word_to_index[curr_word] = index
            index_to_word[index] = curr_word
            word_to_vec_map[curr_word] = np.array(line[1:], dtype=np.float64)
            index += 1
    return word_to_index, index_to_word, word_to_vec_map

def sentences_to_indices(X, word_to_index, max_len):
    m = len(X)
    X_indices = np.zeros((m, max_len))
    for i in range(m):
        sentence_words = [w.lower() for w in X[i].split()]
        j = 0
        for word in sentence_words:
            if word in word_to_index:
                X_indices[i, j] = word_to_index[word]
            j += 1
    return X_indices
