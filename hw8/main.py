import asyncio
from datetime import datetime

storage = {
    "students": [],
    "marks": []
}

class Student:
    def __init__(self, id_: int, name: str, creation_date: datetime):
        self.id = id_
        self.name = name
        self.creation_date = creation_date

class Mark:
    def __init__(self, student_id: int, value: float, creation_date: datetime):
        self.student_id = student_id
        self.value = value
        self.creation_date = creation_date

def add_student(student: Student):
    storage["students"].append(student)

def add_mark(mark: Mark):
    storage["marks"].append(mark)

def students_per_month():
    result = {}
    for s in storage["students"]:
        key = s.creation_date.strftime("%Y-%m")
        result[key] = result.get(key, 0) + 1
    return result

def average_today():
    today = datetime.now().date()
    today_marks = [m.value for m in storage["marks"] if m.creation_date.date() == today]
    if not today_marks:
        return 0
    return sum(today_marks) / len(today_marks)

def send_email(report: str):
    print(f"\n====== EMAIL REPORT ======")
    print(report)
    print("==========================\n")

async def report_sender():
    while True:
        students_by_month = students_per_month()
        avg_mark = average_today()
        report_lines = [
            f"Report generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "Students per month:"
        ]
        for month, count in sorted(students_by_month.items()):
            report_lines.append(f"  {month}: {count}")
        report_lines.append(f"Today's average mark: {avg_mark:.2f}")
        report = "\n".join(report_lines)
        send_email(report)
        await asyncio.sleep(10)


async def main():
    add_student(Student(1, "Alice", datetime(2025, 7, 1)))
    add_student(Student(2, "Bob", datetime(2025, 7, 5)))
    add_student(Student(3, "Charlie", datetime(2025, 6, 15)))
    add_student(Student(4, "David", datetime(2025, 5, 20)))

    add_mark(Mark(1, 85, datetime.now()))
    add_mark(Mark(2, 90, datetime.now()))
    add_mark(Mark(3, 78, datetime.now()))

    add_mark(Mark(1, 100, datetime(2024, 1, 1)))

    asyncio.create_task(report_sender())

    while True:
        cmd = input("Enter command (add_student/add_mark/quit): ").strip()
        if cmd == "add_student":
            name = input("Enter student name: ").strip()
            try:
                year = int(input("Enter registration year (e.g. 2025): "))
                month = int(input("Enter registration month (1-12): "))
                day = int(input("Enter registration day (1-31): "))
                creation_date = datetime(year, month, day)
            except ValueError:
                print("Invalid date, using today instead")
                creation_date = datetime.now()
            student_id = len(storage["students"]) + 1
            add_student(Student(student_id, name, creation_date))
            print(f"Student {name} added with ID {student_id}")
        elif cmd == "add_mark":
            try:
                student_id = int(input("Enter student ID: ").strip())
                value = float(input("Enter mark: ").strip())
                add_mark(Mark(student_id, value, datetime.now()))
                print(f"Mark {value} added for student ID {student_id}")
            except ValueError:
                print("Invalid input")
        elif cmd == "quit":
            print("Exiting...")
            break
        else:
            print("Unknown command")

if __name__ == "__main__":
    asyncio.run(main())
