import unittest


class MyTestCase(unittest.TestCase):
    def test_working(self):
        # print("assert True=True")
        self.assertEqual(True, True)

    def test_false_case(self):
        # print("assert True=True")
        self.assertNotEqual("abcd", "ABCD")

    def test_true_case(self):
        # print("assert True=True")
        self.assertEqual(2 * 4, 8)


if __name__ == '__main__':
    unittest.main()
