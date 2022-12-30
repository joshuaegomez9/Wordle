from a2 import WordleWords
from a2 import Guess
from a2 import Wordle
from a2 import TooLongError
from a2 import TooShortError
from a2 import NotLettersError

class ConsolePlayer:
    '''
    This class interfaces with the WorldeWords, Guess, and World classes to
    allow the game to be played on the console (as long as those classes
    work correctly!)
    '''
    def ask_play_again(self):
        '''
        Returns True if the player would like to play again, otherwise
        it returns False.
        '''
        while True:
            entry = input("Would you like to play again?").upper()
            if entry[0] == 'N':
                return False
            elif entry[0] == 'Y':
                return True
            else:
                print("Please enter y or n!")

    def ask_letters(self):
        '''
        Returns a positive integer number of letters.
        '''
        while True:
            entry = input("How many letters would you like to play?")
            try:
                return int(entry)
            except ValueError:
                print("Please enter a positive integer!")
    
    def ask_word(self):
        '''
        Returns the word that the player guessed.
        '''
        while True:
            entry = input("Guess a word: ").upper()
            try:
                self._words.check_word(entry)
            except TooShortError:
                print("Enter a longer word!")
            except TooLongError:
                print("Enter a shorter word!")
            except NotLettersError:
                print("Enter a word with only letters A-Z!")
            if entry in self._words:
                return entry
            else:
                print("That's not a word! Enter a real word!")

    def new_game(self):
        '''
        Initializes a new game.
        '''
        self._letters = self.ask_letters()
        self._words = WordleWords(self._letters)
        self._words.load_file("words.txt")
        self._wordle = Wordle(self._words)
        self._known_wrong = set()
        self._known_misplaced = list()
        self._known_correct = ["_"] * self._letters
        self._possible = []
        for index in range(self._letters):
            self._possible.append(set("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
        self._won = False
    
    def print_possible(self):
        max_len = 0
        for possible in self._possible:
            if len(possible) > max_len:
                max_len = len(possible)
        if max_len <= 27:
            lists = []
            for index in range(self._letters):
                lists.append(sorted(self._possible[index]))
            for index in range(max_len):
                string = ""
                for a_list in lists:
                    if index < len(a_list):
                        string = string + a_list[index]
                    else:
                        string = string + " "
                print(f"Possible:  {string}")
    
    def print_guess(self, guess):
        print(f"Guess:     {guess.guess()}")
        print(f"Correct:   {guess.correct()}")
        if len(guess.misplaced()) > 0:
            print(f"Misplaced: {guess.misplaced()}")
        if len(guess.wrong()) > 0:
            print(f"Wrong:     {guess.wrong()}")
        self.print_possible()
        known_wrong = "".join(sorted(self._known_wrong))
        known_misplaced = "".join(sorted(self._known_misplaced))
        known_correct = "".join(self._known_correct)
        print(f"Known wrong letters:     {known_wrong}")
        print(f"Known misplaced letters: {known_misplaced}")
        print(f"Known correct letters:   {known_correct}")
    
    def set_known_correct(self, index, letter):
        if self._known_correct[index] == "_" and letter in self._known_misplaced:
            self._known_misplaced.remove(letter)
        self._known_correct[index] = letter
    
    def wrong_not_misplaced_impossible(self, possible):
        if len(possible) > 1:
            for letter in list(possible):
                if (letter in self._known_wrong
                    and not letter in self._known_misplaced):
                    possible.remove(letter)
    
    def compute_possible(self, guessed):
        # remove possibilities based on blanks in the answer
        for index in range(self._letters):
            guessed_correct = guessed.correct()[index]
            guessed_letter = guessed.guess()[index]
            if guessed_correct == "_":
                self._possible[index].discard(guessed_letter)
            else:
                self._possible[index] = set(guessed_correct)

        # remove letters we know are wrong (and not misplaced)
        for possible in self._possible:
            self.wrong_not_misplaced_impossible(possible)

        # determine if we've figured out any part of the solution
        # by process of elimination...
        for index in range(self._letters):
            possible = self._possible[index]
            known_correct = self._known_correct[index]
            if len(possible) == 1 and known_correct == "_":
                letter = self._possible[index].copy().pop()
                self.set_known_correct(index, letter)
    
    def remember(self, guessed):
        self._known_wrong |= set(guessed.wrong())
        for index in range(self._letters):
            guessed_correct = guessed.correct()[index]
            if guessed_correct != "_":
                self.set_known_correct(index, guessed_correct)

        # add all misplaced letters (being careful not to duplicate)
        new_misplaced = []
        for letter in guessed.misplaced():
            if letter in self._known_misplaced:
                self._known_misplaced.remove(letter)
            new_misplaced.append(letter)
        self._known_misplaced.extend(new_misplaced)
        self.compute_possible(guessed)
    
    def guess_once(self):
        guessed = self._wordle.guess(self.ask_word())
        self.remember(guessed)
        if guessed.is_win():
            self._won = True
        else:
            self.print_guess(guessed)
    
    def game_over(self):
        return self._won
    
    def play(self):
        while self._play_again:
            self.new_game()
            while not self._won:
                self.guess_once()
            print(f"Yay! You won in {self._wordle.guesses()} guesses!")
            self._play_again = self.ask_play_again()
    
    def __init__(self):
        self._play_again = True

def main():
    ConsolePlayer().play()

if __name__=="__main__":
    main()
