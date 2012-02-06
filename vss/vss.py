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

    def __to_options_list(self, options):
        """
        Convert options to their VSS format.
        """

        result = []

        options_map = {
            'format': {
                'binary': '-B',
                'text': '-B-',
            },
            'base_version_number': '-B{param}',
            'base_version_date': '-B{param}',
            'base_version_label': '-Bl{param}',
        }

        for option, value in options.items():

            if not option in options_map:
                raise ValueError('Invalid option name (%s)' % repr(option))

            map_entry = options_map[option]

            if isinstance(map_entry, dict):

                if not value in map_entry:
                    raise ValueError('Invalid option value for %s (%s)' % (repr(option), repr(value)))

                result.append(map_entry[value])

            elif isinstance(map_entry, str):

                result.append(map_entry.replace('{param}', value))

        return result

    def about(self):
        """
        Calls the VSS About command.

        Returns the standard output.
        """

        return self.__execute(['About'])

    def add(self, files, **options):
        """
        Calls the VSS Add command for the specified files.

        Returns the standard output.
        """

        if not isinstance(files, list):
            files = [str(files)]

        return self.__execute(['Add'] + files + self.__to_options_list(options))
