import unittest

from pysqler.helper import strings


class SearchTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_replace(self):
        test_case = """
        你是什么呢
        是天空
        是大海?
        或许   你是碌碌无为的灵魂?
        哈哈  哈哈
        go 
        """

        expected = """你是什么呢是天空是大海？或许你是碌碌无为的灵魂？哈哈哈哈go"""

        t = strings.replace(test_case, {"\t": "", " ": "", "\n": "", "?": "？"})
        print(t)

        self.assertEqual(expected, t, msg="not equal")


if __name__ == '__main__':
    unittest.main()
