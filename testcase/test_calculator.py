# Unit Tests for Calculator App

# Run with the following command:
# python3 -m unittest test_calculator.py
# or just press the Run button on the top right!

import unittest
import testcase.calculator as calculator

# Unit tests
class TestCalculator(unittest.TestCase):
    def test_add(self):
        result = calculator.add(10, 5)
        self.assertEqual(result, 15)
        
        result = calculator.add(20, 5)
        self.assertEqual(result, 25)
        
    def test_add(self):
        result = calculator.multiply(20, 5)
        self.assertEqual(result, 4)
        
    
    # Similarly, test the other functions of the Calculator App.
        

# Run the tests
if __name__ == "__main__":
    unittest.main()