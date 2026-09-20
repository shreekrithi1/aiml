"""Local-only learning workspace; Python standard library, no dependencies."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse
import json, threading, os
ROOT=Path(__file__).resolve().parent
DATA=ROOT/'data/library.json'
LOCK=threading.Lock()
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs): super().__init__(*args,directory=str(ROOT/'app'),**kwargs)
    def do_GET(self):
        if urlparse(self.path).path=='/api/library':
            with LOCK: body=DATA.read_bytes()
            self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(body)
        else: super().do_GET()
    def do_POST(self):
        if self.path!='/api/update': self.send_error(404);return
        if self.headers.get('Origin') not in (None,'http://127.0.0.1:8765','http://localhost:8765'):
            self.send_error(403);return
        try:
            size=int(self.headers.get('Content-Length',0))
            if not 0<size<500000: raise ValueError('Invalid request size')
            x=json.loads(self.rfile.read(size))
            with LOCK:
                d=json.loads(DATA.read_text())
                if x.get('type')=='task':
                    key=x['id']; valid={f'{i}-{j}' for i,s in enumerate(d['stages']) for j in range(len(s['tasks']))}
                    if key not in valid: raise ValueError('Unknown task')
                    done=set(d['completedTasks']);done.add(key) if x['done'] else done.discard(key);d['completedTasks']=sorted(done)
                elif x.get('type')=='resource':
                    r=next((r for r in d['resources'] if r['id']==x['id']),None)
                    if r is None: raise ValueError('Unknown resource')
                    if x.get('status') not in ('saved','reading','complete'): raise ValueError('Invalid status')
                    if not isinstance(x.get('notes'),str) or len(x['notes'])>20000: raise ValueError('Invalid notes')
                    r.update(status=x['status'],notes=x['notes'])
                else: raise ValueError('Unknown action')
                tmp=DATA.with_suffix('.tmp');tmp.write_text(json.dumps(d,indent=2,ensure_ascii=False));os.replace(tmp,DATA)
            self.send_response(200);self.send_header('Content-Type','application/json');self.end_headers();self.wfile.write(b'{"ok":true}')
        except (ValueError,KeyError,TypeError) as e: self.send_error(400,str(e))
if __name__=='__main__':
    print('AI/ML Learning: http://127.0.0.1:8765',flush=True)
    ThreadingHTTPServer(('127.0.0.1',8765),Handler).serve_forever()
