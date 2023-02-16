# More On Keyboard Mapping

The key map records character values using the UTF-8 encoding of the
Unicode Standard, making it possible to map keys to characters in any of
the world's scripts. UTF-8 encodes 16-bit Unicode values in a variable
number of bytes (from one to four). The main benefit to UTF-8 is that
one-byte UTF characters $00 through $7F are identical to the ASCII standard
that's been around for decades.

A {cpp:enumerator}`B_KEY_DOWN` message holds the character mapped to the
key the user pressed as an array of bytes named, simply, {hparam}`byte`.
The array is passed as a string to the {cpp:func}`KeyDown()
<BView::KeyDown>` hook function along with a count of the number of bytes
in the string:

:::{code} c
virtual void KeyDown(const char* bytes, int32 numBytes)
:::

See "{ref}`Character Encoding`" in the Interface Kit chapter for a
description of UTF-8 encoding and {ref}`get_key_map()` for an explanation
of the key map.

Most keys are mapped to more than one character. The precise character
that the key produces depends on which modifier keys are being held down
and which lock states the keyboard is in at the time the key is pressed.

A few examples are given in the table below:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Key

	- No modifiers

	- Shift alone

	- Option alone

	- Shift + Option

	- Control

-
	- 0x15

	- 4

	- $

	- 

	- 

	- 4

-
	- 0x18

	- 7

	- &

	- ¦

	- ¤

	- 7

-
	- 0x26

	- {cpp:enumerator}`B_TAB`

	- {cpp:enumerator}`B_TAB`

	- {cpp:enumerator}`B_TAB`

	- {cpp:enumerator}`B_TAB`

	- {cpp:enumerator}`B_TAB`

-
	- 0x2e

	- i

	- I

	- 

	- 

	- {cpp:enumerator}`B_TAB`

-
	- 0x40

	- g

	- G

	- "

	- 

	- 0x07

-
	- 0x43

	- k

	- K

	- 

	- 

	- {cpp:enumerator}`B_PAGE_UP`

-
	- 0x51

	- n

	- N

	- ñ

	- Ñ

	- 0x0e

-
	- 0x55

	- /

	- ?

	- ¸

	- À

	- /

-
	- 0x64

	- {cpp:enumerator}`B_INSERT`

	- 0

	- {cpp:enumerator}`B_INSERT`

	- 0

	- {cpp:enumerator}`B_INSERT`


:::

The mapping follows some fixed rules, including these:

-   If a {hkey}`Command` key is held down, the {hkey}`Control` keys are
ignored. {hkey}`Command` trumps {hkey}`Control`. Otherwise, {hkey}`Command`
doesn't affect the character that's reported for the key. If only
{hkey}`Command` is held down, the character that's reported is the same as
if no modifiers were down; if {hkey}`Command` and {hkey}`Option` are held
down, the character that's reported is the same as for {hkey}`Option`
alone; and so on.

-   If a {hkey}`Control` key is held down (without a {hkey}`Command` key),
{hkey}`Shift`, {hkey}`Option`, and all keyboard locks are ignored.
{hkey}`Control` trumps the other modifiers (except for {hkey}`Command`).

-   {hkey}`Num Lock` applies only to keys on the numerical keypad. While this
lock is on, the effect of the {hkey}`Shift` key is inverted. {hkey}`Num
Lock` alone yields the same character that's produced when a {hkey}`Shift`
key is down (and {hkey}`Num Lock` is off). {hkey}`Num Lock` plus
{hkey}`Shift` yields the same character that's produced without either
{hkey}`Shift` or the lock.

-   {hkey}`Menu` and {hkey}`Scroll Lock` play no role in determining how keys
are mapped to characters.

The default key map also follows the conventional rules for {hkey}`Caps
Lock` and {hkey}`Control`:

-   {hkey}`Caps Lock` applies only to the 26 alphabetic keys on the main
keyboard. It serves to map the key to the same character as {hkey}`Shift`.
Using {hkey}`Shift` while the lock is on undoes the effect of the lock; the
character that's reported is the same as if neither {hkey}`Shift` nor
{hkey}`Caps Lock` applied. For example, {hkey}`Shift`+{hkey}`g` and
{hkey}`Caps Lock`+{hkey}`g` both are mapped to uppercase 'G', but
{hkey}`Shift`+{hkey}`Caps Lock`+{hkey}`g` is mapped to lowercase 'g'.

-   However, if the lock doesn't affect the character, {hkey}`Shift` plus the
lock is the same as {hkey}`Shift` alone. For example, {hkey}`Caps
Lock`+{hkey}`7` produces '7' (the lock is ignored) and
{hkey}`Shift`+{hkey}`7` produces '&' ({hkey}`Shift` has an effect), so
{hkey}`Shift`+{hkey}`Caps Lock`+{hkey}`7` also produces '&' (only
{hkey}`Shift` has an effect).

-   When {hkey}`Control` is used with a key that otherwise produces an
alphabetic character, the character that's reported has a value 0x40 less
than the value of the uppercase version of the character (0x60 less than
the lowercase version of the character). This often results in a character
that is produced independently by another key. For example,
{hkey}`Control`+{hkey}`i` produces the {cpp:enumerator}`B_TAB` character
and {hkey}`Control`+{hkey}`l` produces {cpp:enumerator}`B_PAGE_DOWN`.

-   When {hkey}`Control` is used with a key that doesn't produce an alphabetic
character, the character that's reported is the same as if no modifiers
were on. For example, {hkey}`Control`+{hkey}`7` produces a '7'.
