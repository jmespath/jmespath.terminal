"""JMESPath text terminal."""
import os
import sys
import json
import argparse

import urwid
import jmespath
import pygments.lexers


__version__ = '0.2.1'


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
OUTPUT_MODES = [
    'result',
    'expression',
    'quiet',
]


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

    def __init__(self, input_data, output_mode='result'):
        self.view = None
        self.parsed_json = input_data
        self.lexer = pygments.lexers.get_lexer_by_name('json')
        self.formatter = ConsoleJSONFormatter()
        self.output_mode = output_mode
        self.last_result = None
        self.last_expression = None

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
        self.last_expression = text
        if not text:
            # If a user has hit backspace until there's no expression
            # left, we can exit early and just clear the result text
            # panel.
            self.jmespath_result.set_text('')
            return
        try:
            result = jmespath.compile(text).search(self.parsed_json)
            self.footer.set_text("Status: success")
        except Exception:
            pass
        else:
            if result is not None:
                self.last_result = result
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
        elif key == 'ctrl ]':
            # Keystroke to quickly empty out the
            # currently entered expression.  Avoids
            # having to hold backspace to delete
            # the current expression current expression.
            self.input_expr.edit_text = ''
            self.jmespath_result.set_text('')
        elif key == 'ctrl p':
            new_mode = OUTPUT_MODES[
                (OUTPUT_MODES.index(self.output_mode) + 1) % len(OUTPUT_MODES)]
            self.output_mode = new_mode
            self.footer.set_text("Status: output mode set to %s" % new_mode)

    def display_output(self, filename):
        if self.output_mode == 'result' and \
                self.last_result is not None:
            result = json.dumps(self.last_result, indent=2)
        elif self.output_mode == 'expression' and \
                self.last_expression is not None:
            result = self.last_expression
        else:
            # If the output_mode is 'quiet' then we don't need to print anything.
            return
        if filename is not None:
            with open(filename, 'w') as f:
                f.write(result)
        else:
            sys.stdout.write(result)


def _load_input_json(filename):
    if filename is not None:
        with open(filename) as f:
            input_json = json.load(f)
    elif not os.isatty(sys.stdin.fileno()):
        # If stdin is a pipe, we need read the JSON from
        # stdin and then reset stdin this back to the controlling tty.
        input_json = json.loads(sys.stdin.read())
        sys.stdin = open(os.ctermid(), 'r')
    else:
        # If the user didn't provide a filename,
        # we want to be helpful so we'll use a sample
        # document so they can still try out the
        # JMESPath Terminal.
        input_json = SAMPLE_JSON
    return input_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input-json', nargs='?',
                        help='The initial input JSON file to use. '
                        'If this value is not provided, a sample '
                        'JSON document will be provided.')
    parser.add_argument('-m', '--output-mode',
                        choices=OUTPUT_MODES,
                        default='result',
                        help="Specify what's printed to stdout "
                        "when jpterm exits. This can also be changed "
                        "when jpterm is running using Ctrl-o")
    parser.add_argument('-o', '--output-file',
                        help="By default, the output is printed "
                        "to stdout when jpterm exits.  You can "
                        "instead direct the output to a file using "
                        "the -o/--ouput-file option.")
    parser.add_argument('--version', action='version',
                        version='jmespath-term %s' % __version__)

    args = parser.parse_args()
    try:
        input_json = _load_input_json(getattr(args, 'input-json', None))
    except ValueError as e:
        sys.stderr.write("Unable to load the input JSON: %s\n\n" % e)
        return 1

    screen = urwid.raw_display.Screen()
    display = JMESPathDisplay(input_json, args.output_mode)
    try:
        display.main(screen=screen)
    except KeyboardInterrupt:
        pass
    display.display_output(args.output_file)
    return 0


if __name__ == '__main__':
    sys.exit(main())
