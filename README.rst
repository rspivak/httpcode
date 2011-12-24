::

     _   _ _____ _____ ____   ____ ___  ____  _____
    | | | |_   _|_   _|  _ \ / ___/ _ \|  _ \| ____|
    | |_| | | |   | | | |_) | |  | | | | | | |  _|
    |  _  | | |   | | |  __/| |__| |_| | |_| | |___
    |_| |_| |_|   |_| |_|    \____\___/|____/|_____|


`httpcode` is a little utility that explains the meaning of an HTTP
status code on the command line.

`http://httpcode.readthedocs.org <http://httpcode.readthedocs.org>`_

Installation
------------

::

    $ [sudo] pip install httpcode


Usage
-----

Explain 405 status code

::

    $ hc 405
    Status code 405
    Message: Method Not Allowed
    Code explanation: Specified method is invalid for this resource.

Or 418 status code :)

::

    $ hc 418
    Status code 418
    Message: I'm a teapot
    Code explanation: The HTCPCP server is a teapot

List all codes

::

    $ hc
    Status code 100
    Message: Continue
    Code explanation: Request received, please continue

    Status code 101
    Message: Switching Protocols
    Code explanation: Switching to new protocol; obey Upgrade header

    Status code 200
    Message: OK
    Code explanation: Request fulfilled, document follows

    ...

Search code(s) by description (case-insensitive)

::

    $ hc -s too
    Status code 413
    Message: Request Entity Too Large
    Code explanation: Entity is too large.

    Status code 414
    Message: Request-URI Too Long
    Code explanation: URI is too long.

Filter codes with a regex

::

    $ hc 30[12]
    Status code 301
    Message: Moved Permanently
    Code explanation: Object moved permanently -- see URI list

    Status code 302
    Message: Found
    Code explanation: Object moved temporarily -- see URI list

Use an 'x' for any digit

::

    $ hc 1xx
    Status code 100
    Message: Continue
    Code explanation: Request received, please continue

    Status code 101
    Message: Switching Protocols
    Code explanation: Switching to new protocol; obey Upgrade header

Show help

::

    $ hc -h
    Usage: hc [code]

    Without parameters lists all available
    HTTP status codes and their description


    Options:
      -h, --help            show this help message and exit
      -s SEARCH, --search=SEARCH
                            Search for a code by name or description. Search text
                            may contain regular expressions.


Roadmap
-------

Add more codes
