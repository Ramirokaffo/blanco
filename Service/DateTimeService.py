

class DateTimeService:

    @staticmethod
    def format_date_time(dte):
        """Mettre la date sous une forme lisible par l'utilisateur"""
        dte = str(dte)
        if len(dte) == 10:
            return DateTimeService.change_date_format(dte)
        elif len(dte) > 10:
            return DateTimeService.change_date_format(dte) + " à " + dte[11:16]
        else:
            return None

    @staticmethod
    def change_date_format(date_str):
        date_str = date_str[:10]
        if "-" in date_str:
            spli = date_str.split("-")
            spli.reverse()
        elif "/" in date_str:
            spli = date_str.split("/")
            spli.reverse()
        else:
            return None
        return "-".join(spli)

    @staticmethod
    def parse_date(str_date: str):
        str_date = str_date.replace("/", "-")
        if not str_date:
            return None
        elif len(str_date) == 4:
            return str_date + "-12-31"
        elif len(str_date) == 7:
            return "-".join(reversed(str_date.split("-"))) + "-28"
        else:
            return str_date


