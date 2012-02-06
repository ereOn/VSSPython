"""
A set of high-level functions to ease the use of Microsoft Visual SourceSafe.
"""

from vss import VSS

def checkout(repository_path, vss_project_path, local_path, ss_path=None):
    """
    Check out a VSS project to the specified local directory.

    Return the standard output.
    """

    vss = VSS(repository_path, ss_path)

    return vss.checkout(vss_project_path, recursive=True, get_folder=local_path, output='error')

def undo_checkout(repository_path, vss_project_path, local_path, ss_path=None):
    """
    Undo a checkout of a VSS project to the specified local directory.

    Return the standard output.
    """

    vss = VSS(repository_path, ss_path)

    return vss.undo_checkout(vss_project_path, recursive=True, get_folder=local_path, output='error')

def checkin(repository_path, vss_project_path, local_path, ss_path=None):
    """
    Check in a VSS project from the specified local directory.

    Return the standard output.
    """

    vss = VSS(repository_path, ss_path)

    return vss.checkin(vss_project_path, recursive=True, get_folder=local_path, output='error', comment_no_text=True)

