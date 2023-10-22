from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build as build_service


def build(spreadsheet_id, service_account_info):
    """
    Arrange the objects and return a Sheety instance
    """
    spreadsheet = GoogleSheets(
        spreadsheet_id=spreadsheet_id,
        service_account_info=service_account_info,
    )

    return Sheety(spreadsheet)


class GoogleSheets:
    """
    Google Sheets API adapter
    """

    def __init__(self, spreadsheet_id, service_account_info):
        self.id = spreadsheet_id
        self.service = self._build_service(service_account_info)

    def _build_service(self, service_account_info):
        creds = Credentials.from_service_account_info(service_account_info)
        return build_service("sheets", "v4", credentials=creds)

    def append(self, range, data=[]) -> None:
        """
        Append data to a spreadsheet
        """
        self.service.spreadsheets().values().append(
            spreadsheetId=self.id,
            range=range,
            body={"values": [data]},
            valueInputOption="USER_ENTERED",
        ).execute()

    def get(self, range) -> list:
        """
        Get data from a spreadsheet
        """
        return (
            self.service.spreadsheets()
            .values()
            .get(
                spreadsheetId=self.id,
                range=range,
            )
            .execute()
        ).get("values", [])


class Sheety:
    def __init__(self, spreadsheet: GoogleSheets):
        self.spreadsheet = spreadsheet

    def model(self, id=None, name=None):
        """
        Return a model class that wraps user-defined class
        """

        def wrap(cls):
            cls._columns = list(cls.__annotations__.keys())

            cls.objects = Objects(
                cls=cls,
                name=name,
                spreadsheet=self.spreadsheet,
                columns=cls._columns,
            )

            def save(cls) -> None:
                self.spreadsheet.append(
                    range=name, data=list(cls.__dict__.values())
                )

            cls.save = save

            return cls

        return wrap


class Objects:
    def __init__(self, cls, name, spreadsheet, columns):
        self.cls = cls
        self.name = name
        self.spreadsheet = spreadsheet
        self.columns = columns

    def from_records(self, records):
        """
        Build and return a list of objects from records
        """
        result = []
        for record in records:
            d = dict(zip(self.columns, record))

            result.append(self.cls(**d))

        return result

    def _all(self):
        return self.spreadsheet.get(range=self.name)

    def _filter(self, **kwargs):
        result = self._all()

        results = []
        for key, value in kwargs.items():
            index = self.columns.index(key)

            result = [
                record for record in result if record[index] == str(value)
            ]
            results.extend(result)

        return results

    def all(self):
        return self.from_records(self._all())

    def filter(self, **kwargs):
        return self.from_records(self._filter(**kwargs))

    def get(self, **kwargs):
        return self.filter(**kwargs)[0]
