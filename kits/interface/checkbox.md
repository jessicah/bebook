# BCheckBox
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BCheckBox::BCheckBox(BRect frame, const char* name, const char* label, BMessage* message, uint32 resizingMode = B_FOLLOW_LEFT | B_FOLLOW_TOP, uint32 flags = B_WILL_DRAW | B_NAVIGABLE)
:::
:::{cpp:function} BCheckBox::BCheckBox(BMessage* archive)
:::

Initializes the {hclass}`BCheckBox` by passing all arguments to the
{cpp:class}`BControl`
{cpp:func}`~BControl::Constructor`

If necessary, the bottom coordinate of the object's frame rectangle is
increased to accommodate the height of the label, given the object's font
({cpp:enum}`be_plain_font`, by default).

Freshly constructed, the object's state is {cpp:enum}`B_CONTROL_OFF`. Like all
controls, the check box's view and low colors are set to those of its
parent when the object is attached to a window.

::::

::::{abi-group}

:::{cpp:function} virtual BCheckBox::~BCheckBox()
:::

Deletes the {hclass}`BCheckBox` object.

::::

## Member Functions
## Archived Fields