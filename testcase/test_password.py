import testcase.password as password 
import unittest 

# pass cases

class TestPassword(unittest.TestCase):
    def test_1(self):
        result = password.validate_password("Password@123")
        self.assertTrue(result)
        
    def test_2(self):
        result = password.validate_password("Vimal@123")
        self.assertTrue(result)
    
    def test_3(self):
        result = password.validate_password("Vaibav#543")
        self.assertTrue(result)
    
    def test_4(self):
        result = password.validate_password("Bhavana#543")
        self.assertTrue(result)
        
    def test_5(self):
        result = password.validate_password("Greeshma$543")
        self.assertTrue(result)


#Fail cases
    def test_6(self):
        result = password.validate_password("PASSWORD@123")
        self.assertFalse(result)
        
    def test_7(self):
        result = password.validate_password("vimal123")
        self.assertFalse(result)
    
    def test_8(self):
        result = password.validate_password("vaibhav#")
        self.assertFalse(result)
        
    def test_9(self):
        result = password.validate_password("Bhavana454")
        self.assertFalse(result)
        
    def test_10(self):
        result = password.validate_password("Greesh")
        self.assertFalse(result)
        
# Run the tests
if __name__ == "__main__":
    unittest.main()