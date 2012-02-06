"""
A Microsoft Visual SourceSafe class.
"""

import tools

import os
import subprocess

class VSS(object):
    """
    A VSS class that handles all low-level operations on a VSS repository.
    """

    def __init__(self, repository_path, ss_path=None):
        """
        Create a VSS instance attached to a specified repository_path repository.
        """

        self.repository_path = repository_path
        self.ss_path = ss_path or tools.get_ss_path()

    def __execute(self, argv):
        """
        Calls ss.exe with the specified arguments.

        Returns the standard output of the specified command.
        """

        env = os.environ.copy()
        env['SSDIR'] = self.repository_path

        return subprocess.check_output([self.ss_path] + argv, env=env)

    def about(self):
        """
        Calls the VSS About command.

        Returns the about information.
        """

        return self.__execute(['About'])
