# NLP_Kreyol_Segmentation
Introduction: Haitian Creole (or “Kreyòl”) is the native language of the great majority of the 11+ million people living in Haiti, and one of the two official languages in that country, along with French. It is a Creole language, meaning that it arose out of contact between populations that spoke different languages; in this case, French and a variety of west African languages, especially FonLinks to an external site. and IgboLinks to an external site..  

When we spell words in English, we decompose them into “letters": s-p-e-l-l-i-n-g, for example.  In linguistics in general, these letters are called “graphemes” — the indivisible units in a writing system.  The official standard orthography of Kreyòl uses the following graphemes:

a, an, b, ch, d, e, è, en, f, g, h, i, j, k, l, m, n, ng, o, ò, on, ou, oun, p, r, s, t, ui, v, w, y, z
I've highlighted in bold the graphemes that are made up of multiple letters; we call the ones with two letters "digraphs" and the one example with three letters a "trigraph".  This means that a word like achete is “spelled” as a-ch-e-t-e.  That example is easy enough, but what about a word like desounen? Is this spelled as d-e-s-ou-n-e-n? Or d-e-s-oun-e-n?  Or d-e-s-ou-n-en? Or d-e-s-oun-en?
The task for this competition takes Kreyòl words as input, and outputs the correct segmentation into graphemes.  For example, the correct answer for the input desounen should actually be d-e-s-ou-n-en.  

You can think about this as a sequence tagging problem, where you tag each character of the input with a B if it's the start of a grapheme, and an I if it's a continuation of a digraph or trigraph.  So the correct tagging for the example above should be:

d e s o u n e n

B B B B I B B I
