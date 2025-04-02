#!/usr/bin/python

# Ibrahim K

import sys
import os
import unittest
import lcrun
sys.path.append('../')

basedir, bin = os.path.split(os.path.dirname(os.path.abspath(sys.argv[0])))
sys.path.append("%s" % basedir)

ScriptDir = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + "/bin"


class LcRun(unittest.TestCase):
    def test_Connect_host(self):
        print 'Testing the Connect using password functions :'
        rv = lcrun.connect_host('localhost', 'tester', 'object00', 'ls -l')
        self.assertEqual(rv, 0)

    def test_connect_host_key(self):
        print 'Testing the Connect using key functions :'
        rv = lcrun.connect_host_key('localhost', 'tester', 'ls -l')
        self.assertEqual(rv, 0)

    def test_ShortOpts(self):
        cmd = ScriptDir + "/lcrun.py -i hosts.csv -l localhost -u tester " \
                          "-p object00 'ls' < /dev/null"
        rv = os.system(cmd)
        self.assertEqual(rv, 0)

    def test_LongOpts(self):
        cmd = ScriptDir + "/lcrun.py --inputs hosts.csv " \
                          "--hostname localhost --username ibrahim --password object00 uptime < /dev/null"
        result = os.system(cmd)
        self.assertEqual(result, 0)

    def test_WithPassword(self):
        cmd = ScriptDir + "/lcrun.py -i hosts.csv uptime < /dev/null"
        result = os.system(cmd)
        self.assertEqual(result, 0)

    def test_WithKey(self):
        cmd = ScriptDir + "/lcrun.py -i hosts.csv uptime < /dev/null"
        result = os.system(cmd)
        self.assertEqual(result, 0)

    def test_WithInputFileAndExtraHost(self):
        cmd = ScriptDir + "/lcrun.py -i hosts.csv -l localhost " \
                          "-u tester -p object00 'ls' < /dev/null"
        result = os.system(cmd)
        self.assertEqual(result, 0)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(LcRun, "test")
    unittest.TextTestRunner().run(suite)
