guess = "hello"
secret = "apple"



#check for green first
def guess_with_context(word, secret):
    guess_arr = list(word)
    secret_arr = list(secret)

    for i in range(5):
        letter = guess_arr[i]
        if letter == secret_arr[i]:
            guess_arr[i] = f"{letter}: green"
            secret_arr[i] = "*"
    print(secret_arr)
    print(guess_arr)
    #check for yellow 
    for i in range(5):
        letter = guess_arr[i]
        print(letter)

        if "green" in letter:
            continue
        
        if letter in secret_arr:
            guess_arr[i] = f"{letter}: yellow"
            secret_arr.remove(letter)
    
    for i in range(5):
        letter = guess_arr[i]
        if len(letter) == 1:
            guess_arr[i] = f"{letter}: no match"
    print(guess_arr)
    print(secret_arr)


print(guess_with_context(guess, secret))