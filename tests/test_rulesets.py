import unittest
import lgr
from lgr.codepoints import InvalidCodepoint

class LGRTestCase(unittest.TestCase):


    def testAdd(self):

        i = lgr.Ruleset()
        i.add('a')
        i.add('a-z')
        i.add('U+0061')
        i.add('U+0061-U+0074')
        self.assertRaises(lgr.codepoints.InvalidCodepoint, i.add, '-z')
        self.assertRaises(lgr.codepoints.InvalidCodepoint, i.add, 'z-')
        self.assertRaises(lgr.codepoints.InvalidCodepoint, i.add, 'U+XXXX')

    def testContains(self):

        i = lgr.Ruleset()
        i.add('a-z')
        self.assertTrue('b' in i)
        self.assertTrue('ab' in i)
        self.assertFalse('0' in i)
        self.assertFalse('xn--4ca' in i)
        i.add('\u00e4')
        self.assertTrue('xn--4ca' in i)

    def testTableLength(self):

        i = lgr.Ruleset()
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
