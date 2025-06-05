import  enum
class Role(enum.StrEnum):
    STUDENT = enum.auto()
    TEACHER = enum.auto()


class User:
    def __init__(self, name: str, email: str, role: Role) -> None:
        self.name = name
        self.email = email
        self.role = role

    @staticmethod
    def send_notification(notification):
        print(notification.format())


class Notification:
    def __init__(self, subject: str, message: str, attachment: str = "") -> None:
        self.subject = subject
        self.message = message
        self.attachment = attachment

    def format(self) -> str:
        return f"Subject: {self.subject}\nMessage: {self.message}\nAttachment: {self.attachment or 'None'}"


class StudentNotification(Notification):
    def format(self) -> str:
        return super().format() + "\n[Sent via Student Portal]"

class TeacherNotification(Notification):
    def format(self) -> str:
        return super().format() + "\n[Teacher's Desk Notification]"

def send_notification(self, notification):
    print(notification.format())


def main():
    student = User("Alice", "alice@gmail.com", Role.STUDENT)
    teacher = User("Bob", "bob@gmail.com", Role.TEACHER)

    notif1 = StudentNotification("Exam Reminder", "Don't forget your exam on Friday!")
    notif2 = TeacherNotification("Meeting", "Staff meeting on Monday at 9am.", "Agenda.pdf")

    student.send_notification(notif1)
    teacher.send_notification(notif2)

if __name__ == "__main__":
    main()