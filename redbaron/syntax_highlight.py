HAS_PYGMENTS = True

try:
    import pygments
except ImportError:
    HAS_PYGMENTS = False


if HAS_PYGMENTS:
    from pygments.token import Comment, Text, String, Keyword, Name, Operator
    from pygments.lexer import RegexLexer, bygroups
    from pygments import highlight
    from pygments.lexers import PythonLexer
    from pygments.formatters import Terminal256Formatter, HtmlFormatter


    class HelpLexer(RegexLexer):
        name = 'Lexer for RedBaron .help() method output'

        tokens = {
            'root': [
                (r"#.*$", Comment),
                (r"('([^\\']|\\.)*'|\"([^\\\"]|\\.)*\")", String),
                (r"(None|False|True)", String),
                (r'(\*)( \w+Node)', bygroups(Operator, Keyword)),
                (r'\w+Node', Name.Function),
                (r'(\*|=|->|\(|\)|\.\.\.)', Operator),
                (r'\w+', Text),
                (r'\s+', Text),
            ]
        }

    def help_highlight(string):
        return highlight(string, HelpLexer(), Terminal256Formatter(style='monokai'))

    def python_highlight(string):
        return highlight(string, PythonLexer(encoding="Utf-8"),
                         Terminal256Formatter(style='monokai',
                                              encoding="Utf-8"))

    def python_html_highlight(string):
        return highlight(string, PythonLexer(encode="Utf-8"),
                         HtmlFormatter(noclasses=True, encoding="UTf-8"))

else:
    def help_highlight(string):
        return string.encode("Utf-8")

    def python_highlight(string):
        return string.encode("Utf-8")

    def python_html_highlight(string):
        return string.encode("Utf-8")
