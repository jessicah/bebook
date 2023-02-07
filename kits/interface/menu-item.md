# BMenuItem
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BMenuItem::BMenuItem(const char* label, BMessage* message, char shortcut = 0, uint32 modifiers = 0)
:::
:::{cpp:function} BMenuItem::BMenuItem(BMenu* submenu, BMessage* message = NULL)
:::
:::{cpp:function} BMenuItem::BMenuItem(BMessage* archive)
:::

Creates a new {hclass}`BMenuItem` and sets its
{hparam}`label`, its invocation {hparam}`message`, both
of which can be {cpp:enum}`NULL`. When the user invokes the menu item,
{hparam}`message` is copied and the following fields

Whenever the user invokes the item, the model message is copied and the
copy is posted and marked for delivery to the target handler. Three
pieces of information are added to the copy before it's posted:

FieldType codeDescriptionwhenB_INT64_TYPEThe time the item was invoked, as measured by the number of microseconds since 12:00:00 AM January 1, 1970.sourceB_POINTER_TYPEA pointer to the BMenuItem object.indexB_INT32_TYPEThe index of the item, its ordinal position in the menu. Indices begin at 0.

By default, the target of the message is the window that the contains the
menu that the item is part of. Use
{cpp:func}`~BInvoker::SetTarget`
to set a different target.

The constructor can also set a keyboard {hparam}`shortcut` for the item. The
character that's passed as the {hparam}`shortcut` parameter will be displayed to
the right of the item's label. Upper case characters are mapped to lower
case characters; if you want the user to have to type an upper case
character, you must include {cpp:enum}`B_SHIFT_KEY` in the modifers mask.

The {hparam}`modifiers` mask determines which modifier keys the user must hold down
for the shortcut to work. The mask can be formed by combining any of the
modifiers constants, especially these:

- {cpp:enum}`B_SHIFT_KEY`
- {cpp:enum}`B_CONTROL_KEY`
- {cpp:enum}`B_OPTION_KEY`

{cpp:enum}`B_COMMAND_KEY` is required for all keyboard shortcuts; it doesn't have to
be explicitly included in the mask.

If the {hclass}`BMenuItem` is constructed to control a
{hparam}`submenu`, it can't take a
shortcut and it typically doesn't post messages—its role is to
bring up the submenu. However, it can be assigned a model {hparam}`message` if the
application must take some collateral action when the submenu is opened.
The item's initial label will be taken from the name of the submenu. It
can be changed after construction by calling
{cpp:func}`~BMenuItem::SetLabel`.

::::

::::{abi-group}

:::{cpp:function} virtual BMenuItem::~BMenuItem()
:::

Frees the item's label and its model
{cpp:class}`BMessage` object. If the item
controls a submenu, that menu and all its items are also freed. Deleting
a {hclass}`BMenuItem` destroys the entire menu hierarchy under that item.

::::

## Hook Functions
::::{abi-group}

:::{cpp:function} virtual void BMenuItem::Draw()
:::
:::{cpp:function} virtual void BMenuItem::DrawContent()
:::

These functions draw the menu item and highlight it if it's currently
selected. They're called by the {hmethod}`Draw()` function of the
{cpp:class}`BMenu` where the
item is located whenever the menu is required to display itself; they
don't need to be called from within application code.

However, they can both be overridden by derived classes that display
something other than a textual label. The {hmethod}`Draw()` function is called
first. It draws the background for the entire item, then calls
{hmethod}`DrawContent()` to draw the label within the item's content area. After
{hmethod}`DrawContent()` returns, it draws the check mark (if the item is currently
marked) and the keyboard shortcut (if any). It finishes by calling
{cpp:func}`~BMenuItem::Highlight`
if the item is currently selected.

Both functions draw by calling functions of the
{cpp:class}`BMenu` in which the item
is located. For example:

:::{code}
void MyItem::DrawContent()
{
   . . .
   Menu()->DrawBitmap(image);
   . . .
}
:::

A derived class can override either {hmethod}`Draw()`, if it needs to draw the
entire item, or {hmethod}`DrawContent()`, if it needs to draw only within the
content area. A {hmethod}`Draw()` function can find the frame rectangle it should
draw within by calling the {hclass}`BMenuItem`'s
{cpp:func}`~BMenuItem::Frame`
function; a {hmethod}`DrawContent()`
function can calculate the content area from the point returned by
{cpp:func}`~BMenuItem::ContentLocation`
and the dimensions provided by
{cpp:func}`~BMenuItem::GetContentSize`.

When {hmethod}`DrawContent()` is called, the pen is positioned to draw the item's
label and the high color is appropriately set. The high color may be a
shade of gray, if the item is disabled, or black if it's enabled. If some
other distinction is used to distinguish disabled from enabled items,
{hmethod}`DrawContent()` should check the item's current state by calling
{cpp:func}`~BMenuItem::IsEnabled`.

:::{admonition} Note
:class: note
If a derived class implements its own
{hmethod}`DrawContent()` function, but still wants to draw a
textual string, it should do so by assigning the string as the
{hclass}`BMenuItem`'s label and calling the inherited version
of {hmethod}`DrawContent()`, not by calling
{hmethod}`DrawString()`. This preserves the
{hclass}`BMenuItem`'s ability to display a trigger character
in the string.
:::
::::

## Member Functions
::::{abi-group}

:::{cpp:function} virtual status_t BMenuItem::Archive(BMessage* archive, bool deep = true) const
:::

Archives the {hclass}`BMenuItem` by
recording its current settings in the
{cpp:class}`BMessage`
{hparam}`archive`.

See also:
{cpp:func}`BArchivable::Archive`,
{cpp:func}`~BMenuItem::Instantiate` static function

::::

::::{abi-group}

:::{cpp:function} BPoint BMenuItem::ContentLocation() const
:::

Returns the left top corner of the content area of the item, in the
coordinate system of the {cpp:class}`BMenu`
to which it belongs. The content area of
an item is the area where it displays its label (or whatever graphic
substitutes for the label). It doesn't include the part of the item where
a check mark or a keyboard shortcut could be displayed, nor the border
and background around the content area.

You would need to call this function only if you're implementing a
{cpp:func}`~BMenuItem::DrawContent`
function to draw the contents of the menu item. The content
rectangle can be calculated from the point returned by this function and
the size specified by
{cpp:func}`~BMenuItem::GetContentSize`.

If the item isn't part of a menu, the return value is indeterminate.

::::

::::{abi-group}

:::{cpp:function} BRect BMenuItem::Frame() const
:::

Returns the rectangle that frames the entire menu item, in the coordinate
system of the {cpp:class}`BMenu`
to which the item belongs. If the item hasn't been
added to a menu, the return value is indeterminate.

See also:
{cpp:func}`BMenu::AddItem`

::::

::::{abi-group}

:::{cpp:function} virtual void BMenuItem::GetContentSize(float* width, float* height)
:::

Writes the size of the item's content area into the variables referred to
by {hparam}`width` and {hparam}`height`. The
content area of an item is the area where its
label (or whatever substitutes for the label) is drawn.

A {cpp:class}`BMenu` calls
{hmethod}`GetContentSize()` for each of its items as it arranges them
in a column or a row; the function is not called for items in a matrix.
The information it provides helps determine where each item is located
and the overall size of the menu.

{hmethod}`GetContentSize()` must report a size that's large enough to display the
content of the item (and separate one item from another). By default, it
reports an area just large enough to display the item's label. This area
is calculated from the label and the {cpp:class}`BMenu`'s current font.

If you design a class derived from {hclass}`BMenuItem` and implement your own
{cpp:func}`~BMenuItem::Draw` or
{cpp:func}`~BMenuItem::DrawContent`
function, you should also implement a
{hmethod}`GetContentSize()` function to report how much room will be needed to draw
the item's contents.

See also:
{cpp:func}`~BMenuItem::DrawContent`,
{cpp:func}`~BMenuItem::ContentLocation`

::::

::::{abi-group}

:::{cpp:function} virtual void BMenuItem::Highlight(bool flag)
:::

Highlights the menu item when {hparam}`flag` is {cpp:enum}`true`,
and removes the highlighting
when {hparam}`flag` is {cpp:enum}`false`. Highlighting
simply inverts all the colors in the
item's frame rectangle (except for the check mark).

This function is called by the
{cpp:func}`~BMenuItem::Draw` function whenever the item is
selected and needs to be drawn in its highlighted state. There's no
reason to call it yourself, unless you define your own version of
{cpp:func}`~BMenuItem::Draw`.
However, it can be reimplemented in a derived class, if items belonging
to that class need to be highlighted in some way other than simple
inversion.

::::

::::{abi-group}

:::{cpp:function} virtual status_t BMenuItem::Invoke(BMessage* message = NULL)
:::

Augments the {cpp:class}`BInvoker`
version of {cpp:func}`~BInvoker::Invoke`
to ensure that only enabled
menu items that are attached to a menu hierarchy can be invoked. This
function appropriately marks items when the user invokes them. Before
sending a message, it adds when,
source, and index
field to it, as
explained under the {hclass}`BMenuItem`
{cpp:func}`~BMenuItem::Constructor`.

::::

::::{abi-group}

:::{cpp:function} bool BMenuItem::IsSelected() const
:::

Returns {cpp:enum}`true` if the menu item is currently selected,
and {cpp:enum}`false` if not.
Selected items are highlighted.

::::

::::{abi-group}

:::{cpp:function} BMenu* BMenuItem::Menu() const
:::

Returns the menu where the item is located, or {cpp:enum}`NULL` if the item hasn't
yet been added to a menu.

See also:
{cpp:func}`BMenu::AddItem`

::::

::::{abi-group}

:::{cpp:function} virtual void BMenuItem::SetEnabled(bool enabled)
:::
:::{cpp:function} bool BMenuItem::IsEnabled() const
:::

{hmethod}`SetEnabled()` enables the {hclass}`BMenuItem`
if the {hparam}`enabled` flag is {cpp:enum}`true`, disables
it if {hparam}`enabled` is {cpp:enum}`false`, and
updates the item if it's visible on-screen.
If the item controls a submenu, this function calls the submenu's
{hmethod}`SetEnabled()` virtual function, passing it the same flag. This ensures
that the submenu is enabled or disabled as well.

{hmethod}`IsEnabled()` returns {cpp:enum}`true` if the
{hclass}`BMenuItem` is enabled, its menu is
enabled, and all menus above it in the hierarchy are enabled. It returns
{cpp:enum}`false` if the item is disabled or any objects above it in the menu
hierarchy are disabled.

Items and menus are enabled by default.

When using these functions, keep in mind that:

- Disabling a {hclass}`BMenuItem` that controls a submenu serves to disable the entire menu hierarchy under the item.
- Passing an argument of {cpp:enum}`true` to {hmethod}`SetEnabled()` is not sufficient to enable the item if it's located in a disabled branch of the menu hierarchy. It can only undo a previous {hmethod}`SetEnabled()` call (with an argument of {cpp:enum}`false`) on the same item.

See also:
{cpp:func}`BMenu::SetEnabled`

::::

::::{abi-group}

:::{cpp:function} virtual void BMenuItem::SetLabel(const char* string)
:::
:::{cpp:function} const char* BMenuItem::Label() const
:::

{hmethod}`SetLabel()` frees the item's current label
and copies {hparam}`string` to replace
it. If the menu is visible on-screen, it will be redisplayed with the
item's new label. If necessary, the menu will become wider (or narrower)
so that it fits the new label.

The Interface Kit calls this virtual function to:

- Set the initial label of an item that controls a submenu to the name of the submenu, and
- Subsequently set the item's label to match the marked item in the submenu, if the submenu was set up to have this feature.

{hmethod}`Label()` returns a pointer to the current label.

See also:
{cpp:func}`BMenu::SetLabelFromMarked`,
the {hclass}`BMenuItem` {cpp:func}`~BMenuItem::Constructor`

::::

::::{abi-group}

:::{cpp:function} virtual void BMenuItem::SetMarked(bool flag)
:::
:::{cpp:function} bool BMenuItem::IsMarked() const
:::

{hmethod}`SetMarked()` adds a check mark to the left of
the item label if {hparam}`flag` is
{cpp:enum}`true`, or removes an existing mark if
{hparam}`flag` is {cpp:enum}`false`. If the menu is
visible on-screen. it's redisplayed with or without the mark.

{hmethod}`IsMarked()` returns whether the item is currently marked.

See also:
{cpp:func}`BMenu::SetLabelFromMarked`,
{cpp:func}`BMenu::FindMarked`

::::

::::{abi-group}

:::{cpp:function} virtual void BMenuItem::SetShortcut(char shortcut, uint32 modifiers)
:::
:::{cpp:function} char BMenuItem::Shortcut(uint32* modifiers = NULL) const
:::

{hmethod}`SetShortcut()` sets the {hparam}`shortcut`
character that's displayed at the right
edge of the menu item and the set of {hparam}`modifiers` that are associated with
the character. These two arguments work just like the arguments passed to
the {hclass}`BMenuItem` constructor. See
{cpp:func}`~BMenuItem::Overview` for a more complete
description.

{hmethod}`Shortcut()` returns the character that's used as the keyboard shortcut for
invoking the item, and writes a mask of all the modifier keys the
shortcut requires to the variable referred to by {hparam}`modifiers`. Since the
Command key is required to operate the keyboard shortcut for any menu
item, {cpp:enum}`B_COMMAND_KEY` will always be part of the {hparam}`modifiers` mask. The mask
can also be tested against the {cpp:enum}`B_CONTROL_KEY`, {cpp:enum}`B_OPTION_KEY`, and
{cpp:enum}`B_SHIFT_KEY` constants.

The shortcut is initially set by the
{hclass}`BMenuItem` {cpp:func}`~BMenuItem::Constructor`.

::::

::::{abi-group}

:::{cpp:function} virtual void BMenuItem::SetTrigger(char trigger)
:::
:::{cpp:function} char BMenuItem::Trigger() const
:::

{hmethod}`SetTrigger()` sets the {hparam}`trigger`
character that the user can type to invoke
the item while the item's menu is open on-screen. If a
{hparam}`trigger` is not
set, the Interface Kit will select one for the item, so it's not
necessary to call {hmethod}`SetTrigger()`.

The character passed to this function has to match a character displayed
in the item—either the keyboard shortcut or a character in the
label. The case of the character doesn't matter; lowercase arguments will
match uppercase characters in the item and uppercase arguments will match
lowercase characters. When the item can be invoked by its trigger, the
trigger character is underlined.

If more than one character in the item matches the character passed,
{hmethod}`SetTrigger()` tries first to mark the keyboard shortcut. Failing that, it
tries to mark an uppercase letter at the beginning of a word. Failing
that, it marks the first instance of the character in the label.

If the {hparam}`trigger` doesn't match any characters in the item, the item won't
have a trigger, not even one selected by the system.

{hmethod}`Trigger()` returns the character set by
{hmethod}`SetTrigger()`, or {cpp:enum}`NULL` if
{hmethod}`SetTrigger()` didn't succeed or if
{hmethod}`SetTrigger()` was never called and the
trigger is selected automatically.

See also:
{cpp:func}`BMenu::SetTriggersEnabled`

::::

::::{abi-group}

:::{cpp:function} BMenu* BMenuItem::Submenu() const
:::

Returns the {cpp:class}`BMenu`
object that the item controls, or {cpp:enum}`NULL` if the item
doesn't control a submenu.

See also:
the {hclass}`BMenuItem` {cpp:func}`~BMenuItem::Constructor`,
the {cpp:class}`BMenu` class

::::

::::{abi-group}

:::{cpp:function} virtual void BMenuItem::TruncateLabel(float maxWidth, char* newLabel)
:::

Removes characters from the middle of the item label and replaces them
with an ellipsis. This is done so that the label will fit within {hparam}`maxWidth`
coordinate units. The shortened string is copied into the {hparam}`newLabel` buffer.

This function is called by the {hclass}`BMenuItem` when it draws the item's label,
but only if it's necessary to fit a long item into a smaller space. It
can be reimplemented by derived classes to do a better job of shortening
the string based on the actual content of the label.

Your version of {hmethod}`TruncateLabel()` should be careful to not cut the trigger
character from the string.

See also:
{cpp:func}`BFont::GetTruncatedStrings`

::::

## Static Functions
::::{abi-group}

:::{cpp:function} static BArchivable* BMenuItem::Instantiate(BMessage* archive)
:::

Returns a new {hclass}`BMenuItem` object, allocated by new and created with the
version of the constructor that takes a {cpp:class}`BMessage`
archive. However, if the
archive message doesn't contain data for a {hclass}`BMenuItem` object, this
function returns {cpp:enum}`NULL`.

See also:
{cpp:func}`BArchivable::Instantiate`,
{cpp:func}`~instantiate::object`,
{cpp:func}`~BMenuItem::Archive`

::::

## Archived Fields