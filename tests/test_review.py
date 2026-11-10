import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'src'))
from review import analyze,sentences
class ReviewTests(unittest.TestCase):
 def test_literal(self): self.assertEqual(analyze('A entrega custa 12 reais.','A entrega custa 12 reais.')['overall_status'],'matched')
 def test_number(self): self.assertEqual(analyze('A entrega custa 12 reais.','A entrega custa 19 reais.')['overall_status'],'review')
 def test_negation(self): self.assertEqual(analyze('The office is not open.','The office is open.')['overall_status'],'review')
 def test_swap(self): self.assertEqual(analyze('Alice supervises Bob.','Bob supervises Alice.')['overall_status'],'review')
 def test_paraphrase_abstain(self): self.assertEqual(analyze('Entry costs ten dollars.','Admission is $10.')['overall_status'],'abstain')
 def test_substring_not_matched(self): self.assertNotEqual(analyze('It is not true that the store opens.','The store opens.')['overall_status'],'matched')
 def test_multi_claim(self):
  x=analyze('Cost is 12 dollars. Delivery takes 3 days.','Cost is 12 dollars. Delivery takes 8 days.');self.assertEqual(x['summary'],{'review':1,'abstain':0,'matched':1})
 def test_empty(self):self.assertEqual(analyze('','')['overall_status'],'abstain')
 def test_decimal(self):self.assertEqual(len(sentences('Cost is 12.50 dollars. Open now.')),2)
 def test_no_factual_approval(self):self.assertEqual(analyze('The earth is flat.','The earth is flat.')['overall_status'],'matched')
if __name__=='__main__':unittest.main()
