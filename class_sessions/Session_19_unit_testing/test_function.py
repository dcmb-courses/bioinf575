def computeGCp(seq):
    return (seq.count("C") + seq.count("G"))/len(seq)


def test_answer():
    assert computeGCp("CCG") == 1
    
def test_answer2():
    assert computeGCp("AAATT") == 0