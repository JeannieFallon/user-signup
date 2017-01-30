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

html_head = """
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
"""

html_form = """
        <body>
        <h1>Sign-up</h1>
        <form>
            <table>
                <tbody>
                <tr>
                    <td>
                        <label>Username</label>
                    </td>
                    <td>
                        <input type=text name="username">
                    </td>
                <tr>
                    <td>
                        <label>Password</label>
                    </td>
                    <td>
                        <input type=password name="password">
                    </td>
                </tr>
                <tr>
                    <td>
                        <label>Verify Password</label>
                    </td>
                    <td>
                        <input type=password name="verify">
                    </td>
                </tr>
                <tr>
                    <td>
                        <label>Email (optional)</label>
                    </td>
                    <td>
                        <input type=email name="email">
                    </td>
                </tr>
                <tr>
                    <td>
                    <input type=submit name="submit">
                    </td>
                </tr>
                </tbody>

"""

html_foot = """
    </body>
</html>
"""


class MainHandler(webapp2.RequestHandler):
    def get(self):
        content = html_head + html_form + html_foot
        self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
