# BMediaFormats

The {cpp:class}`BMediaFormats` class provides a means for translating
between BeOS media format identifiers and those used by the codecs
themselves. This is primarily useful if you're writing a codec add-on or a
file format parser.

## Supported Families

The {cpp:class}`BMediaFormats` class currently knows how to translate
among the following formats' codec identification methods:

:::{list-table}
---
header-rows: 0
align: left
widths: auto
---
-
	- BeOS
	- BeOS uses a constant within the {cpp:func}`media_format <media::format>`
		structure to indicate the kind of media being handled.
-
	- QuickTime
	- QuickTime uses a two-word vendor/codec pair to indicate the type of media.
-
	- AVI
	- The media format is indicated by a one-word constant.
-
	- AVR
	- The media format is indicated by a one-word constant.
-
	- ASF
	- The media format is indicated by a 128-bit UUID value.
-
	- MPEG
	- The media format is specified by a word that indicates the MPEG version
		and layer.
-
	- AIFF
	- The media format is specified by a codec ID word.
-
	- WAV
	- The media format is specified by a codec ID word.
-
	- Miscellaneous
	- The media format is indicated by a one-word file format value and a
		one-word codec ID.

:::
