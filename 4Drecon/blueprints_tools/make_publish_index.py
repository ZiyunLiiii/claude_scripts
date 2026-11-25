"""Make the publish copy of the front page of a set of blueprints.

The Artifact publish step adds its own document skeleton, so the copy keeps only the title, the
style, and the content of the front page.  The other pages of a set are published as they are.

Usage: python3 -I make_publish_index.py <index.html> <publish/index.html> "<title of the artifact>"
"""
import re
import sys

src, out, title = sys.argv[1], sys.argv[2], sys.argv[3]
text = open(src, encoding='utf-8').read()


def swap(old, new):
    global text
    assert text.count(old) == 1, (old[:50], text.count(old))
    text = text.replace(old, new)


text = text[text.index('<title>'):]
text = re.sub(r'<title>.*?</title>',
              lambda _: f'<title>{title}</title>\n<meta name="claude:viewport-fit-sides" content="cover">',
              text, count=1, flags=re.S)
swap('</style>\n</head>\n<body>\n', '</style>\n')
swap('</div>\n</body>\n</html>\n', '</div>\n')
swap('padding-inline: 16px; padding-block: 36px 64px;',
     'padding-left: max(16px, env(safe-area-inset-left, 0px)); '
     'padding-right: max(16px, env(safe-area-inset-right, 0px)); padding-block: 36px 64px;')
# The published set has no decisions.md beside it, so the foot points to the section on each page.
foot = 'Decisions and rejected alternatives are recorded, with dates, in\n<code>decisions.md</code>.'
if foot in text:
    swap(foot, 'Decisions and rejected alternatives are recorded, with dates, at the end of each page.')
open(out, 'w', encoding='utf-8').write(text)
