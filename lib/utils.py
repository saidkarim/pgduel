# -*- coding: utf-8 -*-


class Color:
    RESET = "\033[0m"
    GREEN = "\033[92m"


def compose_dsn(
    host='', port='', db_name='', db_user='', db_password=None, dsn=None
) -> str:
    if dsn:
        return dsn
    return f"postgresql://{db_user}{':' + db_password if db_password else ''}@{host}:{port}/{db_name}"
