## Purpose
- database related stuff.
- ease the need to Synchronize/exchange data and schema in our database.
- To separate Model/Service from Control/View pattern

`service`: contains lowest data access layer. SQL statements will only appear in this package.
`model`: Models in MVC pattern, on top of `service` layer.
`settings.py`: database settings. including current using database name.


`wolfie_home.db`: This is our database file.
