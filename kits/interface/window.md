# BWindow
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BWindow::BWindow(BRect frame, const char* title, window_type type, uint32 flags, uint32 workspaces = B_CURRENT_WORKSPACE)
:::
:::{cpp:function} BWindow::BWindow(BRect frame, const char* title, window_look look, window_feel feel, uint32 flags, uint32 workspaces = B_CURRENT_WORKSPACE)
:::
:::{cpp:function} BWindow::BWindow(BMessage* archive)
:::

Creates a new window:

:::{list-table}
---
header-rows: 1
---
-
	- Field
	- Description
-
	- frame
	- Is the window's content area rectangle given in screen coordinates. The window's border and title tab (if any) are wrapped around the content area. The frame's coordinates are rounded to the nearest whole number. You can further restrict the window's frame through {cpp:func}`~BWindow::SetWindowAlignment` and {cpp:func}`~BWindow::SetSizeLimits`.
-
	- title
	- Is the string that's displayed in the window's title tab (if it has one). The string is also used, with the prefix "w>", as the name of the window's looper thread: "w>{hparam}`title`". You can reset the title through {cpp:func}`~BWindow::SetTitle`.
-
	- look/feelortype.
	- The appearance and behavior of the window is defined by a combination of the {hparam}`look` and {hparam}`feel` arguments, or by a single {hparam}`type`. See the {cpp:func}`~BWindow::window`, {cpp:func}`~BWindow::window`, and {cpp:func}`~BWindow::window` descriptions for a list of values. The look and feel can be reset through {cpp:func}`~BWindow::SetLook`, {cpp:func}`~BWindow::SetFeel`, and {cpp:func}`~BWindow::SetType`.
-
	- flags
	- The {hparam}`flags` argument is a mask that defines the window's "user attributes"—whether the user can resize or close the window, whether the window avoids front when the user closes other windows, and so on. See "{cpp:func}`~BWindow::Window`" for a list of values. The flags can be reset through {cpp:func}`~BWindow::SetFlags`.
-
	- workspaces
	- Is a mask that tells the window which of the 32 potential workspace(s) it should be displayed in (it can be displayed in more than one workspace at the same time). For example, a workspaces of (1<<2)+(1<<7) tells the window to display itself in workspaces 2 and 7. Instead of passing a bitmask, you can also use the {cpp:enum}`B_CURRENT_WORKSPACE` or {cpp:enum}`B_ALL_WORKSPACES` constant. By default, the window appears in the current (active) workspace. You can reset the workspaces through {cpp:func}`~BWindow::SetWorkspaces`.
:::

A freshly-created window is hidden and locked. After construction, you add
{cpp:class}`BView`s to the
{hclass}`BWindow` through
{cpp:func}`~BWindow::AddChild`, and then show the window
(and start its message loop) by calling
{cpp:func}`~BWindow::Show`.

::::

::::{abi-group}

You never delete your {hclass}`BWindow`s; call
{cpp:func}`~BWindow::Quit` instead.

::::

## Hook Functions
::::{abi-group}

:::{cpp:function} virtual void BWindow::FrameMoved(BPoint* origin)
:::
:::{cpp:function} virtual void BWindow::FrameResized(float width, float height)
:::

These hook functions are invoked just after the window's frame is moved
or resized, whether by the user or programatically. The arguments give
the window's new origin (in screen coordinates) or dimensions. The
default implementations do nothing.

See also: {cpp:enum}`B_WINDOW_MOVED`, {cpp:enum}`B_WINDOW_RESIZED`.

::::

::::{abi-group}

:::{cpp:function} virtual void BWindow::MenusBeginning()
:::
:::{cpp:function} virtual void BWindow::MenusEnded()
:::

The {hmethod}`MenusBeginning()` hook function is called just before menus belonging
to the window are about to be shown to the user. {hmethod}`MenusEnded()` is called
when the menus have been removed from the screen. The default
implementations do nothing. You can implement these functions to make
sure the menus' states accurately reflect the state of the window.

:::{admonition} Important
:class: important
These hook functions are not invoked because of messages—don't go
looking for a "menus beginning" or "menus ended" message.
:::
::::

::::{abi-group}

:::{cpp:function} virtual void BWindow::MessageReceived(BMessage* message)
:::

Implementation detail. See
{cpp:func}`BHandler::MessageReceived`.

::::

::::{abi-group}

:::{cpp:function} virtual void BWindow::ScreenChanged(BRect frame, color_space mode)
:::

Hook function that's called when the screen (on which this window is
located) changes size or location in the screen coordinate system, or
changes color space (depth). {hparam}`frame` is the screen's new frame rectangle,
and {hparam}`mode` is its new color space.

See also:
{cpp:func}`BScreen::Frame`

::::

::::{abi-group}

:::{cpp:function} virtual void BWindow::WindowActivated(bool active)
:::
{hmethod}`WindowActivated()` is a hook function
that's automatically invoked on the {hclass}`BWindow` (and
each of its
{cpp:class}`BView` children) when
the window is activated or deactivated. If
{hparam}`active` is {cpp:enum}`true`, the
window has just become the active window; if it's
{cpp:enum}`false`, it's about to give up that status. You can
implement {hmethod}`WindowActivated()` to do whatever you
want; the default implementation does nothing.
::::

::::{abi-group}

:::{cpp:function} virtual void BWindow::WorkspaceActivated(int32 workspace, bool active)
:::

Implemented by derived classes to respond to a notification that the
workspace displayed on the screen has changed. All windows in the newly
activated workspace as well as those in the one that was just deactivated
get this notification.

The {hparam}`workspace` argument is an index to the workspace in question and the
{hparam}`active` flag conveys its current status. If {hparam}`active` is {cpp:enum}`true`, the workspace
has just become the active workspace. If {hparam}`active` is {cpp:enum}`false`, it has just
stopped being the active workspace.

The default ({hclass}`BWindow`) version of this function is empty.

See also: "{cpp:enum}`B_WORKSPACE_ACTIVATED`" in the Message Protocols appendix,
{cpp:func}`~activate::workspace`

::::

::::{abi-group}

:::{cpp:function} virtual void BWindow::WorkspacesChanged(uint32 oldWorkspaces, uint32 newWorkspaces)
:::

Implemented by derived classes to respond to a notification the the
window has just changed the set of workspaces in which it can be
displayed from {hparam}`oldWorkspaces` to {hparam}`newWorkspaces`. This typically happens
when the user moves a window from one workspace to another, but it may
also happen when a programmatic change is made to the set of permitted
workspaces. Each workspace is represented by a corresponding bit in the
{hparam}`oldWorkspaces` and {hparam}`newWorkspaces` masks.

The default ({hclass}`BWindow`) version of this function is empty.

See also: {cpp:enum}`B_WORKSPACES_CHANGED` in the Message Protocols appendix,
{cpp:func}`~BWindow::SetWorkspaces`

::::

::::{abi-group}

:::{cpp:function} void BWindow::Zoom()
:::
:::{cpp:function} virtual void BWindow::Zoom(BPoint origin, float width, float height)
:::

The non-virtual {hmethod}`Zoom()` (which is called when the user clicks the zoom
button, but can also be called programatically) figures out a new size
and location for the window (as described below), and then passes these
dimensions to the virtual {hmethod}`Zoom()` hook function. It's hook {hmethod}`Zoom()`'s
responsibility to actually resize and move the window; the default
version applies the arguments explicitly by calling
{cpp:func}`~BWindow::MoveTo` and
{cpp:func}`~BWindow::ResizeTo`.
You can re-implement hook {hmethod}`Zoom()` to create a new zooming
algorithm that incorporates or ignores the arguments as you see fit.

The dimensions that non-virtual {hmethod}`Zoom()` passes to hook {hmethod}`Zoom()` are deduced
from the smallest of three rectangles: 1) the screen rectangle, 2) the
rectangle defined by
{cpp:func}`~BWindow::SetZoomLimits`, 3) the rectangle defined by
{cpp:func}`~BWindow::SetSizeLimits`. However, if the window's rectangle already matches these
"zoom" dimensions (give or take a few pixels), {hmethod}`Zoom()` passes the window's
previous ("non-zoomed") size and location.

You can effectively call {hmethod}`Zoom()` even if the window is {cpp:enum}`B_NOT_ZOOMABLE`.

{hmethod}`Zoom()` may both move and resize the window, resulting in
{cpp:func}`~BWindow::FrameMoved` and
{cpp:func}`~BWindow::FrameResized` notifications.

::::

## Member Functions
::::{abi-group}

:::{cpp:function} void BWindow::Activate(bool flag = true)
:::
:::{cpp:function} bool BWindow::IsActive() const
:::

{hmethod}`Activate()` makes the {hclass}`BWindow`
the active window (if {hparam}`flag` is {cpp:enum}`true`), or
causes it to relinquish that status (if {hparam}`flag` is {cpp:enum}`false`). The active window
is made frontmost, its title tab is highlighted, and it becomes the
target of keyboard events. The
{cpp:func}`~BWindow::Show` function automatically activates
the window.

:::{admonition} Important
:class: important
You can't activate a hidden window.
:::
:::{admonition} Note
:class: note
You rarely call {hmethod}`Activate()` yourself. Deciding which window to make
active is the user's choice.
:::

{hmethod}`IsActive()` returns {cpp:enum}`true` if the
window is currently the active window, and {cpp:enum}`false` if
it's not.

See also:
{cpp:func}`BView::WindowActivated`

::::

::::{abi-group}

:::{cpp:function} void BWindow::AddChild(BView* aView, BView* sibling = NULL)
:::
:::{cpp:function} bool BWindow::RemoveChild(BView* aView)
:::
:::{cpp:function} BView* BWindow::ChildAt(int32 index) const
:::
:::{cpp:function} int32 BWindow::CountChildren() const
:::

{hmethod}`AddChild()` places {hparam}`aView`
(and its child views) in the window, adds it to
the window's view list, and adds it to the window's list of handlers:

- Graphically, the view is placed in the window's coordinate system at the location defined by the view's frame rectangle.
- In the window's view list, {hparam}`aView` is inserted before {hparam}`sibling`. if {hparam}`sibling` is {cpp:enum}`NULL`, {hparam}`aView` is added at the end of the list. Note, however, that window list order is of little significance; for example, it doesn't affect the order in which sibling views are drawn.
- {hparam}`aView` and its children are added to the window's handler list; {hparam}`aView`'s next handler is set to this {hclass}`BWindow`.

Each {cpp:class}`BView` in aView's
hierarchy is sent an
{cpp:func}`~BView::AttachedToWindow`
call. When they've all had a chance to respond, they're each sent an
{cpp:func}`~BView::AllAttached`
call.

If {hparam}`aView` has already been added to a view hierarchy,
or if {hparam}`sibling` isn't
in the window's view list, {hmethod}`AddChild()` fails.

{hmethod}`RemoveChild()` removes {hparam}`aView` (and its children) from the window's display,
view list, and handler list, and sets {hparam}`aView`'s next handler to {cpp:enum}`NULL`.

{cpp:func}`~BView::DetachedFromWindow` and
{cpp:func}`~BView::AllDetached`
are invoked on {hparam}`aView` and each of
its children. If {hparam}`aView` isn't in the window's view list, the function
fails and returns {cpp:enum}`false`; it returns {cpp:enum}`true` upon success.

{hmethod}`ChildAt()` returns the {hparam}`index`'th
view in the window's view list, or {cpp:enum}`NULL` if
{hparam}`index` is out of bounds (you've reached the end of the list). The view
list doesn't recurse; to build a full map of a window's view hierarchy,
you call {cpp:func}`BView::ChildAt`
iteratively on each of the window's views (and
each of their children, etc.).

See also:
{cpp:func}`BView::Parent`

::::

::::{abi-group}

:::{cpp:function} void BWindow::AddShortcut(uint32 key, uint32 modifiers, BMessage* message)
:::
:::{cpp:function} void BWindow::AddShortcut(uint32 key, uint32 modifiers, BMessage* message, BHandler* handler)
:::
:::{cpp:function} void BWindow::RemoveShortcut(uint32 key, uint32 modifiers)
:::

{hmethod}`AddShortcut()` creates a keyboard shortcut: When the
user types
Command+{hparam}`modifiers`+{hparam}`key`,
{hparam}`message` is sent to {hparam}`handler`. If
a shortcut already exists for
{hparam}`modifiers`+{hparam}`key`, it's removed
before the new shortcut is added.

{hmethod}`RemoveShortcut()` removes the shortcut for
{hparam}`modifiers`+{hparam}`key`.

:::{admonition} Warning
:class: warning
Don't use these functions to create and remove menu shortcuts; use
{cpp:class}`BMenuItem` objects instead.
:::

Notes on the arguments:

- {hparam}`key` is a case-insensitive character value. If you want to map to an uppercase character, you have to include {cpp:enum}`B_SHIFT_KEY` in the {hparam}`modifiers` mask.
- {hparam}`modifiers` is an OR'd list of modifier key numbers. {cpp:enum}`B_COMMAND_KEY`, which is always assumed, needn't be added to the mask. See {ref}`modifiers()` for a list of modifier keys.
- {hparam}`message` is a model of the {cpp:class}`BMessage` you want sent when the user types the shortcut. The {hclass}`BWindow` takes ownership of the {hparam}`message` object and adds a when field to it:Field nameType codeDescriptionwhenB_INT64_TYPEThe time of the key-down, in microseconds since 01/01/70.
- {hparam}`handler` must be in the window's handler list (or the message won't be sent). If you exclude the argument, this {hclass}`BWindow` handles the message. If handler is (literally) {cpp:enum}`NULL`, the message is sent to the {hclass}`BWindow`'s focus view (or to the {hclass}`BWindow` if no view is in focus).

As with all Command events, a {cpp:enum}`B_KEY_DOWN` message isn't sent when the user
invokes a keyboard shortcut, but the subsequent {cpp:enum}`B_KEY_UP` is.

Every {hclass}`BWindow` has five built-in shortcuts:

ShortcutMessageHandlerCommand+xB_CUTthe focus viewCommand+cB_COPYthe focus viewCommand+vB_PASTEthe focus viewCommand+aB_SELECT_ALLthe focus viewCommand+w (closable windows only)B_QUIT_REQUESTEDthe BWindow

In addition, {hclass}`BWindow`s respond to
Command+q
by posting {cpp:func}`~B::QUIT` to
be_app.

::::

::::{abi-group}

:::{cpp:function} status_t BWindow::AddToSubset(BWindow* window)
:::
:::{cpp:function} status_t BWindow::RemoveFromSubset(BWindow* window)
:::

Adds windows to and removes them from this window's subset. This affects
modal and floating windows with a subset feel only (i.e.
{cpp:enum}`B_MODAL_SUBSET_WINDOW_FEEL` or {cpp:enum}`B_FLOATING_SUBSET_WINDOW_FEEL`). A subset
feel window blocks or floats above only those windows in its subset. To
set the window's feel, use
{cpp:func}`~BWindow::SetFeel`.

::::

::::{abi-group}

:::{cpp:function} virtual status_t BWindow::Archive(BMessage* archive, bool deep = true) const
:::

Archives the {hclass}`BWindow` by recording its frame rectangle, title, type, and
flags in the {cpp:class}`BMessage` {hparam}`archive`.
If the {hparam}`deep` flag is {cpp:enum}`true`, this function
also archives all the views in the window's view hierarchy. If the flag
is {cpp:enum}`false`, only the {hclass}`BWindow` is archived.

See also:
{cpp:func}`BArchivable::Archive`,
{cpp:func}`~BWindow::Instantiate` static function

::::

::::{abi-group}

:::{cpp:function} BRect BWindow::Bounds() const
:::
:::{cpp:function} BRect BWindow::Frame() const
:::

These functions return the rectangle that encloses the window's content
area. The bounds rectangle ({hmethod}`Bounds()`) is expressed in the window's
coordinate system; the frame rectangle ({hmethod}`Frame()`) is expressed in the
screen's coordinate system.

The rectangles are cached by the {hclass}`BWindow` itself—calling these
functions doesn't incur a trip to the App Server.

::::

::::{abi-group}

:::{cpp:function} BPoint BWindow::ConvertToScreen(BPoint windowPoint) const
:::
:::{cpp:function} void BWindow::ConvertToScreen(BPoint* windowPoint) const
:::
:::{cpp:function} BRect BWindow::ConvertToScreen(BRect windowRect) const
:::
:::{cpp:function} void BWindow::ConvertToScreen(BRect* windowRect) const
:::
:::{cpp:function} BPoint BWindow::ConvertFromScreen(BPoint windowPoint) const
:::
:::{cpp:function} void BWindow::ConvertFromScreen(BPoint* windowPoint) const
:::
:::{cpp:function} BRect BWindow::ConvertFromScreen(BRect windowRect) const
:::
:::{cpp:function} void BWindow::ConvertFromScreen(BRect* windowRect) const
:::

Converts the argument from window coordinates to screen coordinates or
vice versa. The point or rect needn't fall within this {hclass}`BWindow`'s bounds.

If the argument is passed by value, the function returns the converted
value; if it's by pointer, the conversion is done in-place.

The {hclass}`BWindow` must be locked.

::::

::::{abi-group}

:::{cpp:function} BView* BWindow::CurrentFocus() const
:::

returns the current focus view for the {hclass}`BWindow`, or {cpp:enum}`NULL` if no view is
currently in focus. The focus view is the {cpp:class}`BView` that's responsible for
showing the current selection and is the target for keyboard messages
directed at this {hclass}`BWindow`. The focus view is set through
{cpp:func}`BView::MakeFocus`.

The {hclass}`BWindow` sets its preferred handler to be the focus view, so the
inherited {cpp:func}`~BLooper::PreferredHandler`
function will return this same object (but
as a {cpp:class}`BHandler`).

::::

::::{abi-group}

:::{cpp:function} void BWindow::DisableUpdates()
:::
:::{cpp:function} void BWindow::EnableUpdates()
:::

These functions disable automatic updating within the window, and
re-enable it again. Any drawing that's done while updates are disabled is
suppressed until updates are re-enabled. If you're doing a lot of drawing
within the window, and you want the results of the drawing to appear all
at once, you should disable updates, draw, and then re-enable updates.

See also:
{cpp:func}`BView::Invalidate`,
{cpp:func}`~BWindow::UpdateIfNeeded`

::::

::::{abi-group}

Implementation detail; see
{cpp:func}`BLooper::DispatchMessage`.

:::{admonition} Warning
:class: warning
You shouldn't override this function in a {hclass}`BWindow` subclass; if you want
to augment the window's message-dispatching mechanism, override
{cpp:func}`~BWindow::MessageReceived`.
:::
::::

::::{abi-group}

:::{cpp:function} BView* BWindow::FindView(BPoint* point) const
:::
:::{cpp:function} BView* BWindow::FindView(const char* name) const
:::

Returns the view located at {hparam}`point` within the window, or the view tagged
with {hparam}`name`. The functions returns {cpp:enum}`NULL` if no view is found.

::::

::::{abi-group}

:::{cpp:function} void BWindow::Flush() const
:::
:::{cpp:function} void BWindow::Sync() const
:::

Both of these functions cause this window's App Server-bound messages to
be sent immediately. {hmethod}`Flush()` sends the messages and returns immediately;
{hmethod}`Sync()` send the messages and waits for the App Server to respond. In
other words, when {hmethod}`Sync()` returns you're guaranteed that all of the
flushed messages have been processed.

See also:
{cpp:func}`BView::Flush`

::::

::::{abi-group}

:::{cpp:function} virtual status_t BWindow::GetSupportedSuites(BMessage* message)
:::

Adds the name "suite/vnd.Be-window" to the message.

See also:
{cpp:func}`BHandler::GetSupportedSuites`

::::

::::{abi-group}

:::{cpp:function} bool BWindow::IsFront() const
:::
:::{cpp:function} bool BWindow::IsFloating() const
:::
:::{cpp:function} bool BWindow::IsModal() const
:::

These functions return {cpp:enum}`true` if the window is frontmost on screen, if it
has a floating window feel, and if it has a modal window feel,
respectively.

:::{admonition} Note
:class: note
A floating window can never be the frontmost window.
:::
::::

::::{abi-group}

:::{cpp:function} BView* BWindow::LastMouseMovedView()
:::

Returns a pointer to the view in this window that most recently received
a {cpp:enum}`B_MOUSE_MOVED` message.

::::

::::{abi-group}

:::{cpp:function} void BWindow::MoveBy(float horizontal, float vertical)
:::
:::{cpp:function} void BWindow::MoveTo(BPoint point)
:::
:::{cpp:function} void BWindow::MoveTo(float x, float y)
:::

These functions move the window without resizing it. {hmethod}`MoveBy()` adds
{hparam}`horizontal` coordinate units to the left and right components of the
window's frame rectangle and {hparam}`vertical` units to the frame's top and
bottom. if {hparam}`horizontal` and {hparam}`vertical` are negative, the window moves upward
and to the left. if they're positive, it moves downward and to the right.
{hmethod}`MoveTo()` moves the left top corner of the window's content area to
{hparam}`point`—or ({hparam}`x`, {hparam}`y`)
– in the screen coordinate system; it adjusts
all coordinates in the frame rectangle accordingly.

None of the values passed to these functions should specify fractional
coordinates; a window must be aligned on screen pixels. Fractional values
will be rounded to the closest whole number.

Neither function alters the {hclass}`BWindow`'s coordinate system or bounds
rectangle.

When these functions move a window, a window-moved event is reported to
the window. This results in the {hclass}`BWindow`'s
{cpp:func}`~BWindow::FrameMoved` function being
called.

::::

::::{abi-group}

:::{cpp:function} bool BWindow::NeedsUpdate() const
:::

Returns {cpp:enum}`true` if any of the views within the window need to be updated,
and {cpp:enum}`false` if they're all up-to-date.

::::

::::{abi-group}

:::{cpp:function} virtual void BWindow::OpenViewTransaction()
:::
:::{cpp:function} virtual void BWindow::CommitViewTransaction()
:::

These two functions bracket a series of "batched" drawing instructions.
After you call {hmethod}`OpenViewTransaction()`, everything you draw in the window
is bundled up and then sent to the app server (and rendered) when you
call {hmethod}`CommitViewTransaction()`. You can only perform one transaction (per
window) at a time. The {hclass}`BWindow` must be locked when you call
{hmethod}`OpenViewTransaction()`, and must remain locked until after you call
{hmethod}`CommitViewTransaction()`. Invocations of
{cpp:func}`~BWindow::Flush` are ignored while a
transaction is open (and locked).

::::

::::{abi-group}

:::{cpp:function} virtual void BWindow::Quit()
:::

{hmethod}`Quit()` removes the window from the screen, deletes all the
{cpp:class}`BView`s in its
view hierarchy, destroys the window thread, removes the window's
connection to the Application Server, and deletes the {hclass}`BWindow` object.

Use this function, rather than the delete operator, to destroy a window.

{hclass}`BWindow`'s {hmethod}`Quit()` works much like the
{cpp:class}`BLooper` function it overrides. When
called from the {hclass}`BWindow`'s thread, it doesn't return. When called from
another thread, it returns after all previously posted messages have been
processed and the {hclass}`BWindow` and its thread have been destroyed.

:::{admonition} Note
:class: note
The window must be locked when you call {hmethod}`Quit()`.
:::

See also:
{cpp:func}`BLooper::QuitRequested`,
{cpp:func}`BLooper::Quit`,
{cpp:func}`BApplication::QuitRequested`

::::

::::{abi-group}

:::{cpp:function} void BWindow::ResizeBy(float horizontal, float vertical)
:::
:::{cpp:function} void BWindow::ResizeTo(float width, float height)
:::

These functions resize the window, while keeping its left top corner
constant. {hmethod}`ResizeBy()` adds {hparam}`horizontal` pixels to the width of the window's
frame and {hparam}`vertical` pixels to its height. {hmethod}`ResizeTo()` sets the frame
absolutely to [{hparam}`width`, {hparam}`height`] pixels. Fractional components are rounded
to the nearest whole number.

The {cpp:func}`~BWindow::FrameResized`
hook function is called after the frame has been resized.

::::

::::{abi-group}

:::{cpp:function} virtual BHandler* BWindow::ResolveSpecifier(BMessage* message, int32 index, BMessage* specifier, int32 command, const char* property)
:::

Resolves specifiers for the "Frame", "Title", and "View" properties. See
"{cpp:func}`~BWindow::Scripting`"
in the class overview for more information.

See also:
{cpp:func}`BHandler::ResolveSpecifier`

::::

::::{abi-group}

:::{cpp:function} status_t BWindow::SendBehind(const BWindow* window)
:::

Relayers the windows on the screen so this window is behind {hparam}`window`.

::::

::::{abi-group}

:::{cpp:function} void BWindow::SetDefaultButton(BButton* button)
:::
:::{cpp:function} BButton* BWindow::DefaultButton() const
:::

Set and return the window's default button. This is the button that's
mapped to the Enter key. The user can activate the default button at any
time—even if another
{cpp:class}`BView` is the focus view (the focus view will
not receive a {cpp:enum}`B_KEY_DOWN` message). To remove the current default (without
promoting another button) call `SetDefaultButton(NULL)`. There can only be
one default button at a time; {hmethod}`SetDefaultButton()` demotes the previous
default.

When you promote or demote a default button, it's automatically
redisplayed and receives a
{cpp:func}`BButton::MakeDefault`
call.

::::

::::{abi-group}

:::{cpp:function} status_t BWindow::SetFeel(window_feel feel)
:::
:::{cpp:function} window_feel BWindow::Feel() const
:::

{hmethod}`SetFeel()` changes the window's feel to the specified value.

{hmethod}`Feel()` returns the current feel of the window.

See the {hclass}`BWindow`
{cpp:func}`~BWindow::Constructor` for a list of
window_feel constants.

::::

::::{abi-group}

:::{cpp:function} status_t BWindow::SetFlags(uint32 flags)
:::
:::{cpp:function} uint32 BWindow::Flags() const
:::

{hmethod}`SetFlags()` set the window's flags (or
"user attributes") to the specified
combination. {hmethod}`Flags()` returns the current flags.

See
"{cpp:func}`~BWindow::Window`". for a list of the flag values.

::::

::::{abi-group}

:::{cpp:function} void BWindow::SetKeyMenuBar(BMenuBar* menuBar)
:::
:::{cpp:function} BMenuBar* BWindow::KeyMenuBar() const
:::

{hmethod}`SetKeyMenuBar()` makes the specified
{cpp:class}`BMenuBar` object the "key" menu bar
for the window—the object that's at the root of the menu hierarchy
that users can navigate using the keyboard. {hmethod}`KeyMenuBar()` returns the
object with key status, or {cpp:enum}`NULL` if the window doesn't have a
{cpp:class}`BMenuBar`
object in its view hierarchy.

If a window contains only one
{cpp:class}`BMenuBar`
view, it's automatically
designated the key menu bar. If there's more than one
{cpp:class}`BMenuBar` in the
window, the last one added to the window's view hierarchy is considered
to be the key one.

If there's a "true" menu bar displayed along the top of the window, its
menu hierarchy is the one that users should be able to navigate with the
keyboard. {hmethod}`SetKeyMenuBar()` can be called to make sure that the
{cpp:class}`BMenuBar`
object at the root of that hierarchy is the "key" menu bar.

::::

::::{abi-group}

:::{cpp:function} status_t BWindow::SetLook(window_look look)
:::
:::{cpp:function} window_look BWindow::Look() const
:::

{hmethod}`SetLook()` changes the window's look to the specified value.

{hmethod}`Look()` returns the current look of the window.

See the {hclass}`BWindow`
{cpp:func}`~BWindow::Constructor` for a list of
window_look constants.

::::

::::{abi-group}

:::{cpp:function} void BWindow::SetPulseRate(bigtime_t microseconds)
:::
:::{cpp:function} bigtime_t BWindow::PulseRate()
:::

These functions set and return how often
{cpp:func}`BView::Pulse` is called for the
{hclass}`BWindow`'s views (how often {cpp:enum}`B_PULSE` messages are posted to the window).
All {cpp:class}`BView`s attached to the same window share the same pulse rate.

By turning on the {cpp:enum}`B_PULSE_NEEDED` flag, a {cpp:class}`BView` can request periodic
{cpp:func}`BView::Pulse`
notifications. By default, {cpp:enum}`B_PULSE` messages are posted
every 500,000 microseconds, as long as no other messages are pending. Each
message causes {cpp:func}`BView::Pulse` to be called
once for every {cpp:class}`BView`
that requested the notification. There are no pulses if no {cpp:class}`BView`s request them.

{hmethod}`SetPulseRate()` permits you to set a different interval. The interval set
should not be less than 100,000 microseconds; differences less than
50,000 microseconds may not be noticeable. A finer granularity can't be
guaranteed.

Setting the pulse rate to 0 disables pulsing for all views in the window.

See also:
The {hclass}`BView` {cpp:func}`~BView::Constructor`

::::

::::{abi-group}

:::{cpp:function} void BWindow::SetSizeLimits(float minWidth, float maxWidth, float minHeight, float maxHeight)
:::
:::{cpp:function} void BWindow::GetSizeLimits(float* minWidth, float* maxWidth, float* minHeight, float* maxHeight)
:::
:::{cpp:function} void BWindow::SetZoomLimits(float maxWidth, float maxHeight)
:::

These functions set and report limits on the size of the window. The user
won't be able to resize the window beyond the limits set by
{hmethod}`SetSizeLimits()`–to make it have a width less than
{hparam}`minWidth` or
greater than {hparam}`maxWidth`, nor a height less than {hparam}`minHeight` or greater than
{hparam}`maxHeight`. By default, the minimums are sufficiently small and the
maximums sufficiently large to accommodate any window within reason.

{hmethod}`SetSizeLimits()` constrains the user, not the programmer. It's legal for
an application to set a window size that falls outside the permitted
range. The limits are imposed only when the user attempts to resize the
window; at that time, the window will jump to a size that's within range.

{hmethod}`GetSizeLimits()` writes the current limits to the variables provided.

{hmethod}`SetZoomLimits()` sets the maximum size that the window will zoom to (when
the {cpp:func}`~BWindow::Zoom` function is called).
The maximums set by {hmethod}`SetSizeLimits()` also
apply to zooming; the window will zoom to the screen size or to the
smaller of the maximums set by these two functions.

Since the sides of a window must line up on screen pixels, the values
passed to both {hmethod}`SetSizeLimits()` and {hmethod}`SetZoomLimits()` should be whole
numbers.

::::

::::{abi-group}

:::{cpp:function} void BWindow::SetTitle(const char* newTitle)
:::
:::{cpp:function} const char* BWindow::Title() const
:::

These functions set and return the window's title. {hmethod}`SetTitle()` replaces
the current title with {hparam}`newTitle`. It also renames the window thread in the
following format:

:::{code}
"w>newTitle"
:::

where as many characters of the {hparam}`newTitle` are included in the thread name
as will fit.

{hmethod}`Title()` returns a pointer to the current title. The returned string is
null-terminated. It belongs to the {hclass}`BWindow` object, which may alter the
string or free the memory where it resides without notice. Applications
should ask for the title each time it's needed and make a copy for their
own purposes.

A window's title and thread name are originally set by an argument passed
to the {hclass}`BWindow` {cpp:func}`~BWindow::Constructor`.

::::

::::{abi-group}

:::{cpp:function} status_t BWindow::SetType(window_type type)
:::
:::{cpp:function} window_type BWindow::Type() const
:::

{hmethod}`SetType()` changes the type of the window to the specified value.
{hmethod}`Type()` returns the type. You normally set the window's type when it's
constructed.

The type is set at construction (or by {hmethod}`SetType()`) as one of the following
constants (full descriptions can be found in the discussion of the
{hclass}`BWindow` {cpp:func}`~BWindow::Constructor`):

- {cpp:enum}`B_UNTYPED_WINDOW`
- {cpp:enum}`B_MODAL_WINDOW`
- {cpp:enum}`B_BORDERED_WINDOW`
- {cpp:enum}`B_TITLED_WINDOW`
- {cpp:enum}`B_DOCUMENT_WINDOW`
- {cpp:enum}`B_FLOATING_WINDOW`

::::

::::{abi-group}

:::{cpp:function} status_t BWindow::SetWindowAlignment(window_alignment mode, int32 h, int32 hOffset = 0, int32 width = 0, int32 widthOffset = 0, int32 v = 0, int32 vOffset = 0, int32 height = 0, int32 heightOffset = 0)
:::
:::{cpp:function} status_t BWindow::GetWindowAlignment(window_alignment* mode = NULL, int32* h = NULL, int32* hOffset = NULL, int32* width = NULL, int32* widthOffset = NULL, int32* v = NULL, int32* vOffset = NULL, int32* height = NULL, int32* heightOffset = NULL) const
:::

{hmethod}`SetWindowAlignment()` sets the current alignment of
the window content on the screen. {hparam}`mode` is either
{cpp:enum}`B_PIXEL_ALIGNMENT` or
{cpp:enum}`B_BYTE_ALIGNMENT`.

If {hparam}`mode` is {cpp:enum}`B_PIXEL_ALIGNMENT`,
{hmethod}`SetWindowAlignment()` aligns the window in pixel
coordinates. {hparam}`h` and {hparam}`hOffset`
together determine the horizontal alignment: {hparam}`h` gives
the horizontal origin step while {hparam}`hOffset` is the
horizontal offset. {hparam}`hOffset` must be between 1 and
{hparam}`h` (as a convenience, 0 is taken to mean 1). For
example, if {hparam}`h` is 4 and {hparam}`hOffset`
is 1, valid horizontal origins would be …, -7, -3, 1, 5, 9, … Similarly,
{hparam}`width`/{hparam}`widthOffset`,
{hparam}`v`/{hparam}`vOffset`,
{hparam}`height`/{hparam}`heightOffset` give you
control over the other window parameters.

If {hparam}`mode` is {cpp:enum}`B_BYTE_ALIGNMENT`, then the alignment is given in terms of
frame buffer offsets. However, the setting only affects the horizontal
origin and width. You can't align the right and bottom edges in
{cpp:enum}`B_BYTE_ALIGNMENT` mode.

{hmethod}`GetWindowAlignment()` returns the current window alignment.

Both methods return {cpp:enum}`B_NO_ERROR` on success and {cpp:enum}`B_ERROR` otherwise.

::::

::::{abi-group}

:::{cpp:function} void BWindow::SetWorkspaces(uint32 workspaces)
:::
:::{cpp:function} uint32 BWindow::Workspaces() const
:::

These functions set and return the set of workspaces where the window can
be displayed. The workspaces argument passed to {hmethod}`SetWorkspaces()` and the
value returned by {hmethod}`Workspaces()` is a bitfield with one bit set for each
workspace in which the window can appear. Usually a window appears in
just one workspace.

{hmethod}`SetWorkspaces()` can associate a window with workspaces that don't exist
yet. The window will appear in those workspaces if and when the user
creates them.

You can pass {cpp:enum}`B_CURRENT_WORKSPACE` as the {hparam}`workspaces` argument to place the
window in the workspace that's currently displayed (the active workspace)
and remove it from all others, or {cpp:enum}`B_ALL_WORKSPACES` to make sure the
window shows up in all workspaces, including any new ones that the user
might create. {hmethod}`Workspaces()` may return {cpp:enum}`B_ALL_WORKSPACES`, but will identify
the current workspace rather than return {cpp:enum}`B_CURRENT_WORKSPACE`.

Changing a {hclass}`BWindow`'s set of workspaces causes it to be notified with a
{cpp:func}`~BWindow::WorkspacesChanged` function call.

See also:
the {hclass}`BWindow` {cpp:func}`~BWindow::Constructor`

::::

::::{abi-group}

:::{cpp:function} virtual void BWindow::Show()
:::
:::{cpp:function} virtual void BWindow::Hide()
:::
:::{cpp:function} bool BWindow::IsHidden() const
:::
:::{cpp:function} virtual void BWindow::Minimize(bool minimize)
:::
:::{cpp:function} bool BWindow::IsMinimized() const
:::

These functions hide and show the window.

{hmethod}`Show()` places the window frontmost on the screen
(but behind any applicable floating or modal windows), places it on
Deskbar's window list, and makes it the active window. If this is the
{hclass}`BWindow`'s first {hmethod}`Show()`, the
object's message loop is started, and the object is unlocked.

{hmethod}`Hide()` removes the window from the screen, removes
it from Deskbar's window list, and passes active status to some other window
(if this is the active window). If {hmethod}`Hide()` is called
more than once, you'll need to call {hmethod}`Show()` an equal
number of times for the window to become visible again.

{hmethod}`Minimize()` hides and shows the window (and passes
active status), as {hparam}`minimize` is
{cpp:enum}`true` or {cpp:enum}`false`. The difference
between this function and
{hmethod}`Hide()`/{hmethod}`Show()` is that
{hmethod}`Minimize()` dims (and undims) the window's entry in
Deskbar's window list, but doesn't remove the entry altogether. Also, a
single `Minimize(false)` "undoes" any number of
`Minimize(true)` calls.

{hmethod}`Minimize()` also acts as a hook that's invoked when
the user double-clicks the window's title tab or selects the window from
DeskBar's window list. If {hparam}`minimize` is
{cpp:enum}`true`, the window is about to be hidden; if
{cpp:enum}`false`, it's about to be shown. The
{hmethod}`Minimize()` function itself does the hiding and
showing–if you override {hmethod}`Minimize()` and you
want to inherit the {hclass}`BWindow` behaviour, you must call
{hmethod}`BWindow::Minimize()` in your implementation.

{hmethod}`IsHidden()` returns {cpp:enum}`true` if the
window is currently hidden (i.e. through {hmethod}`Hide()`).
{hmethod}`IsMinimized()` returns {cpp:enum}`true` if
the window is minimized. Hiding takes precendence over minimization. For
example, in both of these sequences…

:::{code}
window->Hide();
window->Minimize(true);
/* or */
window->Minimize(true);
window->Hide();
:::

…the window is hidden but not minimized.

See also: {cpp:enum}`B_MINIMIZE`

::::

::::{abi-group}

:::{cpp:function} void BWindow::UpdateIfNeeded()
:::

Immediately and synchronously invokes
{cpp:func}`~BView::Draw` on each child view that
needs updating. This function is ignored if its called from any thread
other than the {hclass}`BWindow`'s message loop. You call it as part of the
implementation of a user interface hook function (
{cpp:func}`~BView::MouseMoved`,
{cpp:func}`~BView::KeyDown`(),
et. al.) to force invalid views to be immediately redrawn
without having to wait for the hook function to finish. See
{cpp:func}`~TheInterfaceKit::Drawing` for details and an example.

::::

## Static Functions
::::{abi-group}

See {cpp:func}`BArchivable::Instantiate`

::::

## Constants and Defined Types
::::{abi-group}

The window_look constants define the appearance of the window–the
look of its title tab, border, and the type of "resize control" (in the
bottom right corner of the window). The look is set in the constructor or
in the {cpp:func}`~BWindow::SetLook`
function. The table below lists and briefly describes
the window_look values.

:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_DOCUMENT_WINDOW_LOOK`
	- Large title bar, thick border, draggable "resizebox".
-
	- {cpp:enum}`B_TITLED_WINDOW_LOOK`
	- Same as the document window, but with a less substantial "resize corner".
-
	- {cpp:enum}`B_FLOATING_WINDOW_LOOK`
	- Small title bar, thin border, resize corner.
-
	- {cpp:enum}`B_MODAL_WINDOW_LOOK`
	- No title bar, thick border, no resize control (by convention; see the {cpp:enum}`B_NOT_RESIZABLE` window flag).
-
	- {cpp:enum}`B_BORDERED_WINDOW_LOOK`
	- No title bar, line border, no resize control.
-
	- {cpp:enum}`B_NO_BORDER_WINDOW_LOOK`
	- A borderless white rectangle. The user can't move or close this window.
:::
::::

::::{abi-group}

The window_feel constants govern a window's behavior in relation to other
windows. The feel is set in the {hclass}`BWindow` constructor or in
{cpp:func}`~BWindow::SetFeel`. The
table below briefly describes the window feels.

- To set a window's subset, use {cpp:func}`~BWindow::AddToSubset`.
- Modal windows are drawn in front of floating windows.

:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_NORMAL_WINDOW_FEEL`
	- Behaves like a normal window (non-modal, non-floating).
-
	- {cpp:enum}`B_MODAL_SUBSET_WINDOW_FEEL`,{cpp:enum}`B_MODAL_APP_WINDOW_FEEL`,{cpp:enum}`B_MODAL_ALL_WINDOW_FEEL`
	- When displayed, blocks all windows in its subset1, app, or across the entire system. A modal subset/app window is visible only if a window in its subset/app is visible. Modal all windows are always visible in all workspaces
-
	- {cpp:enum}`B_FLOATING_SUBSET_WINDOW_FEEL`,{cpp:enum}`B_FLOATING_APP_WINDOW_FEEL`,{cpp:enum}`B_FLOATING_ALL_WINDOW_FEEL`
	- Floats above all windows in its subset1, app, or across the entire system. A floating subset/app window is visible only if a window in its subset/app is frontmost. Floating all windows are always visible in all workspaces.
:::
::::

::::{abi-group}

The window_type constants are pre-defined combinations of looks and
feels. You set the type through the {hclass}`BWindow`
{cpp:func}`~BWindow::Constructor` or
{cpp:func}`~BWindow::SetType`.

Window TypeLook and FeelB_TITLED_WINDOWB_TITLED_WINDOW_LOOK and B_NORMAL_WINDOW_FEEL.B_DOCUMENT_WINDOWB_DOCUMENT_WINDOW_LOOK and B_NORMAL_WINDOW_FEEL.B_MODAL_WINDOWB_MODAL_WINDOW_LOOK and B_MODAL_APP_WINDOW_FEEL.B_FLOATING_WINDOWB_FLOATING_WINDOW_LOOK and B_FLOATING_APP_WINDOW_FEEL.B_BORDERED_WINDOWB_BORDERED_WINDOW_LOOK and B_NORMAL_WINDOW_FEEL.B_UNTYPED_WINDOWA window of unknown or undefined type.
::::

::::{abi-group}

The window flags (or "user attributes") define miscellaneous aspects of
the window's interface, such as whether it can be moved or closed by the
user. You combine the flags that you want and pass them to the {hclass}`BWindow`
{cpp:func}`~BWindow::Constructor` or
{cpp:func}`~BWindow::SetFlags`.

The default behavior is the inverse of all these flags–i.e. a
window is normally movable, closable, resizable, and so on. However, some
window looks and feels cause imply some of these flags. For example, a
modal feel window can't be minimized (hidden)

Window FlagDescriptionB_NOT_MOVABLEPrevents the user from being able to move the window.B_NOT_CLOSABLEPrevents the user from closing the window.B_NOT_ZOOMABLEPrevents the user from zooming the window.B_NOT_MINIMIZABLEPrevents the user from hiding the window by double-clicking the title tab.B_NOT_H_RESIZABLE B_NOT_V_RESIZABLE B_NOT_RESIZABLEPrevents the user from resizing the window horizontally and/or vertically (B_NOT_RESIZABLE is the same as the sum of the other two constants).B_OUTLINE_RESIZEThe window draws only the outline of its new dimensions as it's being resized, and doesn't refresh its contents.B_WILL_ACCEPT_FIRST_CLICKTells a non-active window to process an activating mouse click (the "first" mouse click) as if it were already active. The BView that responds to the mouse-down message must activate the window. By default, the first mouse click in a non-active window activates the window, and then the mouse click event is thrown away. B_AVOID_FRONTPrevents the window from becoming the frontmost window.B_AVOID_FOCUSPrevents the window from being the target of keyboard events.B_NO_WORKSPACE_ACTIVATIONWhen a window is first shown, the workspace normally switches to the one in which the window is displayed. Setting this flag keeps this from happening.B_NOT_ANCHORED_ON_ACTIVATETells the system to bring the window to the current workspace when the window is selected from Deskbar's window list. Normally, selecting a window from the list activates the workspace that the window is currently in.B_ASYNCHRONOUS_CONTROLSTells the window to allow controls to run asynchronously. All windows that contain controls should include this flag (it's off by default because of backwards compatibility).B_QUIT_ON_WINDOW_CLOSECurrently has no effect.
::::

::::{abi-group}

You tell a window which workspaces to appear through the constructor, or
through the
{cpp:func}`~BWindow::SetWorkspaces`
function. In practice, the only two realistic
settings are represented by these constants.

Workspace ConstantDescriptionB_CURRENT_WORKSPACEAppear in the current workspace.B_ALL_WORKSPACESAppear in all workspaces.
::::

## Scripting Support
::::{abi-group}

B_WINDOW_MOVE_BY, B_WINDOW_MOVE_TOMessageDescriptionB_WINDOW_MOVE_BYMoves the window by the distance specified by the B_POINT_TYPE field data.B_WINDOW_MOVE_TOMoves the window to the position specified by the B_POINT_TYPE field data.
FeelThe Feel property represents the workspaces in which the window resides. The messages are equivalent to manipulating the window with the {cpp:func}`~BWindow::Feel` and {cpp:func}`~BWindow::SetFeel` methods.MessageSpecifiersDescriptionB_GET_PROPERTYB_DIRECT_SPECIFIERReturns the current feel of the window.B_SET_PROPERTYB_DIRECT_SPECIFIERSets the feel of the window.
FlagsThe Flags property represents the window flags. The messages are equivalent to manipulating the window with the {cpp:func}`~BWindow::Flags` and {cpp:func}`~BWindow::SetFlags` methods.MessageSpecifiersDescriptionB_GET_PROPERTYB_DIRECT_SPECIFIERReturns the current flags of the window.B_SET_PROPERTYB_DIRECT_SPECIFIERSets the window flags.
FrameThe Frame property represents the frame rectangle of the window. The frame is passed as a {cpp:class}`BRect` ({cpp:enum}`B_RECT_TYPE`).MessageSpecifiersDescriptionB_GET_PROPERTYB_DIRECT_SPECIFIERReturns the window's frame rectangle.B_SET_PROPERTYB_DIRECT_SPECIFIERSets the window's frame rectangle.
HiddenThe "Hidden" property determines the visibility of the window. The messages are equivalent to manipulating the window with the {cpp:func}`~BWindow::IsHidden`, {cpp:func}`~BWindow::Hide` and {cpp:func}`~BWindow::Show` methods with one caveat: nested {cpp:func}`~BWindow::Hide` and {cpp:func}`~BWindow::Show` calls are disabled so that multiple scripted "hides" are undone with a single scripted "show".MessageSpecifiersDescriptionB_GET_PROPERTYB_DIRECT_SPECIFIERReturns true if the window is hidden; false otherwise.B_SET_PROPERTYB_DIRECT_SPECIFIERHides or shows the window.
LookThe "Look" property represents the constant that indicates how the window appears. The messages are equivalent to manipulating the window with the {cpp:func}`~BWindow::Look` and {cpp:func}`~BWindow::SetLook` methods.MessageSpecifiersDescriptionB_GET_PROPERTYB_DIRECT_SPECIFIERReturns the current look of the window.B_SET_PROPERTYB_DIRECT_SPECIFIERSets the look of the window.
MenuBarThe "MenuBar" property pops the current specifier off the specifier stack and then passes the scripting message to the key menu bar. If no such menu b/r is present, then an error is returned.MessageSpecifiersDescriptionanyB_DIRECT_SPECIFIERDirects the scripting message to the key menu bar.
MinimizeThe "Minimize" property controls the whether the window is minimized or not. The message is equivalent to manipulating the window with the {cpp:func}`~BWindow::Minimize` method.MessageSpecifiersDescriptionB_SET_PROPERTYB_DIRECT_SPECIFIERMinimizes the window if "data" is true; restores otherwise.
TitleThe "Title" property represents the title of the window. The messages are equivalent to manipulating the window with the {cpp:func}`~BWindow::Title` and {cpp:func}`~BWindow::SetTitle` methods.MessageSpecifiersDescriptionB_DIRECT_SPECIFIERReturns a string containing the window title. B_SET_PROPERTYB_DIRECT_SPECIFIERSets the window title.
ViewThe "View" property redirects all requests to the window's top view without popping the specifier from the stack.MessageSpecifiersDescriptionanyanyDirects the scripting message to the top view without popping the current specifier.
WorkspacesThe "Workspaces" property represents the workspaces in which the window resides. The messages are equivalent to manipulating the window with the {cpp:func}`~BWindow::Workspaces` and {cpp:func}`~BWindow::SetWorkspaces` methods.MessageSpecifiersDescriptionB_GET_PROPERTYB_DIRECT_SPECIFIERReturns int32 bitfield of the workspaces in which the window appears.B_SET_PROPERTYB_DIRECT_SPECIFIERSets the workspaces in which the window appears.
::::

## Archived Fields