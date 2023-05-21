from unittest.mock import patch
import sheety


class FakeSpreadsheet:
    def __init__(self, *args, **kwargs):
        self.data = {}

    def build(self):
        pass

    def add(self, range, data=[]):
        self.data[range] = data


def test_save():
    with patch("sheety.Spreadsheet", FakeSpreadsheet):
        Base = sheety.connect(
            spreadsheet_id="test",
            service_account_info={
                "key": "value"
            },  # Replace with the correct test value
        )

        class Blog(Base):
            __sheet__ = "first"

            def __init__(self, title, author, content):
                self.title = title
                self.author = author
                self.content = content

        blog = Blog(title="hello", author="me", content="hello world")

        blog.save()

        assert sheety.Base.spreadsheet.data == {
            "first": [blog.title, blog.author, blog.content]
        }
