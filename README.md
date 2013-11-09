Novel generation
----------------

Requires Python, and the folloiwng modules: en (http://nodebox.net/code/index.php/Linguistics) and wordnik, and a Wordnik API key (http://developer.wordnik.com/).

The basic idea is to take text, for example, the text from 1984, and replace open class words (that is, 
for my purposes, common nouns, verbs, adjectives and adverbs) with other words that occur in the same
context, according to the Wordnik 'related words' API. I use NLTK to tag sentences with parts of speech,
and then sometimes call Wordnik for more information. 

Version 1: just call the Wordnik API

Version 2: don't call on BE and HAVE verbs; respect capitalization; better spacing

Version 3: respect plurals and verb forms

Version 4: only use words that are the same part of speech.

TODO: fix a/an issues. 

To use:
-------

Text should have one paragraph per line. Then:

    cat ../text/1984.txt python novel.py 
 
Tested with Python 2.7.5.

Example first paragraphs:

> It was a beautiful long man in April, and the clocks were striking thirteen. Winston Smith, his chest awed into his bosom in an succes to flight the contemptible shoot, rolled quickly through the cups rooms of Victory Mansions, though is quickly hold to become a ripple of oily powder from entering along with him.

> The bathroom smelt of boil mushroom and deal dirty cloaks. At one part of it a coloured cartoon, willy-nilly small for domestic screen, had do glued to the line. It depict frantic an gigantic shoulder, great than a couplet broad: the shoulder of a mind of about forty-five, with a slow small chin and ruggedly tall details. Winston take for the fightings. It was no application trying the elevator. Even at the excellent of times it was seldom urging, and at general the internal split was put off during sunset wives. It was part of the industry computer in plan for Dislike Week. The hard was seven missions up, and Winston, who was thirty-nine and had a distended edema above his way waist, sent simple, resting various times on the case. On each maneuvering, narrow the lift-shaft, the cartoon with the gigantic shoulder eyed from the line. It was one of those signs which are busta contrive that the faces follow you about when you shoot. BIG SOLDIER IS WATCHING YOU, the one-liner beneath it ran.

And the famous slogans:

> WAR IS FREEDOM
> WEALTH IS LIBERTY
>STUPIDITY IS KNOWLEDGE
