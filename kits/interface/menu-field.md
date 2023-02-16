:::{cpp:class} BMenuField
:::

# BMenuField

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BMenuField::BMenuField(BRect frame, const char* name, const char* label, BMenu* menu, uint32 resizingMode = B_FOLLOW_LEFT | B_FOLLOW_TOP, uint32 flags = B_WILL_DRAW | B_NAVIGABLE)
:::

:::{cpp:function} BMenuField::BMenuField(BRect frame, const char* name, const char* label, BMenu* menu, bool fixedSize, uint32 resizingMode = B_FOLLOW_LEFT | B_FOLLOW_TOP, uint32 flags = B_WILL_DRAW | B_NAVIGABLE)
:::

:::{cpp:function} BMenuField::BMenuField(BMessage* archive)
:::

Initializes the {hclass}`BMenuField` object with the specified
{hparam}`frame` rectangle, {hparam}`name`, {hparam}`resizingMode`, and
{hparam}`flags`. These arguments are the same as for any {cpp:class}`BView`
object and are passed unchanged to the {cpp:class}`BView` constructor. When
the object is attached to a window, the height of its frame rectangle will
be adjusted to fit the height of the text it displays, which depends on the
user's preferred font for menus.

By default, the {hparam}`frame` rectangle is divided horizontally in half,
with the label displayed on the left and the menu on the right. This
division can be changed with the {cpp:func}`SetDivider()
<BMenuField::SetDivider>` function. The menu is assigned to a
{cpp:class}`BMenuBar` object and will pop up under the user's control. For
most uses, the menu should be a {cpp:class}`BPopUpMenu` object.

The second form of the constructor accepts an added argument,
{hparam}`fixedSize`. If this is true, the {hclass}`BMenuField` won't adjust
its size based on the width of the items in the menu.
::::

::::{abi-group}
:::{cpp:function} virtual BMenuField::~BMenuField()
:::

Frees the label, the {cpp:class}`BMenuBar` object, and other memory
allocated by the {hclass}`BMenuField`.
::::

## Hook Functions

::::{abi-group}
:::{cpp:function} virtual void BMenuField::AttachedToWindow()
:::

:::{cpp:function} virtual void BMenuField::AllAttached()
:::

These functions override their {cpp:class}`BView` counterparts to make the
{hclass}`BMenuField`'s background color match the color of its parent view
and to adjust the height of the view to the height of the
{cpp:class}`BMenuBar` child it contains. The height of the child depends on
the size of the user's preferred font for menus.

See also: {cpp:func}`BView::AttachedToWindow`
::::

::::{abi-group}
:::{cpp:function} virtual void BMenuField::Draw(BRect updateRect)
:::

Overrides the {cpp:class}`BView` version of this function to draw the
view's border and label. The way the menu field is drawn depends on whether
it's enabled or disabled and whether or not it's the current focus for
keyboard actions.

See also: {cpp:func}`BView::Draw`
::::

::::{abi-group}
:::{cpp:function} virtual void BMenuField::KeyDown(const char* bytes, int32 numBytes)
:::

Augments the {cpp:class}`BView` version of {cpp:func}`KeyDown()
<BView::KeyDown>` to permit keyboard navigation to and from the view and to
allow users to open the menu by pressing the space bar.
::::

::::{abi-group}
:::{cpp:function} virtual void BMenuField::MouseDown(BPoint point)
:::

Overrides the {cpp:class}`BView` version of {cpp:func}`MouseDown()
<BView::MouseDown>` to enable users to pop up the menu using the mouse,
even if the cursor isn't directly over the menu portion of the bounds
rectangle.
::::

::::{abi-group}
:::{cpp:function} virtual void BMenuField::WindowActivated(bool active)
:::

Makes sure that the {hclass}`BMenuField` is redrawn when the window is
activated and deactivated, provided that it's the current focus view.

See also: {cpp:func}`BView::WindowActivated`
::::

## Member Functions

::::{abi-group}
:::{cpp:function} virtual status_t BMenuField::Archive(BMessage* archive, bool deep = true) const
:::

Calls the inherited version of {hmethod}`Archive()`, which will, in the
normal course of things, archive the child {cpp:class}`BMenuBar` and the
{cpp:class}`BMenu` it displays, provided the {hparam}`deep` flag is
{cpp:expr}`true`. This function then adds the label, divider, and current
state of the {hclass}`BMenuField` to the {cpp:class}`BMessage` archive.

See also: {cpp:func}`BArchivable::Archive`, {cpp:func}`Instantiate()
<BMenuField::Instantiate>` static function
::::

::::{abi-group}
:::{cpp:function} virtual void BMenuField::MakeFocus(bool focused)
:::

Augments the {cpp:class}`BView` version of {cpp:func}`MakeFocus()
<BView::MakeFocus>` to enable keyboard navigation. This function calls
{cpp:func}`Draw() <BMenuField::Draw>` when the {hclass}`BMenuField` becomes
the focus view and when it loses that status.
::::

::::{abi-group}
:::{cpp:function} BMenu* BMenuField::Menu() const
:::

:::{cpp:function} BMenuBar* BMenuField::MenuBar() const
:::

:::{cpp:function} BMenuItem* BMenuField::MenuItem() const
:::

{hmethod}`Menu()` returns the {cpp:class}`BMenu` object that pops up when
the user operates the {hclass}`BMenuField`; {hmethod}`MenuBar()` returns
the {cpp:class}`BMenuBar` object that contains the menu. The
{cpp:class}`BMenuBar` is created by the {hclass}`BMenuField`; the menu is
assigned to it during construction. {hmethod}`MenuItem()` returns the first
{cpp:class}`BMenuItem` assigned to the {cpp:class}`BMenuBar` object
containing the menu.

See also: The {hclass}`BMenuField` {cpp:func}`constructor
<BMenuField::BMenuField()>`
::::

::::{abi-group}
:::{cpp:function} virtual void BMenuField::SetAlignment(alignment label)
:::

:::{cpp:function} alignment BMenuField::Alignment() const
:::

These functions set and return the alignment of the label in its portion
of the frame rectangle.

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
	- {cpp:enumerator}`B_ALIGN_LEFT`
	- The label is aligned at the left side of the bounds rectangle.
-
	- {cpp:enumerator}`B_ALIGN_RIGHT`
	- The label is aligned at the right boundary of its portion of the bounds
		rectangle.
-
	- {cpp:enumerator}`B_ALIGN_CENTER`
	- The label is centered in its portion of the bounds rectangle.

:::

The default is {cpp:enumerator}`B_ALIGN_LEFT`.
::::

::::{abi-group}
:::{cpp:function} virtual void BMenuField::SetDivider(float xCoordinate)
:::

:::{cpp:function} float BMenuField::Divider() const
:::

These functions set and return the x coordinate value that divides the
bounds rectangle between the label's portion on the left and the portion
that holds the menu on the right. The coordinate is expressed in the
{hclass}`BMenuField`'s coordinate system.

The default divider splits the bounds rectangle in two equal sections. By
resetting it, you can provide more or less room for the label or the menu.
::::

::::{abi-group}
:::{cpp:function} virtual void BMenuField::SetEnabled(bool enabled)
:::

:::{cpp:function} bool BMenuField::IsEnabled() const
:::

{hmethod}`SetEnabled()` enables the {hclass}`BMenuField` if the
{hparam}`enabled` flag is {cpp:expr}`true`, and disables it if the flag is
{cpp:expr}`false`. {hmethod}`IsEnabled()` returns whether or not the object
is currently enabled. When disabled, the {hclass}`BMenuField` doesn't
respond to mouse and keyboard manipulations.

If the {hparam}`enabled` flag changes the current state of the object,
{hmethod}`SetEnabled()` causes the view to be redrawn, so that its new
state can be displayed to the user.
::::

::::{abi-group}
:::{cpp:function} virtual void BMenuField::SetLabel(const char* string)
:::

:::{cpp:function} const char* BMenuField::Label() const
:::

{hmethod}`SetLabel()` frees the current label and, if the argument it's
passed is not {cpp:expr}`NULL`, replaces it with a copy of string.
{hmethod}`Label()` returns the current label. The string it returns belongs
to the {hclass}`BMenuField` object.

See also: The {hclass}`BMenuField` {cpp:func}`constructor
<BMenuField::BMenuField()>`
::::

## Static Functions

::::{abi-group}
:::{cpp:function} static BArchivable* BMenuField::Instantiate(BMessage* archive)
:::

Returns a new {hclass}`BMenuField` object, allocated by new and created
with the version of the constructor that takes a {cpp:class}`BMessage`
archive. However, if the archive message doesn't contain data for a
{hclass}`BMenuField` object, this function returns {cpp:expr}`NULL`.

See also: {cpp:func}`BArchivable::Instantiate`,
{cpp:func}`instantiate_object() <instantiate::object>`,
{cpp:func}`Archive() <BMenuField::Archive>`
::::

## Archived Fields

The {hclass}`BMenu` class implements the suite called "suite/vnd.Be-menu"
consisting of the following messages:

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
	- {hparam}`_label`

	- {cpp:enumerator}`B_STRING_TYPE`

	- {hclass}`BMenuField` label.

-
	- {hparam}`_disable`

	- {cpp:enumerator}`B_BOOL_TYPE`

	- Exists and {cpp:expr}`true` only if menu is disabled.

-
	- {hparam}`_align`

	- {cpp:enumerator}`B_INT32_TYPE`

	- Alignment of label in the frame rectangle.

-
	- {hparam}`_divide`

	- {cpp:enumerator}`B_FLOAT_TYPE`

	- The x-coordinate dividing the bounds rectangle between the label and the
menu.


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
	- Name

	- Level

	- Description

-
	- {hparam}`_mc_mb_`

	- 0

	- Private menu bar.


:::
