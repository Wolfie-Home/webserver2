#!/usr/bin/env python3

import subprocess

if __name__ == "__main__":
    """
    HOW THIS PROGRAM WORK:
    each `curl` call runs on different process. So unlike web browser, it is basically dose not
    share session between `curl` requests but there is a way around.
    When login, HTTP response will contain a Set-Cookie header like this:
        Set-Cookie:session=<encoded session>; Path=/; HttpOnly
    We need to send this cookie with new curl request, using --cookie argument.
    """
    # First login and get session code
    command = """\
        curl -v -H "Content-Type: application/json" \
            -X POST -d '{"username":"defaultUser","password":"dummypassword"}' \
            http://localhost:8000/api/login 2>&1 |grep -o -P 'session=[^;]*'\
        """
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    (msg, err) = p.communicate()
    session_cookie = msg.decode("utf-8").strip()  # This is the cookie.
    print(session_cookie)

    # Then curl again with session code
    command = """\
        curl -v --cookie "%s" -H "Content-Type: application/json" -X GET http://localhost:8000/api/device
        """ % session_cookie

    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    (msg, err) = p.communicate()
    print(msg.decode("utf-8"))
