import unittest
import sys

def run_tests():
    """
    Discovers and runs all tests in the 'tests' directory.
    """
    # Discover all tests in the 'tests' directory
    loader = unittest.TestLoader()
    suite = loader.discover('tests')

    # Run the tests
    runner = unittest.TextTestRunner()
    result = runner.run(suite)

    # Exit with a non-zero status code if any tests failed
    if not result.wasSuccessful():
        sys.exit(1)

if __name__ == '__main__':
    run_tests()
