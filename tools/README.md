## Tools
- Contains useful tools for this project.
- `db_xxxx.py`: Database related program. run `python3 db_xxxx.py` to use.
  - `db_clean_tables.py`: Clean all data of the table in DB or create a new DB with empty tables.
  - `db_backup.py`: Backup `wolfie_home.db` located in `database`. `.sql.bak` file will be created.
  - `db_restore.py`: restore database from `wolfie_home.sql.bak`. Existing database will become `.old` file.
