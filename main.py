import os
import json
import uuid
from datetime import datetime

def save_to_json(notes):
    notes_dicts = [note.to_dict() for note in notes]
    with open("notes.json", "w", encoding="utf-8") as f:
        json.dump(notes_dicts, f, indent=4, ensure_ascii=False)


def load_from_json():
    try:
        with open("notes.json", "r", encoding="utf-8") as f:
            notesDict = json.load(f)
            notes = []
            for n in notesDict:
                note = Note(
                    n["_text"],
                    id=n["_id"],
                    status=n["_status"],
                    priority=n["_priority"],
                    created_at=n["_created_at"],
                    deadline=n["_deadline"]
                )
                notes.append(note)
            return notes    
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    

statuses = [
    "Не начато",
    "В процессе",
    "Выполнено"
]

priorities = [
    "Срочно!",
    "Средний",
    "Не срочно"
]

menuList = [
    "Показать все заметки",
    "Добавить заметку",
    "Удалить заметку",
    "Изменить дедлайн задачи",
    "Проверка дедлайна задачи",
    "Изменить приоритет задачи",
    "Изменить статус задачи",
    "Выйти"
]

class Note:
    def __init__(self, text, id = None, status = "Не начато", priority = "Не срочно", created_at = None, deadline = "Без дедлайна"):
        self._id = id or str(uuid.uuid4())
        self._text = text
        self._created_at = datetime.strftime(datetime.now(), '%Y/%m/%d %H:%M:%S') if created_at is None else created_at
        self._status = status
        self._priority = priority
        self._deadline = deadline


    def __str__(self):
        return f"""id: {self._id}, Задание: {self._text}, Приоритет: {self._priority}, 
    Создано: {self._created_at}, Дедлайн: {self._deadline}, Статус: {self._status}"""
    
    def __repr__(self):
        return f"""Note(id: {self._id}, text: {self._text}, priority: {self._priority}, 
    created_at: {self._created_at}, deadline: {self._deadline}, status: {self._status})"""
    
    def change_status(self):
        for s in enumerate(statuses):
            print(f"{s[0] + 1}. {s[1]}")
        try:
            selected = int(input("Введите число статуса: ")) - 1
            return statuses[selected]
        except IndexError:
            print(f"Введите число должно быть в диапозоне от 1 до {len(statuses)}")
        
    def change_priority(self):
        for p in enumerate(priorities):
            print(f"{p[0] + 1} {p[1]}")
        try: 
            selected = int(input("Введите номер приоритета для задачи: ")) - 1
            return priorities[selected]
        except IndexError:
            print("Введенне не правильный номер приоритета, введите число от 1 до 3")
            
    def change_deadline(self):
        try:
            year = input("Введите год: ")
            month = input("Введите месяц: ")
            day = input("Введите день: ")
            
            date = (year + "/" + month + "/" + day)
            check_date = datetime.strptime(date, '%Y/%m/%d')
            
            return date
        except ValueError:
            print("Дедлайн должен быть в формате гггг/мм/дд")
        
    def edit_text(self, text):
        self._text = text
        
    def check_deadline(self):
        try:
            created_at = datetime.strptime(self._created_at, '%Y/%m/%d %H:%M:%S')
            deadline = datetime.strptime(self._deadline, '%Y/%m/%d')
            res = deadline - created_at
            return res
        except ValueError:
            print("В дедлайне указана не правильная дата! Дата должна быть в формате: ггггг/мм/дд")
    
    
    def to_dict(self):
        return {
            "_id": self._id,
            "_text": self._text,
            "_created_at": self._created_at,
            "_status": self._status,
            "_priority": self._priority,
            "_deadline": self._deadline
        }
    #Сеттеры|Геттеры
    @property
    def id(self):
        return self._id

    @property
    def text(self):
        return self._text
    @text.setter
    def text(self, text):
        self._text = text
        
    @property
    def priority(self):
        return self._priority
    @priority.setter
    def priority(self, priority):
        self._priority = priority
    
    @property
    def created_at(self):
        return self._created_at
    
    @property
    def deadline(self):
        return self._deadline
    @deadline.setter
    def deadline(self, deadline):
        self._deadline = deadline
    
    @property
    def status(self):
        return self._status
    @status.setter
    def status(self, status):
        self._status = status
        
    

    
def add_notes(notes):
    text = input("Напишите вашу заметку: ")

    note = Note(text)
    notes.append(note)

    save_to_json(notes)
    
    return notes

def delete_notes(notes):
    for i, note in enumerate(notes):
        print(f"{i+1}. {note.text}")
    index = int(input("Введите номер заметки для удаления: ")) - 1

    if 0 <= index < len(notes):
        del notes[index]
        save_to_json(notes)
    else:
        print("Неверный номер заметки для удаления.")

    return notes


def list_notes(notes):
    if not notes:
        print("Нет заметок для отображения.")
        print("")
    else:
        for i, note in enumerate(notes):
            print(f"Задача {i+1}")
            print(note)
            print("-" * 50)

def check_all_deadlines(notes):
    for n in notes:
        delta = n.check_deadline()
        print(f"Дедлайн через: {delta}" if delta else "дедлайн не выставлен")

def change_deadline(notes):
    list_notes(notes)
    try:
        note = int(input("Введите номер задачи: ")) - 1
        notes[note].deadline = notes[note].change_deadline()
        save_to_json(notes)
    except ValueError:
        print("Номер задачи должен быть числом")
    except IndexError:
        print("Такого номера задачи нету в списке!")

def change_priority(notes):
    list_notes(notes)
    try:
        note = int(input("Введите номер задачи: ")) - 1
        notes[note].priority = notes[note].change_priority()
        save_to_json(notes)
    except ValueError:
        print("Номер задачи должен быть числом")
    except IndexError:
        print("Такого номера задачи нету в списке!")

def change_status(notes):
    list_notes(notes)
    try:
        note = int(input("Введите номер задачи: ")) - 1
        notes[note].status = notes[note].change_status()
        save_to_json(notes)
    except ValueError:
        print("Номер задачи должен быть числом")
    except IndexError:
        print("Такого номера задачи нету в списке!")

def main():
    notes = load_from_json()
    while True:
        for m in enumerate(menuList):
            print(f"{m[0]+1}. {m[1]}")
        try:    
            choice = int(input("Введите число меню: "))
            if choice > len(menuList):
                raise IndexError
            if choice == 1:
                list_notes(notes)
            elif choice == 2:
                add_notes(notes)
            elif choice == 3:
                delete_notes(notes)
            elif choice == 4:
                change_deadline(notes)
            elif choice == 5:
                check_all_deadlines(notes)
            elif choice == 6:
                change_priority(notes)
            elif choice == 7:
                change_status(notes)
            elif choice == 8:
                print("Пока!")
                break
        except ValueError:
            print("Ввести можно только число!")
        except IndexError:
            print(f"Введённое число должно быть в диапазоне от 1 до {len(menuList)}")


if __name__ == "__main__":
    main()