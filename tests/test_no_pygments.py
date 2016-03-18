from redbaron import RedBaron, private_config

private_config.force_ipython_behavior = True
private_config.DEBUG = True


def test_repr():
    assert private_config.runned_from_ipython()
    RedBaron("a = 1").__str__()
    RedBaron("a = 1")[0].__str__()
    RedBaron("a = 1").__repr__()
    RedBaron("a = 1")[0].__repr__()


def test_help():
    RedBaron("a = 1").help()
    RedBaron("a = 1")[0].help()


def test_endl_html():
    RedBaron("a\n").node_list[-1]._repr_html_()
