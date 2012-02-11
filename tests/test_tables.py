import unittest
import idntables

class IDNTablesTestCase(unittest.TestCase):

		# Tests
		# 'a'; 'a-z', 'U+0061', 'U+0061-U+0074'
		# fail: '-z', 'z-', 'U+XXXX'
		
	def testTableLength1(self):
		i = idntables.IDNTable()
		i.add('a')
		
	def testTableLength(self):
		i = idntables.IDNTable()
		self.assertEqual(len(i), 0)
		i.add('a')
		self.assertEqual(len(i), 1)
		i.addrange('b','z')
		self.assertEqual(len(i), 26)
		i.delete('b-d')
		self.assertEqual(len(i), 23)
		
		
	#def testAddNakedRange(self):
	#	pass
		
	#def testAddUnicodeCodepoint(self):
	#
	
if __name__ == '__main__':
    unittest.main()
