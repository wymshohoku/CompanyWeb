import unittest
from api import verify

class verifyTest(unittest.TestCase):
    """字符串操作包测试类"""

    def setUp(self):
        """初始化测试环境"""
        print('------ini------')

    def tearDown(self):
        """清理测试环境"""
        print('------clear------')

    def test(self):
        verify.get_verify()

if __name__ == '__main__':
    unittest.main()