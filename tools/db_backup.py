#!/usr/bin/env python3

import subprocess

if __name__ == "__main__":
    command = "sqlite3 ../database/wolfie_home.db .dump > ../database/wolfie_home.sql.bak"
    subprocess.Popen(command, shell=True)
