import nltk
nltk.download('words')
from nltk.corpus import words
import random
from sklearn.ensemble import RandomForestRegressor
import os
import joblib  # Add this import for model saving/loading

new_path = r"C:\Users\ADMIN\Desktop\AI\Final\Wordle-Proj"
os.chdir(new_path)


word_list = [x.lower() for x in words.words()]

LETTER_FREQUENCY = {
    'e': 12.49, 't': 9.28, 'a': 8.04, 'o': 7.64, 'i': 7.57, 'n': 7.23, 's': 6.51, 'r': 6.28, 
    'h': 5.05, 'd': 3.82, 'l': 4.07, 'u': 2.73, 'c': 3.34, 'm': 2.51, 'f': 2.40, 'y': 1.66, 
    'w': 1.68, 'g': 1.87, 'p': 2.14, 'b': 1.48, 'v': 1.05, 'k': 0.54, 'x': 0.23, 'q': 0.12, 
    'j': 0.16, 'z': 0.09
}

FIRST_LETTER_FREQUENCY = {
    't': 17.0, 'a': 11.0, 'o': 7.5, 'i': 5.5, 's': 10.0, 'w': 6.8, 'c': 3.0, 'b': 2.5,
    'p': 3.5, 'f': 3.0, 'm': 2.0, 'r': 5.5, 'd': 2.5, 'h': 6.0, 'e': 3.0, 'l': 2.0,
    'n': 4.0, 'g': 3.5, 'u': 1.5, 'y': 1.5, 'v': 1.0, 'j': 0.5, 'k': 0.8, 'q': 0.3,
    'z': 0.2, 'x': 0.3
}

BIGRAM_FREQUENCY = {
    'th': 3.56, 'he': 3.02, 'in': 2.43, 'er': 2.05, 'an': 1.99, 're': 1.85, 'on': 1.76, 'at': 1.49,
    'en': 1.45, 'nd': 1.35, 'ti': 1.34, 'es': 1.34, 'or': 1.28, 'te': 1.20, 'of': 1.17, 'ed': 1.17,
    'is': 1.13, 'it': 1.12, 'al': 1.09, 'ar': 1.07, 'st': 1.05, 'to': 1.04, 'nt': 1.04, 'ng': 0.95,
    'se': 0.93, 'ha': 0.93, 'as': 0.87, 'ou': 0.87, 'io': 0.83, 've': 0.83, 'le': 0.79, 'me': 0.79,
    'de': 0.76, 'hi': 0.76, 'ri': 0.73, 'ro': 0.73, 'ic': 0.70, 'ne': 0.69, 'ea': 0.69, 'ra': 0.69,
    'ce': 0.68, 'li': 0.62, 'ch': 0.60, 'll': 0.58, 'be': 0.58, 'ma': 0.57, 'si': 0.55, 'om': 0.55,
    'ur': 0.54
}


def train_wordle_model(word_list, length):
    model_filename = f"wordle_model_{length}.joblib"
    if os.path.exists(model_filename):
        choice = input("Model already exists. 1. Load existing. 2. Train new. ")
        if choice == "1":
            print(f"Loading existing model for {length}-letter words...")
            return joblib.load(model_filename)
    
    print(f"Training new model for {length}-letter words...")
    X = []
    y = []

    for word in word_list:
        if len(word) != length:
            continue
            
        features = []

        letter_score = sum(LETTER_FREQUENCY.get(letter, 0) for letter in word)

        features.append(letter_score)
        
        features.append(FIRST_LETTER_FREQUENCY.get(word[0], 0))
        
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
    
    joblib.dump(model, model_filename)
    print(f"Model saved as {model_filename}")
    
    return model

def extract_features(word):
    features = []
    
    letter_score = sum(LETTER_FREQUENCY.get(letter, 0) for letter in word)
    features.append(letter_score)
    
    features.append(FIRST_LETTER_FREQUENCY.get(word[0], 0))
    
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
                letter_count_in_word = word.count(guess[i])
                letter_count_in_guess = guess.count(guess[i])
                green_or_yellow_count = 0
                
                for j in range(len(word)):
                    if guess[j] == guess[i] and (result[j] == "🟩" or result[j] == "🟨"):
                        green_or_yellow_count += 1
                
                if green_or_yellow_count < letter_count_in_word:
                    match = False
                    break
        if match:
            new_possible_words.append(word)
    return new_possible_words

def best_guess(possible_words, model, round_num):
    if len(possible_words) == 1:
        return possible_words[0]

    word_scores = []

    for word in possible_words:
        features = extract_features(word)

        ml_score = model.predict([features])[0]
        
        unique_letters = len(set(word))
        info_value = unique_letters / length

        if round_num <= 3:
            if round_num == 1:
                final_score = info_value
            else:
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
    model = train_wordle_model(word_list, length)
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
    model = train_wordle_model(word_list, length)
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
    model = train_wordle_model(word_list, length)
    
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
elif mode == "3":
    length = int(input("Choose the number of letters: "))
    word_list = [x.lower() for x in words.words() if len(x)==length]
    main3()
else:
    length = int(input("Choose the number of letters: "))
    word_list = [x.lower() for x in words.words() if len(x)==length]
    main()