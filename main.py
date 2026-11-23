import dbm
import os
import shelve
from pathlib import Path

import questionary as q

data_path = Path.home() / ".local" / "share" / "notes"
data_path.mkdir(parents=True, exist_ok=True)
db_path = data_path / "users"

try:
    with shelve.open(db_path) as db:
        ...
except dbm.error as e:
    print(f"{e}, deleting db file...")
    if dbm.whichdb(str(db_path)) != "dbm.ndbm":
        os.remove(f"{db_path}.db")


def account():
    while True:
        opt = q.select(
            f"--- {name} ---",
            [
                q.Choice("1. Delete user", "1"),
                q.Choice("2. List", "2"),
                q.Choice("3. Create", "3"),
                q.Choice("4. Remove", "4"),
                q.Choice("5. Check Note", "5"),
                q.Choice("ex. Exit", "ex"),
            ],
        ).ask()
        user = db[name]
        match opt:
            case "1":
                db.pop(name)
                break
            case "2":
                notes = list(user["notes"])
                for index, note in enumerate(notes, start=1):
                    print(
                        f"{index}) NAME: {note[:20]}, CONTENT: '{user['notes'][note][:40]}{'...' if len(user['notes'][note]) > 40 else ''}'"
                    )
                input("Press Key To Continue...")
            case "3":
                note = q.text("Note name: ").ask()
                nvalue = q.text("Note Value: ").ask()
                user["notes"][note] = nvalue
                db[name] = user
            case "4":
                try:
                    note = int(q.text("Note Index: ").ask())
                except ValueError:
                    print("Not a number.")
                    break
                notes = list(user["notes"])
                if note - 1 >= 0 and note - 1 <= len(notes):
                    user["notes"].pop(notes[note - 1])
                    db[name] = user
                else:
                    print("Not a given index", note)
                    input()
            case "5":
                try:
                    note = int(q.text("Which note index do you want to read?: ").ask())
                except ValueError:
                    print("Thats not an index.")
                    break
                notes = list(user["notes"].items())
                noteName, noteContent = notes[note - 1]
                print(f"NAME: {noteName}; CONTENT: {noteContent};")
                input()

            case "ex":
                break
            case _:
                print("not an option")
        os.system("cls" if os.name == "nt" else "clear")


while True:
    opt = q.select(
        "--- NOTES ---",
        [
            q.Choice("1. List Users", "1"),
            q.Choice("2. Create Users", "2"),
            q.Choice("3. Login", "3"),
            q.Choice("ex. Exit", "ex"),
        ],
    ).ask()

    match opt:
        case "ex":
            break
        case "1":
            with shelve.open(db_path) as db:
                if not db:
                    print("No users found")
                else:
                    for usr in db:
                        print(usr)
            input("Press Key To Close...")
        case "2":
            with shelve.open(db_path) as db:
                name = q.text("Username: ", default="ligma").ask()
                password = q.password("Password: ", default="balls").ask()
                if name not in db and len(name) > 2:
                    db[name] = {
                        "pass": password,
                        "notes": {"insert note name": "search with index."},
                    }
                else:
                    print("er: user exists or name is below 3 letters.")
        case "3":
            with shelve.open(db_path) as db:
                name = q.text("Username: ").ask()
                password = q.password("Password: ").ask()
                if name in db and db[name]["pass"] == password:
                    account()
    os.system("cls" if os.name == "nt" else "clear")
