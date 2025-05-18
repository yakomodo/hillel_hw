import csv
from pathlib import Path

STORAGE_FILE_NAME = Path(__file__).parent / "storage/students.csv"

class Repository:
    def __init__(self):
        # Завантаження студентів з файлу
        self.students = self.get_storage()

    def get_storage(self) -> dict[int, dict]:
        students = {}
        with open(STORAGE_FILE_NAME, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")
            for row in reader:
                student_id = int(row["id"])
                name = row["name"]
                marks = list(map(int, row["marks"].split(",")))
                info = row["info"]
                students[student_id] = {
                    "name": name,
                    "marks": marks,
                    "info": info,
                }
        return students

    def save(self):
        # Зберігає self.students у файл
        with open(STORAGE_FILE_NAME, mode="w", encoding="utf-8", newline="") as file:
            fieldnames = ["id", "name", "marks", "info"]
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
            for student_id, student_data in self.students.items():
                writer.writerow({
                    "id": student_id,
                    "name": student_data["name"],
                    "marks": ",".join(map(str, student_data["marks"])),
                    "info": student_data["info"]
                })

    def add_student(self, student: dict):
        # Додає нового студента та зберігає
        next_id = max(self.students.keys(), default=0) + 1
        self.students[next_id] = student
        self.save()

    def get_student(self, id_: int) -> dict | None:
        # Повертає студента за ID
        return self.students.get(id_)

    def update_student(self, id_: int, data: dict):
        # Частково оновлює дані студента
        student = self.students.get(id_)
        if not student:
            return
        for key in data:
            if key in student:
                student[key] = data[key]
        self.save()

    def delete_student(self, id_: int):
        # Видаляє студента
        if id_ in self.students:
            del self.students[id_]
            self.save()

    def add_mark(self, id_: int, mark: int):
        # Додає оцінку студенту
        student = self.students.get(id_)
        if not student:
            return
        student["marks"].append(mark)
        self.save()