"""Render the public aggregate figure as SVG using only Python's standard library.

Run: python3 scripts/render_results_figure.py
Optional PNG (ImageMagick): magick -background white -density 144 \
  docs/figures/same-challenge-results.svg docs/figures/same-challenge-results.png
The data are aggregate reported counts, not a reproducible full research dataset.
"""
from pathlib import Path
import json
from html import escape

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'docs/figures/same-challenge-results.json'
OUT = ROOT / 'docs/figures/same-challenge-results.svg'

def render(data):
    n = data['class_counts']
    assert n == [10, 10, 20] and sum(n) == data['n_claims']
    for model in data['models']:
        cm = model['confusion_rows_true_columns_predicted']
        assert [sum(row) for row in cm] == n
        assert model['correct_by_class'] == [cm[i][i] for i in range(3)]
        assert model['correct_overall'] == sum(model['correct_by_class'])
    assert data['selected_before_evaluation'] == 'baseline_v1'
    bits = ['<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="1100" viewBox="0 0 1500 1100" role="img" aria-labelledby="title description">',
            '<title id="title">Same challenge, different trade-offs</title>',
            '<desc id="description">Both models correctly classify 33 of the same 40 AI-authored and AI-reviewed claims from 10 documents. Baseline and candidate correct counts: contradiction 8 and 6 out of 10; support 6 and 7 out of 10; insufficient evidence 19 and 20 out of 20. All 40 cases still require review. No human validation or automatic approval.</desc>',
            '<rect width="1500" height="1100" fill="#ffffff"/>',
            '<g font-family="Arial, Helvetica, sans-serif">']
    def text(x,y,s,size=24,color='#172b3a',weight='normal',anchor='start'):
        bits.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}">{escape(str(s))}</text>')
    def line(x1,y1,x2,y2,color='#dce4e8',width=1):
        bits.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"/>')
    text(90,65,'EVIDENCELENS  /  EXPLORATORY DIAGNOSTIC',18,'#496573','bold')
    text(90,126,data['title'],44,weight='bold')
    text(90,168,'Same 40 claims  ·  10 source documents  ·  AI-authored and AI-reviewed labels',24,'#496573')
    colors=['#117c83','#6958a5']
    for x,model,color in zip([90,520],data['models'],colors):
        bits.append(f'<rect x="{x}" y="208" width="24" height="24" rx="3" fill="{color}"/>')
        text(x+36,229,model['label'],22)
    text(90,300,'Correctly classified claims',21,'#496573')
    left,right,top,bottom=160,1380,350,750
    for count in range(0,21,5):
        yy=bottom-count*20
        line(left,yy,right,yy,'#c6d2d8' if count==0 else '#e4eaed',2 if count==0 else 1)
        text(left-25,yy+8,count,22,'#496573',anchor='end')
    centers=[360,770,1180]
    for i,(cx,label,total) in enumerate(zip(centers,data['class_labels'],n)):
        for j,(model,color) in enumerate(zip(data['models'],colors)):
            correct=model['correct_by_class'][i];x=cx-102+j*108;height=correct*20;y=bottom-height
            bits.append(f'<rect x="{x}" y="{y}" width="92" height="{height}" rx="3" fill="{color}"/>')
            text(x+46,y-18,f'{correct}/{total}',28,color,'bold','middle')
        text(cx,796,label,25,weight='bold',anchor='middle')
        text(cx,832,f'{total} reference-labelled claims',20,'#496573',anchor='middle')
    line(90,875,1410,875)
    text(90,922,'33/40 correct overall for both models',29,weight='bold')
    text(90,965,'Baseline retained before evaluation. Experimental candidate not promoted.',23,'#496573')
    text(90,1005,'All 40 cases require review; no automatic approvals.',23,'#496573')
    text(90,1054,'Small constructed sample. Observed counts are not human validation or evidence of production safety.',21,'#496573')
    bits.extend(['</g>','</svg>'])
    return '\n'.join(bits)+'\n'

if __name__ == '__main__':
    OUT.write_text(render(json.loads(DATA.read_text())))
    print(OUT.relative_to(ROOT))
