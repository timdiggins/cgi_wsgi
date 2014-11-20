from unittest import TestCase

import cgi_wsgi
from webtest import TestApp

class BaseTestCase(TestCase):

    def get_response(self, app_class=None):
        if not app_class:
            app_class = self.AppUnderTest
        app = TestApp(app_class())
        resp = app.get('/')
        return resp


class TestWsgiBasics(BaseTestCase):

    class AppUnderTest:
        def __call__(self, environ, start_response):
            body = 'some body'
            headers = [('Content-Type', 'text/html; charset=utf8'),
                       ('Content-Length', str(len(body)))]
            start_response('200 OK', headers)

            return [body]

    def test_status_code(self):
        self.assertTrue((self.get_response()).status == '200 OK')
        self.assertTrue((self.get_response()).status_int == 200)

    def test_content_type(self):
        self.assertTrue((self.get_response()).content_type == 'text/html')

    def test_other_headers(self):
        self.assertTrue((self.get_response()).content_length > 0)

    def test_body(self):
        self.get_response().mustcontain('body')
        self.assertTrue('some' in self.get_response())
        self.assertTrue((self.get_response()).body == 'some body')


class TestUnderformedApp(BaseTestCase):

    class AppUnderTest(cgi_wsgi.CGIApp):
        pass

    def test_status_code(self):
        self.assertTrue((self.get_response()).status == '200 OK')
        self.assertTrue((self.get_response()).status_int == 200)

    def test_content_type(self):
        self.assertTrue((self.get_response()).content_type == 'text/plain')

    def test_body(self):
        print(self.get_response().body)
        self.assertTrue('def response' in self.get_response())
        self.assertTrue('should' in self.get_response())
        self.assertTrue('implement' in self.get_response())

class TestWellFormedApp(BaseTestCase):

    class AppUnderTest(cgi_wsgi.CGIApp):
        def response(self, environ, write):
            body = "some body"
            write('Content-Type: text/html; charset=utf8')
            write('Content-Length: %s' % len(body))
            write()
            write(body)

    def test_status_code_default(self):
        self.assertTrue((self.get_response()).status == '200 OK')
        self.assertTrue((self.get_response()).status_int == 200)

    def test_content_type(self):
        self.assertTrue(self.get_response().content_type == 'text/html')

    def test_headers(self):
        self.assertTrue(self.get_response().content_length > 0)

    def test_body(self):
        print("body:%s" % self.get_response().body)
        self.assertTrue('body' in self.get_response())
        self.assertTrue('some' in self.get_response())
        self.assertTrue(self.get_response().body == 'some body')

class TestMultiStringApp(BaseTestCase):

    class AppUnderTest(cgi_wsgi.CGIApp):
        def response(self, environ, writeln):
            writeln(
"""Content-Type: text/html; charset=utf8

some body""")

    def test_status_code_default(self):
        self.assertTrue((self.get_response()).status == '200 OK')
        self.assertTrue((self.get_response()).status_int == 200)

    def test_content_type(self):
        self.assertTrue(self.get_response().content_type == 'text/html')

    def test_headers(self):
        self.assertTrue(self.get_response().content_length > 0)

    def test_body(self):
        print("body:%s" % self.get_response().body)
        self.assertTrue('body' in self.get_response())
        self.assertTrue('some' in self.get_response())
        self.assertTrue(self.get_response().body == 'some body')
