### install dependancies

``` shell
# install mysql. Make sure you are installing MySQL 5.5 or higher.
# If you are installing it on Raspberry Pi, add the following in /etc/apt/sources.list
# deb http://archive.raspbian.org/raspbian/ stretch main
$ sudo apt-get install mysql-server-5.6

# install uwsgi
$ pip install uwsgi

# install mysqlclient
$ sudo apt-get install python-dev libmysqlclient-dev # Debian / Ubuntu
$ sudo apt-get install python3-dev # debian / Ubuntu
$ pip install mysqlclient

# install mysql.connector python. 
# See https://dev.mysql.com/doc/connector-python/en/connector-python-installation.html
# download mysql-connector here: http://dev.mysql.com/downloads/connector/python/
$ dpkg -i mysql-connector-python_2.1.3-1ubuntu15.04_all.deb


# install Django
$ pip install Django

```

### mysql settings
``` SQL
$ mysql -u root -p
> CREATE DATABASE wolfie_home;
> CREATE USER 'wolfie'@'localhost' IDENTIFIED BY 'dummypass';
> GRANT ALL PRIVILEGES ON wolfie_home.* TO 'wolfie'@'localhost';
```
Then create tables. [See here.](https://github.com/Wolfie-Home/Documents/blob/bumsik/Design%20Document/Design_Document.md#51-mysql)


### Before Running Django 
Any changes to static files need to run following, in order to make it visible to the webserver
```
python manage.py collectstatic
```

### Run locally
```
python manage.py runserver
```
### Run globally
Allows computers from different IPs to issue HTTP request.
```
python manage.py runserver 0.0.0.0:8000
```

