import unittest


class MyTestCase(unittest.TestCase):
    def test_working(self):
        self.assertEqual(True, True)

    def test_false_case(self):
        self.assertNotEqual("abcd", "ABCD")

    def test_true_case(self):
        self.assertEqual(2 * 4, 8)


if __name__ == '__main__':
    unittest.main()
