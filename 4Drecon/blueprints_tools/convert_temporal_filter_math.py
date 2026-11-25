"""Rewrite the math of the 4D MACE temporal filter blueprints in MathML.

Usage: python3 -I convert_temporal_filter_math.py <blueprint folder>

The Theory page gets new sections 1 to 3 with MathML equations and symbols.  The other pages get
their symbols as inline MathML.  Every page gets the math style rules of the blueprints kit.
"""
import os
import re
import sys

FOLDER = sys.argv[1]

MATH_CSS = ('math { font-family: "STIX Two Math", "Latin Modern Math", "Cambria Math", math; font-size: 1.05em; }\n'
            '.eq math { font-size: 18px; }\n'
            'mtd { padding: 0.25em 0.3em; }\n'
            'mtd.l { text-align: left; }\n'
            'mtd.r { text-align: right; }\n')


# ---------- MathML helpers ----------
def mi(s, normal=False):
    return f'<mi mathvariant="normal">{s}</mi>' if normal else f'<mi>{s}</mi>'


def mn(s):
    return f'<mn>{s}</mn>'


def mo(s, plain=False):
    return f'<mo stretchy="false">{s}</mo>' if plain else f'<mo>{s}</mo>'


def mtext(s):
    return '<mtext>' + s.replace(' ', '&#160;') + '</mtext>'


def row(*parts):
    return '<mrow>' + ''.join(parts) + '</mrow>'


def sub(a, b):
    return f'<msub>{a}{b}</msub>'


def sup(a, b):
    return f'<msup>{a}{b}</msup>'


def subsup(a, b, c):
    return f'<msubsup>{a}{b}{c}</msubsup>'


def m(*parts):
    return '<math>' + ''.join(parts) + '</math>'


def eq(*rows):
    body = ''.join(f'<mtr>\n<mtd class="r">{left}</mtd>\n<mtd class="l">{right}</mtd>\n</mtr>\n'
                   for left, right in rows)
    return ('<div class="eq"><math display="block">\n<mtable columnalign="right left" displaystyle="true">\n'
            + body + '</mtable>\n</math></div>')


# ---------- Symbols ----------
X, F, P, C, M, B, I, Q, N = (mi(c) for c in 'XFPCMBIQN')
x, p, t, mm, a, b = (mi(c) for c in 'xptmab')
theta = mi('θ')
T = mi('T')
Nt, Nv = sub(N, t), sub(N, mi('v'))
QB, Bc = sub(Q, B), sub(B, mi('c'))
QBT = subsup(Q, B, T)
theta_t = sub(theta, t)
Xtilde = '<mover accent="true"><mi>X</mi><mo>~</mo></mover>'
APPLY = '<mo>&#8289;</mo>'


def fn(name, *argument):
    """A named function applied to its argument, such as cos m theta."""
    return mi(name, normal=True) + APPLY + row(*argument)


def equals(left, value):
    return m(left, mo('='), mn(str(value)))


P_FORMULA = P + mo('=') + I + mo('−') + QB + QBT
EQ_FILTER = eq((Xtilde, mo('=') + X + F))
EQ_JITTER = eq((mtext('jitter') + mo('(', True) + theta + mo(')', True),
                mo('=') + f'<munderover><mo>∑</mo>{row(mm, mo("="), mn("1"))}{p}</munderover>'
                + mo('[') + sub(a, mm) + fn('cos', mm, theta) + mo('+') + sub(b, mm) + fn('sin', mm, theta)
                + mo(']')))

SECTIONS_1_TO_3 = f'''<h2>1. One matrix along the frame axis</h2>
<p>A 4D reconstruction is written here as a matrix {m(X)} with one row for each voxel and one column for each
frame, of size {m(Nv, mo('×'), Nt)}. Each frame is reconstructed from a different arc of view angles. {m(X)}
therefore changes from frame to frame in a way that the object does not. The temporal filter is one
{m(Nt, mo('×'), Nt)} matrix {m(F)}, applied along the frame axis:</p>
{EQ_FILTER}
<p>The pull request changes how {m(F)} is built. It changes nothing else in the computation.</p>

FIGURE_GOES_HERE

<h2>2. The two filters</h2>
<div class="tablewrap"><table>
<tr><th></th><th>DCT filter (before)</th><th>SOR filter (after)</th></tr>
<tr><td><b>Matrix</b></td>
  <td>{m(F, mo('='), sup(C, T), M, C)}. {m(C)} is the type-I DCT along the frames. {m(M)} sets to zero the
  modes at the period and at its harmonics, and one mode on each side of each.</td>
  <td>{m(F, mo('='), P_FORMULA)}. The columns of {m(QB)} are an orthonormal basis of {m(fn('cos', mm, theta))}
  and {m(fn('sin', mm, theta))}, {m(mm, mo('='), mn('1'), mo(','), mo('…'), mo(','), p)}, with their means removed.</td></tr>
<tr><td><b>Needs</b></td>
  <td>{m(Nt)} and the period in frames, which is the number of frames per rotation</td>
  <td>{m(theta)}, the sensor angle of each frame (the center of its arc), and {m(p)}, the highest harmonic removed</td></tr>
<tr><td><b>Assumes</b></td>
  <td>The change repeats every period frames.</td>
  <td>The change is a function of {m(theta)}.</td></tr>
<tr><td><b>Mean over the frames</b></td>
  <td>Changed. The rows of {m(F)} do not sum to 1.</td>
  <td>Kept. The rows of {m(P)} sum to 1.</td></tr>
<tr><td><b>Modes removed</b>, 99 frames at 6 per rotation</td><td>8</td><td>5 ({equals(p, 3)})</td></tr>
<tr><td><b>Modes removed</b>, 199 frames at 12 per rotation</td><td>17</td><td>6 ({equals(p, 3)}), 11 ({equals(p, 6)})</td></tr>
</table></div>
<p>A harmonic that repeats other harmonics at the frame angles adds no column to {m(QB)}. At 6 frames per
rotation, {m(fn('sin', mn('3'), theta))} repeats {m(fn('cos', mn('3'), theta))}, so {equals(p, 3)} removes 5 modes
and not 6. The derivation is in the earlier
<a style="color: var(--accent)" href="https://claude.ai/artifact/648swpno4LjUtjvxwcf8jS">SOR blueprints</a>.</p>

<h2>3. How the SOR matrix is built</h2>
<p>The jitter at one voxel is modeled as a function of the sensor angle {m(theta)} of the frame, written as a sum
of harmonics with the coefficients {m(sub(a, mm))} and {m(sub(b, mm))}. The constant term is left out, because it
is the mean over the frames, and the mean is signal.</p>
{EQ_JITTER}
<p><code>gen_sor_filter_matrix(angles, order)</code> builds {m(P)} in four steps:</p>
<ol>
  <li>Build the harmonic matrix {m(B)}, of size {m(Nt, mo('×'), mn('2'), p)}. Its columns are
  {m(fn('cos', mm, theta_t))} and {m(fn('sin', mm, theta_t))} for {m(mm, mo('='), mn('1'))} to {m(p)}, where
  {m(theta_t)} is the sensor angle of frame {m(t)}.</li>
  <li>Subtract from each column its mean. This gives {m(Bc)}.</li>
  <li>Take an orthonormal basis {m(QB)} of the columns of {m(Bc)}, by an SVD. A column with a relative singular
  value below 1e-4 is left out.</li>
  <li>{m(P_FORMULA)}.</li>
</ol>
<p>Each row of {m(X)} holds the values of one voxel over the frames. The product {m(X, P)} replaces each row by
the row minus its least-squares fit by the harmonics.</p>
<ul>
  <li><b>{m(P)} keeps the mean over the frames.</b> Step 2 makes every column orthogonal to the constant vector.</li>
  <li><b>Applying {m(P)} twice gives the same result as applying it once.</b></li>
  <li><b>{m(P)} removes at most {m(mn('2'), p)} of the {m(Nt)} directions along the frame axis.</b> Its trace is
  the number that it keeps.</li>
  <li><b>{m(P)} does not depend on the data.</b> It depends only on the frame angles and {m(p)}.
  <code>recon</code> builds it once, before the loop, and no voxel is fitted on its own.</li>
  <li><b>The two filters cost the same in the loop.</b> The DCT matrix was also built once, and both matrices are
  applied by the same code. One run of Phantom_30s_Run1 on Delta, with 199 frames and 10 iterations, took 1 h 35 min
  with the DCT filter and 1 h 30 min with SOR.</li>
  <li><b>The cost to the image.</b> Motion of the object that follows the harmonics of {m(theta)} is removed too.
  With many frames this is a small part: 5 of 99 directions at 6 frames per rotation.</li>
</ul>

'''


def add_math_css(text):
    if 'mtd.r' in text:
        return text
    assert text.count('</style>') == 1
    return text.replace('</style>', MATH_CSS + '</style>')


def swap(text, old, new):
    assert text.count(old) == 1, (old[:60], text.count(old))
    return text.replace(old, new)


# ---------- Theory page ----------
path = os.path.join(FOLDER, 'theory.html')
text = open(path, encoding='utf-8').read()
if '<math' not in text:
    start = text.index('<h2>1. One matrix along the frame axis</h2>')
    end = text.index('<h2>4. Measurements</h2>')
    figure = re.search(r'<figure>.*?</figure>', text[start:end], re.S).group(0)
    text = text[:start] + SECTIONS_1_TO_3.replace('FIGURE_GOES_HERE', figure) + text[end:]
    text = swap(text, '<th>SOR, p = 3</th>', f'<th>SOR, {equals(p, 3)}</th>')
    text = swap(text, 'Those runs exist, with p = 6, and are not scored.',
                f'Those runs exist, with {equals(p, 6)}, and are not scored.')
    text = swap(text, '<b>Default p.</b> p = 3.</label>', f'<b>Default {m(p)}.</b> {equals(p, 3)}.</label>')
    text = swap(text, '<b>p and the frames per rotation.</b> p is its own number.',
                f'<b>{m(p)} and the frames per rotation.</b> {m(p)} is its own number.')
    text = swap(text, 'Every harmonic up to p is removed completely.',
                f'Every harmonic up to {m(p)} is removed completely.')
    text = swap(text, 'the sensor angle &theta; of each frame.</figcaption>',
                f'the sensor angle {m(theta)} of each frame.</figcaption>')
    text = swap(text, 'Both filters give one matrix F.', f'Both filters give one matrix {m(F)}.')
    text = add_math_css(text)
    open(path, 'w', encoding='utf-8').write(text)
    print('theory.html rewritten')


# ---------- The other pages: symbols in the text become inline MathML ----------
SKIP = {'code', 'pre', 'svg', 'style', 'title', 'math', 'script'}
TOKEN = re.compile(r'(?<![A-Za-z0-9_&;])([FPp])(?![A-Za-z0-9_])')


def symbols_to_math(text):
    text = text.replace('N<sub>t</sub>', m(Nt)).replace('&theta;', m(theta))
    parts = re.split(r'(<[^>]+>)', text)
    depth, out, count = 0, [], 0
    for part in parts:
        if part.startswith('<'):
            name = re.match(r'</?\s*([A-Za-z0-9]+)', part)
            name = name.group(1).lower() if name else ''
            if name in SKIP and not part.endswith('/>'):
                depth += -1 if part.startswith('</') else 1
            out.append(part)
        elif depth > 0:
            out.append(part)
        else:
            new, n = TOKEN.subn(lambda mt: m(mi(mt.group(1))), part)
            count += n
            out.append(new)
    return ''.join(out), count


for name in ('software-architecture.html', 'user-api.html'):
    path = os.path.join(FOLDER, name)
    text = open(path, encoding='utf-8').read()
    if '<math' in text:
        continue
    head, body = text[:text.index('<body>')], text[text.index('<body>'):]
    body, count = symbols_to_math(body)
    open(path, 'w', encoding='utf-8').write(add_math_css(head) + body)
    print(name, 'symbols converted:', count)
