"""Make a copy of the Sensor Orthogonal Reconstruction blueprints with the math in MathML.

Usage: python3 -I copy_sor_blueprints_mathml.py <folder with the four saved pages> <output folder>

The four pages are index.html, theory.html, theory2.html, and software-architecture.html, as read
from https://claude.ai/artifact/648swpno4LjUtjvxwcf8jS.  The script changes only the math markup:
symbols and formulas in the text become inline MathML, and each displayed equation becomes an
mtable aligned at its relation sign.  Diagrams and pseudo-code are left as they are.  The script
prints every piece of text that it converted, so that the result can be checked.
"""
import os
import re
import sys

SRC, OUT = sys.argv[1], sys.argv[2]
ORIGINAL_URL = 'https://claude.ai/artifact/648swpno4LjUtjvxwcf8jS'

# Private markers that stand for the sub and sup tags while the text is scanned.
SUB, SUP, END = '', '', ''
TILDE, MACRON = '̃', '̄'

MATH_CSS = ('math { font-family: "STIX Two Math", "Latin Modern Math", "Cambria Math", math; font-size: 1.05em; '
            'white-space: nowrap; }\n'
            '.eq math { font-size: 18px; }\n'
            'mtd { padding: 0.25em 0.3em; }\n'
            'mtd.l { text-align: left; }\n'
            'mtd.r { text-align: right; }\n'
            '.eq.numbered { display: grid; grid-template-columns: 1fr auto; align-items: center; }\n'
            '.eqno { font-family: var(--sans); padding-left: 12px; }\n')

UPPER = 'XPBHCQRIWLFGMZKVYN'
LOWER = 'pdmtvjkuw'
GREEK = 'θμβρλΛαφπ'
FUNCS = ('argmin', 'argmax', 'cos', 'sin', 'span', 'diag', 'tr')

TOKEN = re.compile(
    '(?P<script>[' + SUB + SUP + '][^' + END + ']*' + END + ')'
    r'|(?P<func>(?<![A-Za-z])(?:' + '|'.join(FUNCS) + r')(?![A-Za-z]))'
    r"|(?P<sym>(?<![A-Za-z'’])[" + UPPER + LOWER + r'][' + TILDE + MACRON + r']?(?![A-Za-z0-9_])'
    r'|(?<![A-Za-z0-9])D(?![A-Za-z0-9_])'
    r'|[' + GREEK + r']'
    r'|(?<![A-Za-z])x' + MACRON + r'|(?<![A-Za-z])[xg](?=' + SUB + r')|(?<![A-Za-z])h(?=\())'
    r'|(?P<num>\d+(?:\.\d+)?)'
    r'|(?P<op>=|−|\+|×|·|/|…|≤|≥|←|⊂|&lt;)'
    r'|(?P<comma>,)|(?P<open>\()|(?P<close>\))|(?P<norm>‖)|(?P<space> )')


def tokens_of(text, start, stop_at_close=False):
    """Return the math tokens from ``start`` and the index where they end.

    A parenthesis is taken only when the whole group up to its closing parenthesis is math.
    A comma is taken only inside such a group.
    """
    tokens, k = [], start
    while k < len(text):
        m = TOKEN.match(text, k)
        if not m:
            break
        kind = m.lastgroup
        if kind == 'close':
            if stop_at_close:
                return tokens, k
            break
        if kind == 'comma' and not stop_at_close:
            break
        if kind == 'open':
            inner, end = tokens_of(text, m.end(), stop_at_close=True)
            if end >= len(text) or text[end] != ')' or not any(t[0] != 'space' for t in inner):
                break
            tokens.append(('group', inner))
            k = end + 1
            continue
        tokens.append((kind, m.group()))
        k = m.end()
    if stop_at_close:
        return tokens, k            # the caller checks for the closing parenthesis
    return tokens, k


def flat(tokens):
    """The token kinds of a list, with the tokens inside groups."""
    for kind, value in tokens:
        if kind == 'group':
            yield from flat(value)
        else:
            yield kind


def length(tokens):
    return sum(len(v) if k != 'group' else length(v) + 2 for k, v in tokens)


def find_run(text, start):
    """Return the tokens of a math run that starts at ``start``, or None."""
    m = TOKEN.match(text, start)
    if not m or m.lastgroup not in ('sym', 'num', 'func', 'open', 'norm'):
        return None
    if m.lastgroup == 'num' and start > 0 and re.match(r'[A-Za-z0-9.\-]', text[start - 1]):
        return None
    tokens, _ = tokens_of(text, start)
    # A run does not end with a space, an operator, or an open norm bar.
    while tokens:
        kinds = [k for k, _ in tokens]
        if kinds[-1] in ('space', 'op', 'comma') or (kinds[-1] == 'norm' and kinds.count('norm') % 2):
            tokens.pop()
        else:
            break
    if not tokens or [k for k, _ in tokens].count('norm') % 2:
        return None
    kinds = list(flat(tokens))
    if 'sym' not in kinds and 'script' not in kinds:
        return None
    return tokens


# ---------- MathML ----------
def mi(s, normal=False):
    return f'<mi mathvariant="normal">{s}</mi>' if normal else f'<mi>{s}</mi>'


def mo(s, plain=False):
    return f'<mo stretchy="false">{s}</mo>' if plain else f'<mo>{s}</mo>'


def mtext(s):
    return '<mtext>' + s.replace(' ', '&#160;') + '</mtext>'


def row(*parts):
    return '<mrow>' + ''.join(parts) + '</mrow>'


def script_content(s):
    """The MathML of what stands inside a sub or sup tag."""
    if re.fullmatch(r'[a-z]{2,}(-[a-z]+)?', s):
        return mtext(s)
    parts = []
    for piece in re.findall(r'\d+|.', s):
        if piece.isdigit():
            parts.append(f'<mn>{piece}</mn>')
        elif piece in '*−+':
            parts.append(mo(piece))
        elif piece != ' ':
            parts.append(mi(piece, normal=piece == 'Λ'))
    return parts[0] if len(parts) == 1 else row(*parts)


def symbol(s):
    if s.endswith(TILDE):
        return f'<mover accent="true">{mi(s[0])}<mo>~</mo></mover>'
    if s.endswith(MACRON):
        return f'<mover accent="true">{mi(s[0])}<mo>&#x203E;</mo></mover>'
    return mi(s, normal=s == 'Λ')


# A space between two factors of a product becomes a thin space, so that "1 1^T" does not read
# as eleven.
THIN_SPACE = '<mspace width="0.2em"></mspace>'
FACTOR_BEFORE = {'sym', 'num', 'script', 'group', 'norm'}
FACTOR_AFTER = {'sym', 'num', 'group', 'norm', 'func'}


def build(tokens):
    """Return the MathML of a list of tokens."""
    atoms, i = [], 0
    while i < len(tokens):
        kind, value = tokens[i]
        if kind == 'space':
            if (0 < i < len(tokens) - 1 and tokens[i - 1][0] in FACTOR_BEFORE
                    and tokens[i + 1][0] in FACTOR_AFTER):
                atoms.append(THIN_SPACE)
        elif kind == 'script':
            scripts = {value[0]: script_content(value[1:-1])}
            if i + 1 < len(tokens) and tokens[i + 1][0] == 'script' and tokens[i + 1][1][0] not in scripts:
                i += 1
                scripts[tokens[i][1][0]] = script_content(tokens[i][1][1:-1])
            base = atoms.pop() if atoms else row()
            if len(scripts) == 2:
                atoms.append(f'<msubsup>{base}{scripts[SUB]}{scripts[SUP]}</msubsup>')
            elif SUB in scripts:
                tag = 'munder' if base.startswith('<mtext>arg') else 'msub'
                atoms.append(f'<{tag}>{base}{scripts[SUB]}</{tag}>')
            else:
                atoms.append(f'<msup>{base}{scripts[SUP]}</msup>')
        elif kind == 'group':
            atoms.append(row(mo('(', True), build(value), mo(')', True)))
        elif kind == 'norm':
            j = next(n for n in range(i + 1, len(tokens)) if tokens[n][0] == 'norm')
            atoms.append(row(mo('‖'), build(tokens[i + 1:j]), mo('‖')))
            i = j
        elif kind == 'func':
            if value in ('argmin', 'argmax'):
                atoms.append(mtext('arg ' + value[3:]))
            else:
                atoms.append(mi(value, normal=True) + '<mo>&#8289;</mo>')
        elif kind == 'sym':
            atoms.append(symbol(value))
        elif kind == 'num':
            atoms.append(f'<mn>{value}</mn>')
        elif kind in ('op', 'comma'):
            atoms.append(mo(value))
        i += 1
    return ''.join(atoms)


def to_markers(text):
    text = re.sub(r'<sub>(.*?)</sub>', lambda m: SUB + m.group(1) + END, text)
    return re.sub(r'<sup>(.*?)</sup>', lambda m: SUP + m.group(1) + END, text)


def from_markers(text):
    return re.sub('([' + SUB + SUP + '])([^' + END + ']*)' + END,
                  lambda m: ('<sub>' if m.group(1) == SUB else '<sup>') + m.group(2)
                  + ('</sub>' if m.group(1) == SUB else '</sup>'), text)


def plain(text):
    """The marker text as a person would read it, for the check list."""
    return text.replace(SUB, '_').replace(SUP, '^').replace(END, '')


WORD = re.compile(r'[A-Za-z][A-Za-z0-9_]+')


def convert_text(text, log):
    out, i = [], 0
    while i < len(text):
        # A word of letters and digits, such as mace4d, is copied whole.  Its letters are not symbols.
        word = WORD.match(text, i) if (i == 0 or not re.match(r'[A-Za-z0-9_]', text[i - 1])) else None
        if word and word.group() not in FUNCS:
            out.append(word.group())
            i = word.end()
            continue
        tokens = find_run(text, i)
        if tokens:
            n = length(tokens)
            log.append(plain(text[i:i + n]))
            out.append('<math>' + build(tokens) + '</math>')
            i += n
        else:
            out.append(text[i])
            i += 1
    return ''.join(out)


SKIP = {'code', 'pre', 'svg', 'style', 'title', 'math', 'script'}


def convert_body(body, log):
    """Convert the math in the text of a page body, outside code, diagrams, and equations."""
    body = to_markers(body)
    parts = re.split(r'(<[^>]+>)', body)
    depth, out = 0, []
    for part in parts:
        if part.startswith('<'):
            name = re.match(r'</?\s*([A-Za-z0-9]+)', part)
            name = name.group(1).lower() if name else ''
            if name in SKIP and not part.endswith('/>'):
                depth += -1 if part.startswith('</') else 1
            out.append(part)
        elif depth:
            out.append(part)
        else:
            out.append(convert_text(part, log))
    return from_markers(''.join(out))


def formula(spec):
    """The MathML of one side of an equation row, written with _{...} and ^{...} scripts.

    A leading TEXT{...} gives words that stand before the formula.
    """
    words = ''
    m = re.match(r'TEXT\{(.*?)\} ?', spec)
    if m:
        words, spec = mtext(m.group(1) + ' '), spec[m.end():]
    spec = re.sub(r'_\{(.*?)\}', lambda s: SUB + s.group(1) + END, spec)
    spec = re.sub(r'\^\{(.*?)\}', lambda s: SUP + s.group(1) + END, spec)
    tokens, end = tokens_of(spec, 0)
    assert end == len(spec), (spec, end)
    return words + build(tokens)


def equation(rows, number=None):
    body = ''.join(f'<mtr>\n<mtd class="r">{formula(left)}</mtd>\n<mtd class="l">{formula(right)}</mtd>\n</mtr>\n'
                   for left, right in rows)
    math = ('<math display="block">\n<mtable columnalign="right left" displaystyle="true">\n'
            + body + '</mtable>\n</math>')
    if number is None:
        return f'<div class="eq">{math}</div>'
    return f'<div class="eq numbered">{math}<span class="eqno">({number})</span></div>'


EQUATIONS = {
    'theory.html': [
        equation([('h(θ_{t})', '= (cos θ_{t}, sin θ_{t}, cos 2θ_{t}, sin 2θ_{t}, …, cos pθ_{t}, sin pθ_{t})')]),
        equation([('H', '= I − (1/N_{t}) 1 1^{T}')]),
        equation([('B_{c}', '= H B'), ('TEXT{so that} 1^{T} B_{c}', '= (H 1)^{T} B = 0')]),
        equation([('C^{*}', '= argmin_{C} ‖X − C B_{c}^{T}‖_{F}^{2}')], 1),
        equation([('C^{*}', '= X B_{c} (B_{c}^{T} B_{c})^{−1}')], 2),
        equation([('X' + TILDE, '= X − C^{*} B_{c}^{T}')], 3),
        equation([('X' + TILDE, '= X P'), ('P', '= I − Q_{B} Q_{B}^{T}')], 4),
    ],
    'theory2.html': [
        equation([('Q^{*}', '= argmax_{Q} ‖X Q‖_{F}^{2}'), ('TEXT{subject to} Q^{T} Q', '= I_{d}'),
                  ('span(Q)', '⊂ span(B_{c})')], 1),
        equation([('‖X Q‖_{F}^{2}', '= tr(V^{T} K V)'), ('K', '= Q_{B}^{T} X^{T} X Q_{B}')], 2),
        equation([('Q^{*}', '= Q_{B} V_{d}')], 3),
        equation([('X' + TILDE, '= X P'), ('P', '= I − Q^{*} Q^{*T}'),
                  ('', '= I − Q_{B} V_{d} V_{d}^{T} Q_{B}^{T}')], 4),
    ],
}

# Text that the scanner cannot read as math on its own.  Each entry is replaced before the scan.
ONE = '<math><mn>1</mn></math>'
A_OP = '<math><mi>A</mi></math>'
SPECIAL = {
    'theory.html': [
        ('1 is the all-ones vector of length', ONE + ' is the all-ones vector of length'),
        ('the de-jitter operator A; version IV, A D(A W<sub>k</sub>) with L unfiltered',
         'the de-jitter operator ' + A_OP + '; version IV, <math><mi>A</mi><mi>D</mi><mo stretchy="false">(</mo>'
         '<mi>A</mi><msub><mi>W</mi><mi>k</mi></msub><mo stretchy="false">)</mo></math> with L unfiltered'),
    ],
}


def inner_document(text):
    """The saved front page holds the published wrapper around the page.  Return the page."""
    starts = [m.start() for m in re.finditer(r'<!DOCTYPE html>', text, re.I)]
    if len(starts) < 2:
        return text
    return text[starts[1]:text.index('</html>', starts[1]) + len('</html>')] + '\n'


os.makedirs(OUT, exist_ok=True)
for name in ('index.html', 'theory.html', 'theory2.html', 'software-architecture.html'):
    text = inner_document(open(os.path.join(SRC, name), encoding='utf-8').read())
    head, body = text[:text.index('<body')], text[text.index('<body'):]
    for old, new in SPECIAL.get(name, []):
        assert body.count(old) == 1, (name, old[:40], body.count(old))
        body = body.replace(old, new)
    # The displayed equations are set from the list above, in the order of the page.
    found = re.findall(r'<div class="eq"[^>]*>.*?</div>', body, re.S)
    wanted = EQUATIONS.get(name, [])
    assert len(found) == len(wanted), (name, len(found), len(wanted))
    for index, old in enumerate(found):
        body = body.replace(old, f'{index}', 1)
    log = []
    body = convert_body(body, log)
    for index, new in enumerate(wanted):
        body = body.replace(f'{index}', new)
    if name == 'index.html':
        old = ('Decisions and rejected alternatives are recorded, with dates, in <code>decisions.md</code>.')
        assert body.count(old) == 1
        body = body.replace(old, 'Decisions and rejected alternatives are recorded, with dates, at the end of '
                            'each page. This set is a copy of the blueprints at <a href="' + ORIGINAL_URL + '">'
                            + ORIGINAL_URL + '</a>, made on 2026-11-25 with the math rewritten in MathML. The '
                            'file <code>decisions.md</code> of the original set is not part of the copy.')
    assert head.count('</style>') == 1, name
    head = head.replace('</style>', MATH_CSS + '</style>')
    with open(os.path.join(OUT, name), 'w', encoding='utf-8') as f:
        f.write(head + body)
    print(f'===== {name}: {len(log)} pieces of text converted, {len(wanted)} equations')
    seen = {}
    for item in log:
        seen[item] = seen.get(item, 0) + 1
    print('   ' + ' | '.join(f'{k}' + (f' x{v}' if v > 1 else '') for k, v in seen.items()))
