from pygments.style import Style
from pygments.token import *


class BeBookStyle(Style):
    background_color = "#f3f3f3"
    default_style = ""
    styles = {
        Text:                      "#253555",
        Other:                     "#253555",
        Whitespace:                "#434357",
        Comment:                   "italic #dc3c01",
        Comment.Preproc:           "#409090",
        Comment.PreprocFile:       "bg:#404040 #ffcd8b",
        Comment.Special:           "#808bed",
        Name:                      "#000000",
        Name.Class:                "bold #006400",
        Name.Function:             "bold #800080"
        # ... snip (just more colors, you get the idea) ...
    }
