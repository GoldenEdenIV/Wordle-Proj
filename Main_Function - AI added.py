import random
import numpy as np
from nltk.corpus import words
from collections import Counter
from sklearn.ensemble import RandomForestRegressor 

LETTER_FREQUENCY = {
    'e': 12.02, 't': 9.10, 'a': 8.12, 'o': 7.68, 'i': 7.31, 'n': 6.95, 's': 6.28, 'r': 6.02, 
    'h': 5.92, 'd': 4.32, 'l': 3.98, 'u': 2.88, 'c': 2.71, 'm': 2.61, 'f': 2.30, 'y': 2.11, 
    'w': 2.09, 'g': 2.03, 'p': 1.82, 'b': 1.49, 'v': 1.11, 'k': 0.69, 'x': 0.17, 'q': 0.11, 
    'j': 0.10, 'z': 0.07
}

FIRST_LETTER_FREQUENCY = {
    's': 12.55, 'c': 8.40, 'p': 8.02, 'a': 7.86, 't': 7.00, 'b': 6.10, 'f': 5.74, 'm': 5.68,
    'd': 5.52, 'r': 5.50, 'h': 4.98, 'e': 3.91, 'i': 3.70, 'l': 3.49, 'n': 3.01, 'o': 2.85,
    'g': 2.47, 'w': 2.14, 'u': 1.28, 'v': 1.05, 'j': 0.81, 'k': 0.81, 'q': 0.49, 'y': 0.30,
    'z': 0.23, 'x': 0.10
}

LAST_LETTER_FREQUENCY = {
    'e': 21.22, 's': 12.75, 't': 8.61, 'd': 6.73, 'n': 6.27, 'r': 6.03, 'y': 5.75, 'a': 4.97,
    'l': 4.92, 'o': 3.84, 'h': 3.41, 'g': 2.99, 'm': 2.25, 'c': 1.79, 'k': 1.63, 'p': 1.49,
    'f': 1.31, 'i': 1.29, 'b': 0.86, 'u': 0.84, 'w': 0.65, 'z': 0.24, 'x': 0.07, 'v': 0.06,
    'q': 0.02, 'j': 0.01
}

BIGRAM_FREQUENCY = {
    'th': 3.56, 'he': 3.07, 'in': 2.43, 'er': 2.05, 'an': 1.99, 're': 1.85, 'on': 1.76, 'at': 1.49,
    'en': 1.45, 'nd': 1.35, 'ti': 1.34, 'es': 1.34, 'or': 1.28, 'te': 1.20, 'of': 1.17, 'ed': 1.17,
    'is': 1.13, 'it': 1.12, 'al': 1.09, 'ar': 1.07, 'st': 1.05, 'to': 1.04, 'nt': 1.04, 'ng': 0.95
}

word_list = [x.lower() for x in words.words()]

def train_wordle_model(word_list):
    X = []
    y = []

    for word in word_list:
        if len(word) != length:
            continue
            
        features = []

        letter_score = sum(LETTER_FREQUENCY.get(letter, 0) for letter in word)

        features.append(letter_score)
        
        features.append(FIRST_LETTER_FREQUENCY.get(word[0], 0))
        
        features.append(LAST_LETTER_FREQUENCY.get(word[-1], 0))
        
        bigram_score = 0
        for i in range(len(word)-1):
            bigram = word[i:i+2]
            bigram_score += BIGRAM_FREQUENCY.get(bigram, 0)
        features.append(bigram_score)
        
        unique_ratio = len(set(word)) / len(word)
        features.append(unique_ratio)

        X.append(features)
        
        word_score = letter_score + (unique_ratio * 10)
        y.append(word_score)
    
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    return model

def extract_features(word):
    features = []
    
 
    letter_score = sum(LETTER_FREQUENCY.get(letter, 0) for letter in word)
    features.append(letter_score)
    

    features.append(FIRST_LETTER_FREQUENCY.get(word[0], 0))
    

    features.append(LAST_LETTER_FREQUENCY.get(word[-1], 0))
    

    bigram_score = 0
    for i in range(len(word)-1):
        bigram = word[i:i+2]
        bigram_score += BIGRAM_FREQUENCY.get(bigram, 0)
    features.append(bigram_score)

    unique_ratio = len(set(word)) / len(word)
    features.append(unique_ratio)
    
    return features

def choose_word():
    ans = ""
    while len(ans) != length or ans not in word_list:
        ans = input("Choose the word: ")
        ans = ans.lower()
    return ans


def choose_word_ran():
    return random.choice([w for w in word_list if len(w) == length])

def after_guess(word, guess):
    result = []
    for i in range(len(word)):
        if guess[i] == word[i]:
            result.append("🟩") 
        elif guess[i] in word:
            result.append("🟨")  
        else:
            result.append("🟥")  
    return "".join(result)

def filter(possible_words, guess, result):
    new_possible_words = []
    for word in possible_words:
        match = True
        for i in range(len(word)):
            if result[i] == "🟩" and guess[i] != word[i]:
                match = False
                break
            elif result[i] == "🟨" and (guess[i] == word[i] or guess[i] not in word):
                match = False
                break
            elif result[i] == "🟥" and guess[i] in word:
                match = False
                break
        if match:
            new_possible_words.append(word)
    return new_possible_words

def best_guess(possible_words, model, round_num):
    if len(possible_words) == 1:
        return possible_words[0]

    if round_num == 1:
        best_start = ['a', 'am', 'are', 'game', 'arose', 'amount', 'outside', 'mountain', 'education', 'precaution']
        for starter in best_start:
            if starter in possible_words and len(starter) == length:
                return starter
    
    word_scores = []

    for word in possible_words:
        features = extract_features(word)

        ml_score = model.predict([features])[0]
        
        unique_letters = len(set(word))
        info_value = unique_letters / length

        if round_num <= 3:
            final_score = ml_score * 0.3 + info_value * 0.7
        else:
            final_score = ml_score * 0.7 + info_value * 0.3
            
        word_scores.append((word, final_score))
    
    word_scores.sort(key=lambda x: x[1], reverse=True)

    top_count = max(1, int(len(word_scores) * 0.1))
    
    top_words = [word for word, score in word_scores[:top_count]]
    
    return random.choice(top_words)


def main():
    word = choose_word()
    possible_words = [w for w in word_list if len(w) == length]
    model = train_wordle_model(word_list)
    guess = ""
    i = 1
    while guess != word:
        guess = best_guess(possible_words, model, i)
        print(f"Attempt {i}: {guess}")
        result = after_guess(word, guess)
        print(f"Result: {result}")
        if guess == word and i <= 6:
            print("AI found the word!")
            break
        elif guess == word and i > 6:
            print("AI failed.")
            break

        possible_words = filter(possible_words, guess, result)
        i += 1


def main2():
    word = choose_word_ran()
    print("A word has been chosen.")
    possible_words = [w for w in word_list if len(w) == length]
    model = train_wordle_model(word_list)
    ai_help = ""
    guess = ""
    i = 1
    while guess != word:
        ai_help = best_guess(possible_words, model, i)
        print(f"AI suggestion: {ai_help}")
        attempt = True
        while attempt == True:
            guess = input(f"Attempt {i}: ")
            if len(guess) != length or guess not in word_list:
                attempt = True
            else:
                attempt = False
        result = after_guess(word, guess)
        print(f"Result: {result}")
        if guess == word and i <= 6:
            print("You found the word!")
            break
        elif guess != word and i >= 6:
            print(f"You failed. The answer is {word}")
            break
        else:
            if i >= 6:
                print(f"You failed. The answer is {word}")
                break
        possible_words = filter(possible_words, guess, result)
        i += 1
        attempt = True

def main3():
    word = choose_word_ran()
    print("A word has been chosen.")
    guess = ""
    i = 1
    possible_words = [w for w in word_list if len(w) == length]
    model = train_wordle_model(word_list)
    
    while guess != word:
        attempt = True
        while attempt == True:
            print(f"Your attempt {i}: ", end="")
            guess = input()
            if len(guess) != length or guess not in word_list:
                attempt = True
            else:
                attempt = False
        result = after_guess(word, guess)
        print(f"Your result: {result}")

        ai_guess = best_guess(possible_words, model, i)
        print(f"- AI attempt {i}: {ai_guess}")
        ai_result = after_guess(word, ai_guess)
        print(f"- AI result: {ai_result}")
        print("===============")
        if guess == word and ai_guess != word:
            print("You found the word before AI!")
            break
        elif guess != word and ai_guess == word:
            print("You lose.")
            break
        elif guess != word and ai_guess != word and i >= 6:
            print("Hard word, huh?.")
            print(f"The answer was {word}")
            break
        i += 1
        attempt = True
        possible_words = filter(possible_words, ai_guess, ai_result)

print("1. AI guess")
print("2. You guess with assistant")
print("3. You vs AI")
mode = input("Choose the mode: ")
if mode == "1":
    length = int(input("Choose the number of letters: "))
    word_list = [x.lower() for x in words.words() if len(x)==length]
    main()
elif mode == "2":
    length = int(input("Choose the number of letters: "))
    word_list = [x.lower() for x in words.words() if len(x)==length]
    main2()
else:
    length = int(input("Choose the number of letters: "))
    word_list = [x.lower() for x in words.words() if len(x)==length]
    main3()