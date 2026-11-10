"""Review local JSONL pairs, retaining IDs. No external services or automated approval."""
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'src'))
from review import analyze

def review_lines(lines):
 for i,line in enumerate(lines,1):
  if not line.strip(): continue
  try:
   row=json.loads(line)
   if not isinstance(row,dict) or not all(isinstance(row.get(k),str) and row[k].strip() and len(row[k])<=8000 for k in ['evidence','answer']):raise ValueError('Expected evidence and answer strings (1..8000 characters)')
   yield {'id':row.get('id',str(i)),'line':i,**analyze(row['evidence'],row['answer']),'human_review':'pending'}
  except (ValueError,TypeError) as e:yield {'line':i,'error':str(e),'human_review':'invalid_input'}
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('input',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
 if a.input.resolve()==a.output.resolve():p.error('Output must differ from input')
 # Exclusive creation avoids accidentally overwriting prior review reports.
 with a.input.open(encoding='utf-8') as src,a.output.open('x',encoding='utf-8') as dst:
  for row in review_lines(src):dst.write(json.dumps(row,ensure_ascii=False)+'\n')
