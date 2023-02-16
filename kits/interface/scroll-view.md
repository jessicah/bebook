:::{cpp:class} BScrollView
:::

# BScrollView

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BScrollView::BScrollView(const char* name, BView* target, uint32 resizingMode = B_FOLLOW_LEFT | B_FOLLOW_TOP, uint32 flags = 0, bool horizontal = false, bool vertical = false, border_style border = B_FANCY_BORDER)
:::

:::{cpp:function} BScrollView::BScrollView(BMessage* archive)
:::

Creates a {hclass}`BScrollView` that has {hparam}`target` as its target
view. If {hparam}`horizontal` is {cpp:expr}`true`, a horizontal scroll bar
is added to the bottom of the target view. If {hparam}`vertical` is
{cpp:expr}`true`, a vertical scroll bar is added to the target's right
side. The {hclass}`BScrollView`'s frame is manufactured for you to contain
the target view, the scroll bars, and the optional border; the location of
the target view doesn't change. The scroll bar "thickness" constants,
defined in ScrollBar.h, will help you compute the size of the frame:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Constant

	- Description

-
	- {cpp:enumerator}`B_V_SCROLL_BAR_WIDTH`
	- The width of a vertical scroll bar.
-
	- {cpp:enumerator}`B_H_SCROLL_BAR_HEIGHT`
	- The height of a horizontal scroll bar.

:::

The target and the scroll bars are added as (sibling) children of the
scroll view, and the target's {cpp:func}`TargetedByScrollView()
<BView::TargetedByScrollView>` function is called. The target must not
already be the child of some other view.

The border argument can be one of three values:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Constant

	- Description

-
	- {cpp:enumerator}`B_PLAIN_BORDER`
	- Draw a border consisting of just a simple line around the target view and
		scroll bars.
-
	- {cpp:enumerator}`B_FANCY_BORDER`
	- Draw a fancier border that looks like a 3D groove inset into the surface
		of the view.
-
	- {cpp:enumerator}`B_NO_BORDER`
	- Don't draw a border.

:::

If the resize mode of the target view is
{cpp:enumerator}`B_FOLLOW_ALL_SIDES`, it and the scroll bars will be
automatically resized to fill the scroll view whenever the scroll view is
resized.

The scroll bars created by the {hclass}`BScrollView` have an initial range
of 0 to 1000. Use the {cpp:func}`ScrollBar() <BScrollView::ScrollBar>`
function to retrieve the scroll bars and reset their ranges.

The {hparam}`name`, {hparam}`resizingMode`, and {hparam}`flags` arguments
are identical to those declared in the {cpp:class}`BView` class and are
passed to the {cpp:class}`BView` constructor. If a border is requested,
{cpp:enumerator}`B_WILL_DRAW` is automatically added to the flags mask. The
other two arguments are passed to the {cpp:class}`BView` class unchanged.

See also: The {cpp:class}`BView` {cpp:func}`constructor <BView::BView()>`,
{cpp:func}`TargetedByScrollView() <BView::TargetedByScrollView>`
::::

::::{abi-group}
:::{cpp:function} virtual BScrollView::~BScrollView()
:::

Does nothing.
::::

## Hook Functions

::::{abi-group}
:::{cpp:function} virtual void BScrollView::AttachedToWindow()
:::

Resizes scroll bars belonging to {hclass}`BScrollView`s that occupy the
right bottom corner of a document window
({cpp:enumerator}`B_DOCUMENT_WINDOW`) so that room is left for the resize
knob. This function assumes that vertical scroll bars are
{cpp:enumerator}`B_V_SCOLL_BAR_WIDTH` units wide and horizontal scroll bars
are {cpp:enumerator}`B_H_SCROLL_BAR_HEIGHT` units high. It doesn't check to
make sure the window is actually resizable.

This function also sets the default high color to a medium shade of gray.

See also: {cpp:func}`BView::AttachedToWindow`
::::

::::{abi-group}
:::{cpp:function} virtual void BScrollView::Draw(BRect updateRect)
:::

Draws the border around the target view and scroll views, provided a
border was requested when the {hclass}`BScrollView` was constructed.

See also: The {hclass}`BScrollView` {cpp:func}`constructor
<BScrollView::BScrollView()>`, {cpp:func}`BView::Draw`
::::

## Member Functions

::::{abi-group}
:::{cpp:function} virtual status_t BScrollView::Archive(BMessage* archive, bool deep = true) const
:::

Calls the inherited version of {cpp:func}`Archive() <BView::Archive>`,
which will archive the target view and scroll bars if the {hparam}`deep`
flag is {cpp:expr}`true`. This function then adds the
{hclass}`BScrollView`'s border style to the archive message.

See also: {cpp:func}`BArchivable::Archive`, {cpp:func}`Instantiate()
<BScrollView::Instantiate>` static function
::::

::::{abi-group}
:::{cpp:function} BScrollBar* BScrollView::ScrollBar(orientation posture) const
:::

Returns the horizontal scroll bar if posture is
{cpp:enumerator}`B_HORIZONTAL` and the vertical scroll bar if posture is
{cpp:enumerator}`B_VERTICAL`. If the {hclass}`BScrollView` doesn't contain
a scroll bar with the requested orientation, this function returns
{cpp:expr}`NULL`.

See also: The {cpp:class}`BScrollBar` class
::::

::::{abi-group}
:::{cpp:function} virtual void BScrollView::SetBorder(border_style border)
:::

:::{cpp:function} border_style BScrollView::Border() const
:::

These functions set and return the style of the {hclass}`BScrollView`'s
border, which may be {cpp:enumerator}`B_PLAIN_BORDER`,
{cpp:enumerator}`B_FANCY_BORDER`, or {cpp:enumerator}`B_NO_BORDER`. The
border is originally set by the constructor. The three constants and the
border's effect on the {hclass}`BScrollView` are discussed there.

See also: The {hclass}`BScrollView` {cpp:func}`constructor
<BScrollView::BScrollView()>`
::::

::::{abi-group}
:::{cpp:function} virtual status_t BScrollView::SetBorderHighlighted(bool highlighted)
:::

:::{cpp:function} bool BScrollView::IsBorderHighlighted() const
:::

{hmethod}`SetBorderHighlighted()` highlights the border of the
{hclass}`BScrollView` when the {hparam}`highlighted` flag is
{cpp:expr}`true`, and removes the highlighting when the flag is
{cpp:expr}`false`. This function works by calling {cpp:func}`Draw()
<BScrollView::Draw>`. However, it works only for a border in the
{cpp:enumerator}`B_FANCY_BORDER` style. If successful, it returns
{cpp:enumerator}`B_OK`. Otherwise, it returns {cpp:enumerator}`B_ERROR`.

{hmethod}`IsBorderHighlighted()` returns whether the border is currently
highlighted. The return value is always {cpp:expr}`false` for a
{hclass}`BScrollView` that doesn't have a border or has only a "plain" one.

Highlighting a {hclass}`BScrollView`'s border shows that the target view
is the current focus view for the window. Typically, the target view calls
{hmethod}`SetBorderHighlighted()` from its {cpp:func}`MakeFocus()
<BView::MakeFocus>` function when the focus changes. (The target knows that
it's inside a {hclass}`BScrollView` because of the
{cpp:func}`TargetedByScrollView() <BView::TargetedByScrollView>`
notification it received.)
::::

## Static Functions

::::{abi-group}
:::{cpp:function} static BArchivable* BScrollView::Instantiate(BMessage* archive)
:::

Returns a new {hclass}`BScrollView` object, allocated by new and created
with the version of the constructor that takes a {cpp:class}`BMessage`
archive. However, if the message doesn't contain data for an archived
{hclass}`BScrollView` object, {hmethod}`Instantiate()` returns
{cpp:expr}`NULL`.

{cpp:func}`BArchivable::Instantiate`, {cpp:func}`instantiate_object()
<instantiate::object>`, {cpp:func}`Archive() <BScrollBar::Archive>`
::::

## Archived Fields

The {cpp:func}`Archive() <BScrollView::Archive>` function adds the
following fields to its {cpp:class}`BMessage` argument:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Field

	- Type code

	- Description

-
	- {hparam}`_style`

	- {cpp:enumerator}`B_INT32_TYPE`

	- Border type.


:::

The following views are added to the {hparam}`_views` field (deep copy
only):

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Field

	- Type code

	- Description

-
	- {hparam}`target`

	- 0

	- Target view for the object.

-
	- {hparam}`_VSB_`

	- 0

	- Vertical {cpp:class}`BScrollBar`.

-
	- {hparam}`_HSB_`

	- 0

	- Horizontal {cpp:class}`BScrollBar`.


:::

Some of these fields may not be present if the setting they represent
isn't used, or is the default value. For example, if the border type is
{cpp:enumerator}`B_FANCY_BORDER`, the {hparam}`_style` field won't be found
in the archive.
