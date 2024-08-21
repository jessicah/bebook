from pygments import highlight
from pygments.lexers import CppLexer
from pygments.formatters import HtmlFormatter
from pygments.filters import Filter
from pygments.token import Name

code = '''
#include <Application.h>

main()
{
        new BApplication("application/x-vnd.your-app-sig");
        /* Further initialization goes here -- read settings,
           set globals, etc. */
        be_app->Run();
        /* Clean up -- write settings, etc. */
        delete be_app;
}
'''
class CustomFilter(Filter):
    def __init__(self, **options):
        Filter.__init__(self, **options)

    def filter(self, lexer, stream):
        for ttype, value in stream:
            if value == "BApplication":
                ttype = Name.Class
            yield ttype, value

l = CppLexer()
l.add_filter(CustomFilter())

print(highlight(code, l, HtmlFormatter()))
