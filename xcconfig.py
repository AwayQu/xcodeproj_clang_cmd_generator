import codecs
import string


class xcconfig(object):
    xcconfig_file_path = None
    data = None
    config = None

    def __init__(self, xcconfig_file_path):
        super(xcconfig, self).__init__()
        self.xcconfig_file_path = xcconfig_file_path
        fd = codecs.open(self.xcconfig_file_path, 'r', encoding='utf-8-sig', errors='ignore')
        self.data = fd.read()
        self.config = {}

        self._parse()

    def _parse(self):
        lines = self.data.split(u'\n')
        for line in lines:
            kv = line.split(u'=')
            self.config[kv[0].strip(string.whitespace)] = kv[1]


if __name__ == '__main__':
    # TODO: Test & Read $variable
    pass