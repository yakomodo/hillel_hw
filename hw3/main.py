# ─────────────────────────────────────────────
# STORAGE
# ─────────────────────────────────────────────
students: list[dict] = [
    {"id": 1, "name": "Alice Johnson", "marks": [7, 8, 9, 10, 6, 7, 8], "info": "Alice Johnson is 18 y.o. Interests: math"},
    {"id": 2, "name": "Michael Smith", "marks": [6, 5, 7, 8, 7, 9, 10], "info": "Michael Smith is 19 y.o. Interests: science"},
    {"id": 3, "name": "Emily Davis", "marks": [9, 8, 8, 7, 6, 7, 7], "info": "Emily Davis is 17 y.o. Interests: literature"},
    {"id": 4, "name": "James Wilson", "marks": [5, 6, 7, 8, 9, 10, 11], "info": "James Wilson is 20 y.o. Interests: sports"},
    {"id": 5, "name": "Olivia Martinez", "marks": [10, 9, 8, 7, 6, 5, 4], "info": "Olivia Martinez is 18 y.o. Interests: art"},
    {"id": 6, "name": "Emily Davis", "marks": [4, 5, 6, 7, 8, 9, 10], "info": "Daniel Brown is 19 y.o. Interests: music"},
    {"id": 7, "name": "Sophia Taylor", "marks": [11, 10, 9, 8, 7, 6, 5], "info": "Sophia Taylor is 20 y.o. Interests: physics"},
    {"id": 8, "name": "William Anderson", "marks": [7, 7, 7, 7, 7, 7, 7], "info": "William Anderson is 18 y.o. Interests: chemistry"},
    {"id": 9, "name": "Isabella Thomas", "marks": [8, 8, 8, 8, 8, 8, 8], "info": "Isabella Thomas is 19 y.o. Interests: biology"},
    {"id": 10, "name": "Benjamin Jackson", "marks": [9, 9, 9, 9, 9, 9, 9], "info": "Benjamin Jackson is 20 y.o. Interests: history"},
]

# ─────────────────────────────────────────────
# CRUD
# ─────────────────────────────────────────────
def add_student(name: str, marks: list[int], details: str | None) -> dict | None:
    if not name:
        return None

    if details is None:
        details = ''

    next_id = max([s['id'] for s in students], default=0) + 1

    student = {
        "id": next_id,
        "name": name,
        "marks": marks,
        "info": details
    }

    students.append(student)
    return student


def show_students():
    print("=========================")
    for student in students:
        print(f"[{student['id']}] {student['name']}")
    print("=========================")


def search_student(student_id: int) -> dict | None:
    for student in students:
        if student["id"] == student_id:
            return student
    return None


def show_student(student: dict):
    print("=========================")
    print(f"ID: {student['id']}")
    print(f"Name: {student['name']}")
    print(f"Marks: {student['marks']}")
    print(f"Info: {student['info']}")
    print("=========================")


def delete_student(student_id: int):
    student = search_student(student_id)
    if student is None:
        print(f"Student {student_id} not found")
        return

    students.remove(student)
    print(f"Student {student_id} deleted.")


def update_student(student_id: int, raw_input: str) -> dict | None:
    parts = raw_input.split(";")
    if len(parts) != 2:
        print("Invalid format. Use: name;info — you can skip either part.")
        return None

    name_input, info_input = parts[0].strip(), parts[1].strip()
    student = search_student(student_id)

    if student is None:
        print(f"Student with ID {student_id} not found.")
        return None

    if not name_input and not info_input:
        print("Nothing to update.")
        return None

    if name_input:
        student["name"] = name_input

    if info_input:
        old_info = student["info"]

        if info_input == old_info:
            print("Info is the same — no update.")
        elif old_info in info_input:
            student["info"] = info_input
        elif info_input in old_info:
            print("Info already includes this value — no update.")
        else:
            student["info"] = f"{old_info}; {info_input}"

    return student

# ─────────────────────────────────────────────
# OPERATIONAL
# ─────────────────────────────────────────────
def ask_student_payload() -> dict | None:
    ask_prompt = (
        "Enter student's payload data using text template: "
        "John Doe;1,2,3,4,5;Loves chess\n"
        "Format: name;marks;info"
    )
    data = input(ask_prompt)
    if data.count(';') == 2:
        name, raw_marks, info = data.split(";")
        return {
            "name": name,
            "marks": [int(m) for m in raw_marks.replace(" ", "").split(",")],
            "info": info
        }
    elif data.count(';') == 1:
        name, raw_marks = data.split(";")
        return {
            "name": name,
            "marks": [int(m) for m in raw_marks.replace(" ", "").split(",")],
            "info": ''
        }
    else:
        return None


def add_mark() :
    student_id = int(input("Please write student ID: "))
    student = search_student(student_id)

    if student is None :
        print("Student not found")
        return
    else:
        raw_marks = input("Please write new marks (Format: 1,2,3): ")
        new_marks = [int(m) for m in raw_marks.replace(" ", "").split(",")]
        student["marks"].extend(new_marks)
        print(f"Updated marks: {student['marks']}")


def student_management_command_handle(command: str):
    if command == "show":
        show_students()
    elif command == "add marks":
        add_mark()
    elif command == "add":
        data = ask_student_payload()
        student = add_student(data["name"], data["marks"], data["info"])
        if student:
            print(f"Student {student['name']} added.")
        else:
            print("Failed to add student.")
    elif command == "search":
        student_id = input("Enter student ID: ")
        if student_id.isdigit():
            student = search_student(int(student_id))
            if student:
                show_student(student)
            else:
                print("Student not found.")
    elif command == "delete":
        student_id = input("Enter student ID to delete: ")
        if student_id.isdigit():
            delete_student(int(student_id))
    elif command == "update":
        student_id = input("Enter student ID to update: ")
        if student_id.isdigit():
            student = search_student(int(student_id))
            if student:
                show_student(student)
                print("Enter new name and info separated by ';'")
                new_data = input("Input: ")
                updated = update_student(int(student_id), new_data)
                if updated:
                    print("Student updated.")
                else:
                    print("Invalid update format.")
            else:
                print("Student not found.")


def handle_user_input():
    commands = ("show", "add", "search", "delete", "update", "quit", "help","add marks")
    print(f"Available commands: {commands}")
    while True:
        cmd = input("\nSelect command: ").strip()
        if cmd == "quit":
            print("Thanks for using the app.")
            break
        elif cmd == "help":
            print(f"Available commands: {commands}")
        elif cmd in commands:
            student_management_command_handle(cmd)
        else:
            print("Unknown command. Type 'help' to see options.")


if __name__ == "__main__":
    handle_user_input()

