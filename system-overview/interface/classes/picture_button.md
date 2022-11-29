# BPictureButton

A {cpp:class}`BPictureButton` draws a button that displays an image (a {cpp:class}`BPicture` object)
rather than a text label. A {cpp:class}`BPictureButton` can be either a one-state or a two-state
control:

:::{list-table}
-
	- One-state.

	- Acts like a normal {cpp:class}`BButton`: The value is {cpp:enum}`B_CONTROL_ON` while the
	object is being pressed and {cpp:enum}`B_CONTROL_OFF` otherwise. The images for these two states
	should be different; by convention, the "on" image is a highlighted version of the "off" image.
	If the button can be disabled, it needs an additional "disabled" image.

-
	- Two-state.

	- Acts like a checkbox: Its value switches between {cpp:enum}`B_CONTROL_ON` and
	{cpp:enum}`B_CONTROL_OFF` every time the user presses (and releases) the button. If the button
	can be disabled, if needs two additional "disabled" images: One for disabled-while-on and the
	other for disabled-while-off.
