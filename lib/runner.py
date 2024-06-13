# -*- coding: utf-8 -*-
import logging
from .database import DatabaseConnection
from .utils import Color
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
from psycopg2.extensions import parse_dsn
from prettytable import PrettyTable

logger = logging.getLogger(__name__)


class Runner:
    def __init__(
        self, dsn1: str, dsn2: str, query: str, need_result: bool = False
    ) -> None:
        self.dsn1 = dsn1
        self.dsn2 = dsn2
        self.query = query
        self.need_result = need_result

        if (
            parse_dsn(self.dsn1)["host"] == parse_dsn(self.dsn2)["host"]
            and parse_dsn(self.dsn1)["port"] == parse_dsn(self.dsn2)["port"]
            and parse_dsn(self.dsn1)["dbname"] == parse_dsn(self.dsn2)["dbname"]
        ):
            logger.warning("It looks like the databases are the same!")

        self.results = None

    def _start(self, dsn):
        db = DatabaseConnection(dsn=dsn)
        return db.execute_query(query=self.query, need_result=self.need_result)

    def start_all(self):
        with ThreadPoolExecutor() as executor:
            self.results = list(executor.map(self._start, [self.dsn1, self.dsn2]))

    def show_results(self):
        fast_db, slow_db = sorted(self.results)

        xtimes = round(slow_db.timing / fast_db.timing, 5)
        msg = (
            f"{Color.GREEN}{fast_db.dsn['dbname']} is {xtimes} times "
            f"faster than {slow_db.dsn['dbname']}{Color.RESET}"
        )
        logger.info(msg)

        table = PrettyTable()
        fast_db_dict, slow_db_dict = asdict(fast_db), asdict(slow_db)
        for db_dict in [fast_db_dict, slow_db_dict]:
            db_dict["dbname"] = db_dict["dsn"]["dbname"]
            db_dict["timing"] = round(db_dict["timing"], 5)
            del db_dict["dsn"]
            del db_dict["result"]

        table.field_names = fast_db_dict.keys()
        table.add_row(fast_db_dict.values())
        table.add_row(slow_db_dict.values())

        print(table)
