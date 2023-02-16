:::{cpp:class} BPopUpMenu
:::

# BPopUpMenu

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BPopUpMenu::BPopUpMenu(const char* name, bool radioMode = true, bool labelFromMarked = true, menu_layout layout = B_ITEMS_IN_COLUMN)
:::

:::{cpp:function} BPopUpMenu::BPopUpMenu(BMessage* archive)
:::

Initializes the {hclass}`BPopUpMenu` object. If the object is added to a
{cpp:class}`BMenuBar`, its {hparam}`name` also becomes the initial label of
its controlling item (just as for other {cpp:class}`BMenu`s).

If the {hparam}`labelFromMarked` flag is {cpp:expr}`true` (as it is by
default), the label of the controlling item will change to reflect the
label of the item that the user last selected. In addition, the menu will
operate in radio mode (regardless of the value passed as the
{hparam}`radioMode` flag). When the menu pops up, it will position itself
so that the marked item appears directly over the controlling item in the
{cpp:class}`BMenuBar`.

If {hparam}`labelFromMarked` is {cpp:expr}`false`, the menu pops up so
that its first item is over the controlling item.

If the {hparam}`radioMode` flag is {cpp:expr}`true` (as it is by default),
the last item selected by the user will always be marked. In this mode, one
and only one item within the menu can be marked at a time. If
{hparam}`radioMode` is {cpp:expr}`false`, items aren't automatically marked
or unmarked.

However, the {hparam}`radioMode` flag has no effect unless the
{hparam}`labelFromMarked` flag is {cpp:expr}`false`. As long as
{hparam}`labelFromMarked` is {cpp:expr}`true`, radio mode will also be
{cpp:expr}`true`.

The layout of the items in a {hclass}`BPopUpMenu` can be either
{cpp:enumerator}`B_ITEMS_IN_ROW` or the default
{cpp:enumerator}`B_ITEMS_IN_COLUMN`. It should never be
{cpp:enumerator}`B_ITEMS_IN_MATRIX`. The menu is resized so that it exactly
fits the items that are added to it.

The new {hclass}`BPopUpMenu` is empty; you add items to it by calling
{cpp:class}`BMenu`'s {cpp:func}`AddItem() <BMenu::AddItem>` function.

See also: {cpp:func}`BMenu::SetRadioMode`,
{cpp:func}`BMenu::SetLabelFromMarked`
::::

::::{abi-group}
:::{cpp:function} virtual BPopUpMenu::~BPopUpMenu()
:::

Does nothing. The {cpp:class}`BMenu` destructor is sufficient to clean up
after a {hclass}`BPopUpMenu`.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} virtual status_t BPopUpMenu::Archive(BMessage* archive, bool deep = true) const
:::

Calls the inherited version of {cpp:func}`Archive() <BMenu::Archive>` and
stores the {hclass}`BPopUpMenu` in the {cpp:class}`BMessage` archive.

See also: {cpp:func}`BArchivable::Archive`, {cpp:func}`Instantiate()
<BPopUpMenu::Instantiate>` static function
::::

::::{abi-group}
:::{cpp:function} BMenuItem* BPopUpMenu::Go(BPoint screenPoint, bool deliversMessage = false, bool openAnyway = false, bool asynchronous = false)
:::

:::{cpp:function} BMenuItem* BPopUpMenu::Go(BPoint screenPoint, bool deliversMessage, bool openAnyway, BRect clickToOpenRect, bool asynchronous = false)
:::

Places the pop-up menu on-screen so that its left top corner is located at
{hparam}`screenPoint` in the screen coordinate system. If the
{hparam}`asynchronous` flag is {cpp:expr}`true`, {hmethod}`Go()` returns
right away; the return value is {cpp:expr}`NULL`. Otherwise, it doesn't
return until the user dismisses the menu from the screen. If the user
invoked an item in the menu, it returns a pointer to the item. If no item
was invoked, it returns {cpp:expr}`NULL`.

{hmethod}`Go()` is typically called from within the {cpp:func}`MouseDown()
<BView::MouseDown>` function of a {cpp:class}`BView`. For example:

:::{code} cpp
void MyView::MouseDown(BPoint point)
{
   BMenuItem* selected;
   BMessage* copy;
   . . .
   ConvertToScreen(&point);
   selected = myPopUp->Go(point);
   . . .
   if ( selected ) {
      BLooper *looper;
      BHandler *target = selected->Target(&looper);
      looper->PostMessage(selected->Message(), target);
   }
   . . .
}
:::

{hmethod}`Go()` operates in two modes:

-   If the {hparam}`deliversMessage` flag is {cpp:expr}`true`, the
{hclass}`BPopUpMenu` works just like a menu that's controlled by a
{cpp:class}`BMenuBar`. When the user invokes an item in the menu, the item
posts a message to its target.

-   If the {hparam}`deliversMessage` flag is {cpp:expr}`false`, a message is
not posted. Invoking an item doesn't automatically accomplish anything.
It's up to the application to look at the returned {cpp:class}`BMenuItem`
and decide what to do. It can mimic the behavior of other menus and post
the message—as shown in the example above—or it can take some other course
of action.

{hmethod}`Go()` always puts the pop-up menu on-screen, but ordinarily
keeps it there only as long as the user holds a mouse button down. When the
user releases the button, the menu is hidden and {hmethod}`Go()` returns.
However, the {hparam}`openAnyway` flag and the {hparam}`clickToOpenRect`
arguments can alter this behavior so that the menu will stay open even when
the user releases the mouse button (or even if a mouse button was never
down). It will take another user action—such as invoking an item in the
menu or clicking elsewhere—to dismiss the menu.

If the {hparam}`openAnyway` flag is {cpp:expr}`true`, {hmethod}`Go()`
keeps the menu on-screen even if no mouse buttons are held down. This
permits a user to open and operate a pop-up menu from the keyboard. If
{hparam}`openAnyway` is {cpp:expr}`false`, mouse actions determine whether
the menu stays on-screen.

If the user has the click-to-open menu preference turned on and releases
the mouse button while the cursor lies inside the {hparam}`clickToOpenRect`
rectangle, {hmethod}`Go()` interprets the action as clicking to open the
menu and keeps it on-screen. If the cursor is outside the rectangle when
the mouse button goes up, the menu is removed from the screen and
{hmethod}`Go()` returns. The rectangle should be stated in the screen
coordinate system.

Once {hmethod}`Go()` returns, your application should delete the
{hclass}`BPopUpMenu` object.

See also: {cpp:func}`BInvoker::SetMessage`
::::

::::{abi-group}
:::{cpp:function} virtual BPoint BPopUpMenu::ScreenLocation()
:::

Determines where the pop-up menu should appear on-screen (when it's being
run automatically, not by {hmethod}`Go()`). As explained in the description
of the class constructor, this largely depends on whether the label of the
superitem changes to reflect the item that's currently marked in the menu.
The point returned is stated in the screen coordinate system.

This function is called only for {hclass}`BPopUpMenu`s that have been
added to a menu hierarchy (a {cpp:class}`BMenuBar`). You should not call it
to determine the point to pass to {hmethod}`Go()`. However, you can
override it to change where a customized pop-up menu defined in a derived
class appears on-screen when it's controlled by a {cpp:class}`BMenuBar`.

See also: {cpp:func}`BMenu::SetLabelFromMarked`,
{cpp:func}`BMenu::ScreenLocation`, the {hclass}`BPopUpMenu` constructor
::::

::::{abi-group}
:::{cpp:function} void BPopUpMenu::SetAsyncAutoDestruct(bool state)
:::

:::{cpp:function} bool BPopUpMenu::AsyncAutoDestruct() const
:::

{hmethod}`SetAsyncAutoDestruct()` lets you specify whether you want
{hclass}`BPopUpMenu` to automatically delete its {cpp:class}`BMenu` when
the pop-up menu closes. If you want the {cpp:class}`BMenu` to be deleted,
specify {cpp:expr}`true` for {hparam}`state`.

{hmethod}`AsyncAutoDestruct()` returns the current state of the flag.
::::

## Static Functions

::::{abi-group}
:::{cpp:function} static BArchivable* BPopUpMenu::Instantiate(BMessage* archive)
:::

Returns a new {hclass}`BPopUpMenu` object, allocated by new and created
with the version of the constructor that takes a {cpp:class}`BMessage`
archive. However, if the archive message doesn't contain data for a
{hclass}`BPopUpMenu`, this function returns {cpp:expr}`NULL`.

See also: {cpp:func}`BArchivable::Instantiate`,
{cpp:func}`instantiate_object() <instantiate::object>`,
{cpp:func}`Archive() <BMenu::Archive>`
::::
