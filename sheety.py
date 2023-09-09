from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build as build_service

load_dotenv(".env.local")


def build(spreadsheet_id, service_account_info):
    """
    Instantiate a Base class with access to a Google Spreadsheet.
    """
    breakpoint()
    creds = Credentials.from_service_account_info(service_account_info)
    service = build_service("sheets", "v4", credentials=creds)

    google_sheet = GoogleSpreadsheet(id=spreadsheet_id, service=service)

    return Spreadsheet(google_sheet)


class GoogleSpreadsheet:
    def __init__(self, id, service):
        self.id = id
        self.service = service

    def build(self):
        pass

    def add(self, range, data=[]) -> None:
        self.service.spreadsheets().values().append(
            spreadsheetId=self.id,
            range=range,
            body={"values": [data]},
            valueInputOption="USER_ENTERED",
        ).execute()


class Spreadsheet:
    def __init__(self, spreadsheet: GoogleSpreadsheet):
        self.spreadsheet = spreadsheet

    def model(self, id=None, name=None):
        def wraps(cls):
            class Wrapped(cls):
                def __init__(cls, *args, **kwargs):
                    super().__init__(*args, **kwargs)

                def save(cls) -> None:
                    self.spreadsheet.add(
                        range=name, data=list(cls.__dict__.values())
                    )

                @property
                def objects(cls):
                    class Objects:
                        def all(self):
                            ...

                    return Objects()

            return Wrapped

        return wraps
