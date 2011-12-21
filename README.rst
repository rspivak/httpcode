::

     _   _ _____ _____ ____   ____ ___  ____  _____
    | | | |_   _|_   _|  _ \ / ___/ _ \|  _ \| ____|
    | |_| | | |   | | | |_) | |  | | | | | | |  _|
    |  _  | | |   | | |  __/| |__| |_| | |_| | |___
    |_| |_| |_|   |_| |_|    \____\___/|____/|_____|


`httpcode` is a little utility that explains the meaning of an HTTP
status code on the command line.

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


Show help

::

    $ hc -h
    Usage: hc [code]

    Without parameters lists all available
    HTTP status codes and their description


    Options:
      -h, --help  show this help message and exit


Roadmap
-------

Add more codes