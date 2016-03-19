from redbaron import RedBaron, private_config


class Test():
    def setup_method(self, method):
        private_config.force_ipython_behavior = True
        private_config.DEBUG = True

    def teardown_method(self, method):
        private_config.force_ipython_behavior = False
        private_config.DEBUG = False

    def test_repr(self):
        RedBaron("a = 1").__str__()
        RedBaron("a = 1")[0].__str__()
        RedBaron("a = 1").__repr__()
        RedBaron("a = 1")[0].__repr__()

    def test_help(self):
        RedBaron("a = 1").help()
        RedBaron("a = 1")[0].help()

    def test_endl_html(self):
        RedBaron("a\n").node_list[-1]._repr_html_()

    def test_regression_repr(self):
        red = RedBaron("a = 1 + caramba")
        red[0].value.first.parent
        str(red[0].value.first.parent)


class TestClassical(Test):
    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass
