// Checks arvore.html data: references between people, meta (confidence + source) for everyone,
// image keys and image files. Run: node tools/validar_arvore.js
const fs = require("fs"), path = require("path");
const root = path.join(__dirname, "..");
const h = fs.readFileSync(path.join(root, "arvore.html"), "utf8");
const grab = n => {
  const j = h.indexOf("{", h.indexOf("const " + n + " = {"));
  for (let k = j, d = 0; ; k++) {
    if (h[k] == "{") d++;
    if (h[k] == "}" && !--d) return eval("(" + h.slice(j, k + 1) + ")");
  }
};
const people = grab("people"), meta = grab("meta"), IMG = grab("IMG"), IMGS = grab("IMGS");
let err = 0;
const bad = (...m) => { console.log(...m); err++; };
for (const [id, p] of Object.entries(people)) {
  for (const r of [p.f, p.m, ...(p.sp || [])]) if (r && !people[r]) bad("referência inválida", id, r);
  if (!meta[id]) bad("sem meta (confiança/fonte)", id);
  for (const s of p.sp || []) if (people[s] && !(people[s].sp || []).includes(id)) bad("cônjuge não recíproco", id, s);
}
for (const id in meta) if (!people[id]) bad("meta sem pessoa", id);
for (const [id, ks] of Object.entries(IMGS)) {
  if (!people[id]) bad("imagens sem pessoa", id);
  for (const k of ks) if (!IMG[k]) bad("imagem inexistente", id, k);
}
for (const [k, [, p]] of Object.entries(IMG)) if (!fs.existsSync(path.join(root, p))) bad("ficheiro em falta", k, p);
console.log(Object.keys(people).length, "pessoas,", Object.keys(IMG).length, "imagens; erros:", err);
process.exit(err ? 1 : 0);
