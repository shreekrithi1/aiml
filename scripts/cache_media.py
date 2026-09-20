"""Cache only image URLs already captured from the user's LinkedIn page."""
import json,pathlib,urllib.request,concurrent.futures,shutil
root=pathlib.Path(__file__).resolve().parents[1]
data=json.loads((root/'data/library.json').read_text())
media=root/'app/media/linkedin';media.mkdir(parents=True,exist_ok=True)
def fetch(r):
    results=[]
    for i,img in enumerate(r.get('images',[])):
        try:
            if img.get('local') and (root/'app'/img['local'].lstrip('/')).is_file():
                results.append(img);continue
            req=urllib.request.Request(img['url'],headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req,timeout=20) as response:
                ctype=response.headers.get_content_type();raw=response.read(20_000_000)
            ext={'image/jpeg':'.jpg','image/png':'.png','image/gif':'.gif','image/webp':'.webp'}.get(ctype)
            if not ext or len(raw)<100: raise ValueError('No usable image')
            name=f'{r["id"]}-{i+1}{ext}';(media/name).write_bytes(raw)
            results.append({'url':img['url'],'alt':r['title'],'local':'/media/linkedin/'+name})
        except Exception as e:
            results.append(dict(img,error=str(e)))
    return r['id'],results
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    result=dict(pool.map(fetch,data['resources']))
# Re-read to preserve changes to notes/progress made during downloads.
data=json.loads((root/'data/library.json').read_text())
for r in data['resources']:r['images']=result[r['id']]
(root/'data/library.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
print(json.dumps({'cached':sum(bool(i.get('local')) for r in data['resources'] for i in r['images']),'failed':[r['id'] for r in data['resources'] if any(not i.get('local') for i in r['images'])]}))
