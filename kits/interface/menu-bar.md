:::{cpp:class} BMenuBar
:::

# BMenuBar

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BMenuBar::BMenuBar(BRect frame, const char* name, uint32 resizingMode = B_FOLLOW_LEFT_RIGHT | B_FOLLOW_TOP, menu_layout layout = B_ITEMS_IN_ROW, bool resizeToFit = true)
:::

:::{cpp:function} BMenuBar::BMenuBar(BMessage* archive)
:::

Initializes the {hclass}`BMenuBar` by assigning it a {hparam}`frame`
rectangle, a {hparam}`name`, and a {hparam}`resizingMode`, just like other
{cpp:class}`BView`s. These values are passed up the inheritance hierarchy
to the {cpp:class}`BView` {cpp:func}`constructor <BView::BView()>`. The
default resizing mode ({cpp:enumerator}`B_FOLLOW_LEFT_RIGHT` plus
{cpp:enumerator}`B_FOLLOW_TOP`) is designed for a true menu bar (one that's
displayed along the top edge of a window). It permits the menu bar to
adjust itself to changes in the window's width, while keeping it glued to
the top of the window frame.

The layout argument determines how items are arranged in the menu bar. By
default, they're arranged in a row as befits a true menu bar. If an
instance of this class is being used to implement something other than a
horizontal menu, items can be laid out in a column (
{cpp:enumerator}`B_ITEMS_IN_COLUMN` ) or in a matrix (
{cpp:enumerator}`B_ITEMS_IN_MATRIX` ).

If the {hparam}`resizeToFit` flag is turned on, as it is by default, the
frame rectangle of the {hclass}`BMenuBar` will be automatically resized to
fit the items it displays. This is generally a good idea, since it relieves
you of the responsibility of testing user preferences to determine what
size the menu bar should be. Because the font and font size for menu items
are user preferences, items can vary in size from user to user.

When {hparam}`resizeToFit` is {cpp:expr}`true`, the frame rectangle
determines only where the menu bar is located, not how large it will be.
The rectangle's left and top data members are respected, but the right and
bottom sides are adjusted to accommodate the items that are added to the
menu bar.

Two kinds of adjustments are made if the layout is
{cpp:enumerator}`B_ITEMS_IN_ROW`, as it typically is for a menu bar:

-   The height of the menu bar is adjusted to the height of a single item.

-   If the {hparam}`resizingMode` includes
{cpp:enumerator}`B_FOLLOW_LEFT_RIGHT`, the width of the menu bar is
adjusted to match the width of its parent view. This means that a true menu
bar (one that's a child of the window's top view) will always be as wide as
the window.

Two similar adjustments are made if the menu bar layout is
{cpp:enumerator}`B_ITEMS_IN_COLUMN`:

-   The width of the menu bar is adjusted to the width of the widest item.

-   If the {hparam}`resizingMode` includes
{cpp:enumerator}`B_FOLLOW_TOP_BOTTOM`, the height of the menu bar is
adjusted to match the height of its parent view.

After setting up the key menu bar and adding items to it, you may want to
set the minimum width of the window so that certain items won't be hidden
when the window is resized smaller.

Change the {hparam}`resizingMode`, the {hparam}`layout`, and the
{hparam}`resizeToFit` flag as needed for {hclass}`BMenuBar`s that are used
for a purpose other than to implement a true menu bar.

See also: the {cpp:class}`BMenu` {cpp:func}`constructor <BMenu::BMenu()>`,
{cpp:func}`BWindow::SetSizeLimits`
::::

::::{abi-group}
:::{cpp:function} virtual BMenuBar::~BMenuBar()
:::

Frees all the items and submenus in the entire menu hierarchy, and all
memory allocated by the {hclass}`BMenuBar`.
::::

## Hook Functions

::::{abi-group}
:::{cpp:function} virtual void BMenuBar::AttachedToWindow()
:::

Finishes the initialization of the {hclass}`BMenuBar` by setting up the
whole hierarchy of menus that it controls, and by making the
{cpp:class}`BWindow` to which it has become attached the target handler for
all items in the menu hierarchy, except for those items for which a target
has already been set.

This function also makes the {hclass}`BMenuBar` the key menu bar, the
{hclass}`BMenuBar` object whose menu hierarchy the user can navigate from
the keyboard. If a window contains more than one {hclass}`BMenuBar` in its
view hierarchy, the last one that's added to the window gets to keep this
designation. However, the key menu bar should always be the real menu bar
at the top of the window. It can be explicitly set with
{cpp:class}`BWindow`'s {cpp:func}`SetKeyMenuBar() <BWindow::SetKeyMenuBar>`
function.
::::

::::{abi-group}
:::{cpp:function} virtual void BMenuBar::Draw(BRect updateRect)
:::

Draws the menu—whether as a true menu bar, as some other kind of menu
list, or as a single item that controls a pop-up menu. This function is
called as the result of update messages; you don't need to call it
yourself.

See also: {cpp:func}`BView::Draw`
::::

::::{abi-group}
:::{cpp:function} virtual void BMenuBar::MouseDown(BPoint point)
:::

Initiates mouse tracking and keyboard navigation of the menu hierarchy.
This function is called to notify the {hclass}`BMenuBar` of a mouse-down
event.

See also: {cpp:func}`BView::MouseDown`
::::

## Member Functions

::::{abi-group}
:::{cpp:function} virtual status_t BMenuBar::Archive(BMessage* archive, bool deep = true) const
:::

Calls the inherited version of {cpp:func}`Archive() <BMenu::Archive>`
which serves to archive the {hclass}`BMenuBar`'s current state and, if the
{hparam}`deep` flag is {cpp:expr}`true`, all its menu items. This function
then adds the {hclass}`BMenuBar`'s border style to the
{cpp:class}`BMessage` archive.

See also: {cpp:func}`BArchivable::Archive`, {cpp:func}`BMenu::Archive`,
{cpp:func}`Instantiate() <BMenuBar::Instantiate>` static function
::::

::::{abi-group}
:::{cpp:function} virtual void BMenuBar::Hide()
:::

:::{cpp:function} virtual void BMenuBar::Show()
:::

These functions override their {cpp:class}`BMenu` counterparts to restore
the normal behavior for views when they're hidden and unhidden. When an
ordinary {cpp:class}`BMenu` is hidden, the window that displays it is also
removed from the screen. But it would be a mistake to remove the window
that displays a {hclass}`BMenuBar`. Hiding a {hclass}`BMenuBar` is like
hiding a typical view; only the view is hidden, not the window.

See also: {cpp:func}`BView::Hide`
::::

::::{abi-group}
:::{cpp:function} void BMenuBar::SetBorder(menu_bar_border border)
:::

:::{cpp:function} menu_bar_border BMenuBar::Border() const
:::

{hmethod}`SetBorder()` determines how the menu list is bordered. The
{hparam}`border` argument can be any of three values:

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
	- {cpp:enumerator}`B_BORDER_FRAME`
	- The border is drawn around the entire frame rectangle.
-
	- {cpp:enumerator}`B_BORDER_CONTENTS`
	- The border is drawn around just the list of items.
-
	- {cpp:enumerator}`B_BORDER_EACH_ITEM`
	- A border is drawn around each item.

:::

{hmethod}`Border()` returns the current setting. The default is
{cpp:enumerator}`B_BORDER_FRAME`.
::::

## Static Functions

::::{abi-group}
:::{cpp:function} static BArchivable* BMenuBar::Instantiate(BMessage* archive)
:::

Returns a new {hclass}`BMenuBar` object, allocated by new and created with
the version of the constructor that takes a {cpp:class}`BMessage` archive.
However, if the archive message doesn't contain data for a
{hclass}`BMenuBar` object, this function returns {cpp:expr}`NULL`.

See also: {cpp:func}`BArchivable::Instantiate`,
{cpp:func}`instantiate_object() <instantiate::object>`,
{cpp:func}`Archive() <BMenuBar::Archive>`
::::

## Archived Fields

The {cpp:func}`Archive() <BMenuBar::Archive>` function adds the following
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
	- {hparam}`_border`

	- {cpp:enumerator}`B_INT32_TYPE`

	- Menu bar border (exists only if not {cpp:enumerator}`B_BORDER_FRAME`)


:::
