import urwid
import jmespath
import json
import argparse


SAMPLE_JSON = {
    'a': 'foo',
    'b': 'bar',
    'c': {
        'd': 'baz',
        'e': [1,2,3]
    }
}



class JMESPathDisplay(object):
    PALETTE = [
        ('input expr', 'bold', 'default', 'bold'),
    ]

    def __init__(self, input_data):
        self.view = None
        self.parsed_json = input_data

    def _create_view(self):
        self.input_expr = urwid.Edit(('input expr', "JMESPath Expression: "))
        self.status_bar = urwid.Text("JMESPath status")
        self.header = urwid.Pile([self.input_expr, self.status_bar],
                                 focus_item=0)
        urwid.connect_signal(self.input_expr, 'change', self._on_edit)

        self.input_json = urwid.Text(json.dumps(self.parsed_json, indent=2))
        self.input_json_list = [self.input_json]
        self.left_content = urwid.ListBox(self.input_json_list)

        self.jmespath_result = urwid.Text("JMESPath result")
        self.jmespath_result_list = [self.jmespath_result]
        self.right_content = urwid.ListBox(self.jmespath_result_list)

        self.content = urwid.Columns([self.left_content, self.right_content])

        self.footer = urwid.Text("Footer")
        self.view = urwid.Frame(body=self.content, header=self.header,
                                footer=self.footer, focus_part='header')

    def _on_edit(self, widget, text):
        try:
            parsed = jmespath.compile(text)
        except Exception:
            pass
        else:
            result = parsed.search(self.parsed_json)
            if result is not None:
                self.jmespath_result.set_text(json.dumps(result, indent=2))

    def main(self):
        self._create_view()
        self.loop = urwid.MainLoop(self.view, self.PALETTE,
                                   unhandled_input=self.unhandled_input)
        self.loop.run()

    def unhandled_input(self, key):
        if key == 'f8':
            raise urwid.ExitMainLoop()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_json', help='The initial input JSON file to use.')

    args = parser.parse_args()
    if args.input_json is not None:
        input_json = json.load(open(args.input_json))
    else:
        input_json = SAMPLE_JSON

    display = JMESPathDisplay(input_json)
    display.main()


if __name__ == '__main__':
    main()
