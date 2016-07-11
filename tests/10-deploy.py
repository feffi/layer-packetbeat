#!/usr/bin/python3

import amulet
import unittest

seconds = 1100


class TestPacketbeat(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Setup the deployment for this class once and deploy."""
        cls.deployment = amulet.Deployment(series='xenial')

        cls.deployment.add('ubuntu')
        cls.deployment.add('packetbeat')

        try:
            cls.deployment.setup(timeout=seconds)
            cls.deployment.sentry.wait()
        except amulet.helpers.TimeoutError:
            message = "The deploy did not setup in {0} seconds".format(seconds)
            amulet.raise_status(amulet.SKIP, msg=message)
        except:
            raise
        cls.unit = cls.d.sentry['packetbeat'][0]

    def test_packetbeat_binary(self):
        """Verify that the packetbeat binary is installed, on the path and is
        functioning properly for this architecture."""
        # packetbeat -version
        output, code = self.unit.run('packetbeat -version')
        print(output)
        if code != 0:
            message = 'Packetbeat unable to return version.'
            amulet.raise_status(amulet.FAIL, msg=message)
        # packetbeat -devices
        output, code = self.unit.run('packetbeat -devices')
        print(output)
        if code != 0:
            message = 'Packetbeat unable to find devices.'
            amulet.raise_status(amulet.FAIL, msg=message)
