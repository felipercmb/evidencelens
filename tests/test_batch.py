import sys,json,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from review_batch import review_lines
class BatchTests(unittest.TestCase):
 def test_valid(self):
  r=list(review_lines([json.dumps({'id':'case1','evidence':'Delivery takes 2 days.','answer':'Delivery takes 7 days.'})]))[0]
  self.assertEqual(r['id'],'case1');self.assertEqual(r['overall_status'],'review');self.assertEqual(r['human_review'],'pending')
 def test_error_continues(self):
  r=list(review_lines(['[]','bad',json.dumps({'evidence':'hello','answer':'hello'})]));self.assertEqual(len(r),3);self.assertEqual(r[-1]['overall_status'],'matched')
 def test_blank(self):self.assertEqual(list(review_lines([' \n'])),[])
