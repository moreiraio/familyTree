"""Helper for the digitarq API (Arquivo Nacional / arquivos distritais).

Usage (run with plain `python`, not `python -I`: PIL lives in user site-packages):
  python tools/digitarq.py details <docId>                 # description of a record/book
  python tools/digitarq.py search "<query>" [max_pages]     # catalogue search (10 results per page)
  python tools/digitarq.py list <docId>                     # images of a digitized book
  python tools/digitarq.py get <docId> <folder> 1-20 35 40  # download pages as fontes/<folder>/pNNNN.jpg
"""
import json, os, subprocess, sys, time

API = "https://digitarq.arquivos.pt/api"
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fontes")


def curl(url, *extra):
    return subprocess.run(["curl", "-s", *extra, url], capture_output=True, text=True).stdout


def details(doc):
    d = json.loads(curl(f"{API}/docs/details/{doc}"))
    v = lambda k: (d.get(k) or {}).get("value") if isinstance(d.get(k), dict) else d.get(k)
    titles = [t["value"] for t in d.get("titles") or []]
    print(v("referenceCode"), v("dateInitial"), "–", v("dateFinal"), "|", "; ".join(titles))


def search(q, pages=5):
    for f in range(0, int(pages) * 10, 10):
        out = curl(f"{API}/docs/search", "-G", "--data-urlencode", f"query={q}",
                   "--data-urlencode", f"fromIndex={f}", "--data-urlencode", "max=10")
        res = json.loads(out).get("results", [])
        if not res:
            break
        for r in res:
            g = lambda k: (r.get(k) or {}).get("value") if isinstance(r.get(k), dict) else r.get(k)
            print(r["id"], g("referenceCode"), g("dateInitial"), g("dateFinal"))


def images(doc):
    return json.loads(curl(f"{API}/rdigital/{doc}?fromIndex=0&max=500"))["results"]


def pages(specs):
    for s in specs:
        a, _, b = s.partition("-")
        yield from range(int(a), int(b or a) + 1)


def get(doc, folder, specs):
    from PIL import Image
    d = os.path.join(ROOT, folder)
    os.makedirs(d, exist_ok=True)
    imgs = images(doc)
    with open(os.path.join(d, "ids.txt"), "w") as f:
        f.writelines(f"{r['id']} {r['name']}\n" for r in imgs)
    for n in pages(specs):
        jpg = os.path.join(d, f"p{n:04d}.jpg")
        if os.path.exists(jpg):
            continue
        tif = jpg[:-4] + ".tif"
        for _ in range(6):
            subprocess.run(["curl", "-s", "-o", tif, f"https://digitarq.arquivos.pt/rdigital/dissemination?fileId={imgs[n - 1]['id']}"])
            try:
                im = Image.open(tif); im.load(); break
            except Exception:
                time.sleep(20)  # rate limit or truncated download
        else:
            print("falhou", n); continue
        im.convert("RGB").save(jpg, quality=85)
        os.remove(tif)
        print(jpg, im.size)


if __name__ == "__main__":
    cmd, *a = sys.argv[1:]
    {"details": lambda: details(a[0]), "search": lambda: search(*a), "list": lambda: [print(i + 1, r["id"], r["name"]) for i, r in enumerate(images(a[0]))],
     "get": lambda: get(a[0], a[1], a[2:])}[cmd]()
