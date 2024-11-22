import random
pass
def guess_the_number():
    print("Добро пожаловать в игру 'Угадай число'!")
    print("Компьютер загадал число от 1 до 100. Попробуй угадать его!")
    
    number_to_guess = random.randint(1, 100)
    attempts = 0
    
    while True:
        try:
            user_guess = int(input("Введите ваше предположение: "))
            attempts += 1
            
            if user_guess < number_to_guess:
                print("Загаданное число больше.")
            elif user_guess > number_to_guess:
                print("Загаданное число меньше.")
            else:
                print(f"Поздравляю! Вы угадали число за {attempts} попыток!")
                break
        except ValueError:
            print("Пожалуйста, вводите только числа.")

if __name__ == "__main__":
    guess_the_number()
