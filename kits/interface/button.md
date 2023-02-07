# BButton
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BButton::BButton(BRect frame, const char* name, const char* label, BMessage* message, uint32 resizingMode = B_FOLLOW_LEFT | B_FOLLOW_TOP, uint32 flags = B_WILL_DRAW | B_NAVIGABLE)
:::
:::{cpp:function} BButton::BButton(BMessage* archive)
:::
Initializes the {hclass}`BButton` by passing all arguments to the
{cpp:class}`BControl`
constructor. {cpp:class}`BControl`
initializes the button's {hparam}`label` and assigns it a
model {hparam}`message` that identifies the action that
should be carried out when the button is invoked. 
The {hparam}`frame`,
{hparam}`name`, {hparam}`resizingMode`,
and {hparam}`flags` arguments are the same as those
declared for the
{cpp:class}`BView`
class and are passed up the inheritance hierarchy to the
{cpp:class}`BView`
constructor without change.

When the button is attached to a window, it will be resized to its
preferred height; the height of {hclass}`BButton`'s {hparam}`frame` rectangle will exactly
accommodate the button border and label, given the {hclass}`BButton`'s current font.

::::

::::{abi-group}

:::{cpp:function} virtual BButton::~BButton()
:::

Does nothing; a {hclass}`BButton` has no data to free.

::::

## Hook Functions
::::{abi-group}

:::{cpp:function} virtual void BButton::AttachedToWindow()
:::
Augments the
{cpp:class}`BControl`
{cpp:func}`~BControl::AttachedToWindow`
of this function to tell the
{cpp:class}`BWindow` that
the button is the default button, if
{cpp:func}`~BButton::MakeDefault` has already been
called.

See also: {cpp:func}`BView::AttachedToWindow`

::::

::::{abi-group}

:::{cpp:function} virtual void BButton::KeyDown(const char* bytes, int32 numBytes)
:::

Augments the inherited version of {hmethod}`KeyDown()` to respond to
messages reporting that the user pressed the Enter key or the space bar.
Its response is to:

- Momentarily highlight the button and change its value.
- Call {cpp:func}`~BControl::Invoke` to deliver a copy of the model {cpp:class}`BMessage` to the target receiver.

The {hclass}`BButton` gets {hmethod}`KeyDown()`
function calls when it's the focus view for
the active window (which results when the user navigates to it) and also
when it's the default button for the window and the character the user
types is {cpp:enum}`B_ENTER`.

See also: {cpp:func}`BView::KeyDown`,
{cpp:func}`~BButton::MakeDefault`

::::

::::{abi-group}

:::{cpp:function} virtual void BButton::MakeDefault(bool flag)
:::

{hmethod}`MakeDefault()` makes the {hclass}`BButton` the default button for its window when
{hparam}`flag` is {cpp:enum}`true`, and removes that status when {hparam}`flag` is {cpp:enum}`false`. The default
button is the button the user can operate by striking the Enter key when
the window is the active window.

A window can have only one default button at a time. Setting a new
default button, therefore, may deprive another button of that status.
When {hmethod}`MakeDefault()` is called with an argument of {cpp:enum}`true`, it generates a
{hmethod}`MakeDefault()` call with an argument of {cpp:enum}`false` for previous default button.
Both buttons are redisplayed so that the user can see which one is
currently the default.

The default button can also be set by calling
{cpp:class}`BWindow`'s
{cpp:func}`~BWindow::SetDefaultButton` function. That function makes sure that the button
that's forced to give up default status and the button that obtains it
are both notified through {hmethod}`MakeDefault()` function calls.

{hmethod}`MakeDefault()` is therefore a hook function that can be augmented to take
note each time the default status of the button changes. It's called once
for each change in status, no matter which function initiated the change.

See also: {cpp:func}`BWindow::SetDefaultButton`

::::

::::{abi-group}

:::{cpp:function} virtual void BButton::MouseDown(BPoint point)
:::

Overrides the {cpp:class}`BView` version of
{cpp:func}`~BView::MouseDown` to track the cursor while the
user holds the mouse button down. As the cursor moves in and out of the
button, the {hclass}`BButton`'s value is reset accordingly. The
{cpp:func}`~BControl::SetValue` virtual
function is called to make the change each time.

If the cursor is inside the {hclass}`BButton`'s bounds rectangle when the user
releases the mouse button, this function posts a copy of the model
message so that it will be dispatched to the target object.

See also: {cpp:func}`BView::MouseDown`, {cpp:func}`BControl::Invoke`,
{cpp:func}`BInvoker::SetTarget`

::::

## Member Functions
::::{abi-group}

:::{cpp:function} virtual BButton::Archive(BMessage* archive, bool deep = true) const
:::

Stores the {hclass}`BButton` in the
{cpp:class}`BMessage` archive.

See also:
{cpp:func}`BArchivable::Archive`,
{cpp:func}`~BButton::Instantiate`
static function

::::

::::{abi-group}

:::{cpp:function} virtual void BButton::Draw(BRect updateRect)
:::

Draws the button and labels it. If the {hclass}`BButton`'s value is anything but 0,
the button is highlighted. If it's disabled, it drawn in muted shades of
gray. Otherwise, it's drawn in its ordinary, enabled, unhighlighted state.

See also: {cpp:func}`BView::Draw`

::::

::::{abi-group}

:::{cpp:function} virtual void BButton::GetPreferredSize(float* width, float* height)
:::

Calculates how big the button needs to be to display its label in the
current font, and writes the results into the variables that the {hparam}`width`
and {hparam}`height` arguments refer to.
{cpp:func}`~BView::ResizeToPreferred`, defined in the {cpp:class}`BView`
class, resizes a view's frame rectangle to the preferred size, keeping
its left and top sides constant. A button is automatically resized to its
preferred height (but not to its preferred width) by
{cpp:func}`~BButton::AttachedToWindow`.

::::

::::{abi-group}

:::{cpp:function} bool BButton::IsDefault() const
:::

{hmethod}`IsDefault()` returns whether the {hclass}`BButton`
is currently the default button.

See also: {cpp:func}`~BButton::MakeDefault`

::::

::::{abi-group}

:::{cpp:function} virtual void BButton::SetLabel(const char* string)
:::

Overrides the {cpp:class}`BControl` version of this function to make sure that
calculations based on the width of the label won't assume cached results
for the previous label.

See also: {cpp:func}`BControl::SetLabel`

::::

## Static Functions
::::{abi-group}

:::{cpp:function} static BArchivable* BButton::Instantiate(BMessage* archive)
:::

Returns a new {hclass}`BButton` object, allocated by new and created with the
version of the constructor that takes a
{cpp:class}`BMessage` archive. However, if the
archive message doesn't contain data for a {hclass}`BButton` object, this
function returns {cpp:enum}`NULL`.

See also:
{cpp:func}`BArchivable::Instantiate`,
{cpp:func}`~instantiate::object`,
{cpp:func}`~BButton::Archive`

::::

## Archived Fields