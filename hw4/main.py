from repository import Repository

class StudentService:
    def __init__(self, repository: Repository):
        self.repository = repository

    def add_student(self, student: dict) -> dict | None:
        if not student.get("name") or not student.get("marks"):
            return None
        self.repository.add_student(student)
        return student

    def show_students(self):
        print("=========================")
        for student_id, student in self.repository.students.items():
            print(f"{student_id}. {student['name']}")
        print("=========================")

    def show_student(self, id_: int):
        student = self.repository.get_student(id_)
        if student:
            print("=========================")
            print(f"Name: {student['name']}")
            print(f"Marks: {student['marks']}")
            print(f"Info: {student['info']}")
            print("=========================")
        else:
            print("Student not found.")

    def update_student(self, id_: int, raw_input: str):
        parts = raw_input.split(";")
        if len(parts) != 2:
            print("Невірний формат. Треба: ім’я;інфо")
            return
        name = parts[0]
        info = parts[1]
        self.repository.update_student(id_, {"name": name, "info": info})
        print("Студента оновлено.")

    def delete_student(self, id_: int):
        self.repository.delete_student(id_)
        print("Студента видалено.")

    def add_mark(self, id_: int, mark: int):
        self.repository.add_mark(id_, mark)
        print("Оцінку додано.")


def ask_student_payload() -> dict:
    raw = input("Enter student like: John Doe;1,2,3\n")
    try:
        name, marks_raw = raw.split(";")
        marks = [int(m.strip()) for m in marks_raw.split(",")]
        return {"name": name, "marks": marks, "info": ""}
    except:
        return {}


def student_management_command_handle(command: str, service: StudentService):
    if command == "show":
        service.show_students()
    elif command == "add":
        student = ask_student_payload()
        if service.add_student(student):
            print("Студента додано.")
        else:
            print("Невірні дані студента.")
    elif command == "search":
        try:
            id_ = int(input("Введіть ID студента: "))
            service.show_student(id_)
        except ValueError:
            print("ID має бути числом.")
    elif command == "update":
        try:
            id_ = int(input("Введіть ID студента: "))
            service.show_student(id_)
            raw = input("Введіть нові ім’я та опис (name;info): ")
            service.update_student(id_, raw)
        except ValueError:
            print("ID має бути числом.")
    elif command == "delete":
        try:
            id_ = int(input("Введіть ID студента: "))
            service.delete_student(id_)
        except ValueError:
            print("ID має бути числом.")
    elif command == "addmark":
        try:
            id_ = int(input("Введіть ID студента: "))
            mark = int(input("Введіть оцінку: "))
            service.add_mark(id_, mark)
        except ValueError:
            print("ID та оцінка мають бути числами.")
    else:
        print("Невідома команда")


def handle_user_input():
    repo = Repository()
    service = StudentService(repo)
    commands = ("show", "add", "search", "update", "delete", "addmark", "quit", "help")

    print("Вітаємо у Journal!")
    print("Команди:", ", ".join(commands))

    while True:
        command = input("Введіть команду: ").strip().lower()
        if command == "quit":
            print("До побачення!")
            break
        elif command == "help":
            print("Доступні команди:", ", ".join(commands))
        else:
            student_management_command_handle(command, service)


if __name__ == "__main__":
    handle_user_input()
