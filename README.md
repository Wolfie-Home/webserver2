### Run locally
```
python manage.py runserver
```
### Run globally
Allows computers from different IPs to issue HTTP request.
```
./run
```


### install dependancies

``` shell
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
