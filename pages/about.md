---
layout: page
title: About
permalink: /about
description: What Nuchronic is, who it's for, how the webring works, and how to submit or remove a feed.
extra_js: /assets/js/copy-button.js
---

Nuchronic is a dark-mode, Hacker News-style feed aggregator for the chronically ill on the indie web — a webring that gathers posts from independent blogs and sites into one place, so the community has somewhere to share and discover each other's writing.

## Who it's for

The webring is open to anyone who identifies as chronically ill. Your posts don't have to be about chronic illness - write about anything. Nuchronic supports free expression and welcomes all content that isn't illegal or harmful. Maintainers review anything that gets flagged, at their discretion.

## How it works

Feeds are checked automatically, roughly once an hour, and new posts are added as they appear.

- To avoid flooding the homepage, only the latest post from each feed is added on each run.
- Publish a post a day, and each one appears here as it's published.
- To resurface an older post, update its published date in your feed and it will be picked up on the next run.
- Publish three posts in one hour, and only the most recent is added.

## Submissions

To add your feed, open a GitHub issue in our repo with the feed URL and a short description of the source. If it's accepted, it joins the webring and starts appearing on the homepage.

If GitHub is too much, email the feed URL and a short description to <submission@nuchronic.uk> — or message thechelsuk on social media.

## Buttons

Old-school 88×31 buttons, for anyone who wants to link back to Nuchronic from their own site. Click Copy and paste the HTML wherever your site takes it.

{% capture dark_snippet %}<a href="{{ '/' | absolute_url }}" title="Nuchronic — a Hacker News-style feed for the chronically ill indie web"><img src="{{ '/assets/buttons/nuchronic-88x31-dark.png' | absolute_url }}" srcset="{{ '/assets/buttons/nuchronic-88x31-dark@2x.png' | absolute_url }} 2x" width="88" height="31" alt="Nuchronic — a Hacker News-style feed for the chronically ill indie web"></a>{% endcapture %}

<div class="button-row">
  <img src="{{ '/assets/buttons/nuchronic-88x31-dark.png' | absolute_url }}" srcset="{{ '/assets/buttons/nuchronic-88x31-dark@2x.png' | absolute_url }} 2x" width="88" height="31" alt="Nuchronic — a Hacker News-style feed for the chronically ill indie web">
  {% include copy-snippet.html id="snippet-dark" code=dark_snippet %}
</div>

{% capture tile_snippet %}<a href="{{ '/' | absolute_url }}" title="Nuchronic — a Hacker News-style feed for the chronically ill indie web"><img src="{{ '/assets/buttons/nuchronic-88x31-tile.png' | absolute_url }}" srcset="{{ '/assets/buttons/nuchronic-88x31-tile@2x.png' | absolute_url }} 2x" width="88" height="31" alt="Nuchronic — a Hacker News-style feed for the chronically ill indie web"></a>{% endcapture %}

<div class="button-row">
  <img src="{{ '/assets/buttons/nuchronic-88x31-tile.png' | absolute_url }}" srcset="{{ '/assets/buttons/nuchronic-88x31-tile@2x.png' | absolute_url }} 2x" width="88" height="31" alt="Nuchronic — a Hacker News-style feed for the chronically ill indie web">
  {% include copy-snippet.html id="snippet-tile" code=tile_snippet %}
</div>

## Removals

To remove your feed, email <removals@nuchronic.uk>
