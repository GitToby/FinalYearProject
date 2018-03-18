def test_creation_seqLen(self):
    axl.seed(0)
    test_length = 10
    self.instance = CyclerParams(sequence_length=test_length)
    self.assertEqual(self.instance.sequence, [D, C, C, D, C, C, C, C, C, C])
    self.assertEqual(self.instance.sequence_length, test_length)
    self.assertEqual(len(self.instance.sequence), test_length)