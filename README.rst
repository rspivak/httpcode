::

     _   _ _____ _____ ____   ____ ___  ____  _____
    | | | |_   _|_   _|  _ \ / ___/ _ \|  _ \| ____|
    | |_| | | |   | | | |_) | |  | | | | | | |  _|
    |  _  | | |   | | |  __/| |__| |_| | |_| | |___
    |_| |_| |_|   |_| |_|    \____\___/|____/|_____|


`httpcode` is a little utility that displays the meaning of an HTTP
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


