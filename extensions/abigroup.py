from docutils import nodes
from docutils.nodes import Element
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
    required_arguments = 0

    def run(self):
        # nested parsing of content added to an abigroup node
        text = '\n'.join(self.content)
        node = abigroup(text)
        self.add_name(node)
        self.state_nested_parse(self.content, self.content_offset, node)
        return [node]

class CustomHTMLTranslator(HTML5Translator):
    def __init__(self, document: nodes.document, builder: Builder) -> None:
        super().__init__(document, builder)

        self.in_abi_group = False
    
    # override descriptor nodes to omit content generation in
    # an abi group
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
        
    def depart_desc_signature_line(self, node):
        # probably still want the entire signature line
        # for copying into the ABI group later
        if not self.in_abi_group:
            super().depart_desc_signature_line(node)
    
    def visit_desc_name(self, node: Element) -> None:
        if not self.in_abi_group:
            super().visit_desc_name(node)
            return
        
        self.signature_names.append(node)
    
    def depart_desc_name(self, node):
        if not self.in_abi_group:
            super().depart_desc_name(node)
    
    def visit_abigroup(self, node):
        self.in_abi_group = True
        self.signature_ids = []
        self.signature_names = []
        self.saved_body = self.body
        self.body = []
    
    def depart_abigroup(self, node):
        node.attributes['ids'] = self.signature_ids
        
        names = []
        for child in self.signature_names:
            names.append(''.join(str(c) for c in child[0].children))
        
        self.body = self.saved_body + [', '.join(names) + '</h3>\n\n'] + self.body

        self.in_abi_group = False
        self.signature_ids = None
        self.signature_names = None
        self.saved_body = None

def setup(app):
    app.add_directive('abi-group', AbiGroupDirective)
    app.set_translator('html', CustomHTMLTranslator, True)
