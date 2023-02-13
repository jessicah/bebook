# Keyboard Messages

## B_KEY_DOWN, B_KEY_UP, B_UNMAPPED_KEY_DOWN, B_UNMAPPED_KEY_UP

:::{list-table}
---
header-rows: 0
align: left
widths: auto
---
-

	- Source:

	- The system.

-

	- Target:

	- The focus view's {cpp:class}`BWindow`.

-

	- Hook:

	- {cpp:func}`BView::KeyDown` ({cpp:enum}`B_KEY_DOWN`)
{cpp:func}`BView::KeyUp` ({cpp:enum}`B_KEY_UP`) (The {cpp:enum}`…UNMAPPED…`
messages don't map to hook functions.)
:::

{cpp:enum}`B_KEY_DOWN` is sent when the user presses (or holds down) a key
that's mapped to a character; {cpp:enum}`B_KEY_UP` is sent when the user
releases the key. {cpp:enum}`B_UNMAPPED_KEY_DOWN` and
{cpp:enum}`B_UNMAPPED_KEY_UP` are sent if the key isn't mapped to a
character. This doesn't include modifier keys, which are reported in the
{cpp:enum}`B_MODIFIERS_CHANGED` message.

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-

	- Field

	- Type code

	- Description

-

	- when

	- {cpp:enum}`B_INT64_TYPE`

	- Event time, in microseconds since 01/01/70

-

	- key

	- {cpp:enum}`B_INT32_TYPE`

	- The code for the physical key that was pressed. See "{ref}`More On
Keyboard Mapping`" for a discussion of the keymap.

-

	- be:key_repeat

	- {cpp:enum}`B_INT32_TYPE`

	- The "iteration number" of this key down. When the user holds the key down,
successive messages are sent with increasing key repeat values. This field
isn't present in the initial event; the first repeat message (i.e., the
second key down message) has a key repeat value of 1.
({cpp:enum}`B_KEY_DOWN` only)

-

	- modifiers

	- {cpp:enum}`B_INT32_TYPE`

	- The modifier keys that were in effect at the time of the event. See
"{ref}`Modifier Keys`" for a list of values.

-

	- states

	- {cpp:enum}`B_UINT8_TYPE`

	- The state of all keys at the time of the event. See "{ref}`Key States`."

-

	- byte[3]

	- {cpp:enum}`B_INT8_TYPE`

	- The UTF-8 data that's generated.  ({cpp:enum}`B_KEY_DOWN` and
{cpp:enum}`B_KEY_UP` only)

-

	- bytes

	- {cpp:enum}`B_STRING_TYPE`

	- The string that's generated. (The string usually contains a single
character.) ({cpp:enum}`B_KEY_DOWN` and {cpp:enum}`B_KEY_UP` only)

-

	- raw_char

	- {cpp:enum}`B_INT32_TYPE`

	- Modifier-independent ASCII code for the character. ({cpp:enum}`B_KEY_DOWN`
and {cpp:enum}`B_KEY_UP` only)
:::
