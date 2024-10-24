#!/usr/bin/env python3

import os
import sys
from http.server import (HTTPServer, SimpleHTTPRequestHandler,  # type:ignore
                         test)


class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        SimpleHTTPRequestHandler.end_headers(self)


if __name__ == "__main__":

    containing_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    web_folder = os.path.join(containing_folder, "web")
    os.chdir(web_folder)
    print(f"Serving files from {web_folder}")

    test(
        CORSRequestHandler,
        HTTPServer,
        port=int(sys.argv[1]) if len(sys.argv) > 1 else 8000,
    )
