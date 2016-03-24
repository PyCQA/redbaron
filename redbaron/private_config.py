ipython_behavior = True
force_ipython_behavior = False

def runned_from_ipython():
    # for testing
    if force_ipython_behavior:
        return True

    if not ipython_behavior:
        return False
    try:
        __IPYTHON__
        return True
    except NameError:
        return False
