from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
from google.oauth2.service_account import Credentials

load_dotenv(".env.local")


class Spreadsheet:
    def __init__(self, id, service_account_info):
        self.id = id
        self.service_account_info = service_account_info

    def build(self):
        creds = Credentials.from_service_account_info(
            self.service_account_info
        )
        self.service = build("sheets", "v4", credentials=creds)

    def add(self, range, data=[]) -> None:
        self.service.spreadsheets().values().append(
            spreadsheetId=self.id,
            range=range,
            body={"values": [data]},
            valueInputOption="USER_ENTERED",
        ).execute()


def connect(spreadsheet_id, service_account_info):
    """
    Instantiate a Base class with access to a Google Spreadsheet.
    """
    spreadsheet = Spreadsheet(
        id=spreadsheet_id, service_account_info=service_account_info
    )
    spreadsheet.build()

    return Base.add_spreadsheet(spreadsheet)


class Base:
    spreadsheet = None

    @classmethod
    def add_spreadsheet(cls, spreadsheet):
        cls.spreadsheet = spreadsheet

        return cls

    def save(self):
        if self.spreadsheet is None:
            raise ValueError(
                "Spreadsheet not found. Use `connect` to connect to a spreadsheet."
            )
        range = self.__sheet__
        data = [getattr(self, attr) for attr in self.__dict__]
        self.spreadsheet.add(range=range, data=data)


# Client code

sheet = connect(
    spreadsheet_id="1ROul8k3t7PvfsFKLhrveZH2xVq7vDdea4BLHU1ocHW8",
    service_account_info=eval(os.getenv("SERVICE_ACCOUNT_INFO")),
)


class Blog(Base):
    __sheet__ = "first"

    def __init__(self, title, author, content):
        self.title = title
        self.author = author
        self.content = content

    def __repr__(self):
        return f"Blog(title={self.title}, author={self.author}, content={self.content})"


blog = Blog(title="hello", author="world", content="hello here")


blog.save()
