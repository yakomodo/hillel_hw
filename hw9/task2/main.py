import requests
import json
from collections import defaultdict, Counter

BASE_URL = "https://jsonplaceholder.typicode.com"


class Comment:
    def __init__(self, id: int, post_id: int, name: str, email: str, body: str):
        self.id = id
        self.post_id = post_id
        self.name = name
        self.email = email
        self.body = body

    def to_dict(self):
        return {
            "id": self.id,
            "post_id": self.post_id,
            "name": self.name,
            "email": self.email,
            "body": self.body
        }


class CommentModerator:
    def __init__(self):
        self.comments: list[Comment] = []
        self.flagged_comments: list[Comment] = []

    def fetch_comments(self):
        try:
            response = requests.get(f"{BASE_URL}/comments")
            response.raise_for_status()
            data = response.json()

            for entry in data:
                try:
                    comment = Comment(
                        id=entry['id'],
                        post_id=entry['postId'],
                        name=entry['name'],
                        email=entry['email'],
                        body=entry['body']
                    )
                    self.comments.append(comment)
                except (KeyError, TypeError):
                    continue  # пропускаємо некоректні записи

        except requests.RequestException as e:
            print(f"Помилка при отриманні коментарів: {e}")

    def flag_suspicious_comments(self):
        suspicious_keywords = ['buy', 'free', 'offer']
        for comment in self.comments:
            body_lower = comment.body.lower()
            if any(word in body_lower for word in suspicious_keywords) or "!!" in comment.body:
                self.flagged_comments.append(comment)

    def group_by_post(self) -> dict[int, list[Comment]]:
        grouped = defaultdict(list)
        for comment in self.flagged_comments:
            grouped[comment.post_id].append(comment)
        return grouped

    def top_spammy_emails(self, n: int = 5) -> list[str]:
        email_counts = Counter(comment.email for comment in self.flagged_comments)
        return [email for email, _ in email_counts.most_common(n)]

    def export_flagged_to_json(self, filename: str = "flagged_comments.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump([comment.to_dict() for comment in self.flagged_comments], f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    moderator = CommentModerator()
    moderator.fetch_comments()
    moderator.flag_suspicious_comments()

    print(f"🔍 Загальна кількість підозрілих коментарів: {len(moderator.flagged_comments)}")

    grouped = moderator.group_by_post()
    for post_id, comments in grouped.items():
        print(f"📌 Пост {post_id} має {len(comments)} підозрілих(і) коментарів")

    print("\n📧 Топ 5 спамн mail-адрес:")
    for email in moderator.top_spammy_emails():
        print(f" - {email}")

    moderator.export_flagged_to_json()
    print("\n💾  коментарі збережено у файл 'flagged_comments.json'")
