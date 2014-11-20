def info():
    print('cgi-wsgi')


class CGIContext:
    def __init__(self):
        self.headers = {}
        self.body = []
        self.writingHeaders = True

    def appendBody(self, lineOrLinesOrNil):
        # print 'BODY: %s' % lineOrLinesOrNil
        self.body.append(lineOrLinesOrNil or '')

    def addHeader(self, line):
        key, value = line.split(': ', 1)
        # print 'HEAD: %s : %s' % (key,value)
        self.headers[key] = value

    def writeln(self, line=None):
        if not self.writingHeaders:
            self.appendBody(line)
        elif not line:
            # print 'SWITCH'
            self.writingHeaders = False
        else:
            self.addHeader(line)

class CGIApp:
    def __call__(self, environ, start_response):
        status = '200 OK'
        context = CGIContext()
        self.response(environ, context.writeln)
        # print context.headers
        start_response(status, context.headers.items())
        return context.body

    def response(self, environ, writeln):
        writeln('Content-type: text/plain')
        writeln()
        writeln("""You should really implement your own response.

e.g.

class %s(cgi_wsgi.CGIApp):

    def response(self, environ, writeln):
        writeln('Content-type: text/html')
        writeln()
        writeln('<!DOCTYPE html>')
        writeln('<p>Some response required</p>')

        """ % self.__class__.__name__
        )