import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).parents[1];sys.path.insert(0,str(ROOT/'src'))
from evidencelens import features,predict,metrics
class Tests(unittest.TestCase):
    def test_number(self): self.assertEqual(features('Cost 12 dollars.','Cost 18 dollars.')[1],1)
    def test_negation(self): self.assertEqual(features('It is not open.','It is open.')[2],1)
    def test_empty(self): self.assertEqual(features('','text')[4],1)
    def test_range(self):
        model=json.loads((ROOT/'artifacts/model.json').read_text())
        for e,a in [('',''),('A'*8000,'B'*8000),('Cost 12','Cost 12')]:
            p=predict(model,e,a)['review_score']; self.assertGreaterEqual(p,0);self.assertLessEqual(p,1)
    def test_group_disjoint(self):
        rows=json.loads((ROOT/'data/synthetic.json').read_text()); groups={s:{r['group'] for r in rows if r['split']==s} for s in ['train','validation','test']}
        self.assertFalse(groups['train']&groups['test']);self.assertFalse(groups['train']&groups['validation']);self.assertFalse(groups['test']&groups['validation'])
    def test_metrics(self): self.assertEqual(metrics([0,1],[0,1])['f1'],1)
if __name__=='__main__':unittest.main()
