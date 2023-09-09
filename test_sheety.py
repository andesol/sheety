from dataclasses import dataclass

import sheety


@dataclass
class FakeGoogleSpreadsheet:
    data: dict

    def add(self, range, data=[]):
        self.data[range].append(data)


def test_save():
    fakeGoogle = FakeGoogleSpreadsheet({"first": []})
    s = sheety.Spreadsheet(fakeGoogle)

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
