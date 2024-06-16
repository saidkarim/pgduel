import click
import logging

from lib.runner import Runner
from lib.utils import compose_dsn
from lib.settings_comparison import SettingsComparison
import sys

CONTEXT_SETTINGS = {
    "help_option_names": ["-h", "--help"],
}


logging.basicConfig(
    format="%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version="1.0.0")
def cli():
    """A CLI tool to help run pgduel."""


@cli.command()
@click.option("-1", "--database1", help="Database 1 connection string")
@click.option("-2", "--database2", help="Database 2 connection string")
@click.option("-H", "--host1", help="Database 1 hostname")
@click.option("-h", "--host2", help="Database 2 hostname")
@click.option("-P", "--port1", help="Database 1 port number")
@click.option("-p", "--port2", help="Database 2 port number")
@click.option("-D", "--dbname1", help="Database 1 dbname")
@click.option("-d", "--dbname2", help="Database 2 dbname")
@click.option("-U", "--user1", help="Database 1 username")
@click.option("-u", "--user2", help="Database 2 username")
@click.option("-W", "--password1", help="Database 1 password")
@click.option("-w", "--password2", help="Database 2 password")
@click.option("-c", "--command", help="Run single SQL command")
@click.option("-f", "--file", help="Execute commands from file")
def query(
    database1,
    database2,
    host1,
    host2,
    port1,
    port2,
    dbname1,
    dbname2,
    user1,
    user2,
    password1,
    password2,
    command,
    file,
):
    """Compares the performance of queries  between 2 databases."""
    dsn1 = compose_dsn(host1, port1, dbname1, user1, password1, database1)
    dsn2 = compose_dsn(host2, port2, dbname2, user2, password2, database2)
    command_to_execute = None
    if command is None and file is None:
        logger.error("command and file parameters both cannot be empty.")
        sys.exit(1)
    elif command:
        command_to_execute = command
    else:
        try:
            with open(file, "r") as f:
                command_from_file = f.read()
        except FileNotFoundError:
            logger.error("%s not found", file)
            sys.exit(1)
        except Exception as e:
            logger.error("An error occurred: %s", str(e))
            sys.exit(1)

        command_to_execute = command_from_file

    try:
        runner = Runner(dsn1, dsn2, command_to_execute)
        runner.start_all()
        runner.show_results()
    except Exception as e:
        logger.error("An error occurred during running queries:\n %s", str(e))
        sys.exit(1)


@cli.command()
@click.option("-1", "--database1", help="Database 1 connection string")
@click.option("-2", "--database2", help="Database 2 connection string")
@click.option("-H", "--host1", help="Database 1 hostname")
@click.option("-h", "--host2", help="Database 2 hostname")
@click.option("-P", "--port1", help="Database 1 port number")
@click.option("-p", "--port2", help="Database 2 port number")
@click.option("-D", "--dbname1", help="Database 1 dbname")
@click.option("-d", "--dbname2", help="Database 2 dbname")
@click.option("-U", "--user1", help="Database 1 username")
@click.option("-u", "--user2", help="Database 2 username")
@click.option("-W", "--password1", help="Database 1 password")
@click.option("-w", "--password2", help="Database 2 password")
def config(
    database1,
    database2,
    host1,
    host2,
    port1,
    port2,
    dbname1,
    dbname2,
    user1,
    user2,
    password1,
    password2,
):
    """Shows differences in configurations settings."""
    dsn1 = compose_dsn(host1, port1, dbname1, user1, password1, database1)
    dsn2 = compose_dsn(host2, port2, dbname2, user2, password2, database2)
    try:
        runner = Runner(dsn1, dsn2, "SHOW ALL", True)
        runner.start_all()
    except Exception as e:
        err_msg = (
            "A problem occurred when running queries to compare configuration settings"
        )
        logger.error(f"{err_msg}:\n %s", str(e))
        sys.exit(1)

    settings_diff = SettingsComparison(runner.results[0], runner.results[1])
    settings_diff.show_different_settings()


if __name__ == "__main__":
    """
    Sample run:
     pgduel query --host1 localhost --port1 5432 --dbname1 db1 \
     --user1 postgres --password1 pass1 --host2 localhost \
     --port2 5433 --dbname2 db2 --user2 postgres \
     --password2 pass2 --command "select * from foo;"
    """
    cli()
