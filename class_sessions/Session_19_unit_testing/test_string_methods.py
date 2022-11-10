import unittest

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('aCg'.upper(), 'ACG')

    def test_isupper(self):
        self.assertTrue('ACGTT'.isupper())
        self.assertFalse('acgT'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_split_1(self):
        s = 'A,C,G,T'
        self.assertEqual(s.split(","), ["A","C","G","T"])
        
    def test_len(self): # this is the builtin len function but we test it for strings
        s = "AAACGT"
        self.assertEqual(len(s), 6, "The result should be 6")
        
    def test_strip(self):
        s = "   \t  GTAC TCA \n\t "
        self.assertEqual(s.strip(),"GTAC TCA")
        
    def test_index(self):
        s = "AAACGTA"
        self.assertEqual(s.index("C"), 3, "Index of 'C' in 'AAACGTA' should be 3")
        
    def test_hello_world(self):
        print("Hello world")

            
            
if __name__ == '__main__':
      unittest.main()