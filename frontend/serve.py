"""SPA 静态服务 + API 反向代理 —— /api → localhost:8900，其余回退到 index.html"""
import http.server
import os
import sys
import urllib.request
import urllib.error

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
ROOT = os.path.join(os.path.dirname(__file__), "dist")
API_TARGET = "http://127.0.0.1:8900"


class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def _proxy_api(self, method):
        """将 /api/* 请求代理到后端 FastAPI"""
        target_url = f"{API_TARGET}{self.path}"
        body = None
        content_len = int(self.headers.get("Content-Length", 0))
        if content_len > 0:
            body = self.rfile.read(content_len)

        req = urllib.request.Request(target_url, data=body, method=method)
        # 转发关键 headers
        for h in ("authorization", "content-type", "accept"):
            v = self.headers.get(h)
            if v:
                req.add_header(h, v)

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                self.send_response(resp.status)
                for k, v in resp.headers.items():
                    if k.lower() not in ("transfer-encoding", "connection"):
                        self.send_header(k, v)
                self.end_headers()
                self.wfile.write(resp.read())
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.end_headers()
            self.wfile.write(e.read())
        except Exception as e:
            self.send_response(502)
            self.end_headers()
            self.wfile.write(f'{{"detail":"后端不可用: {e}"}}'.encode())

    def do_GET(self):
        if self.path.startswith("/api/"):
            return self._proxy_api("GET")
        path = self.translate_path(self.path)
        if not os.path.exists(path) or os.path.isdir(path):
            self.path = "/index.html"
        super().do_GET()

    def do_POST(self):
        if self.path.startswith("/api/"):
            return self._proxy_api("POST")
        super().do_POST()

    def do_DELETE(self):
        if self.path.startswith("/api/"):
            return self._proxy_api("DELETE")
        super().do_DELETE()

    def do_OPTIONS(self):
        if self.path.startswith("/api/"):
            return self._proxy_api("OPTIONS")
        super().do_OPTIONS()


if __name__ == "__main__":
    server = http.server.HTTPServer(("0.0.0.0", PORT), ProxyHandler)
    print(f"Serving Vibe-Research on 0.0.0.0:{PORT} (API → {API_TARGET})")
    server.serve_forever()
