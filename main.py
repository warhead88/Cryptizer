import sys
import pyperclip
import crypto_logic as crypto
import ui_utils as ui

def handle_generate_key():
    key = crypto.generate_key()
    crypto.save_key(key)
    ui.print_header("НОВЫЙ КЛЮЧ СОЗДАН")
    print(f"Ваш ключ: {ui.YELLOW}{key.decode()}{ui.RESET}")
    ui.print_success(f"Ключ сохранен в {crypto.KEY_FILE}")
    print(f"{ui.BOLD}ВАЖНО:{ui.RESET} Передайте этот ключ собеседнику.")
    input("\nНажмите Enter...")

def handle_set_key():
    ui.print_header("УСТАНОВКА КЛЮЧА")
    key_str = ui.get_input("Вставьте ключ")
    if crypto.validate_key_format(key_str):
        crypto.save_key(key_str.encode())
        ui.print_success("Ключ успешно установлен!")
    else:
        ui.print_error("Неверный формат ключа!")
    input("\nНажмите Enter...")

def handle_delete_key():
    ui.print_header("УДАЛЕНИЕ КЛЮЧА")
    ui.print_warning("Вы уверены, что хотите удалить текущий ключ?")
    confirm = ui.get_input("Введите 'yes' для подтверждения")
    if confirm.lower() == 'yes':
        if crypto.delete_key():
            ui.print_success("Ключ успешно удален.")
        else:
            ui.print_info("Файл ключа не найден.")
    else:
        ui.print_info("Удаление отменено.")
    input("\nНажмите Enter...")

def chat_mode():
    cipher = crypto.get_cipher()
    if not cipher:
        ui.print_error("Ключ не найден! Сначала создайте или установите его.")
        input("\nНажмите Enter...")
        return

    while True:
        ui.clear_screen()
        ui.print_header("РЕЖИМ ПЕРЕПИСКИ")
        print(f"1. Написать сообщение (шифровать)")
        print(f"2. Прочитать из буфера (расшифровать)")
        print(f"0. Назад")
        
        choice = ui.get_input("Выбор")
        
        if choice == '1':
            text = ui.get_input("Сообщение")
            encrypted = crypto.encrypt_message(cipher, text)
            if encrypted:
                pyperclip.copy(encrypted)
                ui.print_success("Зашифровано и скопировано!")
            input("\nНажмите Enter...")
        elif choice == '2':
            encrypted_text = pyperclip.paste().strip()
            decrypted = crypto.decrypt_message(cipher, encrypted_text)
            if decrypted:
                print(f"\n🔓 {ui.BOLD}Расшифровано:{ui.RESET} {ui.GREEN}{decrypted}{ui.RESET}")
            else:
                ui.print_error("Ошибка расшифровки! Проверьте буфер обмена и ключ.")
            input("\nНажмите Enter...")
        elif choice == '0':
            break

def main_menu():
    while True:
        ui.clear_screen()
        ui.print_header("CRYPTIZER PRO")
        
        key_exists = crypto.load_key() is not None
        status = f"{ui.GREEN}Активен{ui.RESET}" if key_exists else f"{ui.RED}Отсутствует{ui.RESET}"
        print(f"Статус ключа: {status}\n")
        
        print(f"1. {ui.CYAN}Чат-режим{ui.RESET}")
        print(f"2. Создать новый ключ")
        print(f"3. Ввести существующий ключ")
        if key_exists:
            print(f"4. {ui.RED}Удалить текущий ключ{ui.RESET}")
        print(f"0. Выход")
        
        choice = ui.get_input("Действие")
        
        if choice == '1':
            chat_mode()
        elif choice == '2':
            handle_generate_key()
        elif choice == '3':
            handle_set_key()
        elif choice == '4' and key_exists:
            handle_delete_key()
        elif choice == '0':
            print(f"\n{ui.YELLOW}До встречи!{ui.RESET}")
            break

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{ui.YELLOW}Выход из программы.{ui.RESET}")
        sys.exit(0)