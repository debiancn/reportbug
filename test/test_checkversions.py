import unittest2

from reportbug import checkversions
from nose.plugins.attrib import attr

import mock

class TestCheckversions(unittest2.TestCase):

    def test_compare_versions(self):
        # <current, upstream>
        # 1 upstream newer than current
        # 0 same version or upsteam none
        # -1 current newer than upstream
        self.assertEqual(checkversions.compare_versions('1.2.3', '1.2.4'), 1)

        self.assertEqual(checkversions.compare_versions('123', None), 0)
        self.assertEqual(checkversions.compare_versions('1.2.3', '1.2.3'), 0)
        self.assertEqual(checkversions.compare_versions(None, None), 0)
        self.assertEqual(checkversions.compare_versions('', '1.2.3'), 0)

        self.assertEqual(checkversions.compare_versions('1.2.4', '1.2.3'), -1)

    def test_later_version(self):
        # mock the test_compare_Versions() test

        self.assertEqual(checkversions.later_version('1.2.3', '1.2.4'), '1.2.4')

        self.assertEqual(checkversions.later_version('123', None), '123')
        self.assertEqual(checkversions.later_version('1.2.3', '1.2.3'), '1.2.3')
        self.assertIsNone(checkversions.later_version(None, None))
        self.assertEqual(checkversions.later_version('', '1.2.3'), '')

        self.assertEqual(checkversions.later_version('1.2.4', '1.2.3'), '1.2.4')

class TestNewQueue(unittest2.TestCase):

    def test_bts704040(self):

        # return an iterable object, so that Deb822 (what parses the result)
        # will work
        pkg_in_new = """Source: procps
Binary: libprocps1-dev, procps, libprocps1
Version: 1:3.3.6-2 1:3.3.6-1 1:3.3.7-1 1:3.3.5-1
Architectures: source, amd64
Age: 4 months
Last-Modified: 1353190660
Queue: new
Maintainer: Craig Small <csmall@debian.org>
Changed-By: Craig Small <csmall@debian.org>
Distribution: experimental
Fingerprint: 5D2FB320B825D93904D205193938F96BDF50FEA5
Closes: #682082, #682083, #682086, #698482, #699716
Changes-File: procps_3.3.6-1_amd64.changes

Source: aaa
""".split('\n')

        # save the original checkversions.open_url() method
        save_open_url = checkversions.open_url

        checkversions.open_url = mock.MagicMock(return_value = pkg_in_new)

        res = checkversions.get_newqueue_available('procps', 60)

        self.assertEqual(res.keys()[0], u'experimental (new)')
        self.assertEqual(res[u'experimental (new)'], u'1:3.3.7-1')

        # restore the original checkversions.open_url() method
        checkversions.open_url = save_open_url

class TestVersionAvailable(unittest2.TestCase):

    @attr('network') #marking the test as using network
    def test_bts642032(self):
        vers = checkversions.get_versions_available('reportbug', 60)
        # check stable version is lower than unstable
        chk = checkversions.compare_versions(vers['stable'], vers['unstable'])
        self.assertEqual(chk, 1)

    @attr('network') #marking the test as using network
    def test_bts649649(self):
        # checking for non-existing package should not generate a traceback
        vers = checkversions.get_versions_available('blablabla', 60)
        self.assertEqual(vers, {})

    @attr('network') #marking the test as using network
    def test_673204(self):
        vers = checkversions.get_versions_available('texlive-xetex', 60)
        # squeeze (stable at this time) is the first suite where texlive-xetex
        # is arch:all
        self.assertIn('stable', vers)
