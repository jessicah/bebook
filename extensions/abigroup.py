from docutils import nodes
from docutils.nodes import Element, inline, Inline, TextElement
from docutils.parsers.rst import Directive, directives

from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment
from sphinx.writers.html5 import HTML5Translator
from sphinx.builders import Builder
from sphinx.builders.html import StandaloneHTMLBuilder

from sphinx.util import logging

logger = logging.getLogger(__name__)

# custom nodes for hooking in the translator

class abigroup(Element): pass

# the `{abi-group}` directive
#
# - contains nested content, including `{cpp:function}`
#   directives that are used to generate a combined header
class AbiGroupDirective(Directive):
    has_content = True
    required_arguments = 1

    def run(self):
        abinode = abigroup('\n'.join(self.content))
        id = self.arguments[0].strip()
        
        sectionnode = nodes.section(ids=[id])
        sectionnode += nodes.title(text=id)
        sectionnode += abinode
        
        self.add_name(abinode)
        self.state.nested_parse(self.content, self.content_offset, abinode)
        return [sectionnode]

class CustomHTMLTranslator(HTML5Translator):
    def __init__(self, document: nodes.document, builder: Builder) -> None:
        super().__init__(document, builder)

        self.in_abi_group = False
    
    # override descriptor nodes to omit content generation in
    # an abi group...
    #
    # although... perhaps it would be nice to reuse the code for
    # an abi group, and also a single function description, to get
    # the same output.
    # i.e. still generating an H3 if it's not in an ABI group, and
    # then adding the code block of the whole signature, as would
    # be done in an ABI group. And then an ABI group would be a
    # specialisation of combining multiple signatures into a single
    # header (and separate code blocks)
    def visit_desc(self, node):
        if not self.in_abi_group:
            super().visit_desc(node)

    def depart_desc(self, node):
        if not self.in_abi_group:
            super().depart_desc(node)

    def visit_desc_signature(self, node: Element) -> None:
        # need to save the c++ domain IDs
        if not self.in_abi_group:
            super().visit_desc_signature(node)
            return
        
        self.signature_ids += node.attributes['ids']

    def depart_desc_signature(self, node):
        if not self.in_abi_group:
            super().depart_desc_signature(node)
        
    def visit_desc_signature_line(self, node):
        if not self.in_abi_group:
            super().visit_desc_signature_line(node)
        
        self.body.append('<pre style="background: #f3f3f3">')
        
    def depart_desc_signature_line(self, node):
        # probably still want the entire signature line
        # for copying into the ABI group later
        if not self.in_abi_group:
            super().depart_desc_signature_line(node)
        
        self.body.append('</pre>')
    
    def visit_desc_content(self, node):
        if not self.in_abi_group:
            super().visit_desc_content(node)
        
        # at this point, can we collapse pre?
    
    def depart_desc_content(self, node):
        if not self.in_abi_group:
            super().depart_desc_content(node)
    
    def visit_desc_name(self, node: Element) -> None:
        if not self.in_abi_group:
            super().visit_desc_name(node)
            return
        
        #self.signature_names.append(node)
        name = ''.join(str(c) for c in node[0].children) + '()'
        self.signature_names.append(name)
    
    def depart_desc_name(self, node):
        if not self.in_abi_group:
            super().depart_desc_name(node)
            return
        
        # if the previous name == this name, then...
        # we want to either a) omit the pre tag
        try:
            previous = self.signature_names[-2]
            current = self.signature_names[-1]
        except IndexError:
            pass
    
    def visit_abigroup(self, node):
        self.in_abi_group = True
        self.signature_ids = []
        self.signature_names = []
        self.saved_body = self.body
        self.body = []
    
    def depart_abigroup(self, node):
        node.attributes['ids'] = self.signature_ids

        logger.warning(' **** DEPART ABI GROUP .....')
        saved_link = ''
        while True:
            item = self.saved_body.pop()
            logger.warning('item = {}'.format(item))
            if item.startswith('<a'):
                saved_link = item
            if item.startswith('<h3>'):
                break
        logger.warning(' ===========================')
        
        names = []
        for name in self.signature_names:
            if name not in names:
                names.append(name)
        
        self.body = self.saved_body + [self.starttag(node, 'h3') + ', '.join(names) + '</h3>\n\n'] + ['<div class="wrapper">'] + self.body + ['</div>\n\n']

        self.in_abi_group = False
        self.signature_ids = None
        self.signature_names = None
        self.saved_body = None
    
    def visit_highlight(self, node):
        self.body.append('<span class="' + node.classes + '">')
    
    def depart_highlight(self, node):
        self.body.append('</span>')

class highlight(Inline, TextElement): pass

class highlightMethod(highlight):
    classes = 'hmethod'

class highlightClass(highlight):
    classes = 'hclass'

class highlightParameter(highlight):
    classes = 'hparameter'

class highlightField(highlight):
    classes = 'hfield'

def setup(app):
    app.add_directive('abi-group', AbiGroupDirective)
    app.add_generic_role('hmethod', highlightMethod)
    app.add_generic_role('hclass', highlightClass)
    app.add_generic_role('hparameter', highlightParameter)
    app.add_generic_role('hparam', highlightParameter)
    app.add_generic_role('hfield', highlightField)
    app.set_translator('html', CustomHTMLTranslator, True)
