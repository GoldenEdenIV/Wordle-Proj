import random

from nltk.corpus import words
from collections import Counter
word_list = [x.lower() for x in words.words()]

#Chọn chữ cái lúc ban đầu
def choose_word():
    ans =""
    #Đảm bảo từ đã nhập có đủ số kí tự đã chọn và phải nằm trong List trên
    while len(ans) != length or ans not in word_list:
        ans = input("Choose the word: ")
        ans.lower()
    return ans

def choose_word_ran():
    return random.choice(word_list)

#Hàm trả về kết quả đoán
def after_guess(word, guess):
    result = []
    for i in range(len(word)):
        if guess[i] == word[i]:
            result.append("🟩")  #Chữ cái đúng ("🟩")
        elif guess[i] in word:
            result.append("🟨")  #Đúng chữ cái nhưng sai vị trí ("🟨")
        else:
            result.append("🟥")  #Chữ cái sai ("🟥")
    return "".join(result)

# Lọc từ dựa trên kết quả trước
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

# Hàm tìm từ gần nhất dựa trên độ xuất hiện của chữ cái
def best_guess(possible_words):    
    # Đếm số lượng từ xuất hiện
    letter_counts = Counter()
    for word in possible_words:
        for letter in word:
            letter_counts[letter] += 1

    # Tính điểm cho mỗi từ dựa trên tần suất chữ cái
    scored_words = []
    for word in possible_words:
        score = 0
        unique_letters = set(word)
        for letter in unique_letters:
            score += letter_counts[letter]
        scored_words.append((word, score))
    
    # Sắp xếp các từ theo điểm số từ cao đến thấp
    scored_words.sort(key=lambda x: x[1], reverse=True)
    
    top_count = max(1, int(len(scored_words) * 0.1))
    top_words = [word for word, score in scored_words[:top_count]]
    
    return random.choice(top_words)


# Hàm main
def main():
    word = choose_word()
    possible_words = word_list.copy()
    
    guess = ""
    i = 1
    while guess != word:
        guess = best_guess(possible_words)
        print(f"Attempt {i}: {guess}")
        result = after_guess(word, guess)
        print(f"Result: {result}")
        if guess == word and i <=5:
            print("AI found the word!")
            break
        elif guess == word and i > 5:
            print("AI failed.")
            break

        possible_words = filter(possible_words, guess, result)
        i+=1

def main2():
    word = choose_word_ran()
    print("A word has been chosen.")
    guess = ""
    i = 1
    while guess != word:
        attempt = True
        while attempt == True:
            guess = input(f"Attempt {i}: ")
            if len(guess) != length:
                attempt = True
            else:
                attempt = False
        result = after_guess(word, guess)
        print(f"Result: {result}")
        if guess == word and i <=5:
            print("You found the word!")
            break
        elif guess != word and i >= 5:
            print(f"You failed. The answer is {word}")
            break
        else:
            if i >= 5:
                print(f"You failed. The answer is {word}")
                break
        i+=1
        attempt = True

def main3():
    word = choose_word_ran()
    print("A word has been chosen.")
    guess = ""
    i = 1
    possible_words = word_list.copy()
    while guess != word:
        attempt = True
        while attempt == True:
            print(f"Your attempt {i}: ", end="")
            guess = input()
            if len(guess) != length:
                attempt = True
            else:
                attempt = False
        result = after_guess(word, guess)
        print(f"Your result: {result}")

        ai_guess = best_guess(possible_words)
        print(f"- AI attempt {i}: {ai_guess}")
        ai_result = after_guess(word, ai_guess)
        print(f"- AI result: {ai_result}")
        if guess == word and ai_guess != word:
            print("You found the word before AI!")
            break
        elif guess != word and ai_guess == word:
            print("You lose.")
            break
        elif guess != word and ai_guess != word and i > 5:
            print("Hard word, huh?.")
            break
        i+=1
        attempt = True
        possible_words = filter(possible_words, ai_guess, ai_result)

print("1. AI guess")
print("2. You guess")
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