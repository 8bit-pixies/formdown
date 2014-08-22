import unittest
from formdown import Form

form1 = "name = _"

class TestFormDown(unittest.TestCase):          
    
    def test_form1(self):
        name = Form(form1)
        self.assertTrue(name.get_name() == 'name')
        
if __name__ == '__main__':
    unittest.main()