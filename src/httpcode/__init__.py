###############################################################################
#
# Copyright (c) 2011 - 2017 Ruslan Spivak
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
import argparse
import textwrap
import re

from colorama import Style, init, deinit

# Codes with messages are taken verbatim from BaseHTTPServer.py

# Table mapping response codes to messages; entries have the
# form {code: (shortmessage, longmessage)}.
# See RFC 2616.
STATUS_CODES = {
    100: ('Continue', 'Request received, please continue'),
    101: ('Switching Protocols',
          'Switching to new protocol; obey Upgrade header'),
    102: ('Processing', 'WebDAV; RFC 2518'),

    200: ('OK', 'Request fulfilled, document follows'),
    201: ('Created', 'Document created, URL follows'),
    202: ('Accepted',
          'Request accepted, processing continues off-line'),
    203: ('Non-Authoritative Information', 'Request fulfilled from cache'),
    204: ('No Content', 'Request fulfilled, nothing follows'),
    205: ('Reset Content', 'Clear input form for further input.'),
    206: ('Partial Content', 'Partial content follows.'),
    207: ('Multi-Status', 'WebDAV; RFC 4918'),
    208: ('Already Reported', 'WebDAV; RFC 5842'),
    226: ('IM Used', 'RFC 3229'),

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
    306: ('Switch Proxy', 'Subsequent requests should use the specified proxy'),
    307: ('Temporary Redirect',
          'Object moved temporarily -- see URI list'),
    308: ('Permanent Redirect', 'Object moved permanently'),

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
    413: ('Payload Too Large', 'Payload is too large.'),
    414: ('Request-URI Too Long', 'URI is too long.'),
    415: ('Unsupported Media Type', 'Entity body in unsupported format.'),
    416: ('Requested Range Not Satisfiable',
          'Cannot satisfy request range.'),
    417: ('Expectation Failed',
          'Expect condition could not be satisfied.'),
    418: ("I'm a teapot", 'The HTCPCP server is a teapot'),
    419: ('Authentication Timeout', 'previously valid authentication has expired'),
    420: ('Method Failure / Enhance Your Calm', 'Spring Framework / Twitter'),
    422: ('Unprocessable Entity', 'WebDAV; RFC 4918'),
    423: ('Locked', 'WebDAV; RFC 4918'),
    424: ('Failed Dependency / Method Failure', 'WebDAV; RFC 4918'),
    425: ('Unordered Collection', 'Internet draft'),
    426: ('Upgrade Required', 'client should switch to a different protocol'),
    428: ('Precondition Required', 'RFC 6585'),
    429: ('Too Many Requests', 'RFC 6585'),
    431: ('Request Header Fields Too Large', 'RFC 6585'),
    440: ('Login Timeout', 'Microsoft'),
    444: ('No Response', 'Nginx'),
    449: ('Retry With', 'Microsoft'),
    450: ('Blocked by Windows Parental Controls', 'Microsoft'),
    451: ('Unavailable For Legal Reasons', 'RFC 7725'),
    494: ('Request Header Too Large', 'Nginx'),
    495: ('Cert Error', 'Nginx'),
    496: ('No Cert', 'Nginx'),
    497: ('HTTP to HTTPS', 'Nginx'),
    498: ('Token expired/invalid', 'Esri'),
    499: ('Client Closed Request', 'Nginx'),

    500: ('Internal Server Error', 'Server got itself in trouble'),
    501: ('Not Implemented',
          'Server does not support this operation'),
    502: ('Bad Gateway', 'Invalid responses from another server/proxy.'),
    503: ('Service Unavailable',
          'The server cannot process the request due to a high load'),
    504: ('Gateway Timeout',
          'The gateway server did not receive a timely response'),
    505: ('HTTP Version Not Supported', 'Cannot fulfill request.'),
    506: ('Variant Also Negotiates', 'RFC 2295'),
    507: ('Insufficient Storage', 'WebDAV; RFC 4918'),
    508: ('Loop Detected', 'WebDAV; RFC 5842'),
    509: ('Bandwidth Limit Exceeded', 'Apache bw/limited extension'),
    510: ('Not Extended', 'RFC 2774'),
    511: ('Network Authentication Required', 'RFC 6585'),
    598: ('Network read timeout error', 'Unknown'),
    599: ('Network connect timeout error', 'Unknown'),
    }

MSG_FMT = """\
Status code {code}
Message: {message}
Code explanation: {explain}

"""

_IS_THREE_DIGIT_CODE = re.compile(r'\d{3}$').match


def _colorize(text):
    return Style.BRIGHT + text + Style.RESET_ALL

def _exit(msg):
    sys.stderr.write(msg)
    # stop colorama
    deinit()
    sys.exit(-1)

def _print_filtered_codes(code):
    """Search and print codes based on passed regexp.

    Examples of codes with regexps:
    $ hc 30[12]

    $ hc 3..

    Special case, use 'x' for any digit
    $ hc 1xx
    """
    _has_code_match = re.compile(code.replace('x', '\d') + '$').match
    found_codes = [c for c in STATUS_CODES if _has_code_match(str(c))]
    if not found_codes:
        _exit('No code found corresponding to: %s\n' % code)
    _print_codes(codes=found_codes)

def _print_search(text, noformat=False):
    """Search for a code by description and print it."""
    _is_text_found = re.compile(text, re.IGNORECASE).search
    found_codes = [
        code for code, (short, long) in STATUS_CODES.items()
        if _is_text_found(short + long)
    ]
    if found_codes:
        _print_codes(codes=found_codes, noformat=noformat)
    else:
        _exit('No status code found for search: %s\n' % text)

def _print_codes(codes=STATUS_CODES.keys(), noformat=False):
    for code in sorted(codes):
        _print_code(code, noformat)

def _print_code(code, noformat=False):
    try:
        short, long = STATUS_CODES[code]
    except KeyError as e:
        _exit('No description found for code: %s\n' % code)
    else:
        # colorize code
        code = str(code) if noformat else _colorize(str(code))
        msg = MSG_FMT.format(code=code, message=short, explain=long)
        sys.stdout.write(msg)

def main():
    usage = """\
    usage: hc [code] [options]

    Without parameters lists all available
    HTTP status codes and their description
    """
    parser = argparse.ArgumentParser(usage=textwrap.dedent(usage))
    parser.add_argument(
        'code',
        nargs='?',
        help=("Code may contain regular expression or use 'x' to denote "
              "any digit. Code examples: 418, 30[12], 3.*, 1xx")
    )

    parser.add_argument(
        '-s', '--search',
        dest='search',
        help=('Search for a code by name or description. '
              'Search text may contain regular expressions.')
    )
    parser.add_argument(
        '-p', '--plain',
        action='store_true',
        dest='noformat',
        default=False,
        help=( 'Disable formatting of output')
    )
    args = parser.parse_args()

    # initialize colorama
    init()

    if args.search is not None:
        _print_search(args.search, noformat=args.noformat)
    elif args.code:
        code = args.code
        if _IS_THREE_DIGIT_CODE(code):
            _print_code(int(code), args.noformat)
        else:
            _print_filtered_codes(code)
    else:
        _print_codes(noformat=args.noformat)

if __name__ == '__main__':
    main()
