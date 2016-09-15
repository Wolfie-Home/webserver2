### install dependancies

``` shell
# Update repo
$ sudo apt-get update

# install nginx
$ sudo apt-get install nginx

# install pip3
$ sudo apt-get install python3-pip

# install uwsgi, Flask
$ sudo pip3 install uwsgi
$ sudo pip3 install Flask

```

### database
``` shell
$ cd tools  # user must run tools program in the directory.
$ python3 db_clean_tables.py

```

### Run
```
python3 runserver.py
```
