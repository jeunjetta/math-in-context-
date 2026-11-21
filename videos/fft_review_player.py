"""Build one dependency-free local review HTML from frozen candidate identities."""
import argparse
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent/'fft-latency'


def candidates():
    rows={}
    for key,folder,duration in [('a','teaser-render',28),('b','teaser-slower-render',34)]:
        d=json.loads((ROOT/folder/'candidate.json').read_text())
        if d['publication_approved'] is not False or d['audio'] is not False:
            raise ValueError('Silent unapproved candidates only')
        rows[key]=dict(label=f'{duration}-second cut',sha256=d['sha256'],duration=duration)
    return rows


def html():
    template=(ROOT/'review-player-template.html').read_text()
    if template.count('__CANDIDATE_DATA__')!=1:raise ValueError('Expected one data slot')
    return template.replace('__CANDIDATE_DATA__',json.dumps(candidates(),indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');p.add_argument('--write',action='store_true');a=p.parse_args()
    if a.check==a.write:p.error('Choose --check or --write')
    out=ROOT/'review-player.html'
    if a.write:out.write_text(html())
    elif out.read_text()!=html():raise SystemExit('Review player drift; inspect and regenerate')
    print('Local review HTML matches frozen candidates; no review or approval implied.')
