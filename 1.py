import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    handlers=[logging.FileHandler('file_manager.log', encoding='utf-8')]
)
logger = logging.getLogger(__name__)

def get_filename():
    return input("Введите имя файла: ").strip()

def open_or_create_file(filename):
    try:
        if not os.path.exists(filename):
            with open(filename, 'w', encoding='utf-8') as f:
                pass
            print(f"Файл {filename} создан")

        return open(filename, 'r+', encoding='utf-8')
    except PermissionError as e:
        logger.error(f"Ошибка доступа к {filename}: {e}")
        print(f"Ошибка: нет прав доступа к '{filename}'")
        return None
    except UnicodeEncodeError as e:
        logger.error(f"Ошибка кодировки {filename}: {e}")
        print(f"Ошибка: проблема с кодировкой '{filename}'")
        return None
    except Exception as e:
        logger.exception(f"Непредвиденная ошибка при открытии {filename}: {e}")
        print(f"Ошибка при открытии: {e}")
        return None

def add_line(file):
    try:
        line = input("Введите строку для добавления (или 'выход' для выхода): ")
        if line.lower() == 'выход':
            logger.info("Введено слово 'выход'. Завершение работы")
            return False

        file.seek(0, 2)
        file.write(line + '\n')
        file.flush()
        logger.debug(f"Строка записана: {line}")
        return True
    except Exception as e:
        logger.exception(f"Ошибка при записи в файл: {e}")
        print(f"Ошибка при записи в файл: {e}")
        return False

def display_file_contents(file):
    try:
        file.seek(0)
        contents = file.read()
        print("Содержимое файла")
        print(contents if contents else "(файл пуст)")
        print()
    except UnicodeDecodeError as e:
        logger.error(f"Ошибка декодирования содержимого файла: {e}")
        print("Ошибка: проблема с кодировкой при чтении файл")
    except Exception as e:
        logger.exception("Ошибка при чтении файла")
        print(f"Ошибка при чтении файла: {e}")

def main():
    logger.info("Запуск файлового менеджера")
    print("Файловый менеджер")

    filename = get_filename()
    if not filename:
        logger.warning("Введено пустое имя файла. Завершение работы")
        print("Имя файла не может быть пустым")
        return

    file = open_or_create_file(filename)
    if file is None:
        logger.error("Не удалось открыть или создать файл. Завершение работы")
        return

    try:
        while True:
            if not add_line(file):
                break
            display_file_contents(file)
    finally:
        file.close()
        logger.info("Файл успешно закрыт. Завершение работы")
        print("Файл успешно закрыт. Завершение работы")

if __name__ == "__main__":
    main()

