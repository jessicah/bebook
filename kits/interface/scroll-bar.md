# BScrollBar
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BScrollBar::BScrollBar(BRect frame, const char* name, BView* target, float min, float max, orientation posture)
:::
:::{cpp:function} BScrollBar::BScrollBar(BMessage* archive)
:::

Initializes the {hclass}`BScrollBar` and connects it to the target view that it
will scroll. It will be a horizontal scroll bar if posture is
{cpp:enum}`B_HORIZONTAL` and a vertical scroll bar if posture is
{cpp:enum}`B_VERTICAL`.

The range of values that the scroll bar can represent at the outset is
set by {hparam}`min` and {hparam}`max`.
These values should be calculated from the boundaries
of a rectangle that encloses the entire contents of the target
view—everything that it can draw. If {hparam}`min`
and {hparam}`max` are both 0, the
scroll bar is disabled and the knob is not drawn.

The object's initial value is 0 even if that falls outside the range set
for the scroll bar.

The other arguments, {hparam}`frame` and {hparam}`name`,
are the same as for other
{cpp:class}`BView`s:

- The {hparam}`frame` rectangle locates the scroll bar within its parent view. For consistency in the user interface, a horizontal scroll bar should be {cpp:enum}`B_H_SCROLL_BAR_HEIGHT` coordinate units high, and a vertical scroll bar should be {cpp:enum}`B_V_SCROLL_BAR_WIDTH` units wide.
- The {hclass}`BScrollBar`'s {hparam}`name` identifies it and permits it to be located by the {cpp:func}`~BView::FindView` function. It can be {cpp:enum}`NULL`.

Unlike other {cpp:class}`BView`s,
the {hclass}`BScrollBar` constructor doesn't set an automatic
resizing mode. By default, scroll bars have the resizing behavior that
befits their posture—horizontal scroll bars resize themselves
horizontally (as if they had a resizing mode that combined
{cpp:enum}`B_FOLLOW_LEFT_RIGHT` with {cpp:enum}`B_FOLLOW_BOTTOM`)
and vertical scroll bars resize
themselves vertically (as if their resizing mode combined
{cpp:enum}`B_FOLLOW_TOP_BOTTOM` with {cpp:enum}`B_FOLLOW_RIGHT`).

::::

::::{abi-group}

:::{cpp:function} virtual BScrollBar::~BScrollBar()
:::

Disconnects the scroll bar from its target.

::::

## Hook Functions
::::{abi-group}

:::{cpp:function} virtual void BScrollBar::AttachedToWindow()
:::

Makes sure that the Application Server is
cognizant of the {hclass}`BScrollBar`'s
value, if a value was set before the object was attached to a window.

See also:
{cpp:func}`BView::AttachedToWindow`

::::

::::{abi-group}

:::{cpp:function} virtual void BScrollBar::ValueChanged(float newValue)
:::

Responds to a notification that the value of the scroll bar has changed
to {hparam}`newValue`. For a horizontal scroll bar, this function interprets
{hparam}`newValue` as the coordinate value that should be at the left side of the
target view's bounds rectangle. For a vertical scroll bar, it interprets
{hparam}`newValue` as the coordinate value that should be at the top of the
rectangle. It calls
{cpp:func}`~BView::ScrollTo`
to scroll the target's contents into
position, unless they have already been scrolled.

{hmethod}`ValueChanged()` is called as the result both of user actions
({cpp:enum}`B_VALUE_CHANGED` messages received from the
Application Server) and of
programmatic ones. Programmatically, scrolling can be initiated by the
target view (calling {cpp:func}`~BView::ScrollTo`)
or by the {hclass}`BScrollBar` (calling
{cpp:func}`~BScrollBar::SetValue`
or {cpp:func}`~BScrollBar::SetRange`).

In all these cases, the target view and the scroll bars need to be kept
in synch. This is done by a chain of function calls:
{hmethod}`ValueChanged()` calls
{cpp:func}`~BView::ScrollTo`,
which in turn calls {cpp:func}`~BScrollBar::SetValue`,
which then calls
{hmethod}`ValueChanged()` again. It's up to {hmethod}`ValueChanged()` to get off this
merry-go-round, which it does by checking the target view's bounds
rectangle. If {hparam}`newValue` already matches the left or top side of the bounds
rectangle, if forgoes calling
{cpp:func}`~BView::ScrollTo`.

{hmethod}`ValueChanged()` does nothing if a target
{cpp:class}`BView` hasn't been set—or if
the target has been set by name, but the name doesn't correspond to an
actual {cpp:class}`BView` within the scroll bar's window.

Derived classes can override this function to interpret {hparam}`newValue`
differently, or to do something in addition to scrolling the target view.

See also:
{cpp:func}`~BScrollBar::SetTarget`,
{cpp:func}`~BScrollBar::SetValue`,
{cpp:func}`BView::ScrollTo`

::::

## Member Functions
::::{abi-group}

:::{cpp:function} virtual status_t BScrollBar::Archive(BMessage* archive, bool deep = true) const
:::

Calls the inherited version of
{cpp:func}`~BView::Archive`,
then adds the {hclass}`BScrollBar`'s
range, orientation, current value and proportion, and the size of its big
and little steps to the
{cpp:class}`BMessage` {hparam}`archive`.

See also:
{cpp:func}`BArchivable::Archive`,
{cpp:func}`~BScrollBar::Instantiate` static function

::::

::::{abi-group}

:::{cpp:function} orientation BScrollBar::Orientation() const
:::

Returns {cpp:enum}`B_HORIZONTAL` if the object represents a horizontal scroll bar and
{cpp:enum}`B_VERTICAL` if it represents a vertical scroll bar.

See also:
The {hclass}`BScrollBar`
{cpp:func}`~BScrollBar::Constructor`

::::

::::{abi-group}

:::{cpp:function} void BScrollBar::SetProportion(float ratio)
:::
:::{cpp:function} float BScrollBar::Proportion() const
:::

These functions set and return a value between 0.0 and 1.0 that
represents the proportion of the entire document that can be displayed
within the target view—the ratio of the width (or height) of the
target's bounds rectangle to the width (or height) of its data rectangle.
This ratio determines the size of a proportional scroll knob relative to
the whole scroll bar. It's not adjusted to take into account the minimum
size of the knob.

The proportion should be reset as the size of the data rectangle changes
(as data is entered and removed from the document) and when the target
view is resized.

::::

::::{abi-group}

:::{cpp:function} void BScrollBar::SetRange(float min, float max)
:::
:::{cpp:function} void BScrollBar::GetRange(float* min, float* max) const
:::

These functions modify and return the range of the scroll bar.
{hmethod}`SetRange()`
sets the minimum and maximum values of the scroll bar to {hparam}`min` and {hparam}`max`.
{hmethod}`GetRange()` places the current minimum and maximum in the variables that
{hparam}`min` and {hparam}`max` refer to.

If the scroll bar's current value falls outside the new range, it will be
reset to the closest value—either {hparam}`min` or {hparam}`max`—within range.
{cpp:func}`~BScrollBar::ValueChanged`
is called to inform the {hclass}`BScrollBar` of the change whether
or not it's attached to a window.

If the {hclass}`BScrollBar` is attached to a window, any change in its range will
be immediately reflected on-screen. The knob will move to the appropriate
position to reflect the current value.

Setting both the minimum and maximum to 0 disables the scroll bar. It
will be drawn without a knob.

See also:
The {hclass}`BScrollBar`
{cpp:func}`~BScrollBar::Constructor`

::::

::::{abi-group}

:::{cpp:function} void BScrollBar::SetSteps(float smallStep, float bigStep)
:::
:::{cpp:function} void BScrollBar::GetSteps(float* smallStep, float* bigStep) const
:::

{hmethod}`SetSteps()` sets how much a single user action should change the value of
the scroll bar—and therefore how far the target view should scroll.
{hmethod}`GetSteps()` provides the current settings.

When the user presses one of the scroll arrows at either end of the
scroll bar, its value changes by a {hparam}`smallStep` coordinate units. When the
user clicks in the bar itself (other than on the knob), it changes by a
{hparam}`bigStep` units. For an application that displays text, the small step of a
vertical scroll bar should be large enough to bring another line of text
into view.

The default small step is 1.0, which should be too small for most
purposes; the default large step is 10.0, which is also probably too
small.

:::{admonition} Note
:class: note
Although the step values are specified using type float, only integral
values should be specified; otherwise, the scroll bar won't behave as
expected.
:::

Currently, a {hclass}`BScrollBar`'s steps can be successfully set only after it's
attached to a window.

See also:
{cpp:func}`~BScrollBar::ValueChanged`

::::

::::{abi-group}

:::{cpp:function} void BScrollBar::SetTarget(BView* view)
:::
:::{cpp:function} void BScrollBar::SetTarget(const char* name)
:::
:::{cpp:function} BView* BScrollBar::Target() const
:::

These functions set and return the target of the {hclass}`BScrollBar`, the view
that the scroll bar scrolls. {hmethod}`SetTarget()` sets the target to
{hparam}`view`, or to
the {cpp:class}`BView`
identified by {hparam}`name`. {hmethod}`Target()` returns the current target view.
The target can also be set when the {hclass}`BScrollBar` is constructed.

{hmethod}`SetTarget()` can be called either before or after the
{hclass}`BScrollBar` is
attached to a window. If the target is set by {hparam}`name`, the named view must
eventually be found within the same window as the scroll bar. Typically,
the target and its scroll bars are children of a container view that
serves to bind them together as a unit.

When the target is successfully set, a pointer to the {hclass}`BScrollBar` object
is passed to the target view. This lets the target update its scroll bars
when its contents are scrolled.

See also:
The {hclass}`BScrollBar`
{cpp:func}`~BScrollBar::Constructor`,
{cpp:func}`~BScrollBar::ValueChanged`,
{cpp:func}`BView::ScrollBar`

::::

::::{abi-group}

:::{cpp:function} void BScrollBar::SetValue(float value)
:::
:::{cpp:function} float BScrollBar::Value() const
:::

These functions modify and return the value of the scroll bar. The value
is usually set as the result of user actions; {hmethod}`SetValue()` provides a way
to do it programmatically. {hmethod}`Value()` returns the current value, whether set
by {hmethod}`SetValue()` or by the user.

{hmethod}`SetValue()` assigns a new {hparam}`value` to the scroll bar and calls the
{cpp:func}`~BScrollBar::ValueChanged`
hook function, whether or not the new value is really a
change from the old. If the value passed lies outside the range of the
scroll bar, the {hclass}`BScrollBar` is reset to the closest value within
range—that is, to either the minimum or the maximum value
previously specified.

If the scroll bar is attached to a window, changing its value updates its
on-screen display. The call to
{cpp:func}`~BScrollBar::ValueChanged`
enables the object to
scroll the target view so that it too is updated to conform to the new
value.

The initial value of a scroll bar is 0.

See also:
{cpp:func}`~BScrollBar::ValueChanged`,
{cpp:func}`~BScrollBar::SetRange`

::::

## Static Functions
::::{abi-group}

:::{cpp:function} static BArchivable* BScrollBar::Instantiate(BMessage* archive)
:::

Returns a new {hclass}`BScrollBar` object, allocated by new and created with the
version of the constructor that takes a
{cpp:class}`BMessage` archive. However, if the
{hparam}`archive` message doesn't contain data for a {hclass}`BScrollBar` object, the return
value will be {cpp:enum}`NULL`.

See also:
{cpp:func}`BArchivable::Instantiate`,
{cpp:func}`~instantiate::object`,
{cpp:func}`~BScrollBar::Archive`

::::

## Archived Fields