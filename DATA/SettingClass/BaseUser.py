from datetime import datetime


class BaseUser:
    def __init__(self, id: int = None, firstname: str = None, lastname: str = None,
                 phone_number: str = None, create_at: datetime = None, delete_at: datetime = None,
                 email: str = None):
        self.id = id
        self.firstname = firstname
        self.create_at = create_at
        self.delete_at = delete_at
        self.lastname = lastname
        self.phone_number = phone_number
        self.email = email

    def get_all_name(self):
        return " ".join([self.lastname if self.lastname else "", self.firstname if self.firstname else self.firstname])
