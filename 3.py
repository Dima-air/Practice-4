import json
import csv
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    filename="students.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

FILENAME = "students.json"
CSV_EXPORT = "students_export.csv"

def load_data():
    if not os.path.exists(FILENAME):
        logging.info("Файл базы данных не найден, создан новый список")
        return []
    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            data = json.load(f)
            logging.info(f"Загружено студентов {len(data)}")
            return data
    except (json.JSONDecoder, IOError) as e:
        logging.error(f"Ошибка при чтении JSON: {e}")
        print(f"Ошибка при чтение файла: {e}")
        return []

def save_data(students):
    try:
        with open(FILENAME, "w", encoding="utf-8") as f:
            json.dump(students, f, ensure_ascii=False, indent=4)
            logging.info("Данные синхронизированы с JSON")
    except IOError as e:
        logging.error(f"Ошибка при сохранение JSON: {e}")
        print(f"Ошибка при сохранение: {e}")

def get_valid_age():
    while True:
        try:
            age = int(input("Введите возраст: "))
            if age > 16:
                return age
            logging.warning(f"Попытка ввода слишком малого возраста: {age}")
            print("Ошибка: возраст должен быть больше 16")
        except ValueError:
            logging.warning("Ошибка ввода возраста: введено не число")
            print("Ошибка: введите целое число")

def get_valid_grades():
    while True:
        try:
            raw_input = input("Введите оценки через пробел: ")
            grades = [int(i) for i in raw_input.split()]
            if all(2 <= i <= 5 for i in grades) and grades:
                return grades
            logging.warning(f"Введены некорректные оценки: {grades}")
            print("Ошибка: оценки должны быть от 2 до 5")
        except ValueError:
            logging.warning("Ошибка ввода оценок: нечисловые значения")
            print("Ошибка: вводите только числа")

def add_student(students):
    name = input("Имя студента: ").strip()
    age = get_valid_age()
    group = input("Группа: ").strip()
    grades = get_valid_grades()

    new_id = max([s['id'] for s in students], default=0) + 1
    student = {"id": new_id,
               "name": name,
               "age": age,
               "group": group,
               "grades": grades
               }
    students.append(student)
    save_data(students)
    logging.info(f"Добавлен студент {name} (ID: {new_id}, Группа: {group}")
    print("Студент добавлен")
    print()

def view_students(students):
    if not students:
        print("Список пуст")
        return
    print("Список студентов")
    for s in students:
        print()
        avg = sum(s['grades']) / len(s['grades']) if s['grades'] else 0
        print(f"ID: {s['id']}\nИмя: {s['name']}\nГруппа: {s['group']}\nСредний балл: {avg:.2f}")
        print()
    print()

def search_students(students):
    query = input("Поиск (имя/группа): ").lower()
    logging.info(f"Выполнен поиск по запросу: '{query}'")
    res = [s for s in students if query in s['name'].lower() or query in s['group'].lower()]
    view_students(res) if res else print("Ничего не найдено")
    print()


def export_csv(students):
    if not students:
        logging.warning("Попытка экспорта пустого списка в CSV")
        print("Нет данных для экспорта")
        return

    try:
        with open(CSV_EXPORT, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["ID", "Имя", "Возраст", "Группа", "Средний балл"])
            for s in students:
                avg = sum(s['grades']) / len(s['grades']) if s['grades'] else 0
                writer.writerow([s['id'], s['name'], s['age'], s['group'], f"{avg:.2f}"])
        logging.info(f"Данные экспортированы в {CSV_EXPORT}")
        print(f"Данные экспортированы в {CSV_EXPORT}")
    except IOError as e:
        logging.error(f"Ошибка экспорта в CSV: {e}")
        print(f"Ошибка экспорта {e}")

def main():
    logging.info("Запуск")
    students = load_data()

    actions = {
        '1': lambda: add_student(students),
        '2': lambda: view_students(students),
        '3': lambda: search_students(students),
        '4': lambda: export_csv(students)
    }

    while True:
        print("1. Добавить\n2. Список студентов\n3. Поиск\n4. Экспорт в CSV\n5. Выход")
        choice = input("Выберите действие: ")
        print()
        if choice == '5':
            logging.info("Завершение работы пользователем")
            break
        if choice in actions:
            actions[choice]()
        else:
            print("Неверный выбор")

if __name__ == "__main__":
    main()