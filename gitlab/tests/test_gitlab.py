# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Mika Mäenpää <mika.j.maenpaa@tut.fi>,
#                    Tampere University of Technology
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function

try:
    import unittest
except ImportError:
    import unittest2 as unittest

from httmock import HTTMock  # noqa
from httmock import response  # noqa
from httmock import urlmatch  # noqa

from gitlab import *  # noqa


class TestGitLabRawMethods(unittest.TestCase):
    def setUp(self):
        self.gl = Gitlab("http://localhost", private_token="private_token",
                         email="testuser@test.com", password="testpassword",
                         ssl_verify=True)

    @urlmatch(scheme="http", netloc="localhost", path="/api/v3/known_path",
              method="get")
    def resp_get(self, url, request):
        headers = {'content-type': 'application/json'}
        content = 'response'.encode("utf-8")
        return response(200, content, headers, None, 5, request)

    def test_raw_get_unknown_path(self):

        @urlmatch(scheme="http", netloc="localhost",
                  path="/api/v3/unknown_path",
                  method="get")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json'}
            content = '{"message": "message"}'.encode("utf-8")
            return response(404, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            resp = self.gl._raw_get("/unknown_path")
            self.assertEqual(resp.status_code, 404)

    def test_raw_get_without_kwargs(self):
        with HTTMock(self.resp_get):
            resp = self.gl._raw_get("/known_path")
        self.assertEqual(resp.content, b'response')
        self.assertEqual(resp.status_code, 200)

    def test_raw_get_with_kwargs(self):
        with HTTMock(self.resp_get):
            resp = self.gl._raw_get("/known_path", sudo="testing")
        self.assertEqual(resp.content, b'response')
        self.assertEqual(resp.status_code, 200)

    def test_raw_post(self):

        @urlmatch(scheme="http", netloc="localhost", path="/api/v3/known_path",
                  method="post")
        def resp_post(url, request):
            headers = {'content-type': 'application/json'}
            content = 'response'.encode("utf-8")
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_post):
            resp = self.gl._raw_post("/known_path")
        self.assertEqual(resp.content, b'response')
        self.assertEqual(resp.status_code, 200)

    def test_raw_post_unknown_path(self):

        @urlmatch(scheme="http", netloc="localhost",
                  path="/api/v3/unknown_path",
                  method="post")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json'}
            content = '{"message": "message"}'.encode("utf-8")
            return response(404, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            resp = self.gl._raw_post("/unknown_path")
            self.assertEqual(resp.status_code, 404)

    def test_raw_put(self):

        @urlmatch(scheme="http", netloc="localhost", path="/api/v3/known_path",
                  method="put")
        def resp_put(url, request):
            headers = {'content-type': 'application/json'}
            content = 'response'.encode("utf-8")
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_put):
            resp = self.gl._raw_put("/known_path")
        self.assertEqual(resp.content, b'response')
        self.assertEqual(resp.status_code, 200)

    def test_raw_put_unknown_path(self):

        @urlmatch(scheme="http", netloc="localhost",
                  path="/api/v3/unknown_path",
                  method="put")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json'}
            content = '{"message": "message"}'.encode("utf-8")
            return response(404, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            resp = self.gl._raw_put("/unknown_path")
            self.assertEqual(resp.status_code, 404)

    def test_raw_delete(self):

        @urlmatch(scheme="http", netloc="localhost", path="/api/v3/known_path",
                  method="delete")
        def resp_delete(url, request):
            headers = {'content-type': 'application/json'}
            content = 'response'.encode("utf-8")
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_delete):
            resp = self.gl._raw_delete("/known_path")
        self.assertEqual(resp.content, b'response')
        self.assertEqual(resp.status_code, 200)

    def test_raw_delete_unknown_path(self):

        @urlmatch(scheme="http", netloc="localhost",
                  path="/api/v3/unknown_path",
                  method="delete")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json'}
            content = '{"message": "message"}'.encode("utf-8")
            return response(404, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            resp = self.gl._raw_delete("/unknown_path")
            self.assertEqual(resp.status_code, 404)


class TestGitLabMethods(unittest.TestCase):
    def setUp(self):
        self.gl = Gitlab("http://localhost", private_token="private_token",
                         email="testuser@test.com", password="testpassword",
                         ssl_verify=True)

    def test_list(self):
        @urlmatch(scheme="http", netloc="localhost",
                  path="/api/v3/projects/1/repository/branches", method="get")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json'}
            content = ('[{"branch_name": "testbranch", '
                       '"project_id": 1, "ref": "a"}]').encode("utf-8")
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            data = self.gl.list(ProjectBranch, project_id=1, page=1,
                                per_page=20)
            self.assertEqual(len(data), 1)
            data = data[0]
            self.assertEqual(data.branch_name, "testbranch")
            self.assertEqual(data.project_id, 1)
            self.assertEqual(data.ref, "a")

    def test_list_401(self):
        @urlmatch(scheme="http", netloc="localhost",
                  path="/api/v3/projects/1/repository/branches", method="get")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json'}
            content = '{"message":"message"}'.encode("utf-8")
            return response(401, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            self.assertRaises(GitlabAuthenticationError, self.gl.list,
                              ProjectBranch, project_id=1)

    def test_list_unknown_error(self):
        @urlmatch(scheme="http", netloc="localhost",
                  path="/api/v3/projects/1/repository/branches", method="get")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json'}
            content = '{"message":"message"}'.encode("utf-8")
            return response(405, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            self.assertRaises(GitlabListError, self.gl.list,
                              ProjectBranch, project_id=1)

    def test_list_kw_missing(self):
        self.assertRaises(GitlabListError, self.gl.list, ProjectBranch)

    def test_list_no_connection(self):
        self.assertRaises(GitlabConnectionError, self.gl.list, ProjectBranch,
                          project_id=1)

    def test_get(self):
        @urlmatch(scheme="http", netloc="localhost",
                  path="/api/v3/projects/1", method="get")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json'}
            content = '{"name": "testproject"}'.encode("utf-8")
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            data = self.gl.get(Project, id=1)
            expected = {"name": "testproject"}
            self.assertEqual(expected, data)

    def test_get_unknown_path(self):
        @urlmatch(scheme="http", netloc="localhost", path="/api/v3/groups/1",
                  method="get")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json'}
            content = '{"message": "message"}'.encode("utf-8")
            return response(404, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            self.assertRaises(GitlabGetError, self.gl.get, Group, 1)

    def test_get_missing_kw(self):
        self.assertRaises(GitlabGetError, self.gl.get, ProjectBranch)

    def test_get_401(self):
        @urlmatch(scheme="http", netloc="localhost", path="/api/v3/projects/1",
                  method="get")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json'}
            content = '{"message": "message"}'.encode("utf-8")
            return response(401, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            self.assertRaises(GitlabAuthenticationError, self.gl.get,
                              Project, 1)

    def test_get_404(self):
        @urlmatch(scheme="http", netloc="localhost", path="/api/v3/projects/1",
                  method="get")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json'}
            content = '{"message": "message"}'.encode("utf-8")
            return response(404, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            self.assertRaises(GitlabGetError, self.gl.get,
                              Project, 1)

    def test_get_unknown_error(self):
        @urlmatch(scheme="http", netloc="localhost", path="/api/v3/projects/1",
                  method="get")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json'}
            content = '{"message": "message"}'.encode("utf-8")
            return response(405, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            self.assertRaises(GitlabGetError, self.gl.get,
                              Project, 1)

    def test_delete(self):
        @urlmatch(scheme="http", netloc="localhost", path="/api/v3/groups/1",
                  method="delete")
        def resp_delete_group(url, request):
            headers = {'content-type': 'application/json'}
            content = ''.encode("utf-8")
            return response(200, content, headers, None, 5, request)

        obj = Group(self.gl, data={"name": "testname", "id": 1})
        with HTTMock(resp_delete_group):
            data = self.gl.delete(obj)
            self.assertIs(data, True)

    def test_delete_unknown_path(self):
        obj = Project(self.gl, data={"name": "testname", "id": 1})
        obj._created = True

        @urlmatch(scheme="http", netloc="localhost", path="/api/v3/projects/1",
                  method="delete")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json'}
            content = '{"message": "message"}'.encode("utf-8")
            return response(404, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            self.assertRaises(GitlabDeleteError, self.gl.delete, obj)

    def test_delete_401(self):
        obj = Project(self.gl, data={"name": "testname", "id": 1})

        @urlmatch(scheme="http", netloc="localhost", path="/api/v3/projects/1",
                  method="delete")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json'}
            content = '{"message": "message"}'.encode("utf-8")
            return response(401, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            self.assertRaises(GitlabAuthenticationError, self.gl.delete, obj)

    def test_delete_unknown_error(self):
        obj = Project(self.gl, data={"name": "testname", "id": 1})

        @urlmatch(scheme="http", netloc="localhost", path="/api/v3/projects/1",
                  method="delete")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json'}
            content = '{"message": "message"}'.encode("utf-8")
            return response(405, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            self.assertRaises(GitlabDeleteError, self.gl.delete, obj)

    def test_create(self):
        @urlmatch(scheme="http", netloc="localhost", path="/api/v3/projects",
                  method="post")
        def resp_create_project(url, request):
            headers = {'content-type': 'application/json'}
            content = '{"name": "testname", "id": 1}'.encode("utf-8")
            return response(201, content, headers, None, 5, request)

        obj = Project(self.gl, data={"name": "testname"})

        with HTTMock(resp_create_project):
            data = self.gl.create(obj)
            expected = {u"name": u"testname", u"id": 1}
            self.assertEqual(expected, data)

    def test_create_kw_missing(self):
        obj = Group(self.gl, data={"name": "testgroup"})
        self.assertRaises(GitlabCreateError, self.gl.create, obj)

    def test_create_unknown_path(self):
        obj = User(self.gl, data={"email": "email", "password": "password",
                                  "username": "username", "name": "name",
                                  "can_create_group": True})
        self.assertRaises(GitlabConnectionError, self.gl.create, obj)

    def test_create_401(self):
        obj = Group(self.gl, data={"name": "testgroup", "path": "testpath"})

        @urlmatch(scheme="http", netloc="localhost", path="/api/v3/groups",
                  method="post")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json'}
            content = '{"message": "message"}'.encode("utf-8")
            return response(401, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            self.assertRaises(GitlabAuthenticationError, self.gl.create, obj)

    def test_create_unknown_error(self):
        obj = Group(self.gl, data={"name": "testgroup", "path": "testpath"})

        @urlmatch(scheme="http", netloc="localhost", path="/api/v3/groups",
                  method="post")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json'}
            content = '{"message": "message"}'.encode("utf-8")
            return response(405, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            self.assertRaises(GitlabCreateError, self.gl.create, obj)

    def test_update(self):
        obj = User(self.gl, data={"email": "testuser@testmail.com",
                                  "password": "testpassword",
                                  "name": u"testuser",
                                  "username": "testusername",
                                  "can_create_group": True,
                                  "id": 1})

        @urlmatch(scheme="http", netloc="localhost", path="/api/v3/users/1",
                  method="put")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json'}
            content = '{"first": "return1"}'.encode("utf-8")
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            data = self.gl.update(obj)
            expected = {"first": "return1"}
            self.assertEqual(expected, data)

    def test_update_kw_missing(self):
        obj = Group(self.gl, data={"name": "testgroup"})
        self.assertRaises(GitlabUpdateError, self.gl.update, obj)

    def test_update_401(self):
        obj = Group(self.gl, data={"name": "testgroup", "path": "testpath",
                                   "id": 1})

        @urlmatch(scheme="http", netloc="localhost", path="/api/v3/groups/1",
                  method="put")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json'}
            content = '{"message": "message"}'.encode("utf-8")
            return response(401, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            self.assertRaises(GitlabAuthenticationError, self.gl.update, obj)

    def test_update_unknown_error(self):
        obj = Group(self.gl, data={"name": "testgroup", "path": "testpath",
                                   "id": 1})

        @urlmatch(scheme="http", netloc="localhost", path="/api/v3/groups/1",
                  method="put")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json'}
            content = '{"message": "message"}'.encode("utf-8")
            return response(405, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            self.assertRaises(GitlabUpdateError, self.gl.update, obj)

    def test_update_unknown_path(self):
        obj = Group(self.gl, data={"name": "testgroup", "path": "testpath",
                                   "id": 1})

        @urlmatch(scheme="http", netloc="localhost", path="/api/v3/groups/1",
                  method="put")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json'}
            content = '{"message": "message"}'.encode("utf-8")
            return response(404, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            self.assertRaises(GitlabUpdateError, self.gl.update, obj)


class TestGitLab(unittest.TestCase):

    def setUp(self):
        self.gl = Gitlab("http://localhost", private_token="private_token",
                         email="testuser@test.com", password="testpassword",
                         ssl_verify=True)

    def test_setUrl(self):
        self.gl.setUrl("http://new_url")
        self.assertEqual(self.gl._url, "http://new_url/api/v3")

    def test_set_token(self):
        token = "newtoken"
        expected = {"PRIVATE-TOKEN": token}
        self.gl.set_token(token)
        self.assertEqual(self.gl.private_token, token)
        self.assertDictContainsSubset(expected, self.gl.headers)

    def test_set_credentials(self):
        email = "credentialuser@test.com"
        password = "credentialpassword"
        self.gl.set_credentials(email=email, password=password)
        self.assertEqual(self.gl.email, email)
        self.assertEqual(self.gl.password, password)

    def test_credentials_auth_nopassword(self):
        self.gl.set_credentials(email=None, password=None)
        self.assertRaises(GitlabAuthenticationError, self.gl.credentials_auth)

    def test_credentials_auth_notok(self):
        @urlmatch(scheme="http", netloc="localhost", path="/api/v3/session",
                  method="post")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json'}
            content = '{"message": "message"}'.encode("utf-8")
            return response(404, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            self.assertRaises(GitlabAuthenticationError,
                              self.gl.credentials_auth)

    def test_auth_with_credentials(self):
        self.gl.set_token(None)
        self.test_credentials_auth(callback=self.gl.auth)

    def test_auth_with_token(self):
        self.test_token_auth(callback=self.gl.auth)

    def test_credentials_auth(self, callback=None):
        if callback is None:
            callback = self.gl.credentials_auth
        token = "credauthtoken"
        id_ = 1
        expected = {"PRIVATE-TOKEN": token}

        @urlmatch(scheme="http", netloc="localhost", path="/api/v3/session",
                  method="post")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json'}
            content = '{{"id": {0:d}, "private_token": "{1:s}"}}'.format(
                id_, token).encode("utf-8")
            return response(201, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            callback()
        self.assertEqual(self.gl.private_token, token)
        self.assertDictContainsSubset(expected, self.gl.headers)
        self.assertEqual(self.gl.user.id, id_)

    def test_token_auth(self, callback=None):
        if callback is None:
            callback = self.gl.token_auth
        name = "username"
        id_ = 1

        @urlmatch(scheme="http", netloc="localhost", path="/api/v3/user",
                  method="get")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json'}
            content = '{{"id": {0:d}, "username": "{1:s}"}}'.format(
                id_, name).encode("utf-8")
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            callback()
        self.assertEqual(self.gl.user.username, name)
        self.assertEqual(self.gl.user.id, id_)
        self.assertEqual(type(self.gl.user), CurrentUser)

    def test_getListOrObject_without_id(self):
        @urlmatch(scheme="http", netloc="localhost", path="/api/v3/projects",
                  method="get")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json'}
            content = '[{"name": "testproject", "id": 1}]'.encode("utf-8")
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            projs = Project._getListOrObject(self.gl, None)
            self.assertEqual(len(projs), 1)
            proj = projs[0]
            self.assertEqual(proj.id, 1)
            self.assertEqual(proj.name, "testproject")

    def test_getListOrObject_with_id(self):
        @urlmatch(scheme="http", netloc="localhost", path="/api/v3/projects/1",
                  method="get")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json'}
            content = '{"name": "testproject", "id": 1}'.encode("utf-8")
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            proj = Project._getListOrObject(self.gl, 1)
            self.assertEqual(proj.id, 1)
            self.assertEqual(proj.name, "testproject")

    def test_Hook(self):
        @urlmatch(scheme="http", netloc="localhost", path="/api/v3/hooks/1",
                  method="get")
        def resp_get_hook(url, request):
            headers = {'content-type': 'application/json'}
            content = '{"url": "testurl", "id": 1}'.encode("utf-8")
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_get_hook):
            data = self.gl.Hook(id=1)
            self.assertEqual(type(data), Hook)
            self.assertEqual(data.url, "testurl")
            self.assertEqual(data.id, 1)

    def test_Project(self):
        @urlmatch(scheme="http", netloc="localhost", path="/api/v3/projects/1",
                  method="get")
        def resp_get_project(url, request):
            headers = {'content-type': 'application/json'}
            content = '{"name": "name", "id": 1}'.encode("utf-8")
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_get_project):
            data = self.gl.Project(id=1)
            self.assertEqual(type(data), Project)
            self.assertEqual(data.name, "name")
            self.assertEqual(data.id, 1)

    def test_UserProject(self):
        @urlmatch(scheme="http", netloc="localhost",
                  path="/api/v3/projects/user/2", method="get")
        def resp_get_userproject(url, request):
            headers = {'content-type': 'application/json'}
            content = '{"name": "name", "id": 1, "user_id": 2}'.encode("utf-8")
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_get_userproject):
            self.assertRaises(NotImplementedError, self.gl.UserProject, id=1,
                              user_id=2)

    def test_Group(self):
        @urlmatch(scheme="http", netloc="localhost", path="/api/v3/groups/1",
                  method="get")
        def resp_get_group(url, request):
            headers = {'content-type': 'application/json'}
            content = '{"name": "name", "id": 1, "path": "path"}'
            content = content.encode('utf-8')
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_get_group):
            data = self.gl.Group(id=1)
            self.assertEqual(type(data), Group)
            self.assertEqual(data.name, "name")
            self.assertEqual(data.path, "path")
            self.assertEqual(data.id, 1)

    def test_Issue(self):
        @urlmatch(scheme="http", netloc="localhost", path="/api/v3/issues/1",
                  method="get")
        def resp_get_issue(url, request):
            headers = {'content-type': 'application/json'}
            content = '{"name": "name", "id": 1}'.encode("utf-8")
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_get_issue):
            self.assertRaises(NotImplementedError, self.gl.Issue, id=1)

    def test_User(self):
        @urlmatch(scheme="http", netloc="localhost", path="/api/v3/users/1",
                  method="get")
        def resp_get_user(url, request):
            headers = {'content-type': 'application/json'}
            content = ('{"name": "name", "id": 1, "password": "password", '
                       '"username": "username", "email": "email"}')
            content = content.encode("utf-8")
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_get_user):
            user = self.gl.User(id=1)
            self.assertEqual(type(user), User)
            self.assertEqual(user.name, "name")
            self.assertEqual(user.id, 1)
