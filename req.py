import http.server as http_server
import socketserver
import requests_toolbelt.multipart as rtm
import backend

addr = ('localhost', 825)
db_path = ''


class RequestHandler(http_server.BaseHTTPRequestHandler):
    _encoding = 'utf8'
    _backend = backend.Backend(db_path)

    def end_headers(self):
        """
        Deal with CORS
        """
        self.send_header('Access-Control-Allow-Origin', '*')
        http_server.BaseHTTPRequestHandler.end_headers(self)

    def do_GET(self):
        # TODO: ??
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')

    def do_POST(self):
        get_key = lambda d: d.split(";")[1].split("=")[1].replace('"', '')

        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        self.wfile.write('hello response'.encode(self._encoding))

        received_blob = rtm.decoder.MultipartDecoder(body, self.headers['content-type'])
        pl = {}
        for part in received_blob.parts:
            decoded_header = part.headers[b'Content-Disposition'].decode(self._encoding)
            key = get_key(decoded_header)
            pl[key] = part.content

        # print(pl)
        command: bytes = pl['op']
        target_stack: backend.TargetStack = backend.TargetStack(pl['ts'][0], pl['ts'][1], pl['ts'][2])
        arg: bytes = pl['payload']
        act_status: bytes = self._backend.act(command, target_stack, arg)
        self.wfile.write(act_status)


if __name__ == '__main__':
    try:
        with socketserver.TCPServer(addr, RequestHandler) as httpd:
            print(f'Starting server on {addr[0]}:{addr[1]} ...')
            httpd.serve_forever()
    except KeyboardInterrupt:
        print('Shutting down the server gracefully ...')
        httpd.shutdown()
        httpd.server_close()
