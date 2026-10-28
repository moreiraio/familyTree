#!/usr/bin/env bash
# Publishes arvore.html to GitHub Pages (branch gh-pages) with only the images it cites,
# resized to max 2400 px (fontes/ in grayscale). The full fontes/ (GBs) never goes to GitHub.
# Usage: bash tools/publicar.sh "commit message"
set -euo pipefail
cd "$(dirname "$0")/.."
node tools/validar_arvore.js
WT="${TMPDIR:-${TEMP:-/tmp}}/ghpages_wt"
[ -d "$WT" ] || git worktree add "$WT" gh-pages
node -e '
const h=require("fs").readFileSync("arvore.html","utf8");const i=h.indexOf("const IMG = {");
for(const m of h.slice(i,h.indexOf("};",i)).matchAll(/"((?:fontes|imagens)\/[^"]+)"/g))console.log(m[1])' |
python -c '
import sys, os
from PIL import Image
wt = sys.argv[1]
for p in sys.stdin.read().split():
    out = os.path.join(wt, p)
    if os.path.exists(out): continue
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im = Image.open(p)
    if p.startswith("fontes"): im = im.convert("L")
    else: im = im.convert("RGB")
    im.thumbnail((2400, 2400)); im.save(out, quality=80); print("nova:", p)
' "$WT"
cp arvore.html "$WT/index.html"
cd "$WT"
git add -A
git commit -qm "${1:-Update family tree}" && git push -q origin gh-pages
git log --oneline -1
