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
                        <span>%(error)s</span>
                    </td>
                <tr>
                    <td>
                        <label for="password">Password</label>
                    </td>
                    <td>
                        <input type=password name="password" value="%(password)s" required>
                        <span>%(error)s</span>
                    </td>
                </tr>
                <tr>
                    <td>
                        <label for="verify">Verify Password</label>
                    </td>
                    <td>
                        <input type=password name="verify" value="%(verify)s" required>
                        <span>%(error)s</span>
                    </td>
                </tr>
                <tr>
                    <td>
                        <label for="email">Email (optional)</label>
                    </td>
                    <td>
                        <input type=email name="email" value="%(email)s">
                        <span>%(error)s</span>
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
    return USER_RE.match(username)

USER_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return USER_RE.match(password)

USER_RE = re.compile(r"^.{3,20}$")
def valid_verify(verify):
    return USER_RE.match(verify)

USER_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return USER_RE.match(email)

def escape_html(s):
    return cgi.escape(s,quote = True)


class MainHandler(webapp2.RequestHandler):
    def write_form(self,error="",username="",password="",email="",verify=""):
        self.response.out.write(html_form % {"error":error,
                                        "username": escape_html(username),
                                        "password": escape_html(password),
                                        "verify": escape_html(verify),
                                        "email": escape_html(email)})

    def get(self):
        self.write_form()


    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        if password != verify:
            self.write_form()
        elif not valid_username:
            self.write_form()
        elif not valid_password:
            self.write_form()
        elif not valid_verify:
            self.write_form()
        elif not valid_email:
            self.write_form()
        else:
            self.redirect("/success")


class SuccessHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Success! Account created.")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/success', SuccessHandler)
], debug=True)
