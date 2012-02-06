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
            'number': '-#{param}',
            'help': '-?',
            'format': {
                'binary': '-B',
                'text': '-B-',
            },
            'base_version_number': '-B{param}',
            'base_version_date': '-B{param}',
            'base_version_label': '-Bl{param}',
            'comment_text': '-C"{param}"',
            'comment_no_text': '-C-',
            'comment_file': '-C@{param}',
            'comment_default': '-C?',
            'display': '-D',
            'display_not_last': '-D-',
            'display_standard_width': '-DS{param}',
            'display_unix_width': '-DU{param}',
            'display_visual_width': '-DV{param}',
            'display_context': '-DX{param}',
            'display_no_context': '-DX-',
            'extended': '-E',
            'files_display': {
                True: '-F',
                False: '-F-',
            }
            'get_local': {
                True: '-G',
                False: '-G-',
            }
            'get_file_compare': {
                'content': '-GCC',
                'datetime': '-GCD',
                'checksum': '-GCK',
            },
            'get_force_dir': {
                True: '-GF',
                False: '-GF-',
            }
            'get_folder': '-GL"{param}"',
            'get_eol': {
                'lf': '-GN',
                'cr': '-GR',
                'crlf': '-GRN',
            },
            'get_datetime': {
                'current': '-GTC',
                'modified': '-GTM',
                'checkin': '-GTU',
            },
            'get_dialog': '-GWA',
            'get_merge_files': '-GWM',
            'get_replace_files': '-GWR',
            'get_skip_files': '-GWS',
            'help_online': '-H',
            'ignore': {
                'selected': '-I',
                'all': '-I-',
                'yes': '-I-Y',
                'no': '-I-N',
                'case': '-IC',
                'eol': '-IE',
                'small': '-IS',
                'whitespace': '-IW',
            },
            'keep_checked_out': {
                True: '-K',
                False: '-K-',
            }
            'label': '-L{param}',
            'local': '-L',
            'no_local': '-L-',
            'exclusive_checkouts': {
                True: '-M-',
                False: '-M',
            }
            'file_name_mode': {
                'default': '-N',
                'long': '-NL',
                'short': '-NS',
            },
            'output': {
                'all': '-O',
                'error': '-O-',
                'disable': '-0&-',
            },
            'output_file': '-O@{param}',
            'project': {
                'current': '-P',
            },
            'project_name': '-P{param}',
            'quiet': '-Q',
            'recursive': '-R',
            'smart_mode': {
                True: '-S',
                False: '-S-',
            }
            'user': {
                'current': '-U',
            }
            'user_name': '-U{param}',
            'version_number': '-V{param}',
            'version_date': '-Vd{param}',
            'version_label': '-Vl{param}',
            'working_copy': {
                'read_write': '-W',
                'read_only': '-W-',
            },
            'vss_user_name': '-Y{param}',
        }

        for option, value in options.items():

            if not option in options_map:
                raise ValueError('Invalid option name (%s)' % repr(option))

            map_entry = options_map[option]

            if isinstance(map_entry, dict):

                def handle_value(v):
                    if not v in map_entry:
                        raise ValueError('Invalid option value for %s (%s)' % (repr(option), repr(v)))

                    result.append(map_entry[v])

                if isinstance(value, list):
                    for v in value:
                        handle_value(v)
                else:
                    handle_value(value)

            elif isinstance(map_entry, str):

                result.append(map_entry.replace('{param}', value or ''))

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