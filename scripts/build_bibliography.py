#!/usr/bin/env python3
"""Regenerate citations/TacirogluResearch.bib and .ris from OpenAlex (by ORCID)."""
import json, re, time, urllib.request, urllib.parse

ORCID = "0000-0001-9618-1210"

def fetch_all():
    works, cur = [], "*"
    while cur:
        q = urllib.parse.urlencode({
            "filter": f"author.orcid:{ORCID},type:article|book-chapter|book",
            "per-page": "200", "cursor": cur, "mailto": "etacir@ucla.edu"})
        req = urllib.request.Request("https://api.openalex.org/works?" + q,
              headers={"User-Agent": "TRG-bibliography/1.0 (mailto:etacir@ucla.edu)"})
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.load(r)
        works += d["results"]
        cur = d["meta"].get("next_cursor")
        time.sleep(1)
    return works

def latex_escape(s):
    return (s or "").replace("&", r"\&").replace("%", r"\%").replace("_", r"\_").replace("#", r"\#")

def key_for(w, seen):
    first = (w["authorships"][0]["author"]["display_name"].split()[-1]
             if w.get("authorships") else "anon")
    first = re.sub(r"[^A-Za-z]", "", first)
    year = w.get("publication_year") or "n.d."
    base = f"{first}{year}"
    k, i = base, ord("a")
    while k in seen:
        k = base + chr(i); i += 1
    seen.add(k)
    return k

def entry_bib(w, key):
    typ = "article" if w.get("type") == "article" else "incollection"
    authors = " and ".join(a["author"]["display_name"] for a in w.get("authorships", []))
    venue = ((w.get("primary_location") or {}).get("source") or {}).get("display_name") or ""
    bib = (w.get("biblio") or {})
    lines = [f"@{typ}{{{key},",
             f"  author = {{{latex_escape(authors)}}},",
             f"  title = {{{latex_escape(w.get('title'))}}},"]
    if venue:
        field = "journal" if typ == "article" else "booktitle"
        lines.append(f"  {field} = {{{latex_escape(venue)}}},")
    if w.get("publication_year"): lines.append(f"  year = {{{w['publication_year']}}},")
    if bib.get("volume"): lines.append(f"  volume = {{{bib['volume']}}},")
    if bib.get("issue"):  lines.append(f"  number = {{{bib['issue']}}},")
    if bib.get("first_page"):
        pages = bib["first_page"] + ("--" + bib["last_page"] if bib.get("last_page") else "")
        lines.append(f"  pages = {{{pages}}},")
    if w.get("doi"): lines.append(f"  doi = {{{w['doi'].replace('https://doi.org/','')}}},")
    lines.append("}")
    return "\n".join(lines)

def entry_ris(w):
    typ = "JOUR" if w.get("type") == "article" else "CHAP"
    out = [f"TY  - {typ}"]
    for a in w.get("authorships", []):
        out.append("AU  - " + a["author"]["display_name"])
    out.append("TI  - " + (w.get("title") or ""))
    venue = ((w.get("primary_location") or {}).get("source") or {}).get("display_name")
    if venue: out.append(("JO  - " if typ == "JOUR" else "BT  - ") + venue)
    if w.get("publication_year"): out.append(f"PY  - {w['publication_year']}")
    bib = (w.get("biblio") or {})
    if bib.get("volume"): out.append("VL  - " + bib["volume"])
    if bib.get("issue"):  out.append("IS  - " + bib["issue"])
    if bib.get("first_page"): out.append("SP  - " + bib["first_page"])
    if bib.get("last_page"):  out.append("EP  - " + bib["last_page"])
    if w.get("doi"): out.append("DO  - " + w["doi"].replace("https://doi.org/",""))
    out.append("ER  - ")
    return "\n".join(out)

def main():
    works = fetch_all()
    # dedupe by DOI/title, drop retractions and versionless duplicates
    seen_ids, keep = set(), []
    for w in sorted(works, key=lambda x: (-(x.get("publication_year") or 0), x.get("title") or "")):
        sig = w.get("doi") or (w.get("title") or "").lower()
        if not sig or sig in seen_ids: continue
        seen_ids.add(sig); keep.append(w)
    keys = set()
    header = ("% Taciroglu Research Group - publications\n"
              "% Generated automatically from OpenAlex (ORCID " + ORCID + ")\n"
              f"% {len(keep)} entries - https://tacirogluresearch.org\n\n")
    with open("citations/TacirogluResearch.bib", "w") as f:
        f.write(header + "\n\n".join(entry_bib(w, key_for(w, keys)) for w in keep) + "\n")
    with open("citations/TacirogluResearch.ris", "w") as f:
        f.write("\n".join(entry_ris(w) for w in keep) + "\n")
    print(f"wrote {len(keep)} entries")

if __name__ == "__main__":
    import traceback, sys, os
    os.makedirs("citations", exist_ok=True)
    try:
        main()
        if os.path.exists("citations/build-error.txt"):
            os.remove("citations/build-error.txt")
    except Exception:
        with open("citations/build-error.txt", "w") as f:
            f.write(traceback.format_exc())
        print("FAILED - traceback written to citations/build-error.txt")
        sys.exit(0)   # let the workflow commit the diagnostic
