"""Source-color contrast only; no encoded-pixel or accessibility certification."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
SPEC = ROOT / 'fft-latency/contrast-spec.json'
REPORT = ROOT / 'fft-latency/contrast-report.json'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def luminance(color):
    if not isinstance(color, str) or not re.fullmatch(r'#[0-9a-fA-F]{6}', color):
        raise ValueError('Expected opaque six-digit sRGB hex color')
    channels = [int(color[i:i+2], 16)/255 for i in (1, 3, 5)]
    linear = [c/12.92 if c <= 0.04045 else ((c+0.055)/1.055)**2.4 for c in channels]
    return sum(c*w for c, w in zip(linear, (0.2126, 0.7152, 0.0722)))


def ratio(a, b):
    light, dark = sorted((luminance(a), luminance(b)), reverse=True)
    return (light+0.05)/(dark+0.05)


def meets(value, minimum=4.5):
    # Compare full precision, never the rounded display value.
    return value >= minimum


def palette(source):
    """Read literal module assignments without importing Pillow/rendering code."""
    colors = {}
    for node in ast.parse(source).body:
        if not isinstance(node, ast.Assign):
            continue
        try:
            value = ast.literal_eval(node.value)
        except (ValueError, TypeError):
            continue
        for target in node.targets:
            if isinstance(target, ast.Tuple) and isinstance(value, tuple):
                colors.update({n.id: v for n, v in zip(target.elts, value) if isinstance(n, ast.Name)})
            elif isinstance(target, ast.Name):
                colors[target.id] = value
    return {k: colors[k] for k in ('BG', 'FG', 'MUTED', 'CYAN', 'AMBER', 'PANEL')}


def audit(root=ROOT):
    root = Path(root)
    spec = json.loads((root/'fft-latency/contrast-spec.json').read_text())
    manifest_path = root/'fft-latency/source-only-review/render-report.json'
    if sha(manifest_path) != spec['render_report_sha256']:
        raise ValueError('Referenced render manifest changed; re-audit scope')
    manifest = json.loads(manifest_path.read_text())
    if manifest['sha256'] != spec['movie_sha256'] or manifest['publication_approved'] is not False:
        raise ValueError('Wrong unadopted movie identity')
    for path, digest in manifest['source_hashes'].items():
        if sha(root/path) != digest:
            raise ValueError('Render source drift: '+path)
    for name, key in (('fft-source-only-review.vtt', 'captions_sha256'),
                      ('resolved-lesson.json', 'resolved_lesson_sha256')):
        if sha(manifest_path.parent/name) != manifest[key]:
            raise ValueError('Resolved content drift: '+name)
    colors = palette((root/'render.py').read_text())
    colors['CAPTION_BG'] = spec['caption_background']
    for path in ('render.py', 'caption_layout.py'):
        literals = {n.value for n in ast.walk(ast.parse((root/path).read_text()))
                    if isinstance(n, ast.Constant) and isinstance(n.value, str)}
        if colors['CAPTION_BG'] not in literals:
            raise ValueError('Caption background no longer matches source')
    rows = []
    for pair in spec['pairs']:
        fg, bg = (colors[pair[k]] for k in ('foreground', 'background'))
        value = ratio(fg, bg)
        rows.append(dict(**pair, foreground_hex=fg, background_hex=bg,
                         ratio=value, passes=meets(value, spec['minimum_ratio'])))
    return dict(source_commit=spec['source_commit'], movie_sha256=manifest['sha256'],
                render_report_sha256=sha(manifest_path), spec_sha256=sha(root/'fft-latency/contrast-spec.json'),
                audit_source_sha256=sha(root/'contrast_audit.py'), minimum_ratio=spec['minimum_ratio'],
                all_pairs_pass=all(r['passes'] for r in rows), pairs=rows,
                publication_approved=False,
                limitations='Manually inventoried opaque intended sRGB text/background roles only. '
                'Not automatic role discovery, encoded/color-managed pixel analysis, non-text contrast, '
                'full WCAG conformance, small-screen readability, pacing, device or editorial approval. '
                'Movie bytes not reopened by this source-only audit; identity is from pinned render report.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Reject stale checked-in report')
    args = parser.parse_args()
    result = audit()
    expected = json.dumps(result, indent=2)+'\n'
    if args.check:
        if REPORT.read_text() != expected:
            raise SystemExit('Stale contrast report; run contrast_audit.py after reviewing scope')
    else:
        REPORT.write_text(expected)
    print(f"{len(result['pairs'])} intended-color pairs; minimum {min(r['ratio'] for r in result['pairs']):.3f}:1")
    if not result['all_pairs_pass']:
        raise SystemExit('At least one intended-color pair fails project target')


if __name__ == '__main__':
    main()
