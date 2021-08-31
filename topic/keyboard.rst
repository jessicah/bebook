Keyboard
========

This page details how Haiku reads keys from the keyboard, including modifier
keys and special characters, and how you can read and process these encoded
characters in your application.

Haiku and UTF-8
---------------

Haiku encodes all characters using UTF-8. UTF-8 allows Haiku to represent
characters from all over the world, while still maintaining backwards
compatibility with 7-bit ASCII codes. This means that the most commonly used
characters in Western alphabets are encoded in just one byte, while everything
else can be encoded by extending the character encoding to use multiple bytes.

Key Codes
---------

Each key on the keyboard is assigned a numeric code to identify it to the
operating system. Most of the time you should not have to access these codes
directly, but instead use one of the constants defined in `InterfaceDefs.h`,
such as :cpp:enum:`B_BACKSPACE` or :cpp:enum:`B_ENTER`, or read the character
from the :cpp:type:`key_map` struct.

The following diagram shows the key codes as they appear on a US 104-key
keyboard:

<an image goes here>

International keyboards each differ a bit, but generally share an extra key
located in-between the left shift key and Z, with the key code 0x69.

Mac keyboards have an equals sign in the keypad with key code 0x6a, and some
other differences. Often times, the keys produce the same key code but appear in
different locations.

Modifier Keys
-------------

Modifier keys are keys which have no effect on their own, but when combined with
other keys they modify the usual behaviour of that key.

The following modifier keys are defined in `InterfaceDefs.h`

:cpp:enum:`B_SHIFT_KEY`
	Transforms lowercase characters into uppercase characters, or chooses
	alternative punctuation characters. The shift key is also used in
	combination with :cpp:enum:`B_COMMAND_KEY` to produce keyboard shortcuts.

:cpp:enum:`B_COMMAND_KEY`
	Produces keyboard shortcuts for common operations such as cut, copy, paste,
	print, and find.

:cpp:enum:`B_CONTROL_KEY`
	Outputs control characters in the terminal. The control key is sometimes
	also used as an alternative to the :cpp:enum:`B_COMMAND_KEY` to produce
	keyboard shortcuts in applications.

:cpp:enum:`B_OPTION_KEY`
	Used in combination with other keys to output special characters such as
	accented letters and symbols. Because :cpp:enum:`B_OPTION_KEY` is not found
	on all keyboards, it should not be used for essential functions.

:cpp:enum:`B_MENU_KEY`
	The Menu key is used to produce contextual menus. Like
	:cpp:enum:`B_OPTION_KEY`, the Menu key should not be used for essential
	functions, as it is not available on all keyboards.

In addition, you can access the left and right modifier keys individually with
the following constants: :cpp:enum:`B_LEFT_SHIFT_KEY`,
:cpp:enum:`B_RIGHT_SHIFT_KEY`, :cpp:enum:`B_LEFT_COMMAND_KEY`,
:cpp:enum:`B_RIGHT_COMMAND_KEY`, :cpp:enum:`B_LEFT_CONTROL_KEY`,
:cpp:enum:`B_RIGHT_CONTROL_KEY`, :cpp:enum:`B_LEFT_OPTION_KEY`,
:cpp:enum:`B_RIGHT_OPTION_KEY`.

Scroll lock, num lock, and caps lock alter other keys pressed after they are
released. They are defined by the following constants:

:cpp:enum:`B_CAPS_LOCK`
	Produces uppercase characters. Reverses the effect of
	:cpp:enum:`B_SHIFT_KEY` for letters.

:cpp:enum:`B_CAPS_LOCK`
	Prevents the terminal from scrolling.

:cpp:enum:`B_NUM_LOCK`
	Informs the numeric keyboard to output numbers when on. Reverses the
	function of :cpp:enum:`B_SHIFT_KEY` for keys on the numeric keybpard.

To get the currently active modifiers, use the :cpp:function:`modifiers()`
function defined in `InterfaceDefs.h`. This function returns a bitmap containing
the currently active modifier keys. You can create a bit mask of the above
constants to determine which modifiers are active.

Other Constants
---------------

The Interface Kit also defines constants for keys that are represented by a
symbol; these include: :cpp:enum:`B_BACKSPACE`, :cpp:enum:`B_RETURN`,
:cpp:enum:`B_ENTER`, :cpp:enum:`B_SPACE`, :cpp:enum:`B_TAB`,
:cpp:enum:`B_ESCAPE`, :cpp:enum:`B_SUBSTITUTE`, :cpp:enum:`B_LEFT_ARROW`,
:cpp:enum:`B_RIGHT_ARROW`, :cpp:enum:`B_UP_ARROW`, :cpp:enum:`B_DOWN_ARROW`,
:cpp:enum:`B_INSERT`, :cpp:enum:`B_DELETE`, :cpp:enum:`B_HOME`,
:cpp:enum:`B_END`, :cpp:enum:`B_PAGE_UP`, :cpp:enum:`B_PAGE_DOWN`,
:cpp:enum:`B_FUNCTION_KEY`.

The :cpp:enum:`B_FUNCTION_KEY` constant can be further broken down into the
following constants: :cpp:enum:`B_F1_KEY`, :cpp:enum:`B_F2_KEY`,
:cpp:enum:`B_F3_KEY`, :cpp:enum:`B_F4_KEY`, :cpp:enum:`B_F5_KEY`,
:cpp:enum:`B_F6_KEY`, :cpp:enum:`B_F7_KEY`, :cpp:enum:`B_F8_KEY`,
:cpp:enum:`B_F9_KEY`, :cpp:enum:`B_F10_KEY`, :cpp:enum:`B_F11_KEY`,
:cpp:enum:`B_F12_KEY`, :cpp:enum:`B_PRINT_KEY` (Print Screen),
:cpp:enum:`B_SCOLL_KEY` (Scroll Lock), :cpp:enum:`B_PAUSE_KEY` (Pause/Break).

For Japanese keyboards, two more constants are defined:

* B_KATAKANA_HIRAGANA
* B_HANKAKU_ZENKAKU

The Keymap
----------

The characters produced by each of the keycodes is determined by the keymap. The
usual way for the user to choose and modify their keymap is with the Keymap
preference application. A number of alternative keymaps, such as Dvorak and
keymaps for different locales, are available.

<<picture of the Keymap preference app>>
[caption: A full description of the Keymap preflet can be found in the User
Guide]

The keymap is a map of the characters produced by each key on the keyboard,
including the characters produced when combined with the modifier constants
described above. The keymap also contains the codes of the modifier keys and
tables for dead keys.

To get the current system keymap, create a pointer to a :cpp:type:`key_map`
struct and :cpp:type:`char` array, and pass their addresses to the
:cpp:func:`get_key_map()` function. The :cpp:type:`key_map` struct will be
filled out with the current system keymap, and the :cpp:type:`char` array will
be filled out with the UTF-8 character encodings.

The :cpp:type:`key_map` struct contains a number of fields described below:

:cpp:type:`version`
	The version number of the keymap

:cpp:type:`caps_key`, :cpp:type:`scroll_key`, :cpp:type:`num_key`
	Lock key codes

:cpp:type:`left_shift_key`, :cpp:type:`right_shift_key`
	Left and right shift key codes

To programmatically set a modifier key in the system keymap, use the
:cpp:func:`set_modifier_key()` function. You can also programmatically set the
state of the lock keys by calling the :cpp:func:`set_keyboard_locks()` function.

Character Maps
--------------

