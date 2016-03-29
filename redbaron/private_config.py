from __future__ import absolute_import

import redbaron


def runned_from_ipython():
    # for testing
    if redbaron.force_ipython_behavior:
        return True

    if not redbaron.ipython_behavior:
        return False
    try:
        __IPYTHON__
        return True
    except NameError:
        return False
