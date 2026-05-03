# webring

Dark-mode Hacker News-inspired Jekyll feed for the chronically ill indie web.

## Local development

This repo ships as a plain Jekyll site with GitHub Pages-compatible dependencies.

```bash
bundle install
bundle exec jekyll serve
```

Open `http://127.0.0.1:4000/` to view the site locally.

To refresh static webmention data locally:

```bash
python _python/fetch_webmentions.py
```

## Content model

- The homepage is the `new` feed.
- Posts live in `_posts/` and use only `title`, `link`, `author`, and `date` front matter.
- Pagination is enabled at 30 posts per page.
- The `submit` link routes to the repo's GitHub issue form.
- The site publishes an Atom feed at `/feed.xml`.

## Automation

- `.github/workflows/cicd.yml` syncs source feeds and deploys when new items land.
- `.github/workflows/webmentions.yml` refreshes static webmention data every 3 hours and deploys when counts or mentions change.

## Identity Setup

- The site publishes hidden `rel="me"` links for GitHub and Bridgy in the page head.
- To sign in to webmention.io with `nuchronic.uk`, set the website field on `https://github.com/thechelsuk` to `https://nuchronic.uk/` and then sign in with the domain itself.
- A Cloudflare Worker example for Bridgy's `/.well-known` redirects lives in `cloudflare/bridgy-well-known-worker.js`.
