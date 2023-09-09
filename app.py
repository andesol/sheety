import os

import sheety

# Client code

s = sheety.build(
    spreadsheet_id="1ROul8k3t7PvfsFKLhrveZH2xVq7vDdea4BLHU1ocHW8",
    service_account_info=eval(os.getenv("SERVICE_ACCOUNT_INFO")),
)


@s.model(name="first")
class Blog:
    def __init__(self, id, name, title):
        self.id = id
        self.name = name
        self.title = title


a = Blog(id=1, name="My Blog", title="Hello, World!")

a.save()
