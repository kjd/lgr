import unittest
import idntables.codepoints

class CodepointsTestCase(unittest.TestCase):

	def test_cp_to_int(self):
		
		self.assertEqual(idntables.codepoints.cp_to_int('a'), 97)
		self.assertEqual(idntables.codepoints.cp_to_int('U+0061'), 97)
		self.assertEqual(idntables.codepoints.cp_to_int('\u0061'), 97)
		self.assertEqual(idntables.codepoints.cp_to_int('0061'), 97)
		self.assertEqual(idntables.codepoints.cp_to_int('61'), 97)
		self.assertEqual(idntables.codepoints.cp_to_int('\u61'), 97)
		self.assertEqual(idntables.codepoints.cp_to_int('U+61'), 97)
		self.assertEqual(idntables.codepoints.cp_to_int(['U+0061','U+0062']), [97,98])
		self.assertEqual(idntables.codepoints.cp_to_int('U+0061 U+0062'), [97,98])
		self.assertEqual(idntables.codepoints.cp_to_int('ab', raw=True), [97,98])
		
		self.assertRaises(idntables.codepoints.InvalidCodepoint, idntables.codepoints.cp_to_int, 'xx')
	
	def test_int_to_cp(self):
		
		self.assertEqual(idntables.codepoints.int_to_cp(97), 'U+0061')
		self.assertEqual(idntables.codepoints.int_to_cp(97, prefix=None), '0061')
		self.assertEqual(idntables.codepoints.int_to_cp(97, prefix='\u'), '\u0061')
		self.assertEqual(idntables.codepoints.int_to_cp([97,98]), 'U+0061 U+0062')
	
if __name__ == '__main__':
    unittest.main()
