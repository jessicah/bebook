# Constants

## Control Flags

Declared in: add-ons/graphics/GraphicsCard.h

:::{code} c
B_CRT_CONTROL
B_GAMMA_CONTROL
B_FRAME_BUFFER_CONTROL
:::

These flags report the driver's ability to control the CRT display, make
gamma corrections, and permit nonstandard configurations of the frame
buffer. Only the last has any meaning for the Game Kit.

See also: {cpp:func}`CardInfo() <BWindowScreen::CardInfo>`

## gs_attributes

Declared in: game/GameSoundDefs.h

:::{code} c
B_GS_MAIN_GAIN
B_GS_CD_THROUGH_GAIN
B_GS_GAIN
B_GS_PAN
B_GS_SAMPLING_RATE
B_GS_LOOPING
B_GS_FIRST_PRIVATE_ATTRIBUTE
B_GS_FIRST_USER_ATTRIBUTE
:::

These are the various possible game sound attributes. The range between
{cpp:enumerator}`B_GS_FIRST_PRIVATE_ATTRIBUTE` and
{cpp:enumerator}`B_GS_FIRST_USER_ATTRIBUTE` are reserved; if you need
custom attributes, use values {cpp:enumerator}`B_GS_FIRST_USER_ATTRIBUTE`
and higher.

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
	- {cpp:enumerator}`B_GS_MAIN_GAIN`
	- Main gain control, in decibels. The main gain doesn't support ramping.
-
	- {cpp:enumerator}`B_GS_CD_THROUGH_GAIN`
	- Gain on the CD through, in decibels.
-
	- {cpp:enumerator}`B_GS_GAIN`
	- Gain on the sound, in decibels.
-
	- {cpp:enumerator}`B_GS_PAN`
	- Pan position of the sound. -1.0 for far left, 0 for middle, 1.0 for far
		right.
-
	- {cpp:enumerator}`B_GS_SAMPLING_RATE`
	- Sampling rate in hertz.
-
	- {cpp:enumerator}`B_GS_LOOPING`
	- If the attribute's value is nonzero, the sound automatically loops. If
		it's 0, the sound plays through just once.
-
	- {cpp:enumerator}`B_GS_FIRST_PRIVATE_ATTRIBUTE`
	- Beginning of private attribute range
-
	- {cpp:enumerator}`B_GS_FIRST_USER_ATTRIBUTE`
	- Beginning of user attribute range.

:::
