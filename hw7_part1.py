# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 19:58:26 2022

@author: Philip Paterson
HW07 Part 1
This program autocorrects words based off of four methods:
    1. DROP
    2. INSERT
    3. SWAP
    4. REPLACE
"""

# Defining the functions

def add_valid_word(characters, the_dict, valids):
    '''
    This functions takes a list of characters, joins them together, checks
    if it's a valid English word, and adds it to the given set of valid
    words.

    Parameters
    ----------
    characters : LIST
        A list of characters.
    the_dict : DICT
        The dictionary of all the valid words in the desired language
        (in this case, English).
    valids : SET
        A set of the valid words that fit the criteria.

    Returns
    -------
    None.

    '''
    new_word = ''.join(characters)
    if new_word in the_dict:
        valids.add(new_word)


def gen_valid_words(word, the_dict, keyboard_dict, valid_words, word_type):
    '''
    This function generates and adds to the given set a valid word from the 
    given incorrect word using the four methods: DROP, INSERT, SWAP, and 
    REPLACE.

    Parameters
    ----------
    word : STR
        The given word.
    the_dict : DICT
        The dictionary of all the valid words in the desired language
        (in this case, English)..
    keyboard_dict : DICT
        A dictionary of a letter as a key and for the value, 
        the adjacent keyboard letters as a list.
    valid_words : SET
        A set of the valid words that fit the criteria.
    word_type : STR
        The method specified to be used to generate a valid word.

    Returns
    -------
    None.

    '''
    word_type = word_type.strip().upper()
    word_chars = list(word)
    word_chars_len = len(word_chars)
    
    i = 0
    while i < word_chars_len:
        # Finding all possible words from DROPping a letter
        if word_type == "DROP":
            possible_chars = word_chars.copy()
            possible_chars.pop(i)
            add_valid_word(possible_chars, the_dict, valid_words)
        # Find all possible words from INSERTing a letter
        elif word_type == "INSERT":
            for letter in keyboard_dict:
                possible_chars = word_chars.copy()
                possible_chars.insert(i, letter)
                add_valid_word(possible_chars, the_dict, valid_words)
                if i == word_chars_len - 1:
                    possible_chars = word_chars.copy()
                    possible_chars.append(letter)
                    add_valid_word(possible_chars, the_dict, valid_words)
        # Find all possible words from SWAPping consecutive letters
        elif word_type == "SWAP" and i < word_chars_len - 1:
            possible_chars = word_chars.copy()
            char_i = possible_chars[i]
            possible_chars[i] = possible_chars[i + 1]
            possible_chars[i + 1] = char_i
            add_valid_word(possible_chars, the_dict, valid_words)
        # Find all possible words from REPLACE-ing letters with possible letters
        elif word_type == "REPLACE":
            possible_chars = word_chars.copy()
            for letter in keyboard_dict[possible_chars[i]]:
                possible_chars = word_chars.copy()
                possible_chars[i] = letter
                add_valid_word(possible_chars, the_dict, valid_words)
        i += 1


def correct_word(word, the_dict, keyboard_dict):
    '''
    This function corrects the given word and prints the first three
    associated valid words, or less, if there are valids at all.

    Parameters
    ----------
    word : STR
        The given word.
    the_dict : DICT
        The dictionary of all the valid words in the desired language
        (in this case, English)..
    keyboard_dict : DICT
        A dictionary of a letter as a key and for the value, 
        the adjacent keyboard letters as a list.

    Returns
    -------
    None.

    '''
    # Tests if the word can be FOUND in the dictionary
    if word in the_dict:
        status = "FOUND"
        print("{0:>15} -> {1}".format(word, status))
    else:
        valid_words = set()
        
        # Finding all possible words from different methods
        gen_valid_words(word, the_dict, keyboard_dict, valid_words, "DROP")
        gen_valid_words(word, the_dict, keyboard_dict, valid_words, "INSERT")
        gen_valid_words(word, the_dict, keyboard_dict, valid_words, "SWAP")
        gen_valid_words(word, the_dict, keyboard_dict, valid_words, "REPLACE")
        
        # Determining if valid words were found
        valid_num = len(valid_words)
        if valid_num == 0:
            status = "NOT FOUND"
            print("{0:>15} -> {1}".format(word, status))
        else:
            status = "FOUND"
            # Printing the first three, or less, associated valid words
            valids_sorted = []
            for valid in valid_words:
                valids_sorted.append((the_dict[valid], valid))
            valids_sorted.sort(reverse= True)
            print("{0:>15} -> {1}{2:3d}:".format(word, status, valid_num), end=' ')
            for valid in valids_sorted[:3]:
                print(' ' + valid[1], end='')
            print()
        
    
# Main body of the code
if __name__ == "__main__":
    # Getting the inputs
    fname_dict = input("Dictionary file => ").strip()
    print(fname_dict)
    fname_input = input("Input file => ").strip()
    print(fname_input)
    fname_keyboard = input("Keyboard file => ").strip()
    print(fname_keyboard)
    
    # Creating the dictionary of English words & their frequencies
    f_eng = open(fname_dict)
    english_dict = dict()
    for line in f_eng:
        data = line.strip().strip('\n').split(',')
        english_dict[data[0]] = data[1]
    f_eng.close()
    
    # Creating the dictionary of letter values adjacent to a letter key
    f_key = open(fname_keyboard)
    keyboard_dict = dict()
    for line in f_key:
        data = line.strip().strip('\n').split()
        neighbors = []
        i = 1
        while i < len(data):
            neighbors.append(data[i])
            i += 1
        keyboard_dict[data[0]] = neighbors
    f_key.close()
 
    # Autocorrecting each word in the input file
    f_in = open(fname_input)
    for line in f_in:
        single_word = line.strip().strip('\n').lower()
        correct_word(single_word, english_dict, keyboard_dict)