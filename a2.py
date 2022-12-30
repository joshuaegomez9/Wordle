"""
This code hold the functions used in console_wordle.py
for the simulation of automatic solving of the game Wordle
Author: Joshua Gomez - University of Alberta, Fall 2022
"""


from random import choice
from collections.abc import MutableSet

class TooLongError(Exception):
    pass
class TooShortError(Exception):
    pass
class NotLettersError(Exception):
    pass

class WordleWords(MutableSet):

    def __init__(self, letters):
        ''' __init__(self, letters) - takes int and sets it as word length'''
        self._words = set()
        self._letters = letters
        
    def __contains__(self, word):
        """
        __contains__(self, word) - returns True if the word is in the list, returns False otherwise
        by using the in operator on self._words
        """
        return word in self._words

    def __iter__(self):
        """
        __iter__(self) - returns an iterator over all the words using the iter built-in function
        """
        return iter(self._words)
    
    def __len__(self):
        """
        __len__(self) - return the number of words in the dictionary
        using the len built-in function
        """
        return len(self._words)

    def add(self, word):
        """
        add(self, word) - add the word to the dictionary by using the add method of Python’s set data structure
        Raises an error if the word is too short, or too long, or doesn’t contain only capital letters A-Z
        """
        if len(word) != self._letters or word.isupper() == False or word.isalpha() == False:
            raise ValueError("Invalid word")
        else:
            self._words.add(word)
    
    def discard(self, word):
        """
        discard(self, word) - remove a word from the dictionary 
        by using the discard method of Python’s set data structure
        """
        self._words.discard(word)

    def load_file(self, filename):
        """
        load_file(self, filename) - add words to the set using the content of the file specified by filename
        skip all words that don’t have exactly letters number of letters when reading the file
        convert all the words to capital letters
        """
        with open(filename) as f:
            for line in f: 
                word = line.strip() 
                if len(word) == self._letters:
                    self._words.add(line.strip())
                    
                
    def check_word(self, word):
        """
        check_word(self, word) - takes a word and makes sure that it consists only of 
        the capital letters A-Z (no accents) and is the correct length
        """
        if len(word) > self._letters:
            raise TooLongError("word is too long")
        elif len(word) < self._letters:
            raise TooShortError("word is too short")
        elif not word.isalpha() or not word.isupper():
            raise NotLettersError("word does not consist of only A-Z")

    def letters(self):
        """
        letters(self) - returns the number of letters in every word
        """
        return self._letters
    
    def copy(self):
        """
        copy(self) - returns a second WorldeWords instance which contains the same words
        """
        return set(self)

class Guess:
    def __init__(self, guess, answer):
        """ 
        __init__(self, guess, answer) - take two parameters, the guess the player made and the correct answer.
        """
        self._guess = guess
        self._answer = answer
    def guess(self):
        """
        guess(self) - returns the guess that the player made.
        """
        return self._guess
    def correct(self):
        """
        correct(self) - return a string that is the same length of the answer.
        consist of underscores, except for where the player guessed correctly.
        """
        check = ""
        # i - letter index in word
        for i in range(len(self._answer)):
            if self._guess[i] == self._answer[i]:
                check += self._guess[i]
            else:
                check += "_"
        
        return check

    def misplaced(self):
        """
        misplaced(self) - return a sorted string that contains every letter which the player guessed 
        that is also in the answer, but not at the same position
        """
        check = ""

        # checking for duplicates in answer
        answerLetterCounts = {}
        for letter in self._answer:
            if letter not in answerLetterCounts:
                answerLetterCounts[letter] = 1
            else:
                answerLetterCounts[letter] += 1

        # checking for duplicates
        guessLetterCounts = {}        
        for letter in self._guess:
            if letter not in guessLetterCounts:
                guessLetterCounts[letter] = 1
            else:
                guessLetterCounts[letter] += 1
        

        # i - letter index in word
        for i in range(len(self._answer)):
            if self._guess[i] == self._answer[i]:
                # to enable duplicates
                pass
            elif self._guess[i] in self._answer:
                if guessLetterCounts[self._guess[i]] > answerLetterCounts[self._guess[i]]:
                    #take out a letter count so there are no duplicates
                    guessLetterCounts[self._guess[i]] -= 1
                else:
                    check += self._guess[i]
        
        return check

    def wrong(self):
        """
        misplaced(self) - return a sorted string that contains every letter which the player guessed 
        that is also in the answer, but not at the same position
        """
        check = ""
        miss = self.misplaced()
        for i in range(len(self._answer)):
            if self._guess[i] != self._answer[i] and self._guess[i] not in miss:
                check += self._guess[i]
        
        return ''.join(sorted(check))

    def is_win(self):
        """
        is_win(self) - return True if the guess is the same as the answer.
        """
        if self._guess == self._answer:
            return True
        else:
            return False

class Wordle:
    def __init__(self, words):
        """
        __init__(self, words)- take one parameter, which is a WorldeWords instance object 
        chooses a random word for the game.
        """
        self._word = choice(list(words))
        self._count = 0

    def guesses(self):
        """
        guesses(self) - should return the number of guesses the player has made so far.
        """
        return self._count
    def guess(self, guessed):
        """
        guess(self, guessed) - take a string guessed and return a Guess instance object 
        that represents the results of the guess.
        """
        self._count += 1
        return Guess(guessed, self._word)