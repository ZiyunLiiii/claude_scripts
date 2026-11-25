"""Build the 4D CT reconstruction blueprints from the templates of the blueprints kit.

Usage: python3 -I build_4dct_blueprints.py <kit folder> <output folder>

The head and the style of each page come from the kit's templates.  The equations are MathML.
"""
import os
import re
import sys

KIT, OUT = sys.argv[1], sys.argv[2]
NAME = '4D CT Reconstruction'
TITLE = 'Software blueprint: ' + NAME


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


def frac(a, b):
    return f'<mfrac>{a}{b}</mfrac>'


def paren(*parts):
    return mo('(', True) + ''.join(parts) + mo(')', True)


def norm(*parts):
    return row(mo('‖'), *parts, mo('‖'))


def m(*parts):
    """Inline math."""
    return '<math>' + ''.join(parts) + '</math>'


def eq(*rows):
    """A displayed equation.  Each row is a pair (left side, right side with its relation)."""
    body = ''.join(f'<mtr>\n<mtd class="r">{left}</mtd>\n<mtd class="l">{right}</mtd>\n</mtr>\n'
                   for left, right in rows)
    return ('<div class="eq"><math display="block">\n<mtable columnalign="right left" displaystyle="true">\n'
            + body + '</mtable>\n</math></div>')


# ---------- Symbols ----------
x, y, w, v, u, z, h, f, t, s, k = (mi(c) for c in 'xywvuzhftsk')
A, F, H, N = (mi(c) for c in 'AFHN')
Nt = sub(N, t)
xt, yt, At, ft, ut = sub(x, t), sub(y, t), sub(A, t), sub(f, t), sub(u, t)
Lt = sub(mi('Λ', normal=True), t)
sy, sp, sn, sx = (sub(mi('σ'), mi(c)) for c in 'ypnx')
mu_k, wk, vk, Hk = sub(mi('μ'), k), sub(w, k), sub(v, k), sub(H, k)
rho = sub(mi('ρ'), mtext('Mann'))
xbar = '<mover accent="true"><mi>x</mi><mo>&#x203E;</mo></mover>'
x0 = sup(x, paren(mn('0')))
wtilde_k = sub('<mover accent="true"><mi>w</mi><mo>~</mo></mover>', k)
argmin = '<munder>' + mtext('arg min') + x + '</munder>'
theta, p_order, m_index, Q, B, I = mi('θ'), mi('p'), mi('m'), mi('Q'), mi('B'), mi('I')
theta_t = sub(theta, t)
QB, QBT = sub(Q, B), subsup(Q, B, mi('T'))


def fn(name, *argument):
    return mi(name, normal=True) + '<mo>&#8289;</mo>' + row(*argument)


def pair(a, b):
    return row(a, mo(','), b)


def sum_over(index, first, last):
    return f'<munderover><mo>∑</mo>{row(index, mo("="), first)}{last}</munderover>'


half_over = lambda sigma: frac(mn('1'), row(mn('2'), subsup(mi('σ'), sigma, mn('2'))))

EQ_FORWARD = eq((ft + paren(xt),
                 mo('=') + half_over(mi('y')) + subsup(norm(yt, mo('−'), At, xt), Lt, mn('2'))))
EQ_PROX = eq((ut,
              mo('=') + argmin + mo('{') + ft + paren(x) + mo('+') + half_over(mi('p'))
              + sup(norm(x, mo('−'), sub(w, pair(mn('0'), t))), mn('2')) + mo('}')))
EQ_DENOISER = eq((H + paren(w),
                  mo('=') + argmin + mo('{') + half_over(mi('n')) + sup(norm(w, mo('−'), x), mn('2'))
                  + mo('+') + h + paren(x) + mo('}')))
EQ_ITERATION = eq(
    (z, mo('=') + sum_over(k, mn('0'), mn('3')) + mu_k + paren(mn('2'), vk, mo('−'), wk)),
    (wk, mo('←') + wk + mo('+') + mn('2') + rho + paren(z, mo('−'), vk)),
    (xbar, mo('=') + sum_over(k, mn('0'), mn('3')) + mu_k + vk))
EQ_FILTER_FIT = eq((sub(v, pair(mn('0'), t)),
                    mo('=') + sum_over(s, mn('1'), Nt) + sub(F, pair(t, s)) + sub(u, s)))
EQ_SOR = eq((F, mo('=') + I + mo('−') + QB + QBT))
EQ_FILTER_PRIOR = eq(
    (sub('<mover accent="true"><mi>w</mi><mo>~</mo></mover>', pair(k, t)),
     mo('=') + sum_over(s, mn('1'), Nt) + sub(F, pair(t, s)) + sub(w, pair(k, s))),
    (vk, mo('=') + Hk + paren(wtilde_k)))

THEORY_BODY = f'''<h1>Theory</h1>
<p class="lead">What 4D CT reconstruction computes: one volume for each time frame, as the consensus of one data-fit agent and three prior agents.</p>

<h2>1. The time frames</h2>
<p>One continuous scan of a moving object gives a sinogram {m(y)} whose views are in time order. The scan is
divided into {m(Nt)} overlapping time frames of consecutive views. A new frame starts every
360 / <code>frames_per_rotation</code> degrees, and each frame spans <code>frame_overlap_factor</code> of these
steps.</p>
<p>The reconstruction is a 4D image {m(x)} with one volume {m(xt)} for each frame, {m(t, mo('='), mn('1'), mo(','), mo('…'), mo(','), Nt)}.
The symbols follow the theory page of the mbirtorch documentation. The table lists every quantity by kind.</p>
<div class="tablewrap"><table>
<tr><th>Kind</th><th>Quantity</th><th>In the code</th></tr>
<tr><td>Measured data</td><td>the sinogram {m(yt)} and the weights {m(Lt)} of the views of frame {m(t)}</td>
  <td><code>sinogram[view_slices[t]]</code>, <code>weights[view_slices[t]]</code></td></tr>
<tr><td>Forward model</td><td>the projector {m(At)} of the view angles of frame {m(t)}, and the noise level {m(sy)}</td>
  <td><code>model_list[t]</code></td></tr>
<tr><td>Unknown</td><td>the 4D image {m(x)}, an array with one frame axis and three spatial axes</td>
  <td>the array that <code>recon</code> returns</td></tr>
<tr><td>Run state</td><td>the input {m(wk)} and the output {m(vk)} of agent {m(k)}, and the consensus image {m(xbar)}</td>
  <td><code>MACE.W</code>, <code>MACE.x_bar</code></td></tr>
<tr><td>Temporal filter</td><td>the {m(Nt, mo('×'), Nt)} matrix {m(F)}, built from the sensor angle {m(theta_t)} of
  each frame and the highest harmonic {m(p_order)}</td><td><code>filter_matrix</code>, <code>sor_order</code></td></tr>
<tr><td>Reconstruction parameters</td>
  <td>the agent weights {m(mu_k)}, the step size {m(rho)}, and the strengths {m(sp)}, {m(sn)}, {m(sx)}</td>
  <td><code>mace_prior_weight</code>, <code>rho_mann</code>, <code>sigma_prox</code>, <code>sigma_noise</code>,
  <code>sigma_x</code></td></tr>
</table></div>

<h2>2. The four agents</h2>
<p>The reconstruction is computed by MACE, the multi-slice fusion method of Majee et al. (IEEE Trans. Comput.
Imag., 2021). MACE finds a 4D image on which four agents agree. Agent {m(k)} maps a 4D input {m(wk)} to a 4D
output {m(vk)}.</p>
<p><b>The data-fit agent</b> is agent 0. It applies the proximal map of the forward model term to each frame.
The forward model term of frame {m(t)} is</p>
{EQ_FORWARD}
<p>and the proximal map of that frame returns</p>
{EQ_PROX}
<p>Here {m(sub(w, pair(mn('0'), t)))} is frame {m(t)} of the input, and {m(sp)} is the parameter
<code>sigma_prox</code>. Each call runs <code>prox_num_iterations</code> iterations of vectorized coordinate
descent, starting from the previous output of the frame. So {m(ut)} is an approximate minimizer.</p>
<p><b>The three prior agents</b> are agents 1, 2, and 3, named XY-t, YZ-t, and XZ-t. Each one holds one spatial
axis fixed. Every index along that axis then gives a 3D volume with one time axis and two spatial axes. The agent
denoises each of these volumes with the qGGMRF denoiser</p>
{EQ_DENOISER}
<p>where {m(h)} is the qGGMRF prior of the mbirtorch documentation and {m(sn)} is the parameter
<code>sigma_noise</code>. The time axis is in every volume, so the prior couples neighboring frames as well as
neighboring voxels. The parameter <code>nbr_weight_time</code> sets the weight of a neighbor in time relative to a
neighbor in space.</p>

<figure>
<svg viewBox="0 0 860 250" width="860" height="250" role="img" aria-label="The four agents of 4D MACE and the consensus image">
  <defs><marker id="ah" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="currentColor"/></marker></defs>
  <rect x="10" y="14" width="430" height="44" rx="6" class="box-c"/>
  <text x="24" y="41">Agent 0, data fit: one proximal map per frame</text>
  <rect x="10" y="74" width="430" height="44" rx="6" class="box-b"/>
  <text x="24" y="101">Agent 1, prior XY-t: qGGMRF denoiser</text>
  <rect x="10" y="134" width="430" height="44" rx="6" class="box-b"/>
  <text x="24" y="161">Agent 2, prior YZ-t: qGGMRF denoiser</text>
  <rect x="10" y="194" width="430" height="44" rx="6" class="box-b"/>
  <text x="24" y="221">Agent 3, prior XZ-t: qGGMRF denoiser</text>
  <path d="M440,36 L636,104" class="arrow" marker-end="url(#ah)"/>
  <path d="M440,96 L636,118" class="arrow" marker-end="url(#ah)"/>
  <path d="M440,156 L636,134" class="arrow" marker-end="url(#ah)"/>
  <path d="M440,216 L636,148" class="arrow" marker-end="url(#ah)"/>
  <rect x="640" y="86" width="210" height="80" rx="6" class="box-a"/>
  <text x="656" y="120">Weighted average:</text>
  <text x="656" y="142">the consensus image</text>
</svg>
<figcaption>Each iteration runs the four agents on their own inputs and averages their outputs with the agent weights.</figcaption>
</figure>

<h2>3. The consensus iteration</h2>
<p>Every agent input starts at the initial image {m(x0)}. One iteration runs the four agents and then updates
every input:</p>
{EQ_ITERATION}
<p>The agent weights {m(mu_k)} sum to 1. With {m(mi('c'))} the parameter <code>mace_prior_weight</code>, whose
default is 0.5, the data-fit agent has the weight {m(mn('1'), mo('−'), mi('c'))} and each prior agent has the weight
{m(mi('c'), mo('/'), mn('3'))}. The step size {m(rho)} is the parameter <code>rho_mann</code>, whose default is 0.5.</p>
<p><code>recon</code> returns {m(xbar)}. The iteration stops after <code>max_iterations</code> iterations, or
earlier when {m(xbar)} changes by less than <code>stop_threshold_change_pct</code> percent in one iteration.</p>

<h2>4. The temporal filter</h2>
<p>The overlapping frames produce a change from frame to frame that the object does not have. This change follows
the sensor angle {m(theta_t)} of the frame, which is the center angle of its views. The temporal filter removes it.
The filter is one {m(Nt, mo('×'), Nt)} matrix {m(F)} that acts along the frame axis.</p>
<p><b>How the filter is built.</b> {m(F)} is the matrix of Sensor Orthogonal Reconstruction (SOR). The change at
one voxel is modeled as a sum of the harmonics {m(fn('cos', m_index, theta))} and {m(fn('sin', m_index, theta))} for
{m(m_index, mo('='), mn('1'))} to {m(p_order)}. Here {m(p_order)} is the parameter <code>sor_order</code>, whose
default is 3. Let the columns of {m(QB)} be an orthonormal basis of these harmonics at the frame angles, with their
means removed. Then</p>
{EQ_SOR}
<p>Applying {m(F)} subtracts from each voxel the least-squares fit of the harmonics, and it keeps the mean over the
frames. {m(F)} depends only on the frame angles and {m(p_order)}, so <code>recon</code> builds it once, before the
iteration. The method assumes that two frames with the same sensor angle have the same artifact. This holds when
every rotation uses the same view angles. The derivation is in the linked
<a href="https://claude.ai/artifact/GF7x5MCc174NFPFxSmZxkT">Sensor Orthogonal Reconstruction blueprints</a>.</p>
<p><b>Where the filter is applied.</b> When <code>dejitter</code> is on, {m(F)} is applied in three places.</p>
<ul>
  <li><b>The outputs of the data-fit agent.</b> The output of agent 0 is the filtered stack of the proximal maps:</li>
</ul>
{EQ_FILTER_FIT}
<ul>
  <li><b>The inputs of the prior agents.</b> Each prior agent filters its input and then denoises it. Here
  {m(Hk)} applies the denoiser {m(H)} to every volume of orientation {m(k)}:</li>
</ul>
{EQ_FILTER_PRIOR}
<ul>
  <li><b>The initial image</b>, once, before the strength {m(sx)} of the prior is estimated from it.</li>
</ul>
<p>{m(F)} is not applied to the outputs of the prior agents or to the returned image {m(xbar)}. What pull request 32
changes in the code and in the user interface is in the linked
<a href="https://claude.ai/artifact/6oTS5U8DMXmsULsPXESENM">4D MACE Temporal Filter blueprints</a>.</p>

<h2>5. The initial image and the automatic parameters</h2>
<ul>
  <li><b>The initial image</b> {m(x0)} is a direct reconstruction of each frame from its own views, unless the
  caller gives <code>init_recon</code>.</li>
  <li><b>The noise level</b> {m(sn)} of the denoisers is estimated from the initial image. The three prior agents
  share one value.</li>
  <li><b>The strength</b> {m(sx)} of the qGGMRF prior is estimated from the filtered initial image and scaled by
  <code>sharpness</code>. The three prior agents share one value.</li>
  <li><b>The strength</b> {m(sp)} of the proximal map is the automatic value of the frame's model, unless
  <code>sigma_prox</code> is set.</li>
</ul>

<h2>6. Open questions</h2>
<ol class="questions">
  <li><input type="checkbox" id="q1"><label for="q1"><b>Q1. Review.</b> Should someone else, such as an advisor or
  a collaborator, review the design before it is settled?  Recommendation: yes, Greg or Charlie, because the page
  restates the method of their paper and code.</label></li>
  <li><input type="checkbox" id="q3"><label for="q3"><b>Q3. The fixed point.</b> The page gives the iteration and
  not the image that it converges to. With {m(F)} inside the agents, that image is not stated in the code or in
  the paper. Should the page state it?  Recommendation: no. The page describes the iteration as the code runs
  it.</label></li>
  <li><input type="checkbox" id="q4"><label for="q4"><b>Q4. Two symbols.</b> The mbirtorch documentation uses
  {m(mi('ρ'))} for the qGGMRF potential, so this page writes the step size of the iteration as {m(rho)}. The
  documentation uses {m(p_order)} for a parameter of the qGGMRF prior, and this page uses {m(p_order)} for the
  highest harmonic, as the Sensor Orthogonal Reconstruction blueprints do. Keep both?  Recommendation: yes. This
  page does not write the qGGMRF parameter.</label></li>
</ol>
<h2>7. Decisions</h2>
<ol class="questions">
  <li class="decided"><input type="checkbox" checked disabled><label><span class="chip done">decided 2026-11-25</span>
  <b>Q2. Which code.</b> The set follows the branch <code>sor</code> of pull request 32, in which the temporal
  filter is the SOR filter.</label></li>
  <li class="decided"><input type="checkbox" checked disabled><label><span class="chip done">decided 2026-11-25</span>
  <b>Placement of the filter.</b> {m(F)} stays where the code applies it: after the proximal maps of the data-fit
  agent and before each denoiser. All combinations were tried before, and this placement was agreed on.</label></li>
</ol>
'''

INDEX_BODY = f'''<h1>{TITLE}</h1>
<p class="lead">4D CT reconstruction in mbirtorch computes one volume for each time frame from one continuous scan
of a moving object. The class <code>MACE4DModel</code> holds the method. These pages describe the code as it is,
for the people who use it and extend it. One blueprint per component. Start at the top and read down.</p>

<h2>Core components</h2>
<div class="list">
  <div class="item">
    <h3><a href="theory.html">1. Theory</a></h3>
    <span class="status todo">for review</span>
    <p>One volume per time frame is the consensus of one data-fit agent and three qGGMRF prior agents. The page
    gives the frames, the agents, the consensus iteration, and the SOR temporal filter.</p>
  </div>
  <div class="item">
    <h3>2. Software Architecture</h3>
    <span class="status none">not started</span>
    <p>The objects a user holds, every method of each, the file formats, and which object holds each kind of quantity.</p>
  </div>
  <div class="item">
    <h3>3. Hardware Mapping</h3>
    <span class="status none">not started</span>
    <p>What lives in host memory and in GPU memory, what each processor computes, and what moves between them, with sizes and times.</p>
  </div>
  <div class="item">
    <h3>4. User API</h3>
    <span class="status none">not started</span>
    <p>The script a user writes for each use, and every public name.</p>
  </div>
</div>

<h2>Optional components</h2>
<div class="list">
  <div class="item optional">
    <h3>5. Testing and Verification</h3>
    <span class="status none">not started</span>
    <p>The reference results the code must match, the tests, and what each test guards against.</p>
  </div>
</div>

<h2>Linked sets</h2>
<div class="list">
  <div class="item">
    <h3><a href="https://claude.ai/artifact/6oTS5U8DMXmsULsPXESENM">4D MACE Temporal Filter</a></h3>
    <span class="status todo">for review</span>
    <p>What pull request 32 changes: the DCT filter before and the SOR filter after, in the code and in the user
    interface.</p>
  </div>
  <div class="item">
    <h3><a href="https://claude.ai/artifact/GF7x5MCc174NFPFxSmZxkT">Sensor Orthogonal Reconstruction</a></h3>
    <span class="status todo">for review</span>
    <p>The derivation of the SOR filter.</p>
  </div>
</div>

<p class="foot">Code: <code>mbirtorch/mace4d.py</code> and <code>mbirtorch/mace.py</code> on branch
<code>sor</code> of <code>ZiyunLiiii/mbirtorch_ziyun_fork</code>, at commit <code>a315886</code>. This branch is pull
request 32 into <code>prerelease</code> of <code>cabouman/mbirtorch</code>. Documentation and
release follow the procedures of mbirtorch. Decisions and rejected alternatives are recorded, with dates, in
<code>decisions.md</code>.</p>
'''

DECISIONS = f'''# Decisions: {NAME}

One entry per decision, newest last.  Each entry gives the date, the
blueprint, the question, what was decided, and any alternative that was
rejected.  Rejected alternatives live here, not on the blueprints.

## 2026-11-25, Theory

- **Question.** Which code does the set describe?
- **Decided.** The branch `sor` of pull request 32, in which the temporal filter is the SOR filter.
- **Rejected.** `prerelease`, in which the temporal filter is the DCT filter.

## 2026-11-25, Theory

- **Question.** Where is the temporal filter applied in the MACE loop?
- **Decided.** Where the code applies it: after the proximal maps of the data-fit agent and before each denoiser.
  All combinations were tried before, and this placement was agreed on.
- **Rejected.** The other placements that were tried.
'''


def page(template_path, title, body, crumb=None):
    """Return a page with the head of a kit template and the given body."""
    template = open(template_path, encoding='utf-8').read()
    head = template[template.index('<html'):template.index('<body>')]
    head = re.sub(r'<title>.*?</title>', lambda _: f'<title>{title}</title>', head, flags=re.S)
    crumb_html = '' if crumb is None else (
        f'<p class="crumb"><a href="index.html">{TITLE}</a> &rsaquo; {crumb}</p>\n')
    return ('<!DOCTYPE html>\n' + head + '<body>\n<div class="wrap">\n' + crumb_html + body
            + '</div>\n</body>\n</html>\n')


os.makedirs(OUT, exist_ok=True)
files = {
    'index.html': page(os.path.join(KIT, 'kinds/software/templates/index.html'), TITLE, INDEX_BODY),
    'theory.html': page(os.path.join(KIT, 'templates/blueprint.html'), TITLE + ', Theory', THEORY_BODY,
                        crumb='Theory'),
    'decisions.md': DECISIONS,
}
for name, text in files.items():
    with open(os.path.join(OUT, name), 'w', encoding='utf-8') as f:
        f.write(text)
    print('wrote', name, len(text))
