# bebook
The Be Book / Haiku Book Amalgamation

This contains the work of creating the Be Book documentation in reStructuredText/Markdown
formats with Sphinx and MyST-Parser, and merging the Haiku Book documentation into the Be Book.

It is hoped that this will result in much more complete API documentation.

# install

``` py
pip install beautifulsoup4
pip install lxml
pip install sty
```

# remaining issues

`system-overview/game/direct-window.md` has a list table containing a definition list.

`topics/device-drivers/driver-settings-api.md` has an unordered list containing a code block.
