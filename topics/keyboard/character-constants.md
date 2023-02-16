# Character Constants

The Interface Kit defines constants for characters that aren't normally
represented by a visible symbol. This includes the usual space and
backspace characters, but most invisible characters are produced by the
function keys and the navigation keys located between the main keyboard and
the numeric keypad. The character values associated with these keys are
more or less arbitrary, so you should always use the constant in your code
rather than the actual character value. Many of these characters are also
produced by alphabetic keys when a {hkey}`Control` key is held down.

The table below lists character constants defined in the kit and the keys
they're associated with.

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Key label

	- Key code

	- Character reported

-
	- Backspace

	- 0x1e

	- {cpp:enumerator}`B_BACKSPACE`

-
	- Tab

	- 0x26

	- {cpp:enumerator}`B_TAB`

-
	- Enter

	- 0x47

	- {cpp:enumerator}`B_ENTER`

-
	- space bar

	- 0x5e

	- {cpp:enumerator}`B_SPACE`

-
	- Escape

	- 0x01

	- {cpp:enumerator}`B_ESCAPE`

-
	- F1–F12 0x02 through

	- 0x0d

	- {cpp:enumerator}`B_FUNCTION_KEY`

-
	- Print Screen

	- 0x0e

	- {cpp:enumerator}`B_FUNCTION_KEY`

-
	- Scroll Lock

	- 0x0f

	- {cpp:enumerator}`B_FUNCTION_KEY`

-
	- Pause

	- 0x10

	- {cpp:enumerator}`B_FUNCTION_KEY`

-
	- System Request

	- 0x7e

	- 0xc8

-
	- Break

	- 0x7f

	- 0xca

-
	- Insert

	- 0x1f

	- {cpp:enumerator}`B_INSERT`

-
	- Home

	- 0x20

	- {cpp:enumerator}`B_HOME`

-
	- Page Up

	- 0x21

	- {cpp:enumerator}`B_PAGE_UP`

-
	- Delete

	- 0x34

	- {cpp:enumerator}`B_DELETE`

-
	- End

	- 0x35

	- {cpp:enumerator}`B_END`

-
	- Page Down

	- 0x36

	- {cpp:enumerator}`B_PAGE_DOWN`

-
	- up arrow

	- 0x57

	- {cpp:enumerator}`B_UP_ARROW`

-
	- left arrow

	- 0x61

	- {cpp:enumerator}`B_LEFT_ARROW`

-
	- down arrow

	- 0x62

	- {cpp:enumerator}`B_DOWN_ARROW`

-
	- right arrow

	- 0x63

	- {cpp:enumerator}`B_RIGHT_ARROW`


:::

Several keys are mapped to the {cpp:enumerator}`B_FUNCTION_KEY` character.
An application can determine which function key was pressed to produce the
character by testing the key code against these constants:

:::{list-table}
---
header-rows: 0
align: left
widths: auto
---
-
	- {cpp:enumerator}`B_F1_KEY`

	- {cpp:enumerator}`B_F6_KEY`

	- {cpp:enumerator}`B_F11_KEY`

-
	- {cpp:enumerator}`B_F2_KEY`

	- {cpp:enumerator}`B_F7_KEY`

	- {cpp:enumerator}`B_F12_KEY`

-
	- {cpp:enumerator}`B_F3_KEY`

	- {cpp:enumerator}`B_F8_KEY`

	- {cpp:enumerator}`B_PRINT_KEY` (the "Print Screen" key)

-
	- {cpp:enumerator}`B_F4_KEY`

	- {cpp:enumerator}`B_F9_KEY`

	- {cpp:enumerator}`B_SCROLL_KEY` (the "Scroll Lock" key)

-
	- {cpp:enumerator}`B_F5_KEY`

	- {cpp:enumerator}`B_F10_KEY`

	- {cpp:enumerator}`B_PAUSE_KEY`


:::

Note that key 0x30 {hkey}`P` is also mapped to
{cpp:enumerator}`B_FUNCTION_KEY` when the {hkey}`Control` key is held down.

Each of the character constants listed above is a one-byte value falling
in the range of values where ASCII and Unicode™ overlap. For convenience,
the Interface Kit also defines some constants for common characters that
fall outside that range. These characters have multibyte representations in
UTF-8, so the constant is defined as a character string. For example:

:::{code} cpp
#define B_UTF8_OPEN_QUOTE  "xE2x80x9C"
#define B_UTF8_CLOSE_QUOTE "xE2x80x9D"
#define B_UTF8_COPYRIGHT   "xC2xA9"
:::

See "{cpp:func}`Character Constants <Constants::Character>`" in the
"{ref}`General Constants`" section of The Interface Kit for a full list of
these constants.
