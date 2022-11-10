import unittest

def computeGCp(seq):
    if seq != None:
        if seq != "":
            return 100 * (seq.count("C") + seq.count("G"))/len(seq)
        else:
            return 0


class TestComputeGCp(unittest.TestCase):
    """
    Class to test the function computeGCp 
    Each method in this class will be a test case
    """
    
    def test_computeGCp(self):
        """
        General test case when we expect a certain percentage
        """
        self.assertEqual(computeGCp("TTAACG"), 100/3, f"The result should be {100/3}")

    def test_computeGCp_None(self):
        """
        Exceptional case when we have None as the input sequence
        """
        self.assertIsNone(computeGCp(None), "The result should be None")

    def test_computeGCp_empty(self):
        """
        Exceptional case when we have None as the input sequence
        """
        self.assertEqual(computeGCp(""), 0, "The result should be 0")

if __name__ == '__main__':
    unittest.main()