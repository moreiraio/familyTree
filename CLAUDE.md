# Genealogia Mimoso (tombo)

Genealogical research for **Maria do Socorro Mimoso Guedes**, who is the user. The goal is the full ancestry of her grandfather **António José Mimoso**, born 7-11-1930 in Godim, Peso da Régua, died 3-4-1995 in Lordelo, Vila Real. He married Emília da Conceição Vicente on 4-3-1961 (assento 41/1961, Régua).
- Ahnentafel numbers in the documents are counted from him: n.º 1 is the avô.
- Roles in arvore.html (avô, bisavô …) are relative to Maria do Socorro.
- A second, separate tree exists for Vítor Roberto Martins Moreira (vitor_moreira.md).

Talk to the user in **Portuguese**. All research documents are in Portuguese.

## Files
| Path | What it is |
|---|---|
| `arvore.md` | Main research document: pedigree diagram, person sections, full transcriptions ("Linha Mimoso: assentos validados"), property records, to-do list. Source of truth for the text. |
| `arvore.html` | Interactive D3 tree, published as GitHub Pages `index.html`. Data lives in JS objects `people`, `LEVELS`, `meta`, `IMG`, `IMGS`. Ancestors are drawn to the right and descendants to the left. Every person shows a source, a confidence level and image buttons. |
| `vitor_moreira.md` | Moreira tree (Valongo / Campo / Sobrado). |
| `fontes/` | Downloaded scans, about 3 GB. Folders `baptYYYY`, `casYYYY`, `obiYYYY`, `bapt1853-59`, `indice_godim`, `sps_*` (S. Pedro do Sul), each with `pNNNN.jpg` and `ids.txt` (`<fileId> <name>`). It is a local cache only, ignored by Git; back it up outside Git. Git tracks only the maps: `fontes/livros.tsv` (folder, reference code, docId, image count) and every `ids.txt`. A lost page can be downloaded again with `python tools/digitarq.py get <docId> <folder> <pages>`. **Never commit or push the scans.** |
| `imagens/` | Family documents: caderneta predial 92-B, registo predial 1973, descrição predial 35.139. |
| `tools/digitarq.py` | Search, details, list and download pages from digitarq. |
| `tools/validar_arvore.js` | Integrity check of arvore.html data. Must report 0 errors before publishing. |
| `tools/publicar.sh` | Publishes arvore.html and the cited images (resized) to gh-pages. |
| `.claude/agents/` | `pesquisador-genealogia` (research) and `organizador-arvore` (merge, validate, publish). |

Published site: https://moreiraio.github.io/familyTree/ (repo moreiraio/familyTree).
- Branch `main`: the md and html files, plus a few early scans.
- Branch `gh-pages`: `index.html` plus only the cited images, resized. The local worktree for it is `$TEMP/ghpages_wt`.

## Sources and how to search
- **tombo.pt** is only a catalogue/index of parish books.
  - Godim = `/f/prg04`, concelho Peso da Régua = `/m/prg`.
  - The saved page `fontes/godim.html` lists every Godim book. The first 32-hex id after each date range is the book's docId; baptisms come first, then marriages, then deaths.
- **digitarq** (digitarq.arquivos.pt) has the scans. Its web pages are an SPA, so use the API through `tools/digitarq.py`:
  - `api/docs/search?query=…&fromIndex=N&max=10`: max is capped at 10.
  - `api/docs/details/<docId>`
  - `api/rdigital/<docId>?fromIndex=0&max=500`: image list.
  - `rdigital/dissemination?fileId=<id>`: the TIFF. Retry on failure; it is rate-limited.
- **Reference codes:**
  - Godim parish: `PT/ADVRL/PRQ/PPRG04/001` baptisms, `/002` marriages, `/003` deaths. Online to 1911.
  - S. Pedro do Sul parish: `PT/ADVIS/PRQ/PSPS14`. Other parishes of that concelho are PSPS01–19, for example Baiões PSPS01 and Bordonhos PSPS02.
  - No S. Pedro do Sul baptism book exists online for 8-1797 to 9-1816.
- **Civil registry after 1911** (Conservatória da Régua) is NOT online:
  - certidões via civilonline.mj.pt / ePortugal;
  - older civil books via the ADVRL ("Pedir…" in digitarq);
  - land registry via predialonline.pt (descrição **00427/Godim**, formerly 35.139, B-89 fl. 181; the house is prédio 58.828).
- **Baptism margins carry civil averbamentos** (marriage and death after 1911). They are the bridge to 20th-century facts.
- **Godim baptism index**, 1861–1911: `fontes/indice_godim`. It often omits the Mimoso surname.

## Research rules
1. **Every fact needs a source.** That means a record, a page file and an entry number, or "família" when the user said it. Never present a deduction as a document.
2. **Confidence levels** (`LEVELS` in arvore.html; the same symbols in arvore.md):

   | Level | Symbol | Approx. | When |
   |---|---|---|---|
   | doc | ✔ | 95% | original record read |
   | reg | ● | 85% | index, marginal note, archive catalogue, land registry |
   | fam | ◆ | 85% | family information without a document |
   | prov | ~ | 70% | deduction, or a hard reading |
   | hip | ? | 40% | hypothesis |

3. **Mark doubtful readings with (?).** Prefer the baptism date over ages in marriage or death records, which are often several years off (Manuel António "75" was really 71).
4. **Match people by both parents and the grandparents**, not by name alone. Godim has several families with the same names: two Joaquim António Mimoso, several José António in Covas.
5. **When new evidence contradicts the documents, correct them.** Mark the correction with ⚠ and say what was wrong.
6. **Record negative searches** (book, pages, years) so they are not repeated.
7. **Ask the user before publishing.** Publishing means a public site; the user approved publishing living people. Ask before pushing anything new and before adding photos of new documents.
8. **Commit on main by name only.** Use `git add arvore.md arvore.html …`, never `git add -A` or `git add .`: fontes/ is GBs. Check `git diff --cached --stat` before committing.

## Working method
- **Research** with the `pesquisador-genealogia` agent: one target or one book per agent, several in parallel for independent targets. Give each one the person, the known parents and grandparents, the expected year range and the docIds. Agents write their reports to the session scratchpad.
- **Merge** with the `organizador-arvore` agent, or directly: read the reports, update arvore.md and arvore.html, run `node tools/validar_arvore.js`, and preview at 1280 px and 390 px (the site is mobile-ready).
- **Publish** on request: run `bash tools/publicar.sh "message"`, then commit and push the changed files on main.
- **Reading images:**
  - look at the whole page downscaled first, then crop and upscale 2x with autocontrast;
  - margin names identify entries;
  - run `python` without `-I` (PIL lives in user site-packages);
  - Playwright can only write inside the repo, so screenshots go to `.playwright-mcp/`.

## State (October 2026)
- **Paternal Mimoso line:** validated against the original records up to n.º 128–135 (roles go up to octavô/octavó).
  - n.º 16, José António Mimoso, married Joanna Emília in Godim on 14-8-1814. His probable baptism is 31-7-1774 in Pouves, S. Pedro do Sul.
  - His parents, José Corrêa × Fructuosa Rodrigues, married 11-2-1771. José Corrêa (n.º 32) was baptised 10-10-1745 in Baiões, the natural son of José Corrêa da Corvaceira (n.º 64), whose parents were Cap. João Marques × Maria Corrêa (n.º 128/129).
  - Open: n.º 64's own baptism (Joseph 1714, which has a margin cross).
  - Origin of the surname: the first "Mimozo" in Godim is the baptism of 4-9-1857 (same pároco as 1853/1855, which have no surname). It is probably a family alcunha adopted c.1856–57, not brought from S. Pedro do Sul. The vigário Mimozo (1811) hypothesis is weak.
  - Deaths of n.º 16/17 not found in Godim deaths 1833–1879. Both were probably alive at the end of 1852.
- **Vicente/Silva line** of the bisavó Francisca: done to n.º 24–31. Its marriages 12+13 and 14+15 are not yet searched.
- **Open questions:**
  - the parents of the avó, Emília da Conceição Vicente; this needs the certidão of marriage 41/1961, Conservatória da Régua;
  - 3 unidentified siblings of the avô;
  - Joaquim António's baptism (about 1860);
  - the marriage of José da Silva × Maria de Jesus Amaral (probably in Loureiro);
  - the deaths of n.º 16 and 17.
- **Documents to request:**
  - ADVRL inventário 1973 (PT/ADVRL/JUD/TJCPRG/C-B/082/1658);
  - testamento of 1921 (PT/ADVRL/NOT/CNPRG5/007/394/38);
  - certidão de teor of the predial descrição 00427/Godim;
  - civil certidões of the avô.
- See "Por fazer" in arvore.md for the full list.
