# BView

A {cpp:class}`BView` object represents a rectangular area within a window.
The object draws within this rectangle and responds to user events (mouse
clicks, key presses) that are directed at the window.

Most of the other classes in the Interface Kit inherit from
{cpp:class}`BView`. You can use these objects off-the-shelf, but for most
applications, you'll also need to create some {cpp:class}`BView`
subclasses, and create instances of these subclasses.

The {cpp:class}`BView` class is one of the largest in the BeOS class
library. Because of this, the {cpp:class}`BView` documentation is split
across a number of files:

-   {cpp:func}`BView General Functions <BView::General>` describes those
functions that you use no matter what you're doing with your
{cpp:class}`BView` object.

-   {cpp:func}`BView Drawing-Related Functions <BView::Drawing>`: Anything
related to drawing subdivided into Primitive Drawing Functions (to draw
lines, circles, polygons, etc.) and Other Drawing Functions (such as
picture recording, and bitmap functions).

-   {cpp:func}`BView Graphics State Functions <BView::Graphics>` modify or
report on the "graphics state," a set of variables (colors, pen position,
scaling, etc.) that control how drawing takes place in the
{cpp:class}`BView`.

-   {cpp:func}`BView Hook Functions <BView::Hook>` gives a list of the
{cpp:class}`BView` functions that can be implemented in a subclass.

-   {cpp:func}`BView View Hierarchy Functions <BView::ViewHierarchy>` relate
to the nested tree of views associated with a window.

-   {cpp:func}`BView Input-Related Functions <BView::Input>` monitor and
process input activity.

-   Scripting and Archival describes the scripting suites and properties, and
archived fields supported by BView.

## Developing a BView Subclass

To define special behavior for a {cpp:class}`BView`—such as the type of
behavior that might be needed for the canvas area of a painting program—you
define your own subclass of {cpp:class}`BView`, and in that subclass
implement the appropriate hook functions of the {cpp:class}`BView` class. A
hook function is a function that is called by the BeOS internals in
response to certain events, and that is intended specifically for
definition in a user-defined subclass. For example, the
{cpp:func}`BView::MouseDown` hook function is called on a BView instance
every time a mouse button is clicked while the mouse is inside the view.
The default {cpp:func}`BView::MouseDown` function does nothing, but you can
override this with your own implementation, to respond to mouse-down events
as you wish.

The following are the most commonly used hook functions. Other hook
functions provide for changes in the size or structure of views and
windows, changes in the input focus, and so forth. For a complete list and
reference of hook functions, see {cpp:func}`BView Hook Functions
<BView::Hook>`.

:::{list-table}
---
header-rows: 0
align: left
widths: auto
---
-
	- Draw()
	- Called whenever the contents of the view need to be drawn or redrawn.
-
	- KeyDown()
	- Called when a keyboard key is pressed.
-
	- KeyUp()
	- Called when a keyboard key is released.
-
	- MouseDown()
	- Called when a mouse button is clicked while the mouse cursor is in the
		view.
-
	- MouseMoved()
	- Called when the mouse cursor enters, exits, or moves within the view.

:::

## The View Structure

A newly created view is an "orphan"—it won't appear onscreen, and can't be
used for much, because it isn't associated with an onscreen & quot;parent".
To rectify this situation, and give your new view a warm and loving home,
invoke the {cpp:func}`AddChild() <BView::AddChild>` method of an existin
{cpp:class}`BWindow` or {cpp:class}`BView` object to add the new view as a
child, i.e.

:::{code} cpp
existingWindowOrView.AddChild(yourNewView);
:::

Ultimately, all views displayed in a window end up as a tree of views,
with the window as the root of the tree.

See the BView View Hierarchy Functions section for BView functions related
to this view structuring.

## Locking the Window

Most {cpp:class}`BView` functions expect the view's BWindow to be locked.
To find a view's {cpp:class}`BWindow` and lock/unlock it, you first call
{cpp:func}`BView::Window` and then call the {cpp:func}`LockLooper()
<BHandler::LockLooper>` and {cpp:func}`UnlockLooper()
<BHandler::UnlockLooper>` functions (defined by {cpp:class}`BHandler`,
inherited by {cpp:class}`BWindow`):

:::{code} cpp
if (window.LockLooper() ) {
   . . .
   window.UnlockLooper();
}
:::

{cpp:class}`BView` functions check to ensure sure the caller has the
window locked. If the window isn't properly locked, they print warning
messages and fail.

Whenever the system calls a {cpp:class}`BView` hook function, it
automatically locks the {cpp:class}`BWindow` for you—you never have to lock
the {cpp:class}`BWindow` in the implementation of {cpp:class}`BView` hook
function.

## Focus

To facilitate keyboard navigation of views, {cpp:class}`BView` provides
integral support for the concept of focus. The view that has the focus is
the one whose {cpp:func}`KeyDown() <BView::KeyDown>` function is called to
process keyboard events. Only one view in a window can have the focus at
any given time

From the user's point-of-view, the tab key rotates the focus from one view
to the next through the navigation group, cycling back to the first view if
the tab key is pressed while the last targetable view in the group has the
focus. {hkey}`shift`+{hkey}`tab` cycles the focus backward. Holding down
the {hkey}`control` key while cycling groups causes the focus to jump from
one navigation group to the next.

When a view has the focus, some sort of indicator should be drawn to
inform the user that the view is the focus. Typically, this involves
drawing a line under a label in the view, or possibly drawing a box around
the view or some portion of it. The global
{ref}`keyboard_navigation_color()` function should be used to obtain the
color used to draw the focus indicator.

The view's {cpp:func}`MakeFocus() <BView::MakeFocus>` function is called
to specify whether or not the control has the focus; it's called with an
argument of {cpp:expr}`true` if the control has the focus, and
{cpp:expr}`false` if it's not the focus; {cpp:func}`MakeFocus()
<BView::MakeFocus>` calls the previously-focused view's
{cpp:func}`MakeFocus() <BView::MakeFocus>` function to inform that view
that it's not the focus anymore. You can augment {cpp:func}`MakeFocus()
<BView::MakeFocus>` in a subclass if you need to take notice when the view
becomes the focus (or loses the focus). For example, you may need to draw
or erase the keyboard navigation indicator.
