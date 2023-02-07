# BMenu
## Constructor and Destructor
::::{abi-group}




:::{cpp:function} BMenu::BMenu(const char* name, menu_layout layout = B_ITEMS_IN_COLUMN)
:::
:::{cpp:function} BMenu::BMenu(const char* name, float width, float height)
:::
:::{cpp:function} BMenu::BMenu(BMessage* archive)
:::
:::{cpp:function} protected BMenu::BMenu(BRect frame, const char* name, uint32 resizingMode, uint32 flags, menu_layout layout, bool resizeToFit)
:::

Initializes the {hclass}`BMenu` object. The name of the object becomes the initial
label of the supermenu item that controls the menu and brings it to the
screen. (It's also the name that can be passed to
{cpp:class}`BView`'s
{cpp:func}`~BView::FindView`
function.)

A new {hclass}`BMenu` object doesn't contain any items; you need to call
{cpp:func}`~BMenu::AddItem`
to set up its contents.

A menu can arrange its items in any of three ways:

:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_ITEMS_IN_COLUMN`
	- The items are stacked vertically in a column, one on top of the other, as in a typical menu.
-
	- {cpp:enum}`B_ITEMS_IN_ROW`
	- The items are laid out horizontally in a row, from end to end, as in a typical menu bar.
-
	- {cpp:enum}`B_ITEMS_IN_MATRIX`
	- The items are arranged in a custom fashion, such as a matrix.
:::

Either {cpp:enum}`B_ITEMS_IN_ROW` or the default {cpp:enum}`B_ITEMS_IN_COLUMN` can be passed as
the layout argument to the public constructor. (A column is the default
for ordinary menus; a row is the default for
{cpp:class}`BMenuBar`s.) This version of
the constructor isn't designed for {cpp:enum}`B_ITEMS_IN_MATRIX` layouts.

A {hclass}`BMenu` object can arrange items that are laid out in a column or a row
entirely on its own. The menu will be resized to exactly fit the items
that are added to it.

However, when items are laid out in a custom matrix, the menu needs more
help. First, the constructor must be informed of the exact width and
height of the menu rectangle. The version of the constructor that takes
these two parameters is designed just for matrix menus—it sets the
layout to {cpp:enum}`B_ITEMS_IN_MATRIX`. Then, when items are added to the menu, the
{hclass}`BMenu` object expects to be informed of their precise positions within the
specified area. The menu is not resized to fit the items that are added.
Finally, when items in the matrix change, you must take care of any
required adjustments in the layout yourself.

The protected version of the constructor is supplied for derived classes
that don't simply devise different sorts of menu items or arrange them in
a different way, but invent a different kind of menu. If the
{hparam}`resizeToFit` flag is
{cpp:enum}`true`, it's expected that the layout will be
{cpp:enum}`B_ITEMS_IN_COLUMN` or
{cpp:enum}`B_ITEMS_IN_ROW`. The menu will resize itself to fit
the items that are added to it. If the layout is
{cpp:enum}`B_ITEMS_IN_MATRIX`, the
{hparam}`resizeToFit` flag should be
{cpp:enum}`false`. 
::::

::::{abi-group}

:::{cpp:function} virtual BMenu::~BMenu()
:::

Deletes all the items that were added to the menu and frees all memory
allocated by the {hclass}`BMenu` object. Deleting the items serves also to delete
any submenus those items control and, thus, the whole branch of the menu
hierarchy.

::::

## Hook Functions
::::{abi-group}

:::{cpp:function} virtual void BMenu::AttachedToWindow()
:::

Finishes initializing the {hclass}`BMenu` object by laying out its items and
resizing the {hclass}`BMenu` view to fit. This function is called for you each time
the {hclass}`BMenu` is assigned to a window. For a submenu, that means each time
the menu is shown on-screen.

See also:
{cpp:func}`BView::AttachedToWindow`

::::

::::{abi-group}

:::{cpp:function} virtual void BMenu::Draw(BRect updateRect)
:::

Draws the menu. This function is called for you whenever the menu is
placed on-screen or is updated while on-screen. It's not a function you
need to call yourself.

See also:
{cpp:func}`BView::Draw`

::::

::::{abi-group}

:::{cpp:function} virtual void BMenu::KeyDown(const char* bytes, int32 numBytes)
:::

Handles keyboard navigation through the menu. This function is called to
respond to messages reporting key-down events. It should not be called
from application code.

See also:
{cpp:func}`BView::KeyDown`

::::

## Member Functions
::::{abi-group}

:::{cpp:function} bool BMenu::AddItem(BMenuItem* item)
:::
:::{cpp:function} bool BMenu::AddItem(BMenuItem* item, int32 index)
:::
:::{cpp:function} bool BMenu::AddItem(BMenuItem* item, BRect frame)
:::
:::{cpp:function} bool BMenu::AddItem(BMenu* submenu)
:::
:::{cpp:function} bool BMenu::AddItem(BMenu* submenu, int32 index)
:::
:::{cpp:function} bool BMenu::AddItem(BMenu* submenu, BRect frame)
:::

Adds an item to the menu list at {hparam}`index`—or, if no index is
mentioned, to the end of the list. If items are arranged in a matrix
rather than a list, it's necessary to specify the item's {hparam}`frame`
rectangle—the exact position where it should be located in the menu
view. Assume a coordinate system for the menu that has the origin, (0.0,
0.0), at the left top corner of the view rectangle. The rectangle will
have the width and height that were specified when the menu was
constructed.

The versions of this function that take an {hparam}`index` (even an implicit one)
can be used only if the menu arranges items in a column or row
({cpp:enum}`B_ITEMS_IN_COLUMN` or {cpp:enum}`B_ITEMS_IN_ROW`); it's an error to use them for
items arranged in a matrix. Conversely, the versions of this function
that take a frame rectangle can be used only if the menu arranges items
in a matrix ({cpp:enum}`B_ITEMS_IN_MATRIX`); it's an error to use them for items
arranged in a list.

If a {hparam}`submenu` is specified rather than an {hparam}`item`,
{hmethod}`AddItem()` constructs a
controlling {cpp:class}`BMenuItem` for the
submenu and adds the item to the menu.

If it's unable to add the item to the menu—for example, if the
index is out-of-range or the wrong version of the function has been
called—{hmethod}`AddItem()` returns {cpp:enum}`false`. If successful, it returns {cpp:enum}`true`.

See also:
the {hclass}`BMenu` constructor,
the {cpp:class}`BMenuItem` class,
{cpp:func}`~BMenu::RemoveItem`

::::

::::{abi-group}

:::{cpp:function} bool BMenu::AddSeparatorItem()
:::

Creates an instance of the
{cpp:class}`BSeparatorItem`
class and adds it to the end of the menu list, returning
{cpp:enum}`true` if successful and {cpp:enum}`false` if not (a very
unlikely possibility). This function is a shorthand for:

:::{code}
BSeparatorItem* separator = new BSeparatorItem;
AddItem(separator);
:::

A separator serves only to separate other items in the list. It counts as
an item and has an indexed position in the list, but it doesn't do
anything. It's drawn as a horizontal line across the menu. Therefore,
it's appropriately added only to menus where the items are laid out in a
column.

See also:
{cpp:func}`~BMenu::AddItem`

::::

::::{abi-group}

:::{cpp:function} virtual status_t BMenu::Archive(BMessage* archive, bool deep = true) const
:::

Calls the inherited version of {cpp:func}`~BView::Archive`,
then archives the {hclass}`BMenu` by
recording its layout and all current settings in the
{cpp:class}`BMessage` {hparam}`archive`. If
the {hparam}`deep` flag is {cpp:enum}`true`, all of the menu items are also archived.

See also:
{cpp:func}`BArchivable::Archive`,
{cpp:func}`~BMenu::Instantiate` static function

::::

::::{abi-group}

:::{cpp:function} int32 BMenu::CountItems() const
:::

Returns the total number of items in the menu, including separator items.

::::

::::{abi-group}

:::{cpp:function} BMenuItem* BMenu::FindItem(const char* label) const
:::
:::{cpp:function} BMenuItem* BMenu::FindItem(uint32 command) const
:::

Returns the item with the specified {hparam}`label`—or the one that sends a
message with the specified {hparam}`command`. If there's more than one item in the
menu hierarchy with that particular {hparam}`label` or associated with that
particular {hparam}`command`, this function returns the first one it finds. It
recursively searches the menu by working down the list of items in order.
If an item controls a submenu, it searches the submenu before returning
to check any remaining items in the menu.

If none of the items in the menu hierarchy meet the stated criterion,
{hmethod}`FindItem()` returns {cpp:enum}`NULL`.

::::

::::{abi-group}

:::{cpp:function} BMenuItem* BMenu::FindMarked()
:::

Returns the first marked item in the menu list (the one with the lowest
index), or {cpp:enum}`NULL` if no item is marked.

See also:
{cpp:func}`~BMenu::SetRadioMode`,
{cpp:func}`BMenuItem::SetMarked`

::::

::::{abi-group}

:::{cpp:function} void BMenu::Hide()
:::
:::{cpp:function} void BMenu::Show(bool selectFirst)
:::
:::{cpp:function} virtual void BMenu::Show()
:::

These functions hide the menu (remove the {hclass}`BMenu` view from the window it's
in and remove the window from the screen) and show it (attach the {hclass}`BMenu`
to a window and place the window on-screen). If the {hparam}`selectFirst` flag
passed to {hmethod}`Show()` is {cpp:enum}`true`, the first item in the menu will be selected
when it's shown. If {hparam}`selectFirst` is {cpp:enum}`false`, the menu is shown without a
selected item.

The version of {hmethod}`Show()` that doesn't take an argument simply calls the
version that does and passes it a {hparam}`selectFirst` value of {cpp:enum}`false`.

These functions are not ones that you'd ordinarily call, even when
implementing a derived class. You'd need them only if you're implementing
a nonstandard menu of some kind and want to control when the menu appears
on-screen.

See also:
{cpp:func}`BView::Show`,
{cpp:func}`~BMenu::Track`

::::

::::{abi-group}

:::{cpp:function} int32 BMenu::IndexOf(BMenuItem* item) const
:::
:::{cpp:function} int32 BMenu::IndexOf(BMenu* submenu) const
:::

Returns the index of the specified menu {hparam}`item`—or the item that
controls the specified {hparam}`submenu`. Indices record the position of the item
in the menu list. They begin at 0 for the item at the top of a column or
at the left of a row and include separator items.

If the menu doesn't contain the specified {hparam}`item`, or the item that controls
{hparam}`submenu`, the return value will be {cpp:enum}`B_ERROR`.

See also:
{cpp:func}`~BMenu::AddItem`

::::

::::{abi-group}

:::{cpp:function} void BMenu::InvalidateLayout()
:::

Forces the {hclass}`BMenu` to recalculate the layout of all menu items and,
consequently, its own size. It can do this only if the items are arranged
in a row or a column. If the items are arranged in a matrix, it's up to
you to keep their layout up-to-date.

All {hclass}`BMenu` and
{cpp:class}`BMenuItem`
functions that change an item in a way that might
affect the overall menu automatically invalidate the menu's layout so it
will be recalculated. For example, changing the label of an item might
cause the menu to become wider (if it needs more room to accommodate the
longer label) or narrower (if it no longer needs as much room as before).

Therefore, you don't need to call {hmethod}`InvalidateLayout()` after using a kit
function to change a menu or menu item; it's called for you. You'd call
it only when making some other change to a menu.

See also: the {hclass}`BMenu`
{cpp:func}`~BMenu::Constructor`

::::

::::{abi-group}

:::{cpp:function} BMenuItem* BMenu::ItemAt(int32 index) const
:::
:::{cpp:function} BMenu* BMenu::SubmenuAt(int32 index) const
:::

These functions return the item at {hparam}`index`—or the submenu controlled
by the item at {hparam}`index`. If there's no item at the index,
they return {cpp:enum}`NULL`.
{hmethod}`SubmenuAt()` is a shorthand for:

:::{code}
ItemAt(index)->Submenu()
:::

It returns {cpp:enum}`NULL` if the item at {hparam}`index`
doesn't control a submenu.

See also:
{cpp:func}`~BMenu::AddItem`

::::

::::{abi-group}

:::{cpp:function} menu_layout BMenu::Layout() const
:::

Returns {cpp:enum}`B_ITEMS_IN_COLUMN` if the items in the menu are stacked in a
column from top to bottom, {cpp:enum}`B_ITEMS_IN_ROW` if they're stretched out in a
row from left to right, or {cpp:enum}`B_ITEMS_IN_MATRIX` if they're arranged in some
custom fashion. By default {hclass}`BMenu` items are arranged in a column and
{cpp:class}`BMenuBar` items in a row.

The layout is established by the constructor.

See also:
The {hclass}`BMenu` {cpp:func}`~BMenu::Constructor` and
{cpp:class}`BMenuBar` {cpp:func}`~BMenuBar::Constructor`.

::::

::::{abi-group}

:::{cpp:function} BMenuItem* BMenu::RemoveItem(int32 index)
:::
:::{cpp:function} bool BMenu::RemoveItem(BMenuItem* item)
:::
:::{cpp:function} bool BMenu::RemoveItem(BMenu* submenu)
:::

Removes the item at {hparam}`index`, or the specified {hparam}`item`, or the item that
controls the specified {hparam}`submenu`. Removing the item doesn't free it.

- If passed an {hparam}`index`, this function returns a pointer to the item so you can free it. It returns a {cpp:enum}`NULL` pointer if the item couldn't be removed (for example, if the {hparam}`index` is out-of-range).
- If passed an {hparam}`item`, it returns {cpp:enum}`true` if the item was in the list and could be removed, and {cpp:enum}`false` if not.
- If passed a {hparam}`submenu`, it returns {cpp:enum}`true` if the submenu is controlled by an item in the menu and that item could be removed, and {cpp:enum}`false` otherwise.

When an item is removed from a menu, it loses its target; the cached
value is set to {cpp:enum}`NULL`. If the item controls a submenu, it remains attached
to the submenu even after being removed.

See also:
{cpp:func}`~BMenu::AddItem`

::::

::::{abi-group}

:::{cpp:function} virtual BPoint BMenu::ScreenLocation()
:::

Returns the point where the left top corner of the menu should appear
when the menu is shown on-screen. The point is specified in the screen
coordinate system.

This function is called each time a hidden menu (a submenu of another
menu) is brought to the screen. It can be overridden in a derived class
to change where the menu appears. For example, the
{cpp:class}`BPopUpMenu` class
overrides it so that a pop-up menu pops up over the controlling item.

::::

::::{abi-group}

:::{cpp:function} virtual void BMenu::SetEnabled(bool enabled)
:::
:::{cpp:function} bool BMenu::IsEnabled() const
:::

{hmethod}`SetEnabled()` enables the {hclass}`BMenu`
if the {hparam}`enabled` flag is {cpp:enum}`true`, and disables
it if {hparam}`enabled` is {cpp:enum}`false`. If the menu is a submenu, this enables or
disables its controlling item, just as if {hmethod}`SetEnabled()` were called for
that item. The controlling item is updated so that it displays its new
state, if it happens to be visible on-screen.

Disabling a menu disables its entire branch of the menu hierarchy. All
items in the menu, including those that control other menus, are disabled.

{hmethod}`IsEnabled()` returns {cpp:enum}`true` if
the {hclass}`BMenu`, and every {hclass}`BMenu` above it in the
menu hierarchy, is enabled. It returns {cpp:enum}`false` if the
{hclass}`BMenu`, or any {hclass}`BMenu`
above it in the menu hierarchy, is disabled.

See also:
{cpp:func}`BMenuItem::SetEnabled`

::::

::::{abi-group}

:::{cpp:function} void BMenu::SetItemMargins(float left, float top, float right, float bottom)
:::
:::{cpp:function} void BMenu::GetItemMargins(float* left, float* top, float* right, float* bottom)
:::

These functions set and get the margins around each item in the {hclass}`BMenu`.
For the purposes of this function, you should assume that all items are
enclosed in a rectangle of the same size, one big enough for the largest
item. Keyboard shortcuts are displayed in the right margin and check
marks in the left.

See also:
{cpp:func}`~BMenu::SetMaxContentWidth`

::::

::::{abi-group}

:::{cpp:function} void BMenu::SetLabelFromMarked(bool flag)
:::
:::{cpp:function} bool BMenu::IsLabelFromMarked()
:::

{hmethod}`SetLabelFromMarked()` determines whether the label of the item that
controls the menu (the label of the superitem) should be taken from the
currently marked item within the menu. If {hparam}`flag` is {cpp:enum}`true`, the menu is
placed in radio mode and the superitem's label is reset each time the
user selects a different item. If {hparam}`flag` is {cpp:enum}`false`, the setting for radio
mode doesn't change and the label of the superitem isn't automatically
reset.

{hmethod}`IsLabelFromMarked()` returns whether the superitem's label is taken from
the marked item (but not necessarily whether the {hclass}`BMenu` is in radio mode).

See also:
{cpp:func}`~BMenu::SetRadioMode`

::::

::::{abi-group}

:::{cpp:function} virtual void BMenu::SetMaxContentWidth(float width)
:::
:::{cpp:function} float BMenu::MaxContentWidth() const
:::

These functions set and return the maximum width of an item's content
area. The content area is where the item label is drawn; it excludes the
margin on the left where a check mark might be placed and the margin on
the right where a shortcut character or a submenu symbol might appear.
The content area is the same size for all items in the menu.

Normally, a menu will be wide enough to accommodate its longest item.
However, items wider than the maximum set by {hmethod}`SetMaxContentWidth()` are
truncated to fit.

See also:
{cpp:func}`~BMenu::SetItemMargins`,
{cpp:func}`BMenuItem::TruncateLabel`

::::

::::{abi-group}

:::{cpp:function} virtual void BMenu::SetRadioMode(bool flag)
:::
:::{cpp:function} bool BMenu::IsRadioMode()
:::

{hmethod}`SetRadioMode()` puts the {hclass}`BMenu`
in radio mode if {hparam}`flag` is {cpp:enum}`true` and takes it
out of radio mode if {hparam}`flag` is {cpp:enum}`false`.
In radio mode, only one item in the
menu can be marked at a time. If the user selects an item, a check mark
is placed in front of it automatically (you don't need to call
{cpp:class}`BMenuItem`'s
{cpp:func}`~BMenuItem::SetMarked`
function; it's called for you). If another item
was marked at the time, its mark is removed. Selecting a currently marked
item retains the mark.

{hmethod}`IsRadioMode()` returns whether the
{hclass}`BMenu` is currently in radio mode. The
default radio mode is {cpp:enum}`false` for ordinary
{hclass}`BMenu`s, but {cpp:enum}`true` for
{cpp:class}`BPopUpMenu`s.

{hmethod}`SetRadioMode()` doesn't change any of the items in the menu. If you want
an initial item to be marked when the menu is put into radio mode, you
must mark it yourself.

When {hmethod}`SetRadioMode()` turns radio mode off, it calls SetLabelFromMarked()
and passes it an argument of {cpp:enum}`false`—turning off the feature that
changes the label of the menu's superitem each time the marked item
changes. Similarly, when
{cpp:func}`~BMenu::SetLabelFromMarked`
turns on this feature, it calls {hmethod}`SetRadioMode()` and
passes it an argument of {cpp:enum}`true`—turning
radio mode on.

::::

::::{abi-group}

:::{cpp:function} virtual status_t BMenu::SetTargetForItems(BHandler* handler)
:::
:::{cpp:function} virtual status_t BMenu::SetTargetForItems(BMessenger messenger)
:::

Assigns {hparam}`handler` or {hparam}`messenger`
as the target for all the items in the menu.
The proposed target is subject to the restrictions imposed by the
{hmethod}`SetTarget()` function that
{cpp:class}`BMenuItem` inherits from
{cpp:class}`BInvoker` in the
Application Kit. See that function for further information.

If it's unable to set the target of any item, {hmethod}`SetTargetForItems()` aborts
and returns the error it encountered. If successful in setting the target
of all items, it returns {cpp:enum}`B_OK`.

This function doesn't work recursively (it doesn't descend into
submenus), and it only acts on items that are currently in the {hclass}`BMenu` (it
doesn't affect items that are added later).

::::

::::{abi-group}

:::{cpp:function} virtual void BMenu::SetTriggersEnabled(bool flag)
:::
:::{cpp:function} bool BMenu::AreTriggersEnabled() const
:::

{hmethod}`SetTriggersEnabled()` enables the triggers for all items in the menu if
{hparam}`flag` is {cpp:enum}`true` and disables them if
{hparam}`flag` is {cpp:enum}`false`.
{hmethod}`AreTriggersEnabled()`
returns whether the triggers are currently enabled or disabled. They're
enabled by default.

Triggers are displayed to the user only if they're enabled, and only when
keyboard actions can operate the menu.

Triggers are appropriate for some menus, but not for others.
{hmethod}`SetTriggersEnabled()` is typically called to
initialize the {hclass}`BMenu` when
it's constructed, not to enable and disable triggers as the application
is running. If triggers are ever enabled for a menu, they should always
be enabled; if they're ever disabled, they should always be disabled.

See also:
{cpp:func}`BMenuItem::SetTrigger`

::::

::::{abi-group}

:::{cpp:function} BMenuItem* BMenu::Superitem() const
:::
:::{cpp:function} BMenu * BMenu::Supermenu() const
:::

These functions return the supermenu item that controls the {hclass}`BMenu` and the
supermenu where that item is located. The supermenu could be a
{cpp:class}`BMenuBar`
object. If the {hclass}`BMenu` hasn't been made the submenu of another menu, both
functions return {cpp:enum}`NULL`.

See also:
{cpp:func}`~BMenu::AddItem`

::::

::::{abi-group}

:::{cpp:function} BMenuItem* BMenu::Track(bool openAnyway = false, BRect* clickToOpenRect = NULL)
:::

Initiates tracking of the cursor within the menu. This function passes
tracking control to submenus (and submenus of submenus) depending on
where the user moves the mouse. If the user ends tracking by invoking an
item, {hmethod}`Track()` returns the item. If the user didn't invoke any item, it
returns {cpp:enum}`NULL`. The item doesn't have to be located in
the {hclass}`BMenu`; it could,
for example, belong to a submenu of the {hclass}`BMenu`.

If the {hparam}`openAnyway` flag is {cpp:enum}`true`,
{hmethod}`Track()` opens the menu and leaves it open
even though a mouse button isn't held down. This enables menu navigation
from the keyboard. If a {hparam}`clickToOpenRect` is specified and the user has set
the click-to-open preference, {hmethod}`Track()` will leave the menu open if the
user releases the mouse button while the cursor is inside the rectangle.
The rectangle should be stated in the screen coordinate system.

{hmethod}`Track()` is called by the {hclass}`BMenu` to initiate tracking in the menu
hierarchy. You would need to call it yourself only if you're implementing
a different kind of menu that starts to track the cursor under
nonstandard circumstances.

::::

## Static Functions
::::{abi-group}

:::{cpp:function} static BArchivable* BMenu::Instantiate(BMessage* archive)
:::

Returns a new {hclass}`BMenu` object, allocated by new and created with the version
of the constructor that takes a {cpp:class}`BMessage`
archive. However, if the {hparam}`archive`
message doesn't contain data for a {hclass}`BMenu` object,
{hmethod}`Instantiate()` returns {cpp:enum}`NULL`.

See also:
{cpp:func}`BArchivable::Instantiate`,
{cpp:func}`~instantiate::object`,
{cpp:func}`~BMenu::Archive`

::::

## Scripting Support
::::{abi-group}

The "Enabled" property reflects whether the menu or menu item is enabled
or disabled.

MessageSpecifiersDescriptionB_GET_PROPERTYB_DIRECT_SPECIFIERReturns true if menu or menu item is enabled; false otherwise.B_SET_PROPERTYB_DIRECT_SPECIFIEREnables or disables menu or menu item.
::::

::::{abi-group}

The "Label" property refers to the text label of a menu or menu item.

MessageSpecifiersDescriptionB_GET_PROPERTYB_DIRECT_SPECIFIERReturns the string label of the menu or menu item.B_SET_PROPERTYB_DIRECT_SPECIFIERSets the string label of the menu or menu item.
::::

::::{abi-group}

The "Mark" property refers to whether or not a given menu item or a given
menu's superitem is marked.

MessageSpecifiersDescriptionB_GET_PROPERTYB_DIRECT_SPECIFIERReturns true if the menu item or the menu's superitem is marked; false otherwise.B_SET_PROPERTYB_DIRECT_SPECIFIERMarks or unmarks the menu item or the menu's superitem.
::::

::::{abi-group}

The "Menu" property refers to individual {hclass}`BMenu`s in the menu.

MessageSpecifiersDescriptionB_CREATE_PROPERTYB_NAME_SPECIFIER, B_INDEX_SPECIFIER, B_REVERSE_INDEX_SPECIFIERAdds a new menu item at the specified index with the text label found in "data" and the int32 command found in "what" (used as the what field in the BMessage sent by the item).B_DELETE_PROPERTYB_NAME_SPECIFIER, B_INDEX_SPECIFIER, B_REVERSE_INDEX_SPECIFIERRemoves the selected menu or menus.any otherB_NAME_SPECIFIER, B_INDEX_SPECIFIER, B_REVERSE_INDEX_SPECIFIERDirects scripting message to the specified menu, first popping the current specifier off the stack.
::::

::::{abi-group}

The "MenuItem" property refers to individual {hclass}`BMenu`Items in the menu.

MessageSpecifiersDescriptionB_COUNT_PROPERTIESB_DIRECT_SPECIFIERCounts the number of menu items in the specified menu.B_CREATE_PROPERTYB_NAME_SPECIFIER, B_INDEX_SPECIFIER, B_REVERSE_INDEX_SPECIFIERAdds a new menu item at the specified index with the text label found in "data" and the int32 command found in "what" (used as the what field in the BMessage sent by the item).B_DELETE_PROPERTYB_NAME_SPECIFIER, B_INDEX_SPECIFIER, B_REVERSE_INDEX_SPECIFIERRemoves the specified menu item from its parent menu.B_EXECUTE_PROPERTYB_NAME_SPECIFIER, B_INDEX_SPECIFIER, B_REVERSE_INDEX_SPECIFIERInvokes the specified menu item.any otherB_NAME_SPECIFIER, B_INDEX_SPECIFIER, B_REVERSE_INDEX_SPECIFIERDirects scripting message to the specified menu, first popping the current specifier off the stack.
::::

## Archived Fields