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

### mysql settings
``` SQL
$ mysql -u root -p
> CREATE DATABASE wolfie_home;
> CREATE USER 'wolfie'@'localhost' IDENTIFIED BY 'dummypass';
> GRANT ALL PRIVILEGES ON wolfie_home.* TO 'wolfie'@'localhost';
```
Then create tables. [See here.](https://github.com/Wolfie-Home/Documents/blob/bumsik/Design%20Document/Design_Document.md#51-mysql)

### Run
```
python3 runserver.py
```
