#!/usr/bin/env python3

import subprocess
import platform


if __name__ == "__main__":
    # First login and get session code
    command = """\
        curl -v -H "Content-Type: application/json" \
            -X POST -d '{"username":"defaultUser","password":"dummypassword"}' \
            http://localhost:8000/api/login 2>&1 |grep -o -P 'session=[^;]*'\
        """
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    (msg, err) = p.communicate()
    session_code = msg.decode("utf-8").strip()
    print(session_code)  # This one prevents executing the next subprocess
                                # before the first subprocess is done

    # Then curl again with session code
    command = """\
        curl -v --cookie "%s" -H "Content-Type: application/json" -X GET http://localhost:8000/api/location
        """ % session_code

    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    (msg, err) = p.communicate()
    print(msg.decode("utf-8"))


# curl -v --cookie "" -H "Content-Type: application/json" -X GET http://localhost:8000/api/location