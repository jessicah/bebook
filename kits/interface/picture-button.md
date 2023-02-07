# BPictureButton
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BPictureButton::BPictureButton(BRect frame, const char* name, BPicture* off, BPicture* on, BMessage* message, uint32 behavior = B_ONE_STATE_BUTTON, uint32 resizingMode = B_FOLLOW_LEFT | B_FOLLOW_TOP, uint32 flags = B_WILL_DRAW | B_NAVIGABLE)
:::
:::{cpp:function} BPictureButton::BPictureButton(BMessage* archive)
:::

Creates a new {hclass}`BPictureButton`. The {hparam}`off` and an
{hparam}`on` images correspond to the
object's {cpp:enum}`B_CONTROL_OFF` and {cpp:enum}`B_CONTROL_ON` values; the {hparam}`behavior` argument
sets the object to be a one-state ({cpp:enum}`B_ONE_STATE_BUTTON`) or two-state
({cpp:enum}`B_TWO_STATE_BUTTON`) control, as explained in the class overview. The
other arguments are inherited from the
{cpp:class}`BView` and
{cpp:class}`BControl` constructors.
The object's initial value is {cpp:enum}`B_CONTROL_OFF`.

If the {hclass}`BPictureButton` can be disabled, it needs additional "disabled"
images, as set through
{cpp:func}`~BPictureButton::SetDisabledOff`
and {cpp:func}`~BPictureButton::SetDisabledOn`.

The {hclass}`BPictureButton` copies all
{cpp:class}`BPicture`s that are passed to it. It's the
caller's responsibility to free the {cpp:class}`BPicture` objects that are passed as
arguments.

::::

::::{abi-group}

:::{cpp:function} virtual BPictureButton::~BPictureButton()
:::

Deletes the object and its data.

::::

## Member Functions
::::{abi-group}

:::{cpp:function} virtual BPictureButton::Archive(BMessage* archive, bool deep = true) const
:::

Stores the {hclass}`BPictureButton` in the
{cpp:class}`BMessage` archive.

See also:
{cpp:func}`BArchivable::Archive`,
{cpp:func}`~BPictureButton::Instantiate`
static function

::::

::::{abi-group}

:::{cpp:function} virtual void BPictureButton::SetBehavior(uint32 behavior)
:::
:::{cpp:function} uint32 BPictureButton::Behavior() const
:::

These functions set and return whether the {hclass}`BPictureButton` is a one-state
({cpp:enum}`B_ONE_STATE_BUTTON`) or a two-state ({cpp:enum}`B_TWO_STATE_BUTTON`) control. A
one-state object acts like a normal button: It's on while the user is
pressing it, and off otherwise. A two-state object switches to the
opposite state each time the user presses and release the button.

::::

::::{abi-group}

:::{cpp:function} virtual void BPictureButton::SetEnabledOff(BPicture* picture)
:::
:::{cpp:function} BPicture* BPictureButton::EnabledOff() const
:::
:::{cpp:function} virtual void BPictureButton::SetEnabledOn(BPicture* picture)
:::
:::{cpp:function} BPicture* BPictureButton::EnabledOn() const
:::
:::{cpp:function} virtual void BPictureButton::SetDisabledOff(BPicture* picture)
:::
:::{cpp:function} BPicture* BPictureButton::DisabledOff() const
:::
:::{cpp:function} virtual void BPictureButton::SetDisabledOn(BPicture* picture)
:::
:::{cpp:function} BPicture* BPictureButton::DisabledOn() const
:::

These pairs of functions set and return one of the four images the
{hclass}`BPictureButton` displays: enabled-and-on, enabled-and-off,
disabled-and-on, and disabled-and-off, respectively. If this is a
one-state object, the disabled-and-on image needn't be set since a
disabled one-state control can never be on.

The {cpp:class}`BPicture`-retrieving
functions return {cpp:enum}`NULL` if the requested image
hasn't been set.

The {hclass}`BPictureButton` copies all
{cpp:class}`BPicture` that are passed to it. It's the
caller's responsibility to free the
{cpp:class}`BPicture` objects that are passed as
arguments.

::::

## Static Functions
::::{abi-group}

:::{cpp:function} static BArchivable* BPictureButton::Instantiate(BMessage* archive)
:::

Returns a new {hclass}`BPictureButton` object, allocated by new and created with the
version of the constructor that takes a
{cpp:class}`BMessage` archive. However, if the
archive message doesn't contain data for a {hclass}`BPictureButton` object, this
function returns {cpp:enum}`NULL`.

See also:
{cpp:func}`BArchivable::Instantiate`,
{cpp:func}`~instantiate::object`,
{cpp:func}`~BPictureButton::Archive`

::::

## Archived Fields