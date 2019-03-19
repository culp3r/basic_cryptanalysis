'''
Mario Morales
2 Dec. 2018
Description: Given a piece of text encoded with a simple monoalphabetic
    substitution cipher, use basic cryptanalytic techniques to recover the
    original plain text.

Solution: After failing at solving through frequency analysis, and nearly
surrendering myself to writing a paper, I did some research and learned
of string isomorphism. The implementation works essentially by "abstracting"
each word and describing it though the positioning of its letters. I.E:
    - 'Egg' and 'Add' are isomorphic.
    - The way we "abstract" the words is by generating a "unique string"
      for one of the words that contains no repeat letters. So egg -> eg,
      now we can describe the word via the indexes. So we have an array
      of indexes [0, 1, 1]. This says for the word egg, the first letter
      in the word is the 0th letter in this word's unique string. The
      second and third letters in the word are the from 1th index of
      this word's unique string. Now if we have another word that is
      isomorphic to 'egg' like 'add' it will generate the same array
      of [0, 1, 1].
    - Given that we're deciphering a monoalphabetic substitution cipher,
      finding a word that is isomorphic to a ciphertext word means that
      it could decrypt to that word. By the nature of how mono ciphers work,
      there is a substitution alphabet and each letter maps to one another.
Input: lhpohes gvjhe ztytwojmmtel lgsfcgver segpsltjyl vftstelc djfl rml catrroel jscvjqjyfo mjlesl lcjmmfqe egvj gsfyhtyq sjfgver csfaotyq lfxtyq gjywplesl lxljm dxcel mpyctyq ztytwojmmtelel mfcgv spres mjm psgvty bfml ofle mjlc dtc tygfycfctjy dfsyl zpygvel csfao yealqsjpml atyl lgsjql qyfsotelc fseyf ojllel gjzmselltyq wpyhtelc zpltgl weygel afyher rstnesl aefleo rtyhes mvflel yphe rstnes qojder dtwwer lojml mfcgvel reocfl djzder djpygtyq gstmmoeafsel reg cpdel qspyqe mflctel csflvtyq vfcl avfghtyq vftsdfool mzer rsjye wjjol psol mplvtyq catrroe mvfqe lgseey leqzeycer wjseqsjpyrer lmjtoes msjwtoel docl djpyger cjpstlcl goefy gojddesl mjrl qjddoe gjy gpdtyql lyftotyq rjayojfr swgl vjle atrqec gjzmfgces frfl qotcgver gspzd zftodjzdl lyfsh
'''
import re
#Make list of words from dictionary and another of ciphertext
d = open('dictionary.lst', 'r')
d_words = d.read().lower().split()
cipher_input = input()
cipher_words = cipher_input.strip().split(' ')
template = ['.' for i in range(26)]
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.lower()
the_map = {}

for word in d_words:
    sub = the_map.get(len(word), {})
    the_map[len(word)] = sub
    #Remove repeat letters
    no_repeats = ''
    for char in word:
        if char not in no_repeats:
            no_repeats += char
    key = [0 for i in range(len(word))]
    # Get the index of a letter in from the temp word (without repeats version)
    # and map to the position of that letter (where it appears) in the word.
    for index, char in enumerate(word):
        key[index] = no_repeats.index(char)
    key = ' '.join([str(n) for n in key])
    array = sub.get(key, [])
    sub[key] = array
    array.append(word)

cipher_len = len(cipher_words)
while True:
    for word in cipher_words:
        uniq = ''
        for char in word:
            if char not in uniq:
                uniq += char
        key = [0 for i in range(len(word))]
        pattern = ''
        for index, char in enumerate(word):
            key[index] = uniq.index(char)
            try:
                temp_idx = template.index(char)
                pattern += alphabet[temp_idx]
            except:
                pattern += '.'
        key = ' '.join([str(n) for n in key])
        matches = the_map[len(word)][key]
        copy = []
        for match in matches:
            if re.fullmatch(pattern, match):
                copy.append(match)
        matches = copy
        if len(matches) == 1:
            cipher_words.remove(word)
            match = matches[0]
            for i in range(len(word)):
                template[alphabet.index(match[i])] = word[i]
    current = len(cipher_words)
    if cipher_len == current:
        break
    cipher_len = current

template = ''.join(template)
out = [' ' for i in range(len(cipher_input))]
for index, char in enumerate(cipher_input):
    if char is not ' ':
        out[index] = alphabet[template.index(char)]
print(''.join(out))
