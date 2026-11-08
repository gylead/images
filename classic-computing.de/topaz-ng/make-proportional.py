import sys
sys.path.insert(0, sys.argv[1])  # usage: make-proportional.py <fonttools-dir> <TopazNG_Classic-Regular.ttf> <out.woff2>
from fontTools.ttLib import TTFont
src, out = sys.argv[2], sys.argv[3]
f = TTFont(src)
PX = 91                      # one pixel of the 8px design grid (727 / 8)
hm, glyf = f['hmtx'], f['glyf']
for g in f.getGlyphOrder():
    gl = glyf[g]
    adv, lsb = hm[g]
    if gl.numberOfContours == 0:
        if g == 'space': hm[g] = (4 * PX, 0)       # 4px word space
        continue
    gl.recalcBounds(glyf)
    w = gl.xMax - gl.xMin
    # shift the outline so that it starts at x=0
    gl.coordinates.translate((-gl.xMin, 0)) if gl.isComposite() is False else None
    gl.recalcBounds(glyf)
    hm[g] = (w + PX, gl.xMin)
f['hhea'].advanceWidthMax = max(a for a, _ in hm.metrics.values())
# rename (OFL: derivative, keep copyright + license)
for r in f['name'].names:
    s = r.toUnicode()
    s = s.replace('TopazNG Classic', 'TopazNG Proportional').replace('TopazNG-Classic', 'TopazNG-Proportional').replace('TopazNGClassic','TopazNGProportional')
    r.string = s
f.flavor = 'woff2'
f.save(out)
