:::{cpp:class} BCheckBox
:::

# BCheckBox

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BCheckBox::BCheckBox(BRect frame, const char* name, const char* label, BMessage* message, uint32 resizingMode = B_FOLLOW_LEFT | B_FOLLOW_TOP, uint32 flags = B_WILL_DRAW | B_NAVIGABLE)
:::

:::{cpp:function} BCheckBox::BCheckBox(BMessage* archive)
:::

Initializes the {hclass}`BCheckBox` by passing all arguments to the
{cpp:class}`BControl` {cpp:func}`constructor <BControl::BControl()>`

If necessary, the bottom coordinate of the object's frame rectangle is
increased to accommodate the height of the label, given the object's font
({cpp:enumerator}`be_plain_font`, by default).

Freshly constructed, the object's state is
{cpp:enumerator}`B_CONTROL_OFF`. Like all controls, the check box's view
and low colors are set to those of its parent when the object is attached
to a window.
::::

::::{abi-group}
:::{cpp:function} virtual BCheckBox::~BCheckBox()
:::

Deletes the {hclass}`BCheckBox` object.
::::

## Member Functions

All of {hclass}`BCheckBox`'s member functions are implementations of
functions declared by its superclasses. For information on specific
functions, look in {cpp:class}`BControl` , then in {cpp:class}`BView` , and
so on up the inheritance hierarchy.

## Archived Fields

See "{cpp:func}`Archived Fields <BControl::ArchivedFields>`" in the
{cpp:class}`BControl` class. {hclass}`BCheckbox` doesn't add any of its own
fields to the archive message.
