# BStatusBar

A {cpp:class}`BStatusBar` is a cosmetic object that graphically indicates the progress of an
operation. It displays a horizontal bar that's filled with color from left to right as the operation
progresses.

The label and text are abutted and aligned at the left of the bar; the trailing text and trailing
label are abutted and aligned at the right of the bar.

The texts can change each time the bar is updated. The label and trailing label are set by the
constructor and remain constant throughout the display, or until the object is reset for another
operation.

To set the amount that the status bar is filled, you can call {cpp:func}`~BStatusBar::Update()`,
which lets you add a delta to the current value. The "filling" itself reflects the ratio
(current_value)/(max_value), where max_value is 100.0 by default, but can be reset through
{cpp:func}`~BStatusBar::SetMaxValue()`. The minimum value of the bar is always 0.0.

You can call {cpp:func}`~BStatusBar::Update()` directly, or invoke it indirectly (and
asynchronously) by sending a {cpp:enum}`B_UPDATE_STATUS_BAR` message to the {cpp:class}`BStatusBar`.

The {cpp:func}`~BStatusBar::Reset()` function, which empties the bar can also be invoked through a
message ({cpp:enum}`B_RESET_STATUS_BAR`).
