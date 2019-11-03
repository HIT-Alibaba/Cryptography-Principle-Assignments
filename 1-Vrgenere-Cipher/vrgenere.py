#!/usr/bin/python3
# -*- coding: utf-8 -*-
import string
import random
from collections import Counter

import numpy as np
import matplotlib.pyplot as plt

ENCODE_TRANS_TABLE = {}
DECODE_TRANS_TABLE = {}
RANDOM_CIPHER = None
CIPHER_LENGTH = None

NORMAL_TEXT_LETTER_FREQUENCY = {
    "A": 0.08167,
    "B": 0.01492,
    "C": 0.02782,
    "D": 0.04253,
    "E": 0.12702,
    "F": 0.02228,
    "G": 0.02015,
    "H": 0.06094,
    "I": 0.06966,
    "J": 0.00153,
    "K": 0.00772,
    "L": 0.04025,
    "M": 0.02406,
    "N": 0.06749,
    "O": 0.07507,
    "P": 0.01929,
    "Q": 0.00095,
    "R": 0.05987,
    "S": 0.06327,
    "T": 0.09056,
    "U": 0.02758,
    "V": 0.00978,
    "W": 0.02360,
    "X": 0.00150,
    "Y": 0.01974,
    "Z": 0.00074,
}

for i in range(0, 26):
    origin = string.ascii_uppercase
    shift_offset = i
    shifted = origin[shift_offset:] + origin[:shift_offset]
    ENCODE_TRANS_TABLE[chr(ord("A") + i)] = string.maketrans(origin, shifted)
    DECODE_TRANS_TABLE[chr(ord("A") + i)] = string.maketrans(shifted, origin)


def preprocess(plaintext):
    table = string.maketrans("", "")
    no_punc = plaintext.translate(table, string.punctuation + string.whitespace)
    return no_punc.upper()


def generate_random_cipher(length):
    global RANDOM_CIPHER
    global CIPHER_LENGTH
    CIPHER_LENGTH = length
    r = []
    for i in range(length):
        r.append(random.choice(string.ascii_uppercase))
    RANDOM_CIPHER = "".join(r)
    return RANDOM_CIPHER


def do_encode(plaintext, cipher):
    return do_vrgenere_trans(plaintext, ENCODE_TRANS_TABLE, cipher)


def do_decode(ciphertext, cipher):
    return do_vrgenere_trans(ciphertext, DECODE_TRANS_TABLE, cipher)


def do_vrgenere_trans(text, trans_table, cipher):
    result = []
    index = 0
    cipher_len = len(cipher)
    for char in text:
        key = cipher[index % cipher_len]
        table = trans_table[key]
        result.append(char.translate(table))
        index += 1

    return "".join(result)


def encode(plaintext, cipher_len):
    cipher_to_use = generate_random_cipher(cipher_len)
    return do_encode(plaintext, cipher_to_use)


def decode(ciphertext):
    return do_decode(ciphertext, RANDOM_CIPHER)


def draw_frequency_bar_chart(text):
    freqs = get_frequency(text)
    draw_bar_chart("frequency", "Ciphertext Letter Frequency(n=16)", freqs)


def draw_bar_chart(xlabel, title, values):
    _yticks = tuple(reversed(sorted(values.keys())))
    y_pos = np.arange(len(_yticks))
    y_val = np.array([values[k] for k in _yticks])
    plt.barh(y_pos, y_val, align="center", alpha=0.4)
    plt.yticks(y_pos, _yticks)
    plt.xlabel(xlabel)
    plt.title(title)
    plt.show()


def get_frequency(text):
    c = Counter(text)
    letters = tuple(string.ascii_uppercase)
    freqs = {}
    for letter in letters:
        freqs[letter] = c[letter]
    return freqs


def get_index_of_coincidence(text):
    freqs = get_frequency(text)
    text_len = len(text)
    letters = string.ascii_uppercase
    above = 0
    for letter in letters:
        above += freqs[letter] * (freqs[letter] - 1)

    below = text_len * (text_len - 1)
    return float(above) / below


def get_index_of_coincidence_with_offset(text, offset=0):
    freqs = get_frequency(text)
    text_len = len(text)
    letters = string.ascii_uppercase
    above = 0
    for letter in letters:
        table = ENCODE_TRANS_TABLE[chr(ord("A") + offset)]
        _letter = letter.translate(table)
        above += freqs[_letter] * NORMAL_TEXT_LETTER_FREQUENCY[letter]

    below = text_len
    return float(above) / below


def split_text(text, step, pos=0):
    l = list(text)
    l2 = []
    for index, ch in enumerate(l):
        if index % step == pos:
            l2.append(ch)

    return "".join(l2)


def factors(n):
    return sorted(
        list(
            set(
                x
                for tup in (
                    [i, n // i] for i in range(1, int(n ** 0.5) + 1) if n % i == 0
                )
                for x in tup
            )
        )
    )


# Kasiski test code From http://www.marksmath.com/files/python/kasiski.py


def findsubs(text, l):
    """
    Find all repeated substrings of length 'l' in 'text'
    """
    for i in range(len(text) - l):
        target = text[i : i + l]
        found = text[i + l :].find(target)
        if found != -1:
            # if the match can be extended in either direction, don't
            # report it
            f = found + i + l
            if i > 0 and text[i - 1 : i + l] == text[f - 1 : f + l]:
                continue
            if i + l < len(text) and text[i : i + l + 1] == text[f : f + l + 1]:
                continue

            print("%-10s %3d %s" % (target, found + l, str(factors(found + l))))


def ktest(text):
    """
    Strip all characters that are not in the cipher alphabet.

    Report all substrings from longest to shortest.  The longest
    possible substring is half the ciphertext length.  Substrings
    shorter than 5 are not reported.
    """
    ctext = ""
    for c in text:
        c = c.upper()
        if c in string.ascii_uppercase:
            ctext += c

    for l in range(len(text) / 2, 2, -1):
        findsubs(ctext, l)


if __name__ == "__main__":
    f = open("plaintext-small.txt")
    plaintext = f.read()
    f.close()
    ciphertext = encode(plaintext, 7)

    f2 = open("ciphertext.txt", "w")
    print (RANDOM_CIPHER)
    f2.write(ciphertext)
    f2.close()
    # ic_dicts = {}
    # ic_dicts[0] = get_index_of_coincidence(plaintext)

    # draw_bar_chart("IC", "Index of Coincidence with different n", ic_dicts)
    draw_frequency_bar_chart(ciphertext)

    ic = get_index_of_coincidence(ciphertext)
    print (ic)
"""
    kp = 0.067
    kr = 0.0385
    ko = ic
    guess_cipher_length = (kp - kr) / (ko - kr)
    print(ic)
    print(guess_cipher_length)
    ktest(ciphertext)
"""
