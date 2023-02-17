__version__ = "1.0"

from docutils import nodes

from myst_parser.config.main import (
    MdParserConfig,
    TopmatterReadError,
    merge_file_level,
    read_topmatter,
)
from myst_parser.mdit_to_docutils.sphinx_ import SphinxRenderer
from myst_parser.parsers.mdit import create_md_parser
from myst_parser.mdit_to_docutils.sphinx_ import create_warning
from myst_parser.parsers.sphinx_ import MystParser

from mdit_py_abbr import abbr_plugin

class CustomParser(MystParser):
	def parse(self, inputstring: str, document: nodes.document) -> None:
		config: MdParserConfig = document.settings.env.myst_config

		try:
			topmatter = read_topmatter(inputstring)
		except TopmatterReadError:
			pass
		else:
			if topmatter:
				warning = lambda wtype, msg: create_warning(
					document, msg, wtype, line=1, append_to=document
				)
				config = merge_file_level(config, topmatter, warning)
		
		parser = create_md_parser(config, SphinxRenderer)
		parser.options["document"] = document
		parser.use(abbr_plugin)
		parser.render(inputstring)

def setup(app):
	from myst_parser.sphinx_ext.main import setup_sphinx

	setup_sphinx(app, load_parser=True)
	return {"version": __version__, "parallel_read_safe": True}
