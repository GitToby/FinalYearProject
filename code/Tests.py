import unittest
from code import full_analysis as fa
import axelrod as axl


class MyTestCase(unittest.TestCase):
    def test_working(self):
        self.assertEqual(True, True)

    def test_false_case(self):
        self.assertNotEqual("abcd", "ABCD")

    def test_true_case(self):
        self.assertEqual(2 * 4, 8)

    def test_example(self):
        run = fa.NewAnalysisRun()
        run.save_file_prefix = "example-"

        run.add_opponent(axl.TitForTat())
        run.add_opponent(axl.Random())
        run.add_opponent(axl.Grudger())

        # must have 12 opponents; 10 Randoms and the other 2
        self.assertEqual(len(run.opponent_list), 12)
        run.start()

        import glob
        all_files = glob.glob("./output/*.csv")
        # assert all files were created
        self.assertEqual(len(all_files), 12)


if __name__ == '__main__':
    unittest.main()
