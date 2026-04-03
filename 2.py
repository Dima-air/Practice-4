import json
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    filename="app.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

FILENAME = "tasks.json"

def load_tasks():
    if not os.path.exists(FILENAME):
        return []
    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            tasks = json.load(f)
            logging.info(f"Загружено задач: {len(tasks)}")
            return tasks
    except (json.JSONDecodeError, IOError) as e:
        logging.error(f"Ошибка загрузки файла: {e}")
        print(f"Ошибка при загрузке файла: {e}")
        return []

def save_tasks(tasks):
    try:
        with open(FILENAME, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=4)
            logging.info("Изменения сохранены в файл")
    except IOError as e:
        logging.error(f"Ошибка сохранения файла: {e}")
        print(f"Ошибка при сохранении файла: {e}")

def add_task(tasks):
    title = input("Введите название задачи: ")
    desc = input("Введите описание задачи: ")

    new_id = max([t['id'] for t in tasks], default=0) + 1
    new_task = {
        "id": new_id,
        "title": title,
        "description": desc,
        "status": "не выполнена"
    }

    tasks.append(new_task)
    save_tasks(tasks)
    logging.info(f"Добавлена новая задача: ID {new_id}")
    print(f"Задача №{new_id} добавлена")


def view_tasks(tasks):
    if not tasks:
        print("Список задач пуст")
        return

    print("Список задач")
    for t in tasks:
        print(f"[{t['id']}] {t['title']} — {t['status']}")
        print(f"    Описание: {t['description']}")


def mark_done(tasks):
    try:
        task_id = int(input("Введите ID задачи для отметки выполнения: "))
        for t in tasks:
            if t['id'] == task_id:
                t['status'] = "выполнена"
                save_tasks(tasks)
                logging.info(f"Задача ID {task_id} отмечена как выполненная")
                print("Статус обновлен")
                return
        logging.warning(f"Попытка отметить задачу: ID {task_id} не найден")
        print("Задача с таким ID не найдена")
    except ValueError:
        logging.error("Ошибка ввода ID (не число) при отметке выполнения")
        print("Ошибка: ID должен быть числом")


def delete_task(tasks):
    try:
        task_id = int(input("Введите ID задачи для удаления: "))
        for i, t in enumerate(tasks):
            if t['id'] == task_id:
                confirm = input(f"Вы уверены, что хотите удалить {t['title']}? (y/n): ")
                if confirm.lower() == 'y':
                    tasks.pop(i)
                    save_tasks(tasks)
                    logging.info(f"Задача ID {task_id} удалена")
                    print("Задача удалена")
                else:
                    logging.info(f"Удаление задачи ID {task_id} отменено пользователем")
                    print("Удаление отменено")
                return
        logging.warning(f"Попытка удаления: ID {task_id} не найден")
        print("Задача с таким ID не найдена")
    except ValueError:
        logging.error("Ошибка ввода ID (не число) при удалении")
        print("Ошибка: ID должен быть числом")

def main():
    logging.info("Приложение запущено")
    tasks = load_tasks()

    while True:
        print("Меню:")
        print("1. Показать задачи\n2. Добавить задачу\n3. Отметить как выполненную\n4. Удалить задачу\n5. Выход")
        choice = input("Выберите действие: ")

        if choice == '1':
            view_tasks(tasks)
        elif choice == '2':
            add_task(tasks)
        elif choice == '3':
            mark_done(tasks)
        elif choice == '4':
            delete_task(tasks)
        elif choice == '5':
            logging.info("Приложение закрыто пользователем")
            print("Завершение работы")
            break
        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()