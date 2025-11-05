#
# Copyright (C) 2025 pdnguyen of HCMC University of Technology VNU-HCM.
# All rights reserved.
# This file is part of the CO3093/CO3094 course,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
#
# WeApRous release
#
# The authors hereby grant to Licensee personal permission to use
# and modify the Licensed Source Code for the sole purpose of studying
# while attending the course
#


"""
start_sampleapp
~~~~~~~~~~~~~~~~~

This module provides a sample RESTful web application using the WeApRous framework.

It defines basic route handlers and launches a TCP-based backend server to serve
HTTP requests. The application includes a login endpoint and a greeting endpoint,
and can be configured via command-line arguments.
"""
import os
import json
import socket
import argparse

from daemon.weaprous import WeApRous
WWW_DIR = os.path.join(os.path.dirname(__file__), "www")

PORT = 8000  # Default port

app = WeApRous()

@app.route('/login', methods=['POST'])
def login(headers="guest", body="anonymous"):
    """
    Handle user login via POST request.

    This route simulates a login process and prints the provided headers and body
    to the console.

    :param headers (str): The request headers or user identifier.
    :param body (str): The request body or login payload.
    """
    print( "[SampleApp] Logging in {} to {}".format(headers, body))

@app.route('/hello', methods=['PUT'])
def hello(headers, body):
    """
    Handle greeting via PUT request.

    This route prints a greeting message to the console using the provided headers
    and body.

    :param headers (str): The request headers or user identifier.
    :param body (str): The request body or message payload.
    """
    print ("[SampleApp] ['PUT'] Hello in {} to {}".format(headers, body))

@app.route('/submit-info', methods=['GET'])
def submit_info_form(headers="guest", body=""):
    try:
        file_path = os.path.join(WWW_DIR, "submit-info.html")
        with open(file_path, "r", encoding="utf-8") as fh:
            content = fh.read()
        return 200, "text/html", content
    except Exception as e:
        return 500, "text/html", f"<h1>500 Internal Server Error</h1><p>{e}</p>"

# ----------------------
# POST /submit-info - xử lý đăng ký
# ----------------------
@app.route('/submit-info', methods=['POST'])
def submit_info_post(headers="guest", body=""):
    # Parse form data
    import urllib.parse
    form = urllib.parse.parse_qs(body)
    username = form.get("username", [""])[0]
    password = form.get("password", [""])[0]

    if not username or not password:
        return 400, "text/html", "<h1>400 Bad Request</h1><p>Missing username or password.</p>"

    # Tạo folder www nếu chưa tồn tại
    os.makedirs(WWW_DIR, exist_ok=True)
    users_file = os.path.join(WWW_DIR, "users.json")

    # Đọc users hiện tại
    users = {}
    try:
        if os.path.exists(users_file):
            with open(users_file, "r", encoding="utf-8") as f:
                users = json.load(f)
    except Exception as e:
        print(f"[SampleApp] Warning: cannot read users.json: {e}")
        users = {}

    # Kiểm tra trùng username
    if username in users:
        return 409, "text/html", f"<h1>409 Conflict</h1><p>Username '{username}' already exists.</p>"

    # Lưu tài khoản mới
    users[username] = password
    try:
        with open(users_file, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
    except Exception as e:
        return 500, "text/html", f"<h1>500 Internal Server Error</h1><p>Cannot save user: {e}</p>"

    # Trả phản hồi thành công
    return 200, "text/html", f"<h1>Registration Successful</h1><p>Welcome, {username}!</p>"

if __name__ == "__main__":
    # Parse command-line arguments to configure server IP and port
    parser = argparse.ArgumentParser(prog='Backend', description='', epilog='Beckend daemon')
    parser.add_argument('--server-ip', default='0.0.0.0')
    parser.add_argument('--server-port', type=int, default=PORT)
 
    args = parser.parse_args()
    ip = args.server_ip
    port = args.server_port

    # Prepare and launch the RESTful application
    app.prepare_address(ip, port)
    app.run()