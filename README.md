# PgDuel

A lightweight tool to compare the performances of 2 PostgreSQL databases.

### Prerequisites
- Python min. 3.9 and pip3
- Install additional packages, with:
  `pip install -r requirements.txt`



## Sub-commands
There are two sub-commands: `query` and `config`. Use `query` to run a query on both databases and compare performances
and `config` is used to check any configuration differences between two databases.

## Command Line Options

### Connection parameters

| Parameter           | Comment                                                                                      |
|:--------------------|:---------------------------------------------------------------------------------------------|
| `-1`\|`--database1` | The full DSN of the first database. DSN layout: `postgresql://<user>@<host>:<port>/<dbname>` |
| `-H`\|`--host1`     | The hostname of the first database.                                                          |
| `-P`\|`--port1`     | The port number of the first database.                                                       |
| `-D`\|`--dbname1`   | The first database name.                                                                     |
| `-U`\|`--user1`     | The user name of the first database.                                                         |
| `-W`\|`--password1` | The password for the first database.                                                         |
|                     |                                                                                              |
| `-2`\|`--database2` | The full DSN of the second database.                                                         |
| `-h`\|`--host2`     | The hostname of the second database.                                                         |
| `-p`\|`--port2`     | The port number of the second database.                                                      |
| `-d`\|`--dbname2`   | The second database name.                                                                    |
| `-u`\|`--user2`     | The user name of the second database.                                                        |
| `-w`\|`--password2` | The password for the second database.                                                        |

### `query` parameters

| Parameter         | Comment                                |
|:------------------|:---------------------------------------|
| `-c`\|`--command` | Run single SQL command.                |
| `-f`\|`--file`    | Execute SQL from file.                 |

### `config` parameters

`config` command doesn't have any parameters (only connection parameters).

### Examples

```bash
pgduel query --host1 localhost --port1 5432 --dbname1 mydb1 \
     --user1 postgres --password1 a1234 --host2 localhost \
     --port2 5432 --dbname2 mydb2 --user2 postgres \
     --password2 b1234 --command "select * from foo;"
```

With DSN:
```bash
python pgduel.py query --database1 postgresql://postgres:a1234@localhost:5432/mydb1 \
--database2 postgresql://postgres:b1234@localhost:5432/mydb2 \
-c "select * from foo;"
```

Check config differences:
```bash
python pgduel.py config --database1 postgresql://postgres:a1234@localhost:5432/mydb1 \
--database2 postgresql://postgres:b1234@localhost:5432/mydb2
```