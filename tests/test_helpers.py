from redbaron import RedBaron


def test_import_modules():
    red = RedBaron("import a, b.c, d.e as f")
    assert red[0].modules() == ['a', 'b.c', 'd.e']
