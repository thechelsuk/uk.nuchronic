# Bridgy Cloudflare Worker

This Worker forwards Bridgy discovery requests for `nuchronic.uk` to `fed.brid.gy` while preserving the query string.

Use it for these paths:

- `/.well-known/host-meta`
- `/.well-known/webfinger`

Suggested route in Cloudflare:

```text
nuchronic.uk/.well-known/*
```

The worker source is in `cloudflare/bridgy-well-known-worker.js`.
