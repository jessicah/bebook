# BBox
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BBox::BBox(BRect frame, const char* name = NULL, uint32 resizingMode = B_FOLLOW_LEFT | B_FOLLOW_TOP, uint32 flags = B_WILL_DRAW | B_FRAME_EVENTS | B_NAVIGABLE_JUMP, border_style border = B_FANCY_BORDER)
:::
:::{cpp:function} BBox::BBox(BMessage* archive)
:::

Initializes the {hclass}`BBox` by passing the {hparam}`frame`, {hparam}`name`, {hparam}`resizingMode`, and {hparam}`flags`
to the {cpp:class}`BView` constructor, and sets the style of its border to {hparam}`border`.
Three border styles are possible:

:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_PLAIN_BORDER`
	- The border is a simple line, lighter on the left and top than on the right and bottom so that the box looks raised from the surrounding surface.
-
	- {cpp:enum}`B_FANCY_BORDER`
	- The border is a fancier line that looks like a 3D groove inset into the surrounding surface of the view.
-
	- {cpp:enum}`B_NO_BORDER`
	- There is no border. This option is not that useful for a {hclass}`BBox` object; it turns the box into something other than a box.
:::
The constructor also sets the font for displaying the {hclass}`BBox`'s label to the
system bold font ({cpp:enum}`be_bold_font`). However, the new object doesn't have a
label; call
{cpp:func}`~BBox::SetLabel`
to assign it one.
::::

::::{abi-group}

:::{cpp:function} virtual BBox::~BBox()
:::

Frees the label, if the {hclass}`BBox` has one.

::::

## Member Functions
::::{abi-group}

:::{cpp:function} virtual BBox::Archive(BMessage* archive, bool deep = true) const
:::

Stores the {hclass}`BBox` in the
{cpp:class}`BMessage` archive.

See also:
{cpp:func}`BArchivable::Archive`,
{cpp:func}`~BBox::Instantiate`
static function

::::

::::{abi-group}

:::{cpp:function} virtual void BBox::AttachedToWindow()
:::

Makes the {hclass}`BBox`'s background view color and its low color match the
background color of its new parent.

::::

::::{abi-group}

:::{cpp:function} virtual void BBox::Draw(BRectupdateRect)
:::

Draws the box and its label. This function is called automatically in
response to update messages.

::::

::::{abi-group}

:::{cpp:function} virtual void BBox::FrameResized(float width, float height)
:::

Makes sure that the parts of the box that change when it's resized are
redrawn.

See also: {cpp:func}`BView::FrameResized`

::::

::::{abi-group}

:::{cpp:function} virtual void BBox::SetBorder(border_style border)
:::
:::{cpp:function} border_style BBox::Border() const
:::

These functions set and return the style of border the {hclass}`BBox`
draws—{cpp:enum}`B_PLAIN_BORDER`, {cpp:enum}`B_FANCY_BORDER`, or {cpp:enum}`B_NO_BORDER`. The border
style is initially set by the {hclass}`BBox` constructor.

::::

::::{abi-group}

:::{cpp:function} void BBox::SetLabel(const char* string)
:::
:::{cpp:function} status_t BBox::SetLabel(BView* viewLabel)
:::
:::{cpp:function} const char* BBox::Label() const
:::
:::{cpp:function} BView* BBox::LabelView() const
:::

These functions set and return the label that's displayed along the top
edge of the box.
{hmethod}`SetLabel()` copies {hparam}`string` and makes it the {hclass}`BBox`'s label,
freeing the previous label, if any. If {hparam}`string` is {cpp:enum}`NULL`, it removes the
current label and frees it.

Alternately, you can use the second form of {hmethod}`SetLabel()` to specify a view
to be used as the {hclass}`BBox`'s label. This view can be anything, including
controls.

{hmethod}`Label()` returns a pointer to the
{hclass}`BBox`'s current label, or {cpp:enum}`NULL` if it
doesn't have one (or the label is a view).

{hmethod}`LabelView()` returns a pointer to the
{cpp:class}`BView` that's being used as the
{hclass}`BBox`'s label, or {cpp:enum}`NULL` if
either there is no label, or the label is a string.

:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- No error occurred.
:::
No other errors are returned.
::::

## Static Functions
::::{abi-group}

:::{cpp:function} static BArchivable* BBox::Instantiate(BMessage* archive)
:::

Returns a new {hclass}`BBox` object, allocated by new and created with the
version of the constructor that takes a
{cpp:class}`BMessage` archive. However, if the
archive message doesn't contain data for a {hclass}`BBox` object, this
function returns {cpp:enum}`NULL`.

See also:
{cpp:func}`BArchivable::Instantiate`,
{cpp:func}`~instantiate::object`,
{cpp:func}`~BBox::Archive`()

::::

## Archived Fields