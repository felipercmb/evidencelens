"""Synthetic smoke experiment; results must never be described as real-world validation."""
import hashlib,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'src'))
from evidencelens import fit,predict,metrics,features
ROOT=Path(__file__).parent
for directory in ['artifacts', 'data']:
    (ROOT/directory).mkdir(exist_ok=True)
DOMAINS={'train':['museum','library','clinic','theater','school','studio'], 'validation':['garden','station'], 'test':['aquarium','observatory']}
def generate():
    rows=[]
    for split,domains in DOMAINS.items():
        for domain in domains:
            for n in range(10,30):
                ev=f'The {domain} opened in 1998. Admission costs {n} dollars. It is not open on Mondays.'
                answers=[(f'Admission to the {domain} costs {n} dollars.',0,'supported'),(f'The {domain} opened in 1998.',0,'supported'),(f'Admission costs {n+41} dollars.',1,'number_changed'),(f'The {domain} is open on Mondays.',1,'negation_dropped'),(f'The {domain} offers free parking and guided tours every evening.',1,'unsupported_addition'),(f'The {domain} does not open on Mondays.',0,'supported_negation')]
                for answer,label,kind in answers:
                    rows.append(dict(evidence=ev,answer=answer,label=label,kind=kind,group=domain,split=split))
    return rows
rows=generate(); model=fit([r for r in rows if r['split']=='train'])
report={'dataset':'controlled_synthetic_v1','warning':'Template overlap across splits. Entity-disjoint only. Not semantic generalization or real-world performance.','split_groups':DOMAINS,'selection':'Fixed features, epochs and threshold; no search. Test only for pipeline smoke test.','splits':{}}
for split in DOMAINS:
    subset=[r for r in rows if r['split']==split]; ys=[r['label'] for r in subset]
    report['splits'][split]={'learned':metrics(ys,[predict(model,r['evidence'],r['answer'])['review_score'] for r in subset]),'lexical_baseline':metrics(ys,[float(features(r['evidence'],r['answer'])[0]>.3) for r in subset]),'always_review':metrics(ys,[1. for r in subset])}
challenge=[{'evidence':'The museum admits adults. Children cannot enter.','answer':'Adults cannot enter the museum.','label':1}, {'evidence':'Entry costs ten dollars.','answer':'The admission price is $10.','label':0}, {'evidence':'Alice supervises Bob.','answer':'Bob supervises Alice.','label':1}]
report['challenge_cases']=[dict(r,prediction=predict(model,r['evidence'],r['answer'])) for r in challenge]
for path,obj in [('artifacts/model.json',model),('artifacts/metrics.json',report),('data/synthetic.json',rows)]:
    (ROOT/path).write_text(json.dumps(obj,indent=2)+'\n')
manifest={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ['artifacts/model.json','data/synthetic.json']}
(ROOT/'artifacts/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(report,indent=2))
