import guess_user
import guess_computer

if __name__ == '__main__':
    print("Welcome to Guessing Game!")
    while True:        
        game_mode = input("Do you want to guess my numer [1] or do you want me to guess your number [2]? ")
        if game_mode == "1":
            guess_computer.start() 
            break
        elif game_mode == "2":
            guess_user.start()
            break
        else:
            print("Please insert your option: 1 / 2 only")

