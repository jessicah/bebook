# Definitions

This section lists and describes the keyboard terms and concepts that you
should be familiar with.

## Key Codes

Keyboards come in a variety of styles and sizes, with different numbers of
keys on them, sometimes in different positions. Some special keys or
symbols even appear more than once on the same keyboard—for example, most
keyboards have two {hkey}`Enter` keys (sometimes one or both of them is
called {hkey}`Return`). Most keyboards have two {hkey}`Shift` keys, and
many have two keys that can generate the "=" character—one of them on the
numeric keypad.

Each of these keys is unique as far as the hardware is concerned, even if
they usually generate the same result as far as the user is concerned.
Because of this, each key has a unique number, called a key code. This is a
numeric byte value between 0x01 and 0x7F. They're not the same as the ASCII
or {ref}`Unicode™` values for the characters generated by the keys—which
makes sense, since not every key generates a character.

For example, the left {hkey}`Shift` key has the key code value of 0x4B, and
the right {hkey}`Shift` key has the key code of 0x56. Neither of these
generates a {cpp:enumerator}`B_KEY_UP` event (although they do generate a
{cpp:enumerator}`B_MODIFIERS_CHANGED` event). The additional implication
here is clear: software can actually tell the difference between these two
keys—and any other keys that generate the same Unicode value—if they need
to do so.

It's also important to note that key codes don't differentiate between
shifted and unshifted keys. Pressing {hkey}`A` generates the key code 0x27
whether the {hkey}`Caps Lock` or {hkey}`Shift` key is down or not.

## The Keymap

Most software written these days expects keys to be received in either
ASCII or Unicode format (or, in the case of BeOS, in UTF-8 format, which is
a form of Unicode in which the ASCII codes are contained). So obviously
receiving a value of 0x27 for the {hkey}`A` key isn't going to help a
program that expects to receive 0x41, the UTF-8 value for the character
"A".

So clearly the key codes the input server add-on obtains from the keyboard
device need to be translated into UTF-8. This is done by using a keymap.
This is a table that can be used to look up a key code and determine, based
on which modifier keys are currently engaged, the UTF-8 bytes that should
be generated. It also defines which keys are treated as modifier keys.

BeOS maintains a keymap for use by all applications. Applications that want
to look up key codes in the keymap can call {cpp:func}`get_key_map()` to
get a copy of it. The Keymap preference panel can be used to configure the
system keymap.

## Character Keys

A character key is a key that's mapped to a particular UTF-8 byte or byte
sequence. For example, in the standard American keymap, the key labeled
{hkey}`A` is mapped to the letter "a" when pressed with no modifier keys
down, "A" when the {hkey}`Caps Lock` or a {hkey}`Shift` key is down, and
{hkey}`control`+{hkey}`A` (UTF-8 code 0x01) when the {hkey}`Control` key is
down. Mapped character keys generate {cpp:enumerator}`B_KEY_DOWN` and
{cpp:enumerator}`B_KEY_UP` messages when they're pressed and released.

Keys that aren't mapped to characters generate
{cpp:enumerator}`B_UNMAPPED_KEY_DOWN` and
{cpp:enumerator}`B_UNMAPPED_KEY_UP` messages.

## Modifier Keys

Modifier keys set states that affect the way character keys are
interpreted. Some modifier keys, such as {hkey}`Caps Lock`, toggle in and
out of a locked-on or locked-off position each time they're pressed.
Others, like Shift, set the state only as long as they're held down.

The keymap contains lists of how to interpret each key depending on which
modifier keys are currently engaged.

## The Scroll Lock Key

The {hkey}`Scroll Lock` key is unique. In the standard keyboard Input
Server add-on, it both generates a character and sets a modifier state.

## Repeating Keys

When a key is pressed and held down, it produces a continuous series of
{cpp:enumerator}`B_KEY_DOWN` or {cpp:enumerator}`B_UNMAPPED_KEY_DOWN`
messages, as long as the key is still held down and doesn't press another
key. After the first message, there's a slight delay before the key begins
repeating. This delay can be determined by calling
{cpp:func}`get_key_repeat_delay()` and can be changed by calling
{cpp:func}`set_key_repeat_delay()` (although you should leave the user's
preference for this alone).

After the key begins to repeat, the {cpp:enumerator}`B_KEY_DOWN` or
{cpp:enumerator}`B_UNMAPPED_KEY_DOWN` messages are sent at a fixed rate;
this rate can be determined by calling {cpp:func}`get_key_repeat_rate()`.

All keys repeat except {hkey}`Pause`, {hkey}`Break`, {hkey}`Caps Lock`,
{hkey}`Num Lock`, and {hkey}`Scroll Lock`.

## Dead Keys

Dead keys don't generate characters until the user strikes another key. If
the key the user presses after the dead key is in a particular set, the two
keys together produce one key-down event (and, usually, one character). If
the second keystroke isn't in that set, two key-down events are generated.

Dead keys are only dead when certain prescribed modifiers (by default, just
the Option key) are held down. They're most appropriate when the character
to be generated can be thought of as being composed of two distinguishable
parts—such as "a" and "e" combining into "æ".

The system permits up to five dead keys. By default, they're reserved for
combining diacritical marks with other characters. The diacritical marks
are the acute (´) and grave (`) accents, dieresis (¨), circumflex (^), and
tilde (~).
