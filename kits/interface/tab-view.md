:::{cpp:class} BTabView
:::

# BTabView

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BTabView::BTabView(BRect frame, const char* name, button_width width = B_WIDTH_AS_USUAL, uint32 resizingMode = B_FOLLOW_ALL, uint32 flags = B_FULL_UPDATE_ON_RESIZE | B_WILL_DRAW | B_NAVIGABLE | B_NAVIGABLE_JUMP | B_FRAME_EVENTS)
:::

:::{cpp:function} BTabView::BTabView(const BTabView& tabView)
:::

:::{cpp:function} BTabView::BTabView(BMessage* archive)
:::

Initializes the {hclass}`BTabView` to the {hparam}`frame` rectangle,
stated in its eventual parent's coordinate system, and assigns it the
specified {hparam}`name`, {hparam}`resizingMode`, and {hparam}`flags`.
These are described in detail in the {cpp:class}`BView` section.

The {hparam}`width` parameter, which can be one of the following values,
specifies the widths of the tabs in the {hclass}`BTabView`. All tabs in a
{hclass}`BTabView` are the same width.

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
	- {cpp:enumerator}`B_WIDTH_FROM_WIDEST`
	- Each tab's width is determined based upon the width of the widest tab
		name.
-
	- {cpp:enumerator}`B_WIDTH_AS_USUAL`
	- The default tab width is used for all tabs.
-
	- {cpp:enumerator}`B_WIDTH_FROM_LABEL`
	- The tab width for each tab is based on the width of the tab's label.

:::

The container view for the {hclass}`BTabView`'s subviews is created and
added to the {hclass}`BTabView` as well.
::::

::::{abi-group}
:::{cpp:function} virtual BTabView::~BTabView()
:::

Frees all memory the {hclass}`BTabView` allocated, and deletes every
{cpp:class}`BTab` attached to it.
::::

## Hook Functions

::::{abi-group}
:::{cpp:function} virtual void BTabView::AttachedToWindow()
:::

Calls {cpp:func}`BView::AttachedToWindow`, then selects the first tab in
the tab view.
::::

::::{abi-group}
:::{cpp:function} virtual void BTabView::Draw(BRect updateRect)
:::

Draws the tabs and the box that encloses the container view that displays
the selected tab's target view.
::::

::::{abi-group}
:::{cpp:function} virtual void BTabView::DrawBox(BRect selTabRect)
:::

Draws the box that encloses the container view. {hparam}`selTabRect` is
the frame rectangle of the currently-selected tab; this information is used
to allow the box to attach properly to the current tab. This is the same
rectangle that the {cpp:func}`DrawTabs() <BTabView::DrawTabs>` function
returns.

This is called for you by the {cpp:func}`Draw() <BTabView::Draw>` function
and is provided primarily as a hook for customizing the appearance of your
{hclass}`BTabView`.
::::

::::{abi-group}
:::{cpp:function} virtual BRect BTabView::DrawTabs()
:::

Draws all the tabs in the {hclass}`BTabView` and returns the frame
rectangle of the currently-selected tab. This rectangle should then be
passed to {cpp:func}`DrawBox() <BTabView::DrawBox>` to draw the container
view's enclosing box.

This is called for you by the {cpp:func}`Draw() <BTabView::Draw>` function
and is provided primarily as a hook for customizing the appearance of your
{hclass}`BTabView`.
::::

::::{abi-group}
:::{cpp:function} virtual void BTabView::KeyDown(const char* bytes, int32 numBytes)
:::

The {hmethod}`KeyDown()` function handles keyboard navigation of the
{hclass}`BTabView`; the down and left arrow keys move the focus to the
left, and the up and right arrow keys move the focus to the right. The
space bar and enter keys select the focused tab.

All other keys are passed through to the {cpp:func}`BView::KeyDown`
function for further processing.

See also: the Keyboard Information appendix, "B_KEY_DOWN" in the Message
Protocols appendix, {cpp:func}`BView::KeyDown`, {ref}`modifiers()`
::::

::::{abi-group}
:::{cpp:function} virtual void BTabView::MouseDown(BPoint point)
:::

Identifies which tab (if any) the user clicked and selects that tab. If
the mouse was not inside a tab when clicked, the
{cpp:func}`BView::MouseDown` function is called.

See also: "B_MOUSE_DOWN" in the Message Protocols appendix,
{cpp:func}`BView::GetMouse`
::::

::::{abi-group}
:::{cpp:function} virtual void BTabView::WindowActivated(bool active)
:::

Calls the inherited version of {cpp:func}`WindowActivated()
<BView::WindowActivated>`, then calls {cpp:func}`DrawTabs()
<BTabView::DrawTabs>` to redraw the tabs.

See also: {cpp:func}`BWindow::WindowActivated`
::::

## Member Functions

::::{abi-group}
:::{cpp:function} virtual void BTabView::AddTab(BView* target, BTab* tab = NULL)
:::

:::{cpp:function} virtual BTab* BTabView::RemoveTab(int32 tab_index)
:::

{hmethod}`AddTab()` adds the specified {hparam}`tab` as the rightmost tab
in the {hclass}`BTabView`. The new tab's target view is set to
{hparam}`target`.

If {hparam}`tab` is {cpp:expr}`NULL`, a new {cpp:class}`BTab` object is
constructed and added to the {hclass}`BTabView`. You can get a pointer to
the new tab using the {cpp:func}`TabAt() <BTabView::TabAt>` function

if you choose to reimplement {hmethod}`AddTab()`, you should call the
inherited form of this function once the {cpp:class}`BTab` has been
customized.

{hmethod}`RemoveTab()` removes the tab with the specified {hparam}`index`
number from the {hclass}`BTabView` and returns a pointer to the
{cpp:class}`BTab` object. The {cpp:class}`BTab` is not deleted—if you don't
need it anymore, you can do that yourself.
::::

::::{abi-group}
:::{cpp:function} virtual BTabView::Archive(BMessage* archive, bool deep = true) const
:::

Calls the inherited version of {cpp:func}`Archive() <BView::Archive>` and
stores the {hclass}`BTabView` in the {cpp:class}`BMessage` archive.

See also: {cpp:func}`BArchivable::Archive`, {cpp:func}`Instantiate()
<BTabView::Instantiate>` static function
::::

::::{abi-group}
:::{cpp:function} virtual void BTabView::MakeFocus(bool focused = true)
:::

Makes the {hclass}`BTabView` the current focus by first calling
{cpp:func}`BView::MakeFocus`, then making the currently-selected tab the
focus of the {hclass}`BTabView`.
::::

::::{abi-group}
:::{cpp:function} virtual void BTabView::Select(int32 tab)
:::

:::{cpp:function} int32 BTabView::Selection() const
:::

{hmethod}`Select()` selects the tab specified by its index number, first
deselecting the previously-selected tab.

{hmethod}`Selection()` returns the index number of the currently-selected
tab.
::::

::::{abi-group}
:::{cpp:function} virtual void BTabView::SetFocusTab(int32 tab, bool focused)
:::

:::{cpp:function} int32 BTabView::FocusTab() const
:::

{hmethod}`SetFocusTab()` sets the focus state of the specified tab. If
{hparam}`focused` is {cpp:expr}`true`, the specified tab becomes the new
focus; if {hparam}`focused` is {cpp:expr}`false`, the focus is removed from
the currently-focused tab but no new focus is set (the {hclass}`BTabView`
becomes focusless).

{hmethod}`FocusTab()` returns the index number of the tab that is
currently the focus.
::::

::::{abi-group}
:::{cpp:function} virtual void BTabView::SetTabHeight(float height)
:::

:::{cpp:function} float BTabView::TabHeight() const
:::

{hmethod}`SetTabHeight()` sets the height of the tabs in the
{hclass}`BTabView`. {hmethod}`TabHeight()` returns the current tab height.

When you change the tab height, the container view for the target views is
resized so that the {hclass}`BTabView` doesn't change size. Making the tabs
taller by _n_ pixels causes the container view's top edge to move down by
_n_ pixels, and decreasing the heights of the tabs increases the height of
the container view.
::::

::::{abi-group}
:::{cpp:function} virtual void BTabView::SetTabWidth(button_width width)
:::

:::{cpp:function} button_width BTabView::TabWidth() const
:::

{hmethod}`SetTabWidth()` sets the width of the tabs in the
{hclass}`BTabView`, and {hmethod}`TabWidth()` returns the current width
setting. {hparam}`width` must be one of the following values:

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
	- {cpp:enumerator}`B_WIDTH_FROM_WIDEST`
	- Each tab's width is determined based upon the width of the widest tab
		name.
-
	- {cpp:enumerator}`B_WIDTH_AS_USUAL`
	- The default tab width is used for all tabs.

:::
::::

::::{abi-group}
:::{cpp:function} virtual BTab* BTabView::TabAt(int32 tab_index)
:::

Returns a pointer to the {cpp:class}`BTab` object at the specified index.
The leftmost tab is index number 0.
::::

::::{abi-group}
:::{cpp:function} virtual BRect BTabView::TabFrame(int32 tab_index)
:::

Returns the frame rectangle of the tab whose index number is specified.
The leftmost tab is index number 0.

See also: {cpp:func}`DrawTabs() <BTabView::DrawTabs>`,
{cpp:func}`DrawBox() <BTabView::DrawBox>`, {cpp:func}`Draw()
<BTabView::Draw>`
::::

## Static Functions

::::{abi-group}
:::{cpp:function} static BArchivable* BTabView::Instantiate(BMessage* archive)
:::

Returns a new {hclass}`BTabView` object, allocated by new and created with
the version of the constructor that takes a {cpp:class}`BMessage` archive.
However, if the {hparam}`archive` message doesn't contain data for a
{hclass}`BTabView` object, {hmethod}`Instantiate()` returns
{cpp:expr}`NULL`.

See also: {cpp:func}`BArchivable::Instantiate`,
{cpp:func}`instantiate_object() <instantiate::object>`,
{cpp:func}`Archive() <BTabView::Archive>`
::::

## Archived Fields

The {cpp:func}`Archive() <BTabView::Archive>` function adds the following
fields to its {cpp:class}`BMessage` argument:

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
	- {hparam}`_high`

	- {cpp:enumerator}`B_FLOAT_TYPE`

	- The height of the tabs.

-
	- {hparam}`_but_width`

	- {cpp:enumerator}`B_INT16_TYPE`

	- The tab width value.

-
	- {hparam}`_sel`

	- {cpp:enumerator}`B_INT32_TYPE`

	- Which tab is selected.


:::

The archived tabs are added to the {hparam}`_l_items` field (deep copy
only). The tabs' target views are added to the {hparam}`_views` field (deep
copy only), with the leftmost tab inserted first in the {hparam}`_views`
array, and the rightmost tab inserted last.
