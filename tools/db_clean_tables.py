#!/usr/bin/env python3

import subprocess

if __name__ == "__main__":
    command = "sqlite3 ../database/wolfie_home.db < ../database/db_schema.sql"
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    (msg, err) = p.communicate()
    print(msg)
