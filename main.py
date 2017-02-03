#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re

html_form = """
<!DOCTYPE html>
    <html>
        <head>
            <title>User Sign-up</title>
            <style>
                body {
                    background-color:#ebedef;
                }
                .error {
                    color:#e74c3c;
                }
            </style>
        </head>
        <body>
        <h1>Sign-up</h1>
        <form method="post">
            <table>
                <tbody>
                <tr>
                    <td>
                        <label for="username">Username</label>
                    </td>
                    <td>
                        <input type=text name="username" value="%(username)s" required>
                        <span class="error">%(error_name)s</span>
                    </td>
                <tr>
                    <td>
                        <label for="password">Password</label>
                    </td>
                    <td>
                        <input type=password name="password" value="%(password)s" required>
                        <span class="error">%(error_pass)s</span>
                    </td>
                </tr>
                <tr>
                    <td>
                        <label for="verify">Verify password</label>
                    </td>
                    <td>
                        <input type=password name="verify" value="%(verify)s" required>
                        <span class="error">%(error_ver)s</span>
                    </td>
                </tr>
                <tr>
                    <td>
                        <label for="email">Email (optional)</label>
                    </td>
                    <td>
                        <input type=email name="email" value="%(email)s">
                        <span class="error">%(error_email)s</span>
                    </td>
                </tr>
                <tr>
                    <td>
                    <input type=submit name="submit">
                    </td>
                </tr>
                </tbody>
            </table>
        </form>
    </body>
</html>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return not email or EMAIL_RE.match(email)

def escape_html(s):
    return cgi.escape(s,quote = True)


class MainHandler(webapp2.RequestHandler):
    def write_form(self,username="",password="",verify="",email="",
                    error_name="",error_pass="",error_ver="",error_email=""):
        self.response.out.write(html_form % {"username": escape_html(username),
                                        "password": escape_html(password),
                                        "verify": escape_html(verify),
                                        "email": escape_html(email),
                                        "error_name": error_name,
                                        "error_pass": error_pass,
                                        "error_ver": error_ver,
                                        "error_email": error_email})

    def get(self):
        self.write_form()

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        error_name = ""
        error_pass = ""
        error_ver = ""
        error_email = ""


        if not valid_username(username):
            have_error = True
            error_name = "Please enter a valid username."

        if not valid_password(password):
            have_error = True
            password = ""
            verify = ""
            error_pass = "Please enter a valid password."

        if password != verify:
            have_error = True
            password = ""
            verify = ""
            error_ver = "Passwords do not match."

        if not valid_email(email):
            have_error = True
            error_email = "Please enter a valid email."

        if have_error == True:
            self.write_form(username,password,verify,email,error_name,error_pass,error_ver,error_email)
        else:
            self.redirect("/success?username=" + username)

class SuccessHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        self.response.out.write("<h1>Success, %s! Account created.</h1>" % username)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/success', SuccessHandler)
], debug=True)
