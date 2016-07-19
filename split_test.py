import subprocess
import unittest
import os.path

class TestSplitRotate(unittest.TestCase):
    def test_split(self):
        subprocess.check_call([
            'mitmdump',
            '-n',
            '-r', './test.dump',
            '-s', 'split.py \'test/{req.host}/{time:%y-%m-%d %H:%M:%S}.dump\''
        ]);

        self.assertTrue(os.path.isfile('test/github.com/16-07-19 18:05:55.dump'))
        self.assertTrue(os.path.isfile('test/perdu.com/16-07-19 18:06:05.dump'))
        self.assertTrue(os.path.isfile('test/perdu.com/16-07-19 18:06:22.dump'))

if __name__ == '__main__':
    unittest.main()
