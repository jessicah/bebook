# BControl
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BControl::BControl(BRect frame, const char* name, const char* label, BMessage* message, uint32 resizingMode, uint32 flags)
:::
:::{cpp:function} BControl::BControl(BMessage* archive)
:::

Initializes the {hclass}`BControl` by setting its initial value to 0
({cpp:enum}`B_CONTROL_OFF`), assigning it a {hparam}`label`,
and registering a model {hparam}`message`
that captures what the control does—the command it gives when it's
invoked and the information that accompanies the command. The {hparam}`label` and
the {hparam}`message` can each be {cpp:enum}`NULL`.

The {hparam}`label` is copied, but the {hparam}`message`
is not. The {cpp:class}`BMessage` object becomes
the property of the {hclass}`BControl`; it should not be deleted, posted, assigned
to another object, or otherwise used in application code. The label and
message can be altered after construction with the
{cpp:func}`~BControl::SetLabel` and
{cpp:func}`~BInvoker::SetMessage` functions.

The {hclass}`BControl` class doesn't define a
{cpp:func}`~BView::Draw`
function to draw the label or a
{cpp:func}`~BView::MouseDown`
function to post the message. (It does define
{cpp:func}`~BView::KeyDown`,
but only to enable keyboard navigation between controls.) It's up to
derived classes to determine how the {hparam}`label` is drawn and how the {hparam}`message`
is to be used. Typically, when a {hclass}`BControl` object needs to take action (in
response to a click, for example), it calls the
{cpp:func}`~BControl::Invoke` function, which
copies the model message and delivers the copy to the designated target.
By default, the target is the window where the control is located, but
{cpp:func}`BInvoker::SetTarget`
can designate another handler.

Before delivering the message,
{cpp:func}`~BControl::Invoke`
adds two data field to it, under
the names when and source.
These names should not be used for data items in the model.

The {hparam}`frame`, {hparam}`name`,
{hparam}`resizingMode`, and {hparam}`flags` arguments are identical to those
declared for the
{cpp:class}`BView` class and are passed unchanged to the
{cpp:class}`BView`
constructor.

The {hclass}`BControl` begins life enabled, and the system plain font is made the
default font for all control devices.

See also: the
{cpp:class}`BView`
{cpp:func}`~BView::Constructor`,
{cpp:func}`BLooper::PostMessage`,
{cpp:func}`~BControl::SetLabel`,
{cpp:func}`~BInvoker::SetMessage`,
{cpp:func}`BInvoker::SetTarget`,
{cpp:func}`~BControl::Invoke`

::::

::::{abi-group}

:::{cpp:function} virtual BControl::~BControl()
:::

Frees the model message and all memory allocated by the {hclass}`BControl`.

::::

## Hook Functions
::::{abi-group}

:::{cpp:function} virtual void BControl::AttachedToWindow()
:::

Overrides
{cpp:class}`BView`'s
version of this function to set the {hclass}`BControl`'s low
color and view color so that it matches the view color of its new parent.
It also makes the
{cpp:class}`BWindow`
to which the {hclass}`BControl` has become attached the
default target for the {cpp:func}`~BControl::Invoke`
function, provided that another target
hasn't already been set.

{hmethod}`AttachedToWindow()` is called for you when the
{hclass}`BControl` becomes a child of
a view already associated with the window.

See also:
{cpp:func}`BView::AttachedToWindow`,
{cpp:func}`~BControl::Invoke`,
{cpp:func}`BInvoker::SetTarget`

::::

::::{abi-group}

:::{cpp:function} virtual void BControl::KeyDown(const char* bytes, int32 numBytes)
:::

Augments the
{cpp:class}`BView` version of
{cpp:func}`~BView::KeyDown`
to toggle the {hclass}`BControl`'s value
and call {cpp:func}`~BControl::Invoke`
when the character encoded in bytes is either {cpp:enum}`B_SPACE`
or {cpp:enum}`B_ENTER`. This is done to facilitate keyboard navigation and make all
derived control devices operable from the keyboard. Some derived
classes—{cpp:class}`BCheckBox`
in particular—find this version of the
function to be adequate. Others, like
{cpp:class}`BRadioButton`, reimplement it.

{hmethod}`KeyDown()` is called only when the
{hclass}`BControl` is the focus view in the
active window. (However, if the window has a default button, {cpp:enum}`B_ENTER`
events will be passed to that object and won't be dispatched to the focus
view.)

See also:
{cpp:func}`BView::KeyDown`,
{cpp:func}`~BControl::MakeFocus`

::::

::::{abi-group}

:::{cpp:function} virtual void BControl::MessageReceived(BMessage* message)
:::

Handles scripting messages for the {hclass}`BControl`. See
"{cpp:func}`~BControl::ScriptingSupport`"
for a description of the messages.

See also: {cpp:func}`BHandler::MessageReceived`

::::

::::{abi-group}

:::{cpp:function} virtual void BControl::SetEnabled(bool enabled)
:::
:::{cpp:function} bool BControl::IsEnabled() const
:::

{hmethod}`SetEnabled()` enables the {hclass}`BControl`
if the {hparam}`enabled` flag is {cpp:enum}`true`, and
disables it if enabled is {cpp:enum}`false`.
{hmethod}`IsEnabled()` returns whether or not the
object is currently enabled. {hclass}`BControl`s are enabled by default.

While disabled, a {hclass}`BControl` won't let the user navigate to it; the
{cpp:enum}`B_NAVIGABLE` flag is turned off if enabled is
{cpp:enum}`false` and turned on again if
{hparam}`enabled` is {cpp:enum}`true`.

Typically, a disabled {hclass}`BControl` also won't post messages or respond
visually to mouse and keyboard manipulation. To indicate this
nonfunctional state, the control device is displayed on-screen in subdued
colors. However, it's left to each derived class to carry out this
strategy in a way that's appropriate for the kind of control it
implements. The {hclass}`BControl` class merely marks an object as being enabled or
disabled; none of its functions take the enabled state of the device into
account.

Derived classes can augment {hmethod}`SetEnabled()` (override it) to take action
when the control device becomes enabled or disabled. To be sure that
{hmethod}`SetEnabled()` has been called to actually make a change, its current state
should be checked before calling the inherited version of the function.
For example:

:::{code}
void MyControl::SetEnabled(bool enabled)
{
   if ( enabled == IsEnabled() )
      return;
   BControl::SetEnabled(enabled);
   /* Code that responds to the change in state goes here. */
}
:::

Note, however, that you don't have to override {hmethod}`SetEnabled()` just to
update the on-screen display when the control becomes enabled or
disabled. If the {hclass}`BControl` is attached to a window, the kit's version of
{hmethod}`SetEnabled()` always calls the
{cpp:func}`~BView::Draw` function. Therefore, the device
on-screen will be updated automatically—as long as
{cpp:func}`~BView::Draw` has been
implemented to take the enabled state into account.

See also: the {hclass}`BControl` {cpp:func}`~BControl::Constructor`

::::

::::{abi-group}

:::{cpp:function} virtual void BControl::SetValue(int32 value)
:::
:::{cpp:function} int32 BControl::Value() const
:::

These functions set and return the value of the {hclass}`BControl` object.

{hmethod}`SetValue()` assigns the object a new value. If the {hparam}`value` passed is in fact
different from the {hclass}`BControl`'s current value, this function calls the
object's {cpp:func}`~BView::Draw` function so that the new value will be reflected in what
the user sees on-screen; otherwise it does nothing.

{hmethod}`Value()` returns the current value.

Classes derived from {hclass}`BControl` should call
{hmethod}`SetValue()` to change the value
of the control device in response to user actions. The derived classes
defined in the Be software kits change values only by calling this
function.

Since {hmethod}`SetValue()` is a virtual function, you can override it to take note
whenever a control's value changes. However, if you want your code to act
only when the value actually changes, you must check to be sure the new
value doesn't match the old before calling the inherited version of the
function. For example:

:::{code}
void MyControl::SetValue(int32 value)
{
   if ( value != Value() ) {
      BControl::SetValue(value);
      /* MyControl's additions to SetValue() go here*/
   }
}
:::

Remember that the {hclass}`BControl` version of
{hmethod}`SetValue()` does nothing unless the
new value differs from the old.

::::

::::{abi-group}

:::{cpp:function} virtual void BControl::WindowActivated(bool active)
:::

Makes sure that the {hclass}`BControl`, if it's the focus view, is redrawn when the
window is activated or deactivated.

See also:
{cpp:func}`BView::WindowActivated`

::::

## Member Functions
::::{abi-group}

:::{cpp:function} virtual status_t BControl::Archive(BMessage* archive, bool deep = true) const
:::

Archives the {hclass}`BControl` by recording its label, current value, model
message, and whether or not it's disabled in the
{cpp:class}`BMessage` {hparam}`archive`.

See also:
{cpp:func}`BArchivable::Archive`,
{cpp:func}`~BControl::Instantiate` static function

::::

::::{abi-group}

:::{cpp:function} virtual status_t BControl::GetSupportedSuites(BMessage* message)
:::

Adds the name "suite/vnd.Be-control" to the message. See
"{cpp:func}`~BControl::ScriptingSupport`"
and the
"{ref}`Scripting`"
section in The Application Kit overview for more information.

See also:
{cpp:func}`BHandler::GetSupportedSuites`

::::

::::{abi-group}

:::{cpp:function} virtual status_t BControl::Invoke(BMessage* message = NULL)
:::

Copies the {hclass}`BControl`'s model
{cpp:class}`BMessage` and sends the copy so that it will
be dispatched to the designated target (which may be a
{cpp:class}`BLooper`'s
preferred handler). The following two pieces of information are added to
the copy before it's delivered:

Data nameType codeDescription"when"B_INT64_TYPEWhen the control was invoked, as measured in the number of milliseconds since 12:00:00 AM January 1, 1970."source"B_POINTER_TYPEA pointer to the BControl object. This permits the message handler to request more information from the source of the message.

These two names shouldn't be used for data fields in the model.

{hclass}`BControl`'s version of {hmethod}`Invoke()`
overrides the
{cpp:func}`~BInvoker::Invoke`
that the {cpp:class}`BInvoker`
class defines. It's designed to be called by derived classes in their
{cpp:func}`~BView::MouseDown` and
{cpp:func}`~BControl::KeyDown`
functions; it's not called for you in {hclass}`BControl`
code. It's up to each derived class to define what user actions trigger
the call to {hmethod}`Invoke()`—what activity constitutes "invoking" the
control.

This function doesn't check to make sure the {hclass}`BControl` is currently
enabled. Derived classes should make that determination before calling
{hmethod}`Invoke()`.

See also:
{cpp:func}`~BControl::SetEnabled`

::::

::::{abi-group}

:::{cpp:function} bool BControl::IsFocusChanging() const
:::

Returns {cpp:enum}`true` if the {hclass}`BControl`
is being asked to draw because the focus
changed, and {cpp:enum}`false` if not. If the return value is {cpp:enum}`true`, either the
{hclass}`BControl` has just become the focus view or it has just lost that status
and the
{cpp:func}`~BView::Draw`
function has been called to update the on-screen display.

This function can be called from inside
{cpp:func}`~BView::Draw` to learn whether it's
necessary to draw or erase the visible indication that the {hclass}`BControl` is
the focus view. {hmethod}`IsFocusChanging()`
will return the new status of the view.

See also: {cpp:func}`~BControl::MakeFocus`

::::

::::{abi-group}

:::{cpp:function} virtual void BControl::MakeFocus(bool focused = true)
:::

Augments the {cpp:class}`BView`
version of this function to call the {hclass}`BControl`'s
{cpp:func}`~BView::Draw`
function when the focus changes. This is done to aid keyboard navigation
among control devices. If the
{cpp:func}`~BView::Draw`
function of a derived class has a
section of code that checks whether the object is in focus and marks the
on-screen display to show that it is (and removes any such marking when
it isn't), the visual part of keyboard navigation will be taken care of.
The derived class doesn't have to reimplement
{hmethod}`MakeFocus()`. Most of the
derived classes implemented in the Interface Kit depend on this version
of the function.

When {cpp:func}`~BView::Draw`
is called from this function,
{cpp:func}`~BControl::IsFocusChanging`
returns {cpp:enum}`true`.

See also: {cpp:func}`BView::MakeFocus`,
{cpp:func}`~BControl::KeyDown`,
{cpp:func}`~BControl::IsFocusChanging`

::::

::::{abi-group}

:::{cpp:function} virtual BHandler* BControl::ResolveSpecifier(BMessage* message, int32 index, BMessage* specifier, int32 command, const char* property)
:::

Resolves specifiers for the "Label" and "Value" properties. See
"{cpp:func}`~BControl::ScriptingSupport`"
and the
"{ref}`Scripting`"
section in The Application Kit overview for more information.

See also: {cpp:func}`BHandler::ResolveSpecifier`

::::

::::{abi-group}

:::{cpp:function} virtual void BControl::SetLabel(const char* string)
:::
:::{cpp:function} const char* BControl::Label() const
:::

These functions set and return the label on a control device—the
text that's displayed, for example, on top of a button or alongside a
check box or radio button. The label is a null-terminated string.

{hmethod}`SetLabel()` frees the old label, replaces it with a copy of
{hparam}`string`, and
updates the control on-screen so the new label will be displayed to the
user—but only if the string that's passed differs from the current
label. The label is first set by the
{cpp:func}`~BControl::Constructor`
and can be modified thereafter by this function.

{hmethod}`Label()` returns the current label. The string it returns belongs to the
{hclass}`BControl` and may be altered or freed in due course.

See also: the {hclass}`BControl` constructor,
{cpp:func}`BView::AttachedToWindow`

::::

## Static Functions
::::{abi-group}

:::{cpp:function} static BArchivable* BControl::Instantiate(BMessage* archive)
:::

Returns a new {hclass}`BControl` object, allocated by new and created with the
version of the constructor that takes a {cpp:class}`BMessage` archive. However, if the
archive doesn't contain data for a {hclass}`BControl` object, {hmethod}`Instantiate()` returns
{cpp:enum}`NULL`.

See also:
{cpp:func}`BArchivable::Instantiate`,
{cpp:func}`~instantiate::object`,
{cpp:func}`~BControl::Archive`

::::

## Scripting Support
::::{abi-group}

Whether or not the control is enabled

The "Enabled" property corresponds to the methods
{cpp:func}`~BControl::IsEnabled` and
{cpp:func}`~BControl::SetEnabled`,
using a boolean to store the data.

MessageSpecifiersDescriptionB_GET_PROPERTYB_DIRECT_SPECIFIERReturns whether or not the BControl is currently enabled.B_SET_PROPERTYB_DIRECT_SPECIFIEREnables or disables the BControl.
::::

::::{abi-group}

The text label for the control

The "Label" property corresponds to the methods
{cpp:func}`~BControl::Label` and
{cpp:func}`~BControl::SetLabel`,
using a string to store the data.

MessageSpecifiersDescriptionB_GET_PROPERTYB_DIRECT_SPECIFIERReturns the BControl's label.B_SET_PROPERTYB_DIRECT_SPECIFIERSets the label of the BControl.
::::

::::{abi-group}

The value of the control

The "Value" property corresponds to the methods
{cpp:func}`~BControl::Value` and
{cpp:func}`~BControl::SetValue`,
using an int32 to store the data.

MessageSpecifiersDescriptionB_GET_PROPERTYB_DIRECT_SPECIFIERReturns the BControl's value.B_SET_PROPERTYB_DIRECT_SPECIFIERSets the value of the BControl.
::::

## Archived Fields