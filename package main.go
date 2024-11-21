package main

import(
	"fmt"
	"math/rand"
	"time"
)

func main() {
	// Иницилизация генератора случайных чисел
	rand.Seed(time.Now().UnixNano())
	secretNumber := rand.Intn(200)+ 1 // Случайное число от 1 до 200

fmt.Println("Добро пожаловать в игру 'Угадай число'!")
fmt.Println("Я загадал число от 1 до 200. Попробуй угадать.")

var guess int 
for{
	fmt.Print("Введите ваше число: ")
	_, err := fmt.Scan(&guess)
    if err != nil{
		fmt.Println("Пожалусьта, введите целое число!")
		continue
	}

   	if guess < secretNumer{
		fmt.Println("Слишком мало! попробуй еще.")
    } else if guess > secretNumber {
		fmt.Println("Слишком много! поробуй еще.")
	} else {
		fmt.Printf("Поздравляю! вы угадали число: %d\n", secretNumber)
	    break
	}
  }
}

go run guess.go
