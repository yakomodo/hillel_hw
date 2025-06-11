import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


class Post:
    def __init__(self, id: int, title: str, body: str):
        self.id = id
        self.title = title
        self.body = body


class User:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.posts: list[Post] = []

    def add_post(self, post: Post):
        self.posts.append(post)

    def average_title_length(self) -> float:
        if not self.posts:
            return 0.0
        return sum(len(post.title) for post in self.posts) / len(self.posts)

    def average_body_length(self) -> float:
        if not self.posts:
            return 0.0
        return sum(len(post.body) for post in self.posts) / len(self.posts)


class BlogAnalytics:
    def __init__(self):
        self.users: list[User] = []

    def fetch_data(self):
        try:
            users_resp = requests.get(f"{BASE_URL}/users")
            users_resp.raise_for_status()
            users_data = users_resp.json()

            for user_entry in users_data:
                user = User(id=user_entry['id'], name=user_entry['name'])

                posts_resp = requests.get(f"{BASE_URL}/posts", params={"userId": user.id})
                posts_resp.raise_for_status()
                posts_data = posts_resp.json()

                for post_entry in posts_data:
                    post = Post(id=post_entry['id'], title=post_entry['title'], body=post_entry['body'])
                    user.add_post(post)

                self.users.append(user)

        except requests.RequestException as e:
            print(f"Error fetching data: {e}")

    def user_with_longest_average_body(self) -> User:
        return max(self.users, key=lambda u: u.average_body_length(), default=None)

    def users_with_many_long_titles(self) -> list[User]:
        result = []
        for user in self.users:
            count = sum(1 for post in user.posts if len(post.title) > 40)
            if count > 5:
                result.append(user)
        return result


if __name__ == "__main__":
    analytics = BlogAnalytics()
    analytics.fetch_data()

    longest_avg_body_user = analytics.user_with_longest_average_body()
    if longest_avg_body_user:
        print(f"User with longest avg body: {longest_avg_body_user.name}")

    users_with_long_titles = analytics.users_with_many_long_titles()
    print("Users with >5 long titles:")
    for user in users_with_long_titles:
        print(f"- {user.name}")