"""Offline JSON inference, compatible with the Hugging Face release bundle."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from evidencelens import predict

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--input',type=Path,required=True,help='JSON object with evidence and answer')
 p.add_argument('--model',type=Path,default=ROOT/'artifacts/model.json')
 args=p.parse_args()
 if args.input.stat().st_size>50000:p.error('Input exceeds 50 KB')
 row=json.loads(args.input.read_text(encoding='utf-8'))
 if not isinstance(row,dict) or not all(isinstance(row.get(k),str) and row[k].strip() and len(row[k])<=8000 for k in ['evidence','answer']):p.error('Expected evidence and answer strings of 1..8000 characters')
 model=json.loads(args.model.read_text(encoding='utf-8'))
 if model.get('feature_names')!=['missing_word_fraction','missing_number_fraction','negation_mismatch','answer_length_ratio','empty_evidence']:p.error('Unsupported model features')
 print(json.dumps(predict(model,row['evidence'],row['answer']),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
