import logging
import re


class NoEscape(logging.Filter):

    def __init__(self):
        self.regex = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')

    def strip_esc(self, s):
        try:  # string-like
            return self.regex.sub('', s)
        except Exception:  # non-string-like
            return s

    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = self.strip_esc(record.msg)
        if type(record.args) is tuple:
            record.args = tuple(map(self.strip_esc, record.args))
        return True


remove_color_filter = NoEscape()
