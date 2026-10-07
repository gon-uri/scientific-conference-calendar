# Sharing Copy And Controls

Approved: 2026-10-07

## Selected Text

Check out Venue Radar, a new conference calendar for ML/AI and related fields.
Search and filter submission deadlines, compare ICORE/CCF rankings, and check
historical acceptance rates.

The Share on X link appends https://gon-uri.github.io/venue-radar/ as a separate
URL parameter. It opens a draft for the visitor to review and post; loading
Venue Radar does not contact X or publish a post. The button uses a local
Lucide share icon instead of an embedded social-media widget.

## Alternative Text

Where should your next paper go? Venue Radar brings conference deadlines, topic
filters, search, ICORE/CCF rankings, and historical acceptance rates together
in one place.

Both candidates are comfortably below a standard 280-character post with the
website link. The first was selected by the user. Rates remain described as
historical, not as predicted acceptance probabilities.

## Maintenance

Edit `SHARE_TEXT` and `SITE_URL` in `scripts/build_site.py`, rebuild, and check
the decoded intent parameters, punctuation/URL encoding and total post length.
Browser/Python checks verify the selected copy and new-tab protections without
posting. The Star the repo link opens gon-uri/venue-radar on GitHub; the visitor
decides whether to star it. Existing footer follow/star links remain available.

Header actions are ordered Share on X, Star the repo, then All events (.ics).
Download calendar appears below the last button. Buttons align along the top
on desktop; mobile wraps them while keeping the download action last/rightmost.

The favicon is maintained separately in `assets/favicon.svg`: radar arcs, sweep
and location dot on opaque white. It is embedded in the generated HTML and
does not replace the full calendar/radar logo in the header or README.
