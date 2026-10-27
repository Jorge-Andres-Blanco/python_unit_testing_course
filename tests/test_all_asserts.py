import unittest
class AllAssertsTests(unittest.TestCase):
    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)

    @unittest.skip("Work in progress")
    def test_skip(self):
        self.assertEqual(2,2)

    @unittest.expectedFailure
    def test_expected_error(self):
        self.assertEqual(1,2)