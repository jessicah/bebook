# BControl

{cpp:class}`BControl` is an abstract class for views that draw control devices on the screen.
Objects that inherit from {cpp:class}`BControl` emulate, in software, real-world control
devices---like the switches and levers on a machine, the check lists and blank lines on a form to
fill out, or the dials and knobs on a home appliance.

Controls translate the messages that report generic mouse and keyboard events into other messages
with more specific instructions for the application. A {cpp:class}`BControl` object can be
customized by setting the message it posts when invoked and the target object that should handle the
message.

Controls also register a current value, stored as an int32 integer that's typically set to
{cpp:enum}`B_CONTROL_ON` or {cpp:enum}`B_CONTROL_OFF`. The value is changed only by calling
{cpp:func}`~BControl::SetValue()`, a virtual function that derived classes can implement to be
notified of the change.

## Derived Classes

The Interface Kit currently includes six classes derived from
{cpp:class}`BControl`---{cpp:class}`BButton`, {cpp:class}`BPictureButton`,
{cpp:class}`BRadioButton`, {cpp:class}`BCheckBox`, {cpp:class}`BColorControl`, and
{cpp:class}`BTextControl`. In addition, it has two classes---{cpp:class}`BListView` and
{cpp:class}`BMenuItem`---that implement control devices but are not derived from this class.
{cpp:class}`BListView` and its subclass, {cpp:class}`BOutlineView`, share an interface with the
{cpp:class}`BList` class (of the Support Kit) and {cpp:class}`BMenuItem` is designed to work with
the other classes in the menu system. Like {cpp:class}`BControl`, {cpp:class}`BListView` and
{cpp:class}`BMenuItem` inherit from the Application Kit's {cpp:class}`BInvoker` class.

As {cpp:class}`BListView` and {cpp:class}`BMenuItem` demonstrate, it's possible to implement a
control device that's not a {cpp:class}`BControl`. However, it's simpler to take advantage of the
code that's already provided by the {cpp:class}`BControl` class. That way you can keep a simple
programming interface and avoid reimplementing functions that {cpp:class}`BControl` has defined for
you. If you application defines its own control devices---dials, sliders, selection lists, and the
like---they should be dervied from {cpp:class}`BControl`.
