# BButton

A {cpp:class}`BButton` object draws a labeled button on-screen and
responds when the button is clicked or when it's operated from the
keyboard. If the {cpp:class}`BButton` is the default button for its window
and the window is the active window, the user can operate it by pressing
the {hkey}`Enter` key.

{cpp:class}`BButton`s have a single state. Unlike check boxes and radio
buttons, the user can't toggle a button on and off. However, the button's
value changes while it's being operated. During a click (while the user
holds the mouse button down and the cursor points to the button on-screen),
the {cpp:class}`BButton`'s value is set to 1 ({cpp:enum}`B_CONTROL_ON`).
Otherwise, the value is 0 ({cpp:enum}`B_CONTROL_OFF`).

This class depends on the control framework defined in the
{cpp:class}`BControl` class. In particular, it calls these
{cpp:class}`BControl` functions:



A {cpp:class}`BButton` is an appropriate control device for initiating an
action. Use a {cpp:class}`BCheckBox`, a {cpp:class}`BPictureButton`, or
{cpp:class}`BRadioButton`s to set a state.
