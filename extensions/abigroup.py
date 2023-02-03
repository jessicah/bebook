from docutils import nodes
from docutils.nodes import Element, Inline, TextElement
from docutils.parsers.rst import Directive

from sphinx.writers.html5 import HTML5Translator
from sphinx.builders import Builder
from sphinx import addnodes

from sphinx.util import logging

logger = logging.getLogger(__name__)

class abigroup(Element): pass

class abigrouptitle(Element): pass

class AbiGroupDirective(Directive):
    has_content = True
    required_arguments = 0

    def _search(self, node, visited, cls):
        if isinstance(node, cls):
            return node
        if node not in visited:
            visited.append(node)
            for child in node:
                result = self._search(child, visited, cls)
                if result is None:
                    continue
                return result
        return None

    def search(self, node, cls):
        return self._search(node, [], cls)

    def run(self):
        header_text = []

        assert self.content, 'abi-group: content is required'

        abinode = abigroup()
        self.state.nested_parse(self.content, self.content_offset, abinode)

        indices = [node for node in abinode if isinstance(node, addnodes.index)]
        descriptors = [node for node in abinode if isinstance(node, addnodes.desc)]

        subsections = []

        for (index, descriptor) in zip(indices, descriptors):
            descriptor.ismethod = True if self.search(descriptor, addnodes.desc_parameterlist) else False
            name = self.search(descriptor, addnodes.desc_name)
            signature_line = self.search(descriptor, addnodes.desc_signature_line)

            assert name, 'abi-group: unable to find a function/member'
            ix = name.first_child_matching_class(addnodes.desc_sig_name)
            if ix == None or ix < 0:
                logger.warning('abi-group: unable to find the name of the function/member')
                continue

            title = name[ix].astext() + ('()' if descriptor.ismethod else '')
            if title not in header_text:
                header_text.append(title)
                signature_line.issame = False

                id = index.attributes['entries'][0][2]

                subsectionnode = nodes.section(ids=[id])
                subsectionnode.omit_titles = True
                subsectiontitle = nodes.title(text=title.replace('()', ''))
                subsectionnode += subsectiontitle
                subsections.append(subsectionnode)
            else:
                signature_line.issame = True

        sectiontitle = abigrouptitle()
        sectiontitle.text = ', '.join(header_text)
        subsections.append(sectiontitle)
        subsections.append(abinode)
        return subsections

class CustomHTMLTranslator(HTML5Translator):
    def __init__(self, document: nodes.document, builder: Builder) -> None:
        super().__init__(document, builder)
        self.in_abi_group = False

    def visit_abigrouptitle(self, node):
        heading = f'h{self.section_level + 1}'
        self.body.append(self.starttag(node, heading))
        self.body.append(node.text)

    def depart_abigrouptitle(self, node):
        heading = f'</h{self.section_level + 1}>'
        self.body.append(heading)

    def visit_title(self, node):
        if hasattr(node.parent, 'omit_titles') and node.parent.omit_titles:
            node.children = []
            return

        super().visit_title(node)

    def depart_title(self, node):
        if hasattr(node.parent, 'omit_titles') and node.parent.omit_titles:
            return

        super().depart_title(node)

    def visit_desc(self, node):
        if not self.in_abi_group:
            super().visit_desc(node)

    def depart_desc(self, node):
        if not self.in_abi_group:
            super().depart_desc(node)

    def visit_desc_signature(self, node: Element) -> None:
        if not self.in_abi_group:
            super().visit_desc_signature(node)

    def depart_desc_signature(self, node):
        if not self.in_abi_group:
            super().depart_desc_signature(node)

    def visit_desc_signature_line(self, node):
        omittag = self.in_abi_group and hasattr(node, 'issame') and node.issame == True

        if omittag:
            self.body.pop()
            self.body.append('<br />')
        else:
            self.body.append('<pre style="background: #f3f3f3; line-height: 2em">')

    def depart_desc_signature_line(self, node):
        self.body.append('</pre>')

    def visit_desc_content(self, node):
        if not self.in_abi_group:
            super().visit_desc_content(node)

    def depart_desc_content(self, node):
        if not self.in_abi_group:
            super().depart_desc_content(node)

    def visit_desc_name(self, node: Element) -> None:
        if not self.in_abi_group:
            super().visit_desc_name(node)
            return

    def depart_desc_name(self, node):
        if not self.in_abi_group:
            super().depart_desc_name(node)
            return

    def visit_abigroup(self, node):
        self.in_abi_group = True

    def depart_abigroup(self, node):
        self.in_abi_group = False

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
