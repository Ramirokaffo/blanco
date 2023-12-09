from tkinter import Misc


class InputCheckService:

    def __init__(self, master: Misc):
        self.master = master
        self.check_digit = self.master.register(self.lettre_interdit)
        self.check_date = self.master.register(self.date_checker)
        self.check_password = self.master.register(self.password_checker)

    def lettre_interdit(self, quoi):
        try:
            int(quoi)
            return True
        except:
            if quoi == ".":
                return True
            else:
                self.master.bell()
                return False

    def password_checker(self, quoi, value):
        try:
            int(quoi)
            if len(value) > 5:
                self.master.bell()
                return False
            return True
        except:
            self.master.bell()
            return False

    def date_checker(self, quoi, value):
        if len(value) > 10:
            self.master.bell()
            return False
        if quoi in list(str(i) for i in range(10)) + ["/", "-"]:
            return True
        else:
            self.master.bell()
            return False
