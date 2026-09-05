# tacirogluresearch.org

Website for the Taciroglu Research Group, UCLA Civil and Environmental
Engineering.

Plain HTML and CSS. No build step, no dependencies, no framework.

## Files

```
index.html      Home
research.html   Approach and publications
code.html       Software and datasets
people.html     PI and current group
contact.html    Contact and prospective students
alumni.html     Doctoral and postdoctoral alumni
grants.html     Current and completed grants
family-tree.html  Academic lineage poster
assets/style.css
CNAME           Custom domain for GitHub Pages
```

## Editing

Everything is hand-editable. Open the file, change the text, commit.

**Add a news item** — `index.html`, in the "Recent news" section. Copy an
existing `<div class="repo">` block and edit it.

**Add a student** — `people.html`. Copy a `<div class="member">` block into the
right group. The avatar class controls the colour: `earth`, `wind`, `fire`, or
`neutral`.

**Add a publication** — `research.html`, in the `<ul class="pubs">` list. Wrap
the group's author name in `<b>`. Add
`<a class="codemark" href="...">Code</a>` if there's a repo.

**Add a repository** — `code.html`. Copy a `<div class="repo">` block into the
matching section.

**Add a photo** — put the image in `assets/`, then replace

```html
<div class="portrait">ET</div>
```

with

```html
<div class="portrait has-photo earth">
  <img src="assets/name.jpg" alt="Full Name">
</div>
```

Same pattern for `.avatar` in the roster. The greyscale-plus-tint treatment is
applied automatically, so photos from different sources still look like a set.

## Colours

| | Hex | Used for |
|---|---|---|
| Earth | `#b26b12` | Earthquake |
| Wind | `#14806a` | Hurricane |
| Fire | `#c6472a` | Wildfire |
| Ink | `#1a1d1b` | Body text |
| Paper | `#fbfbf9` | Background |

Defined once at the top of `assets/style.css`.

## Local preview

```
python3 -m http.server 8000
```

Then open http://localhost:8000

## Repository location

This site lives in the `TRG-UCLA` umbrella organization. The specialized
organizations (TRG-NHM, TRG-SHM, TRG-AI4Good, TRG-SSI, TRG-FEM) hold research
code; `TRG-UCLA` holds the group's public-facing presence.

The repository is private; the published site is public. That is the normal
GitHub Pages arrangement — visitors see the site, not the source or history.

## Deploying changes

```bash
git add .
git commit -m "Update news"
git push
```

GitHub Pages rebuilds within a minute or so. There is no build step to run
locally.
