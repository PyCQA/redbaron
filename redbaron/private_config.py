ipython_behavior = True
DEBUG = False

def runned_from_ipython():
    if not ipython_behavior:
        return False
    try:
        __IPYTHON__
        return True
    except NameError:
        return False
