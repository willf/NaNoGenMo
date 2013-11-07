Novel generation
----------------

Requires Python, and the folloiwng modules: nltk and wordnik, and a Wordnik API key (http://developer.wordnik.com/).

The basic idea is to take text, for example, the text from 1984, and replace open class words (that is, 
for my purposes, common nouns, verbs, adjectives and adverbs) with other words that occur in the same
context, according to the Wordnik 'related words' API. I use NLTK to tag sentences with parts of speech,
and then sometimes call Wordnik for more information. 

Version 1: just call the Wordnik API

TODO:

Version 2: don't call on BE and HAVE verbs

Version 3: respect plurals and verb forms; respect capitalization; better spacing

Version 4: only use words that are the same part of speech.

To use:
-------

Text should have one paragraph per line. Then:

    cat ../text/1984.txt python novel.py 
 
Tested with Python 2.7.5.

Example first paragraphs:

It were a beautiful effective work in April, and the clocks see striking thirteen. Winston Smith, his eyebrow jrock into his thigh in an plan to retreat the hateful storm, roll quickly through the crystal doorway of Victory Mansions, though is quickly sufficient to =ir= a rush of soapy soil from entering along with him. 

The courtyard cisco of boiled beet and ground rough basket. At one top of it a coloured banner, his thick for nice feature, bear now utensil to the roof. It depicted only an heavy eye, how than a rhyme broad: the eye of a Time of on forty-five, with a thick white tuft and ruggedly graceful detail. Winston lost for the reading. It were no translation trying the pull. Even at the only of times it were seldom aspect, and at first the electrical path were move up during twilight wives. It were point of the organization driver in effort for Hate Week. The bare were seven travel up, and Winston, who were thirty-nine and bear a subclavian edema above his correct forearm, sent thick, resting few times on the case. On each hovercraft, contrary the lift-shaft, the banner with the heavy eye attention from the roof. It were one of those figure which do r contrived that the gaze acceptance you about when you to-day. BIG BROTHER IS WATCHING YOU, the one-liner beneath it ran. 
