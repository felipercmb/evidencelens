"""Local-only demo server; bind to loopback by default, never expose publicly."""
import json,sys
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
ROOT=Path(__file__).parent
sys.path.insert(0,str(ROOT/'src'))
from evidencelens import predict
PORT=int(sys.argv[1]) if len(sys.argv)>1 else 8765
MODEL=json.loads((ROOT/'artifacts/model.json').read_text())
class Handler(BaseHTTPRequestHandler):
    def respond(self,status,data,typ='application/json'):
        self.send_response(status);self.send_header('Content-Type',typ+'; charset=utf-8'); self.send_header('X-Content-Type-Options','nosniff'); self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(data)
    def setup(self):
        super().setup(); self.connection.settimeout(5)
    def do_GET(self):
        if self.path not in ['/','/index.html']: return self.respond(404,b'{}')
        self.respond(200,(ROOT/'web/index.html').read_bytes(),'text/html')
    def do_POST(self):
        if self.headers.get('Host') not in [f'127.0.0.1:{PORT}',f'localhost:{PORT}']:
            return self.respond(403,b'{"error":"Host rejected"}')
        if self.headers.get('Origin') not in [None,f'http://127.0.0.1:{PORT}',f'http://localhost:{PORT}']:
            return self.respond(403,b'{"error":"Origin rejected"}')
        if self.headers.get_content_type()!='application/json':
            return self.respond(415,b'{"error":"JSON required"}')
        if self.path!='/api/predict': return self.respond(404,b'{}')
        try:
            size=int(self.headers.get('Content-Length','0'))
            if size<1 or size>20000: raise ValueError('Tamanho inválido')
            obj=json.loads(self.rfile.read(size))
            if not isinstance(obj,dict): raise ValueError('JSON deve ser objeto')
            if not all(isinstance(obj.get(k),str) and 0<len(obj[k].strip()) and len(obj[k])<=8000 for k in ['evidence','answer']): raise ValueError('Informe dois textos de até 8000 caracteres')
            out=predict(MODEL,obj['evidence'],obj['answer']);self.respond(200,json.dumps(out).encode())
        except (ValueError,TypeError,KeyError) as e: self.respond(400,json.dumps({'error':str(e)}).encode())
if __name__=='__main__':
    print(f'EvidenceLens: http://127.0.0.1:{PORT}');ThreadingHTTPServer(('127.0.0.1',PORT),Handler).serve_forever()
