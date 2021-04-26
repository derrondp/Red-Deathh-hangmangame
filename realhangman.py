import sys,random,time


LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

difficulties = {'easy': [10, (3,7)],'normal': [7, (4,10)], 'hard': [4, (5,13)], 'extreme': [2, (8,30)]}
difficulty = input('Enter difficulty: ')
if difficulty not in difficulties:
    print('Difficulty %s not found, Switching difficulty to normal ' % (difficulty))
    difficulty = 'normal'
file = 'words.txt'

def generate_word(difficulties,difficulty,file):
    words = []
    wordslength = random.randrange(difficulties[difficulty][1][0],difficulties[difficulty][1][1])
    with open(file,'r') as file:
        for line in file.read().lower().split("\n"):
            if len(line) == wordslength:
                words.append(line)
    return random.choice(words)

def display(current,guesses,wrong,max_attempts):
    tries = 'LAST TRY' if guesses == max_attempts else ''
    print('Attempts: ' + str(guesses) + "/" + str(max_attempts) + " " + tries)
    print('Current:',' '.join(current))
    print('Wrong:',''.join(wrong))

def guess_word(wordtoguess,max_attempt):
    guesses = 0
    current = ['_' for _ in wordtoguess]
    print(wordtoguess)
    badletters = []
    wordsguessed = []
    while guesses <= max_attempt:
        display(current,guesses,badletters,max_attempt)
        usr_input = input('>>> ')

        if len(usr_input) != 1:
            
            if usr_input == wordtoguess:
                print('You win! The word is %s' % (wordtoguess))
                option = input('Continue? y/n')
                if option.startswith('y') or option.startswith('Y'):
                    newword = generate_word(difficulties,difficulty,file)
                    guess_word(wordtoguess,difficulties[difficulty][0])
                else:
                    sys.exit('Game Closed.')
                    
            else:
                print('Sorry that is not the word!')
                guesses += 1
                
        elif usr_input not in LETTERS:
            print('Enter a letter found in the English Alphabets!')
            
        elif usr_input in wordsguessed:
            print('You have inputted this letter before!')
            

        else:
            wordsguessed.append(usr_input)
            
            if usr_input in wordtoguess:
                for word in range(len(wordtoguess)):
                    if wordtoguess[word] == usr_input:
                        current[word] = usr_input
                print('Nice! You guessed the right letter.')

            else:
                badletters.append(usr_input)
                print('Wrong letter! ')
                guesses += 1

            if '_' not in current:
                print('You Win! The word was %s' % (wordtoguess))
                option = str(input('(c)ontinue? y/n '))
                if option.startswith('y') or option.startswith('Y'):
                    print('-----------------------------------')
                    newword = generate_word(difficulty,difficulties,file)
                    guess_word(newword,difficulties[difficulty][0])
                else:
                    txt = 'GAME OVER'
                    for i in txt:
                        print(i,end=' ')
                        time.sleep(0.25)
                    sys.exit()
                
                
    if guesses >= max_attempt:
        print('You lose! The word was ' + wordtoguess,end='\n')
        option = str(input('(c)ontinue? y/n '))
        if option.startswith('y') or option.startswith('Y'):
            newword = generate_word(difficulty,difficulties,file)
            guess_word(newword,difficulties[difficulty][0])
        else:
            txt = 'GAME OVER'
            for i in txt:
                print(i,end=' ')
                time.sleep(0.25)
            sys.exit()
            


wordtoguess = generate_word(difficulties,difficulty,file)
guess_word(wordtoguess,difficulties[difficulty][0])
