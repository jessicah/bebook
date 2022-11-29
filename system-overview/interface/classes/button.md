# BButton

A {cpp:class}`BButton` object draws a labeled button on-screen and responds when the button is
clicked or when it's operated from the keyboard. If the {cpp:class}`BButton` is the default button
for its window and the window is the active window, the user can oeprate it by pressing the
{key}`Enter` key.

{cpp:class}`BButton`s have a single state. Unlike check boxes and radio buttons, the user can't
toggle a button on and off. However, the button's value changes while it's being operated. During a
click (while the user holds the mouse button down and the cursor points to the button on-screen),
the {cpp:class}`BButton`'s value is set to 1 ({cpp:enum}`B_CONTROL_ON`). Otherwise, the value is 0
({cpp:enum}`B_CONTROL_OFF`).

This class depends on the control framework defined in the {cpp:class}`BControl` class. In
particular, it calls these {cpp:class}`BControl` functions:

{cpp:func}`~BControl::SetValue()`. To make each change in the {cpp:class}`BControl`'s value.

: This is a hook function that you can override to take collateral action when the value changes.

{cpp:func}`~BControl::Invoke()`. To post a message each time the button is clicked or operated from the keyboard.

: You can designate the object that should handle the message by calling {cpp:class}`BControl`s
{cpp:func}`~BControl::SetTarget()` function inherited from {cpp:class}`BInvoker`. A model for the
message is set by the {cpp:class}`BButton` constructor (or by {cpp:class}`BControl`s
{cpp:func}`~BControl::SetMessage()` function inherited from {cpp:class}`BInvoker`).

{cpp:func}`~BControl::IsEnabled()`. To determine how the button should be drawn and whether it's enabled to post a message.

: You can call {cpp:class}`BControl`s {cpp:func}`~BControl::SetEnabled()` to enable and disable the
button.

A {cpp:class}`BButton` is an appropriate control device for initiating an action. Use a
{cpp:class}`BCheckBox`, a {cpp:class}`BPictureButton`, or {cpp:class}`BRadioButton`s to set a state.
