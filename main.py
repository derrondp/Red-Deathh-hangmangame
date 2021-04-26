# This is a sample Python script.
import sys, pathlib, random, time
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
letters = letters + letters.lower()

difficulties = dict(baby=[25, (1, 5)], easy=[10, (3, 7)], normal=[7, (4, 10)], hard=[4, (5, 13)], extreme=[2, (8, 30)])
dictfile = pathlib.Path("dictionary.txt")

print(difficulties)
print('\n')
difficulty = input('Enter difficulty: ')
if difficulty not in difficulties:
    print('Difficulty not found...Switching to default')
    difficulty = 'normal'

def generateWord(dictFile, difficulties, difficulty):
    words = []
    wordlength = random.randint(difficulties[difficulty][1][0], difficulties[difficulty][1][1])
    if dictFile.exists():
        with open(dictFile, 'r') as dfile:
            for word in dfile.read().split('\n'):
                if len(word) == wordlength:
                    words.append(word)
    else:
        print('Such file does not exist!')

    return random.choice(words)

def gui(currently, wrong, guess, max):
    print('_' * 40)
    if guess == max:
        last = 'LAST TRY'
    else:
        last = ''
    print('Attempt:', str(guess)+'/'+str(max),last)
    print('Current:', ' '.join(currently))
    print('Wrong:', ''.join(wrong))

word = generateWord(dictfile, difficulties, difficulty)

def guessWord(word_to_guess, max):
    current = ['_' for _ in word_to_guess]
    badwords = []
    guesses = 0
    guessed = []

    while guesses <= max:
        gui(current, badwords, guesses, max)
        usr_input = input('>>> ')

        if len(usr_input) != 1:

            if usr_input == word_to_guess:
                print('You guessed the word correctly! ', word_to_guess)
                option = str(input('continue? y/n '))
                if option.startswith('y') or option.startswith('Y'):
                    print('-----------------------------------')
                    newword = generateWord(dictfile, difficulties, difficulty)
                    guessWord(newword, difficulties[difficulty][0])
                else:
                    txt = 'GAME OVER'
                    for i in txt:
                        print(i, end=' ')
                        time.sleep(0.25)
                    sys.exit()
            else:
                print('Sorry. That is not the word!')
                guesses += 1

        elif usr_input not in letters:
            print('Enter a letter found in the English alphabets!')

        elif usr_input in guessed:
            print('You have already guessed this letter before')

        else:
            guessed.append(usr_input)

            if usr_input in word_to_guess:
                print('Nice! You guessed the right letter! :)')
                for word in range(len(word_to_guess)):
                    if word_to_guess[word] == usr_input:
                        current[word] = usr_input
            else:
                print('Sorry, that was a wrong letter! :( ')
                badwords.append(usr_input)
                guesses += 1

            if '_' not in current:
                print('You win! The word to guess was', word_to_guess)
                option = str(input('continue? y/n '))
                if option.startswith('y') or option.startswith('Y'):
                    print('-----------------------------------')
                    newword = generateWord(dictfile, difficulties, difficulty)
                    guessWord(newword, difficulties[difficulty][0])
                else:
                    txt = 'GAME OVER'
                    for i in txt:
                        print(i, end=' ')
                        time.sleep(0.25)
                    sys.exit()

    if guesses >= max:
        print('You lose! The word was:',word_to_guess, ':(')

        option = str(input('continue? y/n '))
        if option.startswith('y') or option.startswith('Y'):
            print('-----------------------------------')
            newword = generateWord(dictfile, difficulties, difficulty)
            guessWord(newword, difficulties[difficulty][0])
        else:
            txt = 'GAME OVER'
            for i in txt:
                print(i, end=' ')
                time.sleep(0.25)
            sys.exit()

guessWord(word, difficulties[difficulty][0])