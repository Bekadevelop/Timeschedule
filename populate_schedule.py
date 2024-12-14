from py_vapid import Vapid

def main():
    # Создаём экземпляр Vapid
    vapid = Vapid()

    # Генерируем ключи
    private_key, public_key = vapid.create_keypair()

    # Выводим ключи на экран
    print("Public Key:", public_key)
    print("Private Key:", private_key)

if __name__ == "__main__":
    main()
