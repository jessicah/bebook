# BRadioButton
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BRadioButton::BRadioButton(BRect frame, const char* name, const char* label, BMessage* message, uint32 resizingMode = B_FOLLOW_LEFT | B_FOLLOW_TOP, uint32 flags = B_WILL_DRAW | B_NAVIGABLE)
:::
:::{cpp:function} BRadioButton::BRadioButton(BMessage* archive)
:::

Initializes the {hclass}`BRadioButton` by passing all arguments
to the {cpp:class}`BControl`
constructor without change.
{cpp:class}`BControl`
initializes the radio button's {hparam}`label`
and assigns it a model {hparam}`message` that identifies the action that should be
taken when the radio button is turned on. When the user turns the button
on, the {hclass}`BRadioButton` posts a copy of the {hparam}`message` so that it can be
delivered to the target handler.

The {hparam}`frame`, {hparam}`name`,
{hparam}`resizingMode`, and {hparam}`flags` arguments are the same as those
declared for the {cpp:class}`BView`
class and are passed without change from {cpp:class}`BControl`
to the {cpp:class}`BView` constructor.

The {hclass}`BRadioButton` draws at the bottom of its frame rectangle beginning at
the left side. It ignores any extra space at the top or on the right.
(However, the user can click anywhere within the {hparam}`frame` rectangle to turn
on the radio button). When the object is attached to a window, the height
of the rectangle will be adjusted so that there is exactly the right
amount of room to accommodate the label.

See also:
The {cpp:class}`BControl` and
{cpp:class}`BView` constructors,
{cpp:func}`~BRadioButton::AttachedToWindow`

::::

::::{abi-group}

:::{cpp:function} virtual BRadioButton::~BRadioButton()
:::

Does nothing; a {hclass}`BRadioButton` doesn't need to clean up after itself when
it's deleted.

::::

## Hook Functions
::::{abi-group}

:::{cpp:function} virtual void BRadioButton::AttachedToWindow()
:::

Augments the {cpp:class}`BControl` version of
{cpp:func}`~BControl::AttachedToWindow` to set the view and
low colors of the {hclass}`BRadioButton` to the match its parent's view color, and
to resize the radio button vertically to fit the height of the label it
displays. The height of the label depends on the {hclass}`BRadioButton`'s font.

::::

::::{abi-group}

:::{cpp:function} virtual void BRadioButton::Draw(BRect updateRect)
:::

Draws the radio button—the circular icon—and its label. The
center of the icon is filled when the {hclass}`BRadioButton`'s value is 1
({cpp:enum}`B_CONTROL_ON`); it's left empty when the value is 0
({cpp:enum}`B_CONTROL_OFF`).

See also:
{cpp:func}`BView::Draw`

::::

::::{abi-group}

:::{cpp:function} virtual void BRadioButton::GetPreferredSize(float* width, float* height)
:::

Calculates the optimal size for the radio button to display the icon and
the label in the current font, and places the result in the variables
that the {hparam}`width` and {hparam}`height`
arguments refer to.
{cpp:func}`~BView::ResizeToPreferred`,
defined in the {cpp:class}`BView` class,
resizes a view's frame rectangle to the
preferred size, keeping its left and top sides constant.
{cpp:func}`~BRadioButton::AttachedToWindow`
automatically resizes a radio button to its preferred
height, but doesn't modify its width.

See also:
{cpp:func}`BView::GetPreferredSize`,
{cpp:func}`BView::AttachedToWindow`

::::

::::{abi-group}

:::{cpp:function} virtual void BRadioButton::KeyDown(const char* bytes, int32 numBytes)
:::

Augments the inherited versions of
{cpp:func}`~BControl::KeyDown`
to turn the radio button on
and deliver a message to the target
{cpp:class}`BHandler`
when the character passed in
{hparam}`bytes` is {cpp:enum}`B_SPACE or B_ENTER`.

See also:
{cpp:func}`BView::KeyDown`,
{cpp:func}`~BRadioButton::SetValue`

::::

::::{abi-group}

:::{cpp:function} virtual void BRadioButton::MouseDown(BPoint point)
:::

Responds to a mouse-down event in the radio button by tracking the cursor
while the user holds the mouse button down. If the cursor is pointing to
the radio button when the user releases the mouse button, this function
turns the button on (and consequently turns all sibling {hclass}`BRadioButton`s
off), calls the {hclass}`BRadioButton`'s
{cpp:func}`~BRadioButton::Draw` function, and posts a message that
will be delivered to the target
{cpp:class}`BHandler`. Unlike a
{cpp:class}`BCheckBox`, a
{hclass}`BRadioButton` posts the message—it's
"invoked"—only when it's
turned on, not when it's turned off.

See also:
{cpp:func}`BControl::Invoke`,
{cpp:func}`BInvoker::SetTarget`,
{cpp:func}`~BRadioButton::SetValue`

::::

::::{abi-group}

:::{cpp:function} virtual void BRadioButton::SetValue(int32 value)
:::

Augments the {cpp:class}`BControl`
version of {cpp:func}`~BControl::SetValue` to turn all sibling
{hclass}`BRadioButton`s off (set their values to 0) when this
{hclass}`BRadioButton` is
turned on (when the value passed is anything but 0).

::::

## Member Functions
::::{abi-group}

:::{cpp:function} virtual status_t BRadioButton::Archive(BMessage* archive, bool deep = true) const
:::

Calls the inherited version of
{cpp:func}`~BControl::Archive`
and doesn't add anything
specific to the {hclass}`BRadioButton` class to the
{cpp:class}`BMessage` archive.

{cpp:func}`BArchivable::Archive`,
{cpp:func}`~BRadioButton::Instantiate`
static function

::::

## Static Functions
::::{abi-group}

:::{cpp:function} static BArchivable* BRadioButton::Instantiate(BMessage* archive)
:::

Returns a new {hclass}`BRadioButton` object, allocated by new and created with the
version of the constructor that takes a
{cpp:class}`BMessage` archive. However, if the
message doesn't contain data for an archived {hclass}`BRadioButton` object, this
function returns {cpp:enum}`NULL`.

{cpp:func}`BArchivable::Instantiate`,
{cpp:func}`~instantiate::object`,
{cpp:func}`~BRadioButton::Archive`

::::
