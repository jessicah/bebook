---
title: The Translation Kit
---

# Introduction

The Translation Kit provides a framework for converting data streams between different media
formats. A word processor, for example, could use the Translation Kit to import and export documents
in a variety of formats, including HTML, PostScript, and plain ASCII, while working in its own
native format.

The translation itself is performed by translator add-ons (or, less globally,
{cpp:class}`BTranslator` objects). You can create your own translator add-ons and
{cpp:class}`BTranslator` subclasses, or you can use the translators that are supplied by Haiku and
third parties.

The Translation Kit operates on {cpp:class}`BPositionIO` objects and their descendants. Since
{cpp:class}`BFile` derives from {cpp:class}`BPositionIO`, the Translation Kit is naturally suited
for importing and exporting files. However, it's far more general; the Translation Kit could be
used, for example, to translate input directly to or from a network connection, provided a suitable
{cpp:class}`BPositionIO` subclass was available. More importantly, {cpp:class}`BMemoryIO` and
{cpp:class}`BMallocIO` can be used to load data directly into or out of memory.

Applications primarily interact with the Translation Kit through the {cpp:class}`BTranslatorRoster`
class. This class encapsulates the functionality required to load and unload translators, discover
their capabilities, configure the translators, and execute the translators.

Applications may also use the {cpp:class}`BTranslationUtils` class, a collection of static utility
functions designed to simplify access to the Translation Kit. Currently the class only defines
members for loading bitmap images from files, resources, and general {cpp:class}`BPositionIO` data
streams.

---

# Media Formats

The Translation Kit identifies a particular media format by a media group and format type. Media
groups identify the class of media represented by a format. Defintions for the common media groups
can be found i `translation/TranslatorFormats.h`.

:::{list-table}
---
header-rows: 1
---
-
	- Media Group
	- Constant
-
	- Bitmap
	- {cpp:enum}`B_TRANSLATOR_BITMAP`
-
	- `BPicture` data
	- {cpp:enum}`B_TRANSLATOR_PICTURE`
-
	- Text
	- {cpp:enum}`B_TRANSLATOR_TEXT`
-
	- Sound
	- {cpp:enum}`B_TRANSLATOR_SOUND`
-
	- Standard MIDI
	- {cpp:enum}`B_TRANSLATOR_MIDI`
-
	- Streaming media
	- {cpp:enum}`B_TRANSLATOR_MEDIA`
-
	- nothing
	- {cpp:enum}`B_TRANSLATOR_NONE`
:::

A format type is a type constant identifying the specific data format, i.e. tiff, aiff, mpeg. The
standard type constants can be found in `support/TypeConstants.h`.

It is often convenient to define a baseline format to which all translators of a given media group
adhere. An application that understands the baseline format could then use all the translators for
that group. This also simplifies the job of the translator, which minimally needs only to translate
between the baseline and the new formats. Well-behaved translators will always be able to translate
to and from the default media format (if one exists for its media group).

The Translation Kit defines a default media format for each existing media group. They are explained
at length in the section ["Default Media Formats"](...). The format type constant for each default
format is the same as the media group constant; for example, the format type for the default bitmap
format is {cpp:enum}`B_TRANSLATOR_BITMAP`.
