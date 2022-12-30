from a2 import *
from console_wordle import ConsolePlayer
from random import randrange

class AutoPlayer(ConsolePlayer):
    def ask_play_again(self):
        '''
        Always returns True
        '''
        if hasattr(self, '_solved'):
            if self._last_guess in self._solved:
                raise RuntimeError(f"I already solved {self._last_guess}!"
                    " Make sure you're picking a random word.")
        else:
            self._solved = set()
        self._solved.add(self._last_guess)
                
        return True

    def ask_letters(self):
        '''
        Returns a random number of letters.
        '''
        return randrange(4,8)
    
    def check_possibility(self, word):
        '''
        Returns True if a word matches our list of posibilities.
        '''
        for index in range(self._letters):
            letter = word[index]
            possible = self._possible[index]
            if letter not in possible:
                return False
        return True
        
    
    def ask_word(self):
        '''
        Returns the word we want to guess.
        '''
        for word in self._words:
            if self.check_possibility(word):
                print(f"Guessing {word}...")
                self._last_guess = word
                return word
        raise RuntimeError("Ran out of words to guess! Something is wrong...")
    
        


def main():
    AutoPlayer().play()

if __name__=="__main__":
    main()

