# -*- coding: utf-8 -*-
""" All about database connection. """

from psycopg2.extensions import parse_dsn
from dataclasses import dataclass, field
import psycopg2
import time
import logging

from .utils import compose_dsn

logger = logging.getLogger()


class DatabaseConnectionError(Exception):
    """An error occurred while connecting to a database"""


class DatabaseQueryExecutionError(Exception):
    """An error occurred while executing a query"""


@dataclass(frozen=True, order=True)
class QueryMetric:
    """Stores info about query metrics"""

    timing: float
    dsn: dict = field(default_factory=dict, compare=False)
    result: list[tuple] = field(default_factory=list, compare=False)


class DatabaseConnection:
    """A class to handle connections to PostgreSQL database."""

    def __init__(
        self,
        host=None,
        port=None,
        db_name=None,
        db_user=None,
        db_password=None,
        dsn=None,
    ):
        self.host = host
        self.port = port
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name
        self.dsn = dsn
        if self.dsn is None:
            self.dsn = compose_dsn(
                self.host, self.port, self.db_name, self.db_user, self.db_password
            )
        self.parsed_dsn = parse_dsn(self.dsn)

    def execute_query(self, query: str, need_result: bool = False) -> QueryMetric:
        """Execute a query"""

        conn = None
        result = None
        start = time.time()

        try:
            conn = psycopg2.connect(self.dsn)
        except Exception as e:
            if conn is not None:
                conn.close()
            raise DatabaseConnectionError(
                f"Database connection error on {self.dsn}"
            ) from e

        conn.autocommit = True

        try:
            with conn.cursor() as curs:
                curs.execute(query)

                if need_result:
                    result = curs.fetchall()

            end = time.time()
            logger.info(f"Query running on {self.parsed_dsn['dbname']} completed.")
        except Exception as exc:
            raise DatabaseQueryExecutionError(
                f"Query execution error on {self.dsn} \n{str(exc)}"
            )
        finally:
            if conn is not None:
                conn.close()

        if result is not None:
            return QueryMetric(timing=(end - start), dsn=self.parsed_dsn, result=result)
        return QueryMetric(timing=(end - start), dsn=self.parsed_dsn)
