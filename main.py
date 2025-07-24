import os
import json
from datetime import datetime


def addNotes(notes):
    title = input("Введите название заметки: ")
    description = input("Введите описание заметки: ")
    createdTime = datetime.now()

    note = {
        'title' : title,
        'description' : description,
        'created_at' : createdTime.isoformat()
    }
    print(notes)
    notes.append(note)
    print(notes)

    with open("notes.json", "w") as file:
        json.dump(notes, file, indent=4)
    return notes

def deleteNotes(notes):
    for i, note in enumerate(notes):
        print(f"{i+1}. {note['title']}")
    index = int(input("Введите номер заметки для удаления: ")) - 1

    if 0 <= index < len(notes):
        del notes[index]
        with open("notes.json", "w") as file:
            json.dump(notes, file, indent=4)
    else:
        print("Неверный номер заметки для удаления.")

    return notes


def listNotes(notes):
    if not notes:
        print("Нет заметок для отображения.")
        print("")
    else:
        for note in notes:
            print(f"Название: {note['title']}")
            print(f"Описание: {note['discription']}")
            print(f"Создано: {note['created_at']}")
            print("-" * 20)


def loadNotes():
    try:
        with open("notes.json", "r", encoding="utf-8") as saves:
            return json.load(saves)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def main():
    if os.path.exists("notes.json"):
        notes = loadNotes()
    else:
        notes = []
        

    while True:
        print("\nМеню:")
        print("1. Показать все заметки")
        print("2. Добавить заметку")
        print("3. Удалить заметку")
        print("4. Выйти")
        choice = input("Выберите действие: ")

        if choice == "1":
            listNotes(notes)
        elif choice == "2":
            notes = addNotes(notes)
        elif choice == "3":
            notes = deleteNotes(notes)
        elif choice == "4":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")
main()