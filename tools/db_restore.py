#!/usr/bin/env python3

import subprocess
import platform

is_windows = platform.platform()[0:7].upper() == "WINDOWS"


if __name__ == "__main__":
    # first change the old file name
    if is_windows:
        command = "move ../database/wolfie_home.db ../database/wolfie_home.db.old"
    else:
        command = "mv ../database/wolfie_home.db ../database/wolfie_home.db.old"
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    (msg, err) = p.communicate()
    print(msg.decode("utf-8"))  # This one prevents executing the next subprocess
                                # before the first subprocess is done

    # Then apply
    command = "sqlite3 ../database/wolfie_home.db < ../database/wolfie_home.sql.bak"
    subprocess.Popen(command, shell=True)
