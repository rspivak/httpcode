###############################################################################
#
# Copyright (c) 2011 Ruslan Spivak
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################

__author__ = 'Ruslan Spivak <ruslan.spivak@gmail.com>'

import sys
import optparse
import textwrap
import re

# Codes with messages are taken verbatim from BaseHTTPServer.py

# Table mapping response codes to messages; entries have the
# form {code: (shortmessage, longmessage)}.
# See RFC 2616.
STATUS_CODES = {
    100: ('Continue', 'Request received, please continue'),
    101: ('Switching Protocols',
          'Switching to new protocol; obey Upgrade header'),

    200: ('OK', 'Request fulfilled, document follows'),
    201: ('Created', 'Document created, URL follows'),
    202: ('Accepted',
          'Request accepted, processing continues off-line'),
    203: ('Non-Authoritative Information', 'Request fulfilled from cache'),
    204: ('No Content', 'Request fulfilled, nothing follows'),
    205: ('Reset Content', 'Clear input form for further input.'),
    206: ('Partial Content', 'Partial content follows.'),

    300: ('Multiple Choices',
          'Object has several resources -- see URI list'),
    301: ('Moved Permanently', 'Object moved permanently -- see URI list'),
    302: ('Found', 'Object moved temporarily -- see URI list'),
    303: ('See Other', 'Object moved -- see Method and URL list'),
    304: ('Not Modified',
          'Document has not changed since given time'),
    305: ('Use Proxy',
          'You must use proxy specified in Location to access this '
          'resource.'),
    307: ('Temporary Redirect',
          'Object moved temporarily -- see URI list'),

    400: ('Bad Request',
          'Bad request syntax or unsupported method'),
    401: ('Unauthorized',
          'No permission -- see authorization schemes'),
    402: ('Payment Required',
          'No payment -- see charging schemes'),
    403: ('Forbidden',
          'Request forbidden -- authorization will not help'),
    404: ('Not Found', 'Nothing matches the given URI'),
    405: ('Method Not Allowed',
          'Specified method is invalid for this resource.'),
    406: ('Not Acceptable', 'URI not available in preferred format.'),
    407: ('Proxy Authentication Required', 'You must authenticate with '
          'this proxy before proceeding.'),
    408: ('Request Timeout', 'Request timed out; try again later.'),
    409: ('Conflict', 'Request conflict.'),
    410: ('Gone',
          'URI no longer exists and has been permanently removed.'),
    411: ('Length Required', 'Client must specify Content-Length.'),
    412: ('Precondition Failed', 'Precondition in headers is false.'),
    413: ('Request Entity Too Large', 'Entity is too large.'),
    414: ('Request-URI Too Long', 'URI is too long.'),
    415: ('Unsupported Media Type', 'Entity body in unsupported format.'),
    416: ('Requested Range Not Satisfiable',
          'Cannot satisfy request range.'),
    417: ('Expectation Failed',
          'Expect condition could not be satisfied.'),
    418: ("I'm a teapot", 'The HTCPCP server is a teapot'),

    500: ('Internal Server Error', 'Server got itself in trouble'),
    501: ('Not Implemented',
          'Server does not support this operation'),
    502: ('Bad Gateway', 'Invalid responses from another server/proxy.'),
    503: ('Service Unavailable',
          'The server cannot process the request due to a high load'),
    504: ('Gateway Timeout',
          'The gateway server did not receive a timely response'),
    505: ('HTTP Version Not Supported', 'Cannot fulfill request.'),
    }

MSG_FMT = """\
Status code {code}
Message: {message}
Code explanation: {explain}

"""

def _print_filtered_codes(code):
    code = code.replace('x', '\d') + '$'
    _print_codes(filter(lambda c: re.match(code, str(c)), STATUS_CODES))

def _print_search(text):
    """Search for a code by description and print it."""
    _is_text_found = re.compile(text, re.IGNORECASE).search
    found_codes = dict(
        (code, (short, long))
        for code, (short, long) in STATUS_CODES.items()
        if _is_text_found(short + long)
        )
    if found_codes:
        _print_codes(found_codes)
    else:
        sys.stderr.write('No status code found for search: %s\n' % text)
        sys.exit(-1)

def _print_codes(codes=STATUS_CODES):
    for code in sorted(codes):
        _print_code(code)

def _print_code(code):
    try:
        short, long = STATUS_CODES[code]
    except KeyError as e:
        sys.stderr.write('No description found for code: %s\n' % code)
        sys.exit(-1)
    else:
        msg = MSG_FMT.format(code=code, message=short, explain=long)
        sys.stdout.write(msg)

def main():
    usage = """\
    usage: hc [code]

    Without parameters lists all available
    HTTP status codes and their description
    """
    parser = optparse.OptionParser(usage=textwrap.dedent(usage))
    parser.add_option(
        '-s', '--search', dest='search',
        help=('Search for a code by name or description. '
              'Search text may contain regular expressions.')
        )
    options, args = parser.parse_args()

    if options.search is not None:
        _print_search(options.search)
    elif args:
        if re.match(r'\d{3}$', args[0]):
            _print_code(int(args[0]))
        else:
            _print_filtered_codes(args[0])
    else:
        _print_codes()

if __name__ == '__main__':
    main()
