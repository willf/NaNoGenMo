#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import codecs
import random
import en
import os
from sets import Set
from wordnik import *


sys.stdin = codecs.getreader("utf8")(sys.stdin)
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

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
        words = wordApi.getRelatedWords(word, relationshipTypes="same-context")
        if words:
            return words[0].words
        else:
            return [word]
    except:
        return [word]


def random_word(words):
    return random.choice(words)

#sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

#def break_sentence(para):
#    return sent_detector.tokenize(para)

#tokenizer = nltk.TreebankWordTokenizer()


def tag_tokenize(text):
    return en.sentence.tag(text)

#def tag(tokens):
#    return nltk.pos_tag(tokens)


def is_open_class(pos):
    if pos == "NNP":
        return False
    if pos == "NNPS":
        return False
    if pos[0] == "N":
        return True
    if pos[0] == "V":
        return True
    if pos[0] == "J":
        return True
    if pos[0] == "R":
        return True
    return False


def ngrams(seq, n):
    return [seq[i:i+n] for i in range(1+len(seq)-n)]


def english(pos_tags):
    str = ""
    for (here, there) in ngrams(pos_tags, 2):
        (w1, p1) = here
        (w2, p2) = there
        if (len(p2) == 1) or (w2[0] == u"'") or (w2[0] == u"’"):
            str = str + w1
        else:
            str = str + w1 + ' '
    if len(pos_tags) > 0:
        (last_word, last_pos) = pos_tags[-1]
        str = str + last_word
    return str


def case_match(template, change):
    if template.lower() == template:
        return change.lower()
    if template.upper() == template:
        return change.upper()
    if len(template) > 0 and template[0].upper() == template[0]:
        return change.title()
    return change


keepers = Set(['part', 'is', 'was', 'were', 'am', 'are', 'be', 'has', 'have', 'had'])


def keep_as_is(word, pos):
    return word.lower() in keepers


def match_tense0(old_verb, new_verb):
    inf_new = en.verb.infinitive(new_verb)
    if inf_new == '':
        return ''
    inf_old = en.verb.infinitive(old_verb)
    if inf_old == '':
        return ''
    tense = en.verb.tense(old_verb)
    if tense == 'infinitive':
        return en.verb.infinitive(inf_new)
    if tense == 'present participle':
        return en.verb.present_participle(inf_new)
    if tense == 'past plural':
        return en.verb.past_plural(inf_new)
    if tense == '2nd singular present':
        return en.verb.present(inf_new, person=2)
    if tense == '2nd singular past':
        return en.verb.past(inf_new, person=2)
    if tense == 'past':
        return en.verb.past(inf_new)
    if tense == '3rd singular present':
        return en.verb.present(inf_new, person=3)
    if tense == 'past participle':
        return en.verb.past_participle(inf_new)
    if tense == '1st singular present':
        return en.verb.present(inf_new, person=1)
    if tense == '1st singular past':
        return en.verb.past(inf_new, person=1)
    if tense == '3rd singular past':
        return en.verb.past(inf_new, person=3)
    if tense == 'present plural':
        return en.verb.present(inf_new)


def match_tense(pos, verb):
    inf = en.verb.infinitive(verb)
    if inf == '':
        return ''
    # VB    verb, base form think
    # VBD verb, past tense    they talked
    # VBG verb, gerund or present participle  programming is fun
    # VBN verb, past participle   a sunken ship
    # VBP verb, non-3rd person singular present   I think
    # VBZ verb, 3rd person singular present   she thinks
    if pos == 'VB':
        return inf
    if pos == 'VBD':
        return en.verb.past(inf)
    if pos == 'VBG':
        return en.verb.present_participle(inf)
    if pos == 'VBP':
        return en.verb.present(inf)
    if pos == 'VBZ':
        return en.verb.present(inf, person=3)
    return inf


def match_number(pos, noun):
    s = en.noun.singular(noun)
    if pos == 'NN':
        return s
    if pos == 'NNS':
        return en.noun.plural(s)
    return noun


def match(pos, words):
    if pos[0] == 'N':
        return [match_number(pos, word) for word in words]
    if pos[0] == 'V':
        return [match_tense(pos, word) for word in words]
    return words


@memoize
def exchange(word_pos):
    (word, pos) = word_pos
    if keep_as_is(word, pos):
        return word_pos
    if is_open_class(pos):
        words = related(word)
        matches = [w for w in match(pos, words) if w is not '']
        if len(matches) == 0:
            return word_pos
        choice = random_word(matches)
        return (case_match(word, choice), pos)
    else:
        return word_pos


def main():
    for line in sys.stdin:
        trans = [exchange(word_pos) for word_pos in tag_tokenize(line.strip())]
        #trans = [word_pos for word_pos in tag(tokenize(sentence))]
        #print trans,
        print english(trans),
        sys.stdout.flush()
        print
        print

if __name__ == "__main__":
    sys.exit(main())
