# BTextView

A {cpp:class}`BTextView` object displays text on-screen, and provides these manipulating features:

- It lets the user enter, select, and edit text from the keyboard and mouse.

- It supports standard Cut, Copy, Paste, Delete, and Select All editing commands.

- It provides an Undo mechanism.

By default, a {cpp:class}`BTextView` displays all its text in a single font and color. The
{cpp:func}`~BTextView::SetStylable()` turns on support for multiple character formats.

Paragraph formats---such as alignment and tab widths---are uniform for all text the
{cpp:class}`BTextView` displays. These properties can be set, but the setting always applies to the
entire text.

:::{admonition} Warning
:class: warning
The {cpp:class}`BTextView` class isn't multi-thread safe; don't issue {cpp:class}`BTextView` calls
on a {cpp:class}`BTextView` object from multiple threads, or you may see unusual behavior; in
general, only the thread that created the {cpp:class}`BTextView` should issue calls on it.
:::

## Offsets

The {cpp:class}`BTextView` locates particular characters in its text buffer by offsets from the
beginning of the data. The offsets count bytes, not characters, and begin at 0. A single character
is identified by the offset of the first byte of the character. A group of characters---the current
selection, for example---is delimited by the offsets that bound its first and last characters; all
characters beginning with the first offset up to, but not including, the last offset are part of the
group.

For example, suppose the {cpp:class}`BTextView` contains the following text in UTF-8 encoding,

```
Haiku® is . . .
```

and "Haiku®" is selected. {cpp:func}`~BTextView::GetSelection()` would return 4 and 12 as the
offsets that enclose the selection. The character 'H' occupies the fourth byte of text and the space
following the registered trademark symbol is the twelth byte of text. The characters in "Haiku" are
encoded in one byte, but '®' takes up three bytes in UTF-8. Thus the five-character selection
occupies 7 bytes (and offsets) of text.

Although offsets count bytes, they can also be thought of as designating positions between
characters. The position at the beginning of the text is offset 0, the position between the sapce
and the 'H' in the example above is at offset 4, the position between the '®' and the space is at
offset 12, and so on. Thus, even if no characters are selected, the insertion point (and location of
the caret) can still be designated by an offset.

Most {cpp:class}`BTextView` functions expect the offsets they're passed to mark positions between
characters; the results are not defined if a character-internal offset is specified instead.

## Graphics Primitives

The {cpp:class}`BTextView`s mechanism for formatting and drawing text uses the graphics primitives
it inherits from the {cpp:class}`BView` class. However, it largely presents its own API for
determining the appearance of the text it draws. You should not attempt to affect the
{cpp:class}`BTextView` by calling primitive {cpp:class}`BView` functions like
{cpp:func}`~BView::MovePenTo()`, {cpp:func}`~BView::SetFont()`, or
{cpp:func}`~BView::SetHighColor()`. Instead, use {cpp:class}`BTextView` functions like
{cpp:func}`~BTextView::SetFontAndColor()` and let the object take care of formatting and drawing the
text.

The one inherited function that can influence the {cpp:class}`BTextView` is
{cpp:func}`~BView::SetViewColor()`. This function determines the background against which the text
is drawn and the color that is used in antialiasing calculations.

## Resizing

A {cpp:class}`BTextView` can be made to resize itself to exactly fit the text that the user enters.
This is sometimes appropriate for small one-line text fields. See the
{cpp:func}`~BTextView::MakeResizable()` function.

## BTextView and BScrollBars

If you add scrollbars to control the position of the {cpp:class}`BTextView`'s document---this
includes using a {cpp:class}`BTextView` as the target of a {cpp:class}`BScrollView`---the
{cpp:class}`BTextView` will update the scrollbars for you. (Note that it doesn't own the scrollbars;
you still have to delete them yourself if you created them.) When the {cpp:class}`BTextView` is
first displayed and thereafter resized, the scrollbars' ranges, step sizes, and scroller positions
and proportions are automatically reset to refelct the {cpp:class}`BTextView` object's bounds.
Attempts to set these parameters directly (through {cpp:func}`BScrollBar::SetRange() etc.), are
worse than ignored; they're actually applied, and then (at some point) the {cpp:class}`BTextView`
will notice the change in the scrollbars and reset them. Looks like flicker to me.

## Shortcuts and Menu Items

When it's the focus view for its window, a {cpp:class}`BTextView` automatically responds to a set of
keyboard shortcuts:

- {key}`Command` + {key}`x` cuts text and copies it to the clipboard
- {key}`Command` + {key}`c` copies text to the clipboard without cutting it
- {key}`Command` + {key}`v` pastes text taken from the clipboard
- {key}`Command` + {key}`a` selects all of the text in the {cpp:class}`BTextView`
- {key}`Command` + {key}`z` undoes the previous action

If you create menu items for these actions, you have to assign the {cpp:class}`BMenuItem` shortcuts
and command constants yourself:

:::{list-table}
---
header-rows: 1
---
-
	- Action

	- Constant

	- Shortcut

-
	- Select all

	- {cpp:enum}`B_SELECT_ALL`

	- {key}`Command` + {key}`a`

-
	- Cut

	- {cpp:enum}`B_CUT`

	- {key}`Command` + {key}`x`

-
	- Copy

	- {cpp:enum}`B_COPY`

	- {key}`Command` + {key}`c`

-
	- Paste

	- {cpp:enum}`B_PASTE`

	- {key}`Command` + {key}`v`

-
	- Undo

	- {cpp:enum}`B_UNDO`

	- {key}`Command` + {key}`z`
