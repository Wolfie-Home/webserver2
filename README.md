### install dependancies

``` shell
$ ./install.sh
```

### database
``` shell
$ cd tools  # user must run tools program in the directory.
$ python3 db_clean_tables.py
$ python3 db_create_default_data.py
$ python3 user_login_test.py
```

### Run
```
python3 runserver.py
```

### Run the server in background
```
chmod -x runserver.py
nohup ./runserver.py > log.txt &
```