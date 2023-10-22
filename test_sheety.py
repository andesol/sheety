from dataclasses import dataclass

import sheety.sheety as sheety


@dataclass
class FakeGoogleSpreadsheet:
    data: dict

    def append(self, range, data=[]) -> None:
        self.data[range].append(data)

    def get(self, range):
        return self.data[range]


def test_save():
    fakeGoogle = FakeGoogleSpreadsheet({"first": []})
    s = sheety.Sheety(fakeGoogle)

    @s.model(name="first")
    class Blog:
        def __init__(self, title, author, content):
            self.title = title
            self.author = author
            self.content = content

    blog = Blog(title="hello", author="me", content="hello world")

    blog.save()

    assert fakeGoogle.data["first"] == [
        ["hello", "me", "hello world"],
    ]


def test_get_all():
    fakeGoogle = FakeGoogleSpreadsheet(
        {
            "first": [
                ["hello", "me", "hello world"],
                ["hello2", "me2", "hello world2"],
            ]
        }
    )
    s = sheety.Sheety(fakeGoogle)

    @s.model(name="first")
    class Blog:
        title: str
        author: str
        content: str

        def __init__(self, title, author, content):
            self.title = title
            self.author = author
            self.content = content

    blogs = Blog.objects.all()

    assert len(blogs) == 2
    assert blogs[0].title == "hello"
    assert blogs[0].author == "me"
    assert blogs[0].content == "hello world"
    assert blogs[1].title == "hello2"
    assert blogs[1].author == "me2"
    assert blogs[1].content == "hello world2"


def test_get_one():
    fakeGoogle = FakeGoogleSpreadsheet(
        {
            "first": [
                ["hello", "me", "hello world"],
                ["hello2", "me2", "hello world2"],
            ]
        }
    )
    s = sheety.Sheety(fakeGoogle)

    @s.model(name="first")
    class Blog:
        title: str
        author: str
        content: str

        def __init__(self, title, author, content):
            self.title = title
            self.author = author
            self.content = content

    blog = Blog.objects.get(title="hello2")

    assert blog.title == "hello2"
    assert blog.author == "me2"
    assert blog.content == "hello world2"
