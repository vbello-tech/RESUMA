# a simple guess the number game that checks user input against a certain list of numbers.

import random

while True:
    range_of_numbers = range(0, 51, 2)
    list_of_numbers = []
    for number in range_of_numbers:
        list_of_numbers.append(number)
    # print(list_of_numbers)

    while True:
        user_input = int(input("Guess a number\nInput that number below\n:"))
        # print (user_input)

        q = (len(range_of_numbers)) - 1
        pop = range_of_numbers[q]

        max_num = pop + 1
        # print(q, pop)
        while user_input not in list_of_numbers:
            print ('choose another number\nThe numbers are in multiple of 2 and the maximum nuber u can choose is', + max_num)
            user_input = int(input("Guess a number\nInput that number below\n:"))
            if user_input in list_of_numbers:
                break

        computer_input = random.randint(0, pop)
        # print(computer_input)

        def check(computer_input, user_input):
            if computer_input == user_input:
                print("YOU WON.")
            else:
                print("YOU LOSE.")


        check(computer_input, user_input)

        print("WOULD YOU LIKE TO PLAY AGAIN?")

        answer = input("TYPE 'Y' to play again  OR 'N' to stop playing.\n:").upper()
        #print(answer)

        if answer == "Y":
            check(computer_input, user_input)
        else:
            break

    break