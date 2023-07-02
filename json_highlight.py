from json import dumps
from pygments import highlight, lexers, formatters


# Function ++
class extract_json_colorful():
    def __init__(self, obj, sortkey):
        self.obj = obj
        self.sortkey = sortkey

    def jsonhighlight(self):
        formatted_json = dumps(self.obj, indent=1, sort_keys=bool(self.sortkey), default=str)
        colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
        return colorful_json

    def dumptonjson(self):
        formatted_json = dumps(self.obj, indent=1, sort_keys=bool(self.sortkey), default=str)
        return formatted_json
