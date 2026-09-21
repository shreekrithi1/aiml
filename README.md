# AI/ML Atlas

A local learning workspace containing all 342 posts and articles exposed by your LinkedIn saved list on September 20, 2026.

## Run

```sh
git clone https://github.com/shreekrithi1/aiml.git
cd aiml
python3 server.py
```

Open http://127.0.0.1:8765. Python 3 is the only dependency. The server listens only on your computer. Stop with Ctrl+C.

## Organization

- `app/`: responsive web interface, roadmap, searchable library, resource notes and reading progress.
- `data/library.json`: original LinkedIn links, editorial titles, author attribution, roadmap and saved progress. Back up this file or use Export library.
- `learning-path/01-foundations/` through `06-production/`: portable Markdown reading lists, practice milestones and deliverables.
- `server.py`: local web server and file-backed persistence.

The 12-week schedule is a suggestion. Check off 18 practical milestones, filter resources by stage, and save notes for each post. The Markdown checklists are reference documents; live progress is in the web app and JSON.

## Import scope

Imported all 342 cards exposed by **Saved posts and articles**, continuing until the Show more results control disappeared at the end of the list (oldest post: `7132055302757101568`). Added 263 resources to the original 79, preserving existing notes, reading status and roadmap progress. Includes non-AI topics and 12 posts without image previews. This scope does not include Job tracker, My learning or Service requests, which are separate LinkedIn sections.

Local import snapshots and backups are excluded from Git. `saved-library/` contains reading lists by topic. Categorization is suggested automatically from post content; original curated titles and stages remain intact. This is a one-time snapshot, not live synchronization. Excerpts are short quotations; follow original links for full posts and carousel slides.

## Hosting on Vercel

The repository includes `vercel.json`. Use the repository root as Root Directory; the build runs `node scripts/build-static.mjs` and publishes `dist/`. No server or dependencies are required for the hosted version.

Hosted notes, reading status and milestones persist in this browser using localStorage. They do not sync across devices and may be lost if site data is cleared; use Export library for a backup. The build clears personal notes and progress from the published library. Local `python3 server.py` continues to save progress to `data/library.json`.

## In-app reading

Resources include short attributed excerpts and locally cached images where LinkedIn exposed an image preview. Open **Read in app** from a resource card and click its image to enlarge it. Notes and reading progress remain editable in the reader. Images are stored in `app/media/linkedin/`, so they do not rely on expiring LinkedIn URLs during normal use. These are saved-post preview images (one per resource), not complete multi-slide carousels. Original post links provide the complete text and any additional slides.
