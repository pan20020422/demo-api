cat > app.py <<'EOF'
from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/cpu":
            # cpu压力：浮点循环运算
            s = 0.0
            for i in range(6_000_000):
                s += (i ** 0.5)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f"cpu burn done sum={s}\n".encode())
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"demo-api ok, path=" + self.path.encode())

HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
EOF
