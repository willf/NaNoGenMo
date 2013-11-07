#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import codecs
import locale
import cStringIO
import random
import nltk
import os

sys.stdin = codecs.getreader("utf8")(sys.stdin)
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

from wordnik import *
apiUrl = 'http://api.wordnik.com/v4'
apiKey = os.environ['WORDNIK_API_KEY']
client = swagger.ApiClient(apiKey, apiUrl)
wordApi = WordApi.WordApi(client)

translate = {}

class memoize(dict):
    def __init__(self, func):
        self.func = func

    def __call__(self, *args):
        return self[args]

    def __missing__(self, key):
        result = self[key] = self.func(*key)
        return result


def related(word):
    try:
        words = wordApi.getRelatedWords(word, relationshipTypes ="same-context")
        if words:
            return words[0].words
        else:
            return [word]
    except:
        return [word]

def random_word(words):
    return random.choice(words)
    
sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

def break_sentence(para):
    return sent_detector.tokenize(para)

tokenizer = nltk.TreebankWordTokenizer()

def tokenize(sentence):
    return tokenizer.tokenize(sentence)
    
def tag(tokens):
    return nltk.pos_tag(tokens)

def is_open_class(pos):
    if pos == "NNP": return False
    if pos == "NNPS": return False
    if pos[0] == "N": return True
    if pos[0] == "V": return True
    if pos[0] == "J": return True
    if pos[0] == "R": return True
    return False

def ngrams(seq, n):
    return [seq[i:i+n] for i in range(1+len(seq)-n)]
        
def english(pos_tags):
    str = ""
    for (here, there) in ngrams(pos_tags,2):
        (w1, p1) = here
        (w2, p2) = there
        if len(p2) == 1:
            str = str + w1
        else:
            str = str + w1 + ' '
    if len(pos_tags) > 0:
        (last_word, last_pos) = pos_tags[-1]
        str = str + last_word
    return str

@memoize    
def exchange(word_pos):
    (word, pos) = word_pos
    if is_open_class(pos):
        words = related(word)
        choice = random_word(words)
        return (choice, pos)
    else:
        return word_pos
    


for line in sys.stdin:
    for sentence in break_sentence(line):
        trans = [exchange(word_pos) for word_pos in tag(tokenize(sentence))]
        print english(trans)," ",
        sys.stdout.flush()
    print
    print

    