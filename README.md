# cgi_wsgi python module

## Background

For teaching HTTP, it's good to have a simply way of outputting HTTP responses the way that old-school CGI works:

- write out the headers (delimited with newlines)
- a blank line (two newline characters)
- your response body (starting perhaps with "<!DOCTYPE html>")

However many easy to use python services (e.g. the wonderful http://pythonanywhere.com) only have a WSGI interface 
(sensibly, because why would you want to use old school CGI when there's WSGI around).

However CGI is simpler for teaching purposes and helps you understand what's actually being transmitted over the wire.

So this is an adapter...

## Installation

```pip install cgi_wsgi```

## Usage

    import cgi_wsgi 
    
    class App(cgi_wsgi.CGIApp):
        def response(self, environ, writeln):
            writeln('Content-Type: text/html; charset=utf8')
            writeln()
            writeln("<!DOCTYPE html>")
            writeln("<p>some text</p>")


Alternative:

    import cgi_wsgi 
    
    class App(cgi_wsgi.CGIApp):
        def response(self, environ, writeln):
            writeln(
    """Content-Type: text/html; charset=utf8
    
    <!DOCTYPE html>
    <p>some text</p>
    """)

