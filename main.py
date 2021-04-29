import sys, pathlib, random, time, pickle

letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
letters = letters + letters.lower()

score_dict= {}
score = 0
SCORE_FILE = 'scores.txt'

difficulties = dict(baby=[25, (1, 5)], easy=[10, (3, 7)], normal=[7, (4, 10)], hard=[4, (5, 13)], extreme=[2, (8, 30)])
dictfile = pathlib.Path("dictionary.txt")


print(f"Difficulties: ", difficulties)
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
    print('Attempts:', str(guess)+'/'+str(max),last)
    print('Words Guessed:', ' '.join(currently))
    print('Wrong letters guessed:', ''.join(wrong))


def guessWord(word_to_guess, max):
    current = ['_' for _ in word_to_guess]
    badwords = []
    guesses = 0
    global score
    guessed = []
    name = str(input("What is your name? ")).lower()

    while guesses <= max:
        gui(current, badwords, guesses, max)
        usr_input = input('>>> ')

        if len(usr_input) != 1:

            if usr_input == word_to_guess:
                score += 70
                print('You guessed the word correctly! ', word_to_guess, 'Your score:', score)
                save_score(name, score)
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
                    welcome()
            else:
                print('Sorry. That is not the word!')
                score -= 10
                guesses += 1

        elif usr_input not in letters:
            print('Enter a letter found in the English alphabets!')

        elif usr_input in guessed:
            print('You have already guessed this letter before')

        else:
            guessed.append(usr_input)

            if usr_input in word_to_guess:
                print('Nice! You guessed the right letter! :)')
                score += 2
                for word in range(len(word_to_guess)):
                    if word_to_guess[word] == usr_input:
                        current[word] = usr_input
            else:
                print('Sorry, that was a wrong letter! :( ')
                badwords.append(usr_input)
                guesses += 1

            
            if '_' not in current:
                print("You win! The word was:", word_to_guess)
                print("Your total score for this game is:", score)
                save_score(name, score)
                option = str(input('continue? y/n '))
                if option.startswith('y') or option.startswith('Y'):
                    print('-----------------------------------')
                    score = 0
                    newword = generateWord(dictfile, difficulties, difficulty)
                    guessWord(newword, difficulties[difficulty][0])
                else:
                    txt = 'GAME OVER'
                    for i in txt:
                        print(i, end=' ')
                        time.sleep(0.25)
                    welcome()

    if guesses >= max:
        print('You lose! The word was:',word_to_guess, ':(', 'Your score:', score)
        save_score(name, score)
        option = str(input('continue? y/n '))
        if option.startswith('y') or option.startswith('Y'):
            print('-----------------------------------')
            score = 0
            newword = generateWord(dictfile, difficulties, difficulty)
            guessWord(newword, difficulties[difficulty][0])
        else:
            txt = 'GAME OVER\n'
            for i in txt:
                print(i, end=' ')
                time.sleep(0.25)

            welcome()

    
word = generateWord(dictfile, difficulties, difficulty)


def get_score(name):
    if pathlib.Path(SCORE_FILE).exists():
        with open(SCORE_FILE, 'rb') as file:
            score_dict = pickle.load(file)
    
            if name in score_dict:
                return score_dict[name]
            else:
                return 0
    else:
        print("SCORE FILE DOES NOT EXIST!")


def save_score(name, score):
    global score_dict

    if pathlib.Path(SCORE_FILE).exists():
        with open(SCORE_FILE, 'rb') as file:
            dic = pickle.load(file)
            
        if name in dic:
            if dic[name] < score:
                option = input("A new Personal Best! Save score? (y/n) ")
                if option.lower().startswith("y"):
                    dic[name] = score
                    with open(SCORE_FILE, 'wb') as file:
                        pickle.dump(dic, file)
                    print("Ok! Saved")
                
                else:
                    pass
        
            elif dic[name] > score:
                pass

            else:
                pass
        else:
            dic[name] = score
            with open(SCORE_FILE, 'wb') as file:
                pickle.dump(dic, file)
                print("Ok! Saved")

    
    else:
        print("Score file does not exist! Creating Now...")
        with open(SCORE_FILE, 'wb') as file:
            pickle.dump(score_dict, file)
        print("Score saved!")
    

def view_scores():
    if pathlib.Path(SCORE_FILE).exists():
        with open(SCORE_FILE, 'rb') as file:
            score_dict = pickle.load(file)
        
        for k, v in score_dict.items():
            print(f"{k}\t\t{v}")
    
    else:
        print("Score file does not exist!... You need to save a score first")


def welcome():
    print("\nWelcome to Hangman")
    while True:
        print("Do you want to Play (p) View the leaderboard (l) or quit (q): ")
        choice = input()
        if choice == 'p':
            guessWord(word, difficulties[difficulty][0])


        elif choice == 'l':
            print()
            print("Score\t\tName")
            view_scores()

        elif choice == 'q':
            import sys
            sys.exit()
        
        else:
            print("Invalid choice!")

welcome()
