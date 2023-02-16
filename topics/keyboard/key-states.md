# Key States

You can look at the state of all the keys on the keyboard at a given
moment in time. This information is captured and reported in two ways:

1.    As the {hparam}`states` field in every {cpp:enumerator}`B_KEY_DOWN`
message, and

2.    As the {hparam}`key_states` bitfield reported by {ref}`get_key_info()`.

In both cases, the bitfield is an array of 16 bytes,

:::{code} c
uint8 states[16];
:::

with one bit standing for each key on the keyboard. Bits are numbered from
left to right, beginning with the first byte in the array, as illustrated
below:

![Info Icon](./images/TheKeyboard/KeyboardKeyStates-2.png)

Bit numbers start with 0 and match key codes. For example, bit 0x3c
corresponds to the {hkey}`a` key, 0x3d to the {hkey}`s` key, 0x3e to the
{hkey}`d` key, and so on. The first bit is 0x00, which doesn't correspond
to any key. The first meaningful bit is 0x01, which corresponds to the
{hkey}`Escape` key.

When a key is down, the bit corresponding to its key code is set to 1.
Otherwise, the bit is 0. However, for the three keys that toggle keyboard
locks—{hkey}`Caps Lock` (key 0x3b), {hkey}`Num Lock` (key 0x22), and
{hkey}`Scroll Lock` (key 0x0f)—the bit is set to 1 if the lock is on and
set to 0 if the lock is off, regardless of the state of the key itself.

To test the bitfield against a particular key,

-   Select the byte in the {hparam}`states` array that contains the bit for
that key,

-   Form a mask for the key that can be compared to that byte, and

-   Compare the byte to the mask.

For example:

:::{code} c
if (states[keyCode>>3] & (1 << (7 - (keyCode%8)))) {
   /* the key is down */
}
:::
