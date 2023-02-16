# Modifier Keys

Conceptually, there are eight modifier keys. The global {ref}`modifiers()`
function returns a value that encodes the current status of all eight of
these keys. You can test for the state of a particular modifier key by
comparing {ref}`modifiers()` with the constants listed in the table below.
For example, here's how you can see if the user is holding down one of the
{hkey}`Shift` keys:

:::{code} c
if (modifiers() | B_SHIFT_KEY) {
   /* a shift key is down */
}
:::

The modifier mask is also included in the "modifiers" field in
{cpp:class}`BMessage`s that report keyboard and mouse events.

How your application uses modifier keys is up to you. The list below lists
the eight keys and how they're typically used.

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Constant

	- Description

-
	- {cpp:enumerator}`B_SHIFT_KEY`
	- Maps character keys to their uppercase or alternative versions.
-
	- {cpp:enumerator}`B_COMMAND_KEY`
	- In combination with a character key, performs a keyboard shortcut.
-
	- {cpp:enumerator}`B_CONTROL_KEY`
	- Turns alphabetic keys into control characters.
-
	- {cpp:enumerator}`B_OPTION_KEY`
	- Maps keys to alternative characters, typically characters in an extended
		set—multibyte UTF-8 characters.
-
	- {cpp:enumerator}`B_MENU_KEY`
	- Pops open a menu.
-
	- {cpp:enumerator}`B_CAPS_LOCK`
	- Reverses the effect of the {hkey}`Shift` key on alphabetic characters.
-
	- {cpp:enumerator}`B_NUM_LOCK`
	- Reverses the effect of the {hkey}`Shift` key on numeric characters.
-
	- {cpp:enumerator}`B_SCROLL_LOCK`
	- Stops the display from scrolling.

:::

If you're interested in whether the left or right modifer key of a given
type was pressed, you can check against these additional values:

:::{code} sh
B_LEFT_SHIFT_KEY   B_RIGHT_SHIFT_KEY
B_LEFT_CONTROL_KEY B_RIGHT_CONTROL_KEY
B_LEFT_OPTION_KEY  B_RIGHT_OPTION_KEY
B_LEFT_COMMAND_KEY B_RIGHT_COMMAND_KEY
:::

Most of the modifiers map to single, specific keys: {hkey}`Shift` and
{hkey}`Caps Lock` are examples. But others don't: the {hkey}`Menu` key maps
to _Shortcut_+{hkey}`Escape` (where _Shortcut_ is either {hkey}`Alt`,
{hkey}`Command`, or {hkey}`Control`, depending on the user's preferences
and keyboard).
