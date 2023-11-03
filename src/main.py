#

import json
from os.path import exists
from datetime import datetime

NOTE_ID = 'id'
NOTE_HEADER = 'header'
NOTE_BODY = 'body'
NOTE_CREATE = 'create_date'
NOTE_MODIFY = 'modify_date'

FILE_NAME = 'notes.json'
DATE_TIME_FORMAT = '%m/%d/%y %H:%M:%S'

MAIN_MENU_ADD = 1
MAIN_MENU_SAVE = 2
MAIN_MENU_PRINT = 3
MAIN_MENU_SEARCH = 4
MAIN_MENU_LOAD = 5
MAIN_MENU_CHANGE = 6
MAIN_MENU_REMOVE = 7
MAIN_MENU_EXIT = 8

MAIN_MENU = f'{MAIN_MENU_ADD}. Add  {MAIN_MENU_SAVE}. Save  {MAIN_MENU_PRINT}. Print  {MAIN_MENU_SEARCH}. \
Search  {MAIN_MENU_LOAD}. Load  {MAIN_MENU_CHANGE}. Change  {MAIN_MENU_REMOVE}. Remove  {MAIN_MENU_EXIT}. Exit'

CHANGE_MENU_NOTE_HEADER = 1
CHANGE_MENU_NOTE_BODY = 2
CHANGE_MENU_EXIT = 3

CHANGE_MENU = f'{CHANGE_MENU_NOTE_HEADER}. Header  {CHANGE_MENU_NOTE_BODY}. Body {CHANGE_MENU_EXIT}. Exit'

SEARCH_MENU_NOTE_HEADER = 1
SEARCH_MENU_NOTE_CREATE = 2
SEARCH_MENU_EXIT = 3

SEARCH_MENU = f'{SEARCH_MENU_NOTE_HEADER}. Header {SEARCH_MENU_NOTE_CREATE}. Create date  {SEARCH_MENU_EXIT}. Exit'


def show_menu(menu: str, min_menu_item: int, max_menu_item: int, default_choice: int) -> int:
    while True:
        print(100 * '-')
        print()
        print(menu)
        choice = input(f'choose [{min_menu_item}-{max_menu_item}]: ')
        if choice == '':
            return default_choice
        if choice.isdigit():
            choice_value = int(choice)
            if min_menu_item <= choice_value <= max_menu_item:
                return choice_value


def load_from_file(filename: str) -> list[dict[str, str]]:
    with open(filename, 'r') as file:
        return json.load(file)


def save_to_file(filename: str, notes: list[dict[str, str]]):
    with open(filename, 'w') as file:
        json.dump(notes, file)


def print_notes(notes: list[dict[str, str]]):
    notes.sort(key=lambda d: datetime.strptime(d[NOTE_CREATE], DATE_TIME_FORMAT))
    for note in notes:
        print(
            f"#{note[NOTE_ID]}\tcreate: {note[NOTE_CREATE]}\tmodify: {note[NOTE_MODIFY]}"
            f"\nHeader: {note[NOTE_HEADER]}\nBody: {note[NOTE_BODY]}")


def input_note():
    note_header = input('Input header note: ')
    note_body = input('Input body note: ')
    return note_header, note_body


def add_note(notes: list[dict[str, str]], note_header: str, note_body: str, node_create: datetime,
             node_modify: datetime):
    note = {
        NOTE_ID: str(len(notes) + 1),
        NOTE_BODY: note_body,
        NOTE_HEADER: note_header,
        NOTE_CREATE: node_create.strftime(DATE_TIME_FORMAT),
        NOTE_MODIFY: node_modify.strftime(DATE_TIME_FORMAT)
    }
    notes.append(note)


def add_note_handler(notes: list[dict[str, str]]):
    note_header, note_body = input_note()
    add_note(notes, note_header, note_body, datetime.now(), datetime.now())
    print('Note appended\n')


def save_note_handler(notes: list[dict[str, str]]):
    save_to_file(FILE_NAME, notes)
    print('Notes saved\n')


def print_note_handler(notes: list[dict[str, str]]):
    print('\nNotes:')
    print_notes(notes)
    print()


def search_notes(notes: list[dict[str, str]], column: str, value: str):
    results = []
    for note in notes:
        if value.lower() in note[column].lower():
            results.append(note)
    return results


def search_notes_by_date(notes: list[dict[str, str]], column: str, value: datetime):
    results = []
    for note in notes:
        create_date = datetime.strptime(note[column], DATE_TIME_FORMAT)
        if value.date() == create_date.date():
            results.append(note)
    return results


def search_note_handler(notes: list[dict[str, str]]):
    while True:
        choice = show_menu(SEARCH_MENU, SEARCH_MENU_NOTE_HEADER, SEARCH_MENU_EXIT, SEARCH_MENU_EXIT)
        if choice == SEARCH_MENU_NOTE_HEADER:
            value = input("Input note header: ")
            results = search_notes(notes, NOTE_HEADER, value)
        elif choice == SEARCH_MENU_NOTE_CREATE:
            value = input("Input create date in format month/day/year: ")
            create_date_value = datetime.strptime(value, "%m/%d/%y")
            results = search_notes_by_date(notes, NOTE_CREATE, create_date_value)
        else:
            return

        if results:
            print('Find contacts: ')
            print_notes(results)
        else:
            print('No contacts found')


def load_note_handler():
    if exists(FILE_NAME):
        notes = load_from_file(FILE_NAME)
        print(f"\nLoaded {len(notes)} notes")
        return notes
    print(f'File {FILE_NAME} not found')


def change_note_handler(notes: list[dict[str, str]]):
    index = int(input("Input number for change note, or 0 to exit: "))
    if index == 0:
        return
    elif 1 <= index <= len(notes):
        note = notes[index - 1]
        print(
            f"You choose.\n"
            f"#{note[NOTE_ID]}\tcreate: {note[NOTE_CREATE]}\tmodify: {note[NOTE_MODIFY]}"
            f"\nHeader: {note[NOTE_HEADER]}\nBody: {note[NOTE_BODY]}")

        while True:
            choice = show_menu(CHANGE_MENU, CHANGE_MENU_NOTE_HEADER, CHANGE_MENU_EXIT, CHANGE_MENU_EXIT)
            if choice == CHANGE_MENU_NOTE_HEADER:
                value = input("Input header: ")
                note[NOTE_HEADER] = value
                note[NOTE_MODIFY] = datetime.now().strftime(DATE_TIME_FORMAT)
            elif choice == CHANGE_MENU_NOTE_BODY:
                value = input("Input body name: ")
                note[NOTE_BODY] = value
                note[NOTE_MODIFY] = datetime.now().strftime(DATE_TIME_FORMAT)
            else:
                return


def remove_note_handler(notes: list[dict[str, str]]):
    index = int(input("Input index number for remove note, or 0 to exit: "))
    if index == 0:
        return
    elif 1 <= index <= len(notes):
        note = notes[index - 1]
        print(
            f"You choose.\n"
            f"#{note[NOTE_ID]}\tcreate: {note[NOTE_CREATE]}\tmodify: {note[NOTE_MODIFY]}"
            f"\nHeader: {note[NOTE_HEADER]}\nBody: {note[NOTE_BODY]}")

        yon = input("\npress y for delete note [n]: ")
        if yon.lower() == 'y':
            notes.remove(note)


def exit_handler():
    print()


def main():
    note_book = []

    while True:
        choice = show_menu(MAIN_MENU, MAIN_MENU_ADD, MAIN_MENU_EXIT, MAIN_MENU_EXIT)
        if choice == MAIN_MENU_ADD:
            add_note_handler(note_book)
        elif choice == MAIN_MENU_SAVE:
            save_note_handler(note_book)
        elif choice == MAIN_MENU_PRINT:
            print_note_handler(note_book)
        elif choice == MAIN_MENU_SEARCH:
            search_note_handler(note_book)
        elif choice == MAIN_MENU_LOAD:
            note_book = load_note_handler()
        elif choice == MAIN_MENU_CHANGE:
            change_note_handler(note_book)
        elif choice == MAIN_MENU_REMOVE:
            remove_note_handler(note_book)
        elif choice == MAIN_MENU_EXIT:
            exit_handler()
            break
        else:
            break


if __name__ == '__main__':
    main()
