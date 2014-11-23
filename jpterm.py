"""JMESPath text terminal."""
import os
import sys
import json
import argparse

import urwid
import jmespath
import pygments.lexers


__version__ = '0.1.0'


SAMPLE_JSON = {
    'a': 'foo',
    'b': 2,
    'c': {
        'd': 'baz',
        'e': [1, 2, 3]
    },
    "d": True,
    "e": None,
    "f": 1.1
}


class ConsoleJSONFormatter(object):
    # We only need to worry about the tokens that can come
    # from lexing JSON.
    TOKEN_TYPES = {
        # For the values of JSON strings.
        'Token.Literal.String.Double': urwid.AttrSpec('dark green', 'default'),
        'Token.Literal.Number.Integer': urwid.AttrSpec('dark blue', 'default'),
        'Token.Literal.Number.Float': urwid.AttrSpec('dark blue', 'default'),
        # null, true, false
        'Token.Keyword.Constant': urwid.AttrSpec('light blue', 'default'),
        'Token.Punctuation': urwid.AttrSpec('light blue', 'default'),
        'Token.Text': urwid.AttrSpec('white', 'default'),
        # Key names in a hash.
        'Token.Name.Tag': urwid.AttrSpec('white', 'default'),

    }
    # Used when the token name is not in the list above.
    DEFAULT_COLOR = urwid.AttrSpec('light blue', 'default'),

    def generate_colors(self, tokens):
        types = self.TOKEN_TYPES
        default = self.DEFAULT_COLOR
        for token_type, token_string in tokens:
            yield types.get(str(token_type), default), token_string


class JMESPathDisplay(object):

    PALETTE = [
        ('input expr', 'black,bold', 'light gray'),
        ('bigtext', 'white', 'black'),
    ]

    def __init__(self, input_data):
        self.view = None
        self.parsed_json = input_data
        self.lexer = pygments.lexers.get_lexer_by_name('json')
        self.formatter = ConsoleJSONFormatter()

    def _create_colorized_json(self, json_string):
        tokens = self.lexer.get_tokens(json_string)
        markup = list(self.formatter.generate_colors(tokens))
        return markup

    def _get_font_instance(self):
        return urwid.get_all_fonts()[-2][1]()

    def _create_view(self):
        self.input_expr = urwid.Edit(('input expr', "JMESPath Expression: "))

        sb = urwid.BigText("JMESPath", self._get_font_instance())
        sb = urwid.Padding(sb, 'center', None)
        sb = urwid.AttrWrap(sb, 'bigtext')
        sb = urwid.Filler(sb, 'top', None, 5)
        self.status_bar = urwid.BoxAdapter(sb, 5)

        div = urwid.Divider()
        self.header = urwid.Pile(
            [self.status_bar, div,
             urwid.AttrMap(self.input_expr, 'input expr'), div],
            focus_item=2)
        urwid.connect_signal(self.input_expr, 'change', self._on_edit)

        self.input_json = urwid.Text(
            self._create_colorized_json(json.dumps(self.parsed_json,
                                                   indent=2))
        )
        self.input_json_list = [div, self.input_json]
        self.left_content = urwid.ListBox(self.input_json_list)
        self.left_content = urwid.LineBox(self.left_content,
                                          title='Input JSON')

        self.jmespath_result = urwid.Text("")
        self.jmespath_result_list = [div, self.jmespath_result]
        self.right_content = urwid.ListBox(self.jmespath_result_list)
        self.right_content = urwid.LineBox(self.right_content,
                                           title='JMESPath Result')

        self.content = urwid.Columns([self.left_content, self.right_content])

        self.footer = urwid.Text("Status: ")
        self.view = urwid.Frame(body=self.content, header=self.header,
                                footer=self.footer, focus_part='header')

    def _on_edit(self, widget, text):
        try:
            result = jmespath.compile(text).search(self.parsed_json)
            self.footer.set_text("Status: success")
        except Exception:
            pass
        else:
            if result is not None:
                result_markup = self._create_colorized_json(
                    json.dumps(result, indent=2))
                self.jmespath_result.set_text(result_markup)

    def main(self, screen=None):
        self._create_view()
        self.loop = urwid.MainLoop(self.view, self.PALETTE,
                                   unhandled_input=self.unhandled_input,
                                   screen=screen)
        self.loop.screen.set_terminal_properties(colors=256)
        self.loop.run()

    def unhandled_input(self, key):
        if key == 'f5':
            raise urwid.ExitMainLoop()
        if key == 'ctrl ]':
            # Keystroke to quickly empty out the
            # currently entered expression.  Avoids
            # having to hold backspace to delete
            # the current expression current expression.
            self.input_expr.edit_text = ''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input-json', nargs='?',
                        help='The initial input JSON file to use. '
                        'If this value is not provided, a sample '
                        'JSON document will be provided.')
    parser.add_argument('--version', action='version',
                        version='jmespath-term %s' % __version__)

    args = parser.parse_args()
    input_json = getattr(args, 'input-json', None)
    if input_json is not None:
        with open(input_json) as f:
            input_json = json.load(f)
    else:
        input_json = SAMPLE_JSON

    if not os.isatty(sys.stdin.fileno()):
        # If stdin is a pipe, we need read the JSON from
        #stdin and then reset stdin this back to the controlling tty.
        input_json = json.loads(sys.stdin.read())
        sys.stdin = open(os.ctermid(), 'r')

    screen = urwid.raw_display.Screen()
    display = JMESPathDisplay(input_json)
    display.main(screen=screen)


if __name__ == '__main__':
    main()
