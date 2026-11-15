import ast

import pytest

from redbaron import RedBaron


@pytest.mark.parametrize("body", [
    "try:\n    pass\nexcept:\n    pass\n",
    "try:\n    pass\nfinally:\n    pass\n",
    "try:\n    pass\nexcept ValueError:\n    pass\nexcept TypeError:\n    pass\n",
    "try:\n    pass\nexcept:\n    pass\nelse:\n    pass\nfinally:\n    pass\n",
    "for item in []:\n    pass\nelse:\n    pass\n",
    "while False:\n    pass\nelse:\n    pass\n",
    "with open('example') as handle:\n    pass\n",
    "if True:\n    pass\nelse:\n    pass\n",
])
def test_removing_a_function_preserves_the_previous_functions_blocks(body):
    source = ("def foo():\n" + "".join("    " + line + "\n" for line in body.splitlines())
              + "\n\ndef bar():\n    pass\n\nfoo()\n")
    original = ast.parse(source)
    red = RedBaron(source)
    red.remove(red.find("def", name="bar"))

    result = ast.parse(red.dumps())
    assert len(result.body) == 2
    assert ast.dump(result.body[0]) == ast.dump(original.body[0])
    assert ast.dump(result.body[1]) == ast.dump(original.body[2])


def test_removing_a_comment_preserves_an_earlier_try_block():
    source = ("def foo():\n"
              "    try:\n"
              "        pass\n"
              "    except:\n"
              "        pass\n"
              "    # remove this comment\n"
              "    return 1\n")
    red = RedBaron(source)
    comment = red.find("comment")
    comment.parent.remove(comment)

    assert "remove this comment" not in red.dumps()
    assert ast.dump(ast.parse(red.dumps())) == ast.dump(ast.parse(source))
