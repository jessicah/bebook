# BView
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BView::BView(BRect frame, const char* name, uint32 resizingMode, uint32 flags)
:::
:::{cpp:function} BView::BView(BMessage* archive)
:::

Sets up a view with the {hparam}`frame` rectangle, which is specified in the
coordinate system of its eventual parent, and assigns the {hclass}`BView` an
identifying {hparam}`name`, which can be {cpp:enum}`NULL`.

When it's created, a {hclass}`BView` doesn't belong to a window and has no parent.
It's assigned a parent by having another {hclass}`BView` adopt it with the
{cpp:func}`~BView::AddChild` function. If the other view is in a window, the {hclass}`BView` becomes
part of that window's view hierarchy. A {hclass}`BView` can be made a child of the
window's top view by calling {cpp:class}`BWindow`'s
{cpp:func}`~BWindow::AddChild` of the {hmethod}`AddChild()` function.

When the {hclass}`BView` gains a parent, the values in
{hparam}`frame` are interpreted in the
parent's coordinate system. The sides of the view must be aligned on
screen pixels. Therefore, the {hparam}`frame` rectangle should not contain
coordinates with fractional values. Fractional coordinates will be
rounded to the first lower whole number (for example 1.2 will be rounded
down to 1.0).

The {hparam}`resizingMode` mask determines the behavior of the view when its parent
is resized. It should combine one constant for horizontal resizing,

- {cpp:enum}`B_FOLLOW_LEFT`
- {cpp:enum}`B_FOLLOW_RIGHT`
- {cpp:enum}`B_FOLLOW_LEFT_RIGHT`
- {cpp:enum}`B_FOLLOW_H_CENTER`

with one for vertical resizing:

- {cpp:enum}`B_FOLLOW_TOP`
- {cpp:enum}`B_FOLLOW_BOTTOM`
- {cpp:enum}`B_FOLLOW_TOP_BOTTOM`
- {cpp:enum}`B_FOLLOW_V_CENTER`

For example, if {cpp:enum}`B_FOLLOW_LEFT` is chosen, the margin between the left side
of the view and the left side of its parent will remain
constant—the view will "follow" the parent's left side. Similarly,
if {cpp:enum}`B_FOLLOW_RIGHT` is chosen, the view will follow the parent's right
side. If {cpp:enum}`B_FOLLOW_H_CENTER` is chosen, the view will maintain a constant
relationship to the horizontal center of the parent.

If the constants name opposite sides of the view rectangle—left and
right, or top and bottom—the view will necessarily be resized in
that dimension when the parent is. For example, {cpp:enum}`B_FOLLOW_LEFT_RIGHT` means
that the margin between the left side of the view and left side of the
parent will remain constant, as will the margin between the right side of
the view and the right side of the parent. As the parent is resized
horizontally, the child will be resized with it. Note that
{cpp:enum}`B_FOLLOW_LEFT_RIGHT` is not the same as combining {cpp:enum}`B_FOLLOW_LEFT` and
{cpp:enum}`B_FOLLOW_RIGHT`, an illegal move. The {hparam}`resizingMode` mask can contain only
one horizontal constant and one vertical constant.

If a side is not mentioned in the mask, the distance between that side of
the view and the corresponding side of the parent is free to fluctuate.
This may mean that the view will move within its parent's coordinate
system when the parent is resized. {cpp:enum}`B_FOLLOW_RIGHT` plus {cpp:enum}`B_FOLLOW_BOTTOM`,
for example, would keep a view from being resized, but the view will move
to follow the right bottom corner of its parent whenever the parent is
resized. {cpp:enum}`B_FOLLOW_LEFT` plus {cpp:enum}`B_FOLLOW_TOP` prevents a view from being
resized and from being moved.

In addition to the constants listed above, there are two other
possibilities:

- {cpp:enum}`B_FOLLOW_ALL_SIDES`
- {cpp:enum}`B_FOLLOW_NONE`

{cpp:enum}`B_FOLLOW_ALL_SIDES` is a shorthand for {cpp:enum}`B_FOLLOW_LEFT_RIGHT` and
{cpp:enum}`B_FOLLOW_TOP_BOTTOM`. It means that the view will be resized in tandem
with its parent, both horizontally and vertically.

{cpp:enum}`B_FOLLOW_NONE` behaves just like
{cpp:enum}`B_FOLLOW_LEFT` | {cpp:enum}`B_FOLLOW_TOP`; the view
maintains the same position in its parent's coordinate system, but not in
the screen coordinate system.

Typically, a parent view is resized because the user resizes the window
it's in. When the window is resized, the top view is too. Depending on
how the {hparam}`resizingMode` flag is set for the top view's children and for the
descendants of its children, automatic resizing can cascade down the view
hierarchy. A view can also be resized programmatically by the
{cpp:func}`~BView::ResizeTo`
and {cpp:func}`~BView::ResizeBy`
functions.

The resizing mode can be changed after construction with the
{cpp:func}`~BView::SetResizingMode` function.

The {hparam}`flags` mask determines what kinds of notifications the {hclass}`BView` will
receive. It can be any combination of the following constants:

:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_WILL_DRAW`
	- Indicates that the {hclass}`BView` does some drawing of its own and therefore can't be ignored when the window is updated. If this flag isn't set, the {hclass}`BView` won't receive update notifications—its {cpp:func}`~BView::Draw` function won't be called—and it won't be erased to its background view color if the color is other than white.
-
	- {cpp:enum}`B_PULSE_NEEDED`
	- Indicates that the {hclass}`BView` should receive {cpp:func}`~BView::Pulse` notifications.
-
	- {cpp:enum}`B_FRAME_EVENTS`
	- Indicates that the {hclass}`BView` should receive {cpp:func}`~BView::FrameResized` and {cpp:func}`~BView::FrameMoved` notifications when its frame rectangle changes—typically as a result of the automatic resizing behavior described above. {cpp:func}`~BView::FrameResized` is called when the dimensions of the view change; {cpp:func}`~BView::FrameMoved` is called when the position of its left top corner in its parent's coordinate system changes.
-
	- {cpp:enum}`B_FULL_UPDATE_ON_RESIZE`
	- Indicates that the entire view should be updated when it's resized. If this flag isn't set, only the portions that resizing adds to the view will be included in the clipping region. This doesn't affect the view's children; their own flags determine when updates will occur.
-
	- {cpp:enum}`B_NAVIGABLE`
	- Indicates that the {hclass}`BView` can become the focus view for keyboard actions. This flag makes it possible for the user to navigate to the view and put it in focus by pressing the Tab key. See "{cpp:func}`~TheInterfaceKit::Listening`" at the beginning of this chapter.
-
	- {cpp:enum}`B_NAVIGABLE_JUMP`
	- Marks the position of a group of views for keyboard navigation. By pressing Control+Tab, the user can jump from group to group. The focus lands on the first {hclass}`BView` in the group that has the {cpp:enum}`B_NAVIGABLE` flag set. This may be the same {hclass}`BView` that has the {cpp:enum}`B_NAVIGABLE_JUMP` marker, or the {cpp:enum}`B_NAVIGABLE_JUMP` {hclass}`BView` may be the parent of a group of {cpp:enum}`B_NAVIGABLE` views.
-
	- {cpp:enum}`B_SUBPIXEL_PRECISE`
	- Instructs the rendering methods to use subpixel precision when drawing. If you don't set this flag, coordinates are rounded to the nearest unit.
:::

If none of these constants apply, {hparam}`flags` can be
{cpp:enum}`NULL`. The flags can be
reset after construction with the
{cpp:func}`~BView::SetFlags` function.

See also:
{cpp:func}`BHandler::SetName`

::::

::::{abi-group}

:::{cpp:function} virtual BView::~BView()
:::

Frees all memory the {hclass}`BView` allocated, and ensures that each of the
{hclass}`BView`'s descendants in the view hierarchy is also destroyed.

It's an error to delete a {hclass}`BView` while it remains attached to a window.
Call
{cpp:func}`~BView::RemoveChild` or
{cpp:func}`~BView::RemoveSelf`
before using the delete operator.

::::

## Hook Functions
::::{abi-group}

:::{cpp:function} virtual void BView::AttachedToWindow()
:::
:::{cpp:function} virtual void BView::AllAttached()
:::

Implemented by derived classes to complete the initialization of the
{hclass}`BView` when it's assigned to a window.
A {hclass}`BView` is assigned to a window
when it, or one of its ancestors in the view hierarchy, becomes a child
of a view already attached to a window.

{hmethod}`AttachedToWindow()` is called immediately
after the {hclass}`BView` is formally made
a part of the window's view hierarchy and after it has become known to
the Application Server and its graphics parameters are set. The
{cpp:func}`~BView::Window`
function can identify which
{cpp:class}`BWindow` the
{hclass}`BView` belongs to.

All of the {hclass}`BView`'s children, if it has any, also become attached to the
window and receive their own {hmethod}`AttachedToWindow()` notifications. Parents
receive the notification before their children, but only after all views
have become attached to the window and recognized as part of the window's
view hierarchy. This function can therefore depend on all ancestor and
descendant views being in place.

For example, {hmethod}`AttachedToWindow()` can be implemented to set a view's
background color to the same color as its parent, something that can't be
done before the view belongs to a window and knows who its parent is.

:::{code}
void MyView::AttachedToWindow()
{
   if ( Parent() )
      SetViewColor(Parent()->ViewColor());
   baseClass::AttachedToWindow();
}
:::

The {hmethod}`AllAttached()` notification follows on the heels of
{hmethod}`AttachedToWindow()`, but works its way up the view hierarchy rather than
down. When {hmethod}`AllAttached()` is called for a
{hclass}`BView`, all its descendants have
received both {hmethod}`AttachedToWindow()` and
{hmethod}`AllAttached()` notifications.
Therefore, parent views can depend on any calculations that their
children make in either function. For example, a parent can resize itself
to fit the size of its children, where their sizes depend on calculations
done in {hmethod}`AttachedToWindow()`.

The default ({hclass}`BView`) version of both these functions are empty.

See also:
{cpp:func}`~BView::AddChild`

::::

::::{abi-group}

:::{cpp:function} virtual void BView::DetachedFromWindow()
:::
:::{cpp:function} virtual void BView::AllDetached()
:::

Implemented by derived classes to make any adjustments necessary when the
{hclass}`BView` is about to be removed from a window's view hierarchy. These two
functions parallel the more commonly implemented
{cpp:func}`~BView::AttachedToWindow` and
{cpp:func}`~BView::AllAttached` functions.

{hmethod}`DetachedFromWindow()` notifications work their way down the hierarchy of
views being detached, followed by {hmethod}`AllDetached()` notifications, which work
their way up the hierarchy. The second function call permits an ancestor
view to take actions that depend on calculations a descendant might have
to make when it's first notified of being detached.

The {hclass}`BView` is still attached to the window when both functions are called.

::::

::::{abi-group}

:::{cpp:function} virtual void BView::Draw(BRect updateRect)
:::

Implemented by derived classes to draw the {hparam}`updateRect` portion of the
view. The update rectangle is stated in the {hclass}`BView`'s coordinate system.

{hmethod}`Draw()` is called as the result of update messages whenever the view needs
to present itself on-screen. This may happen when:

- The window the view is in is first shown on-screen, or shown after being hidden (see the {cpp:class}`BWindow` version of the {cpp:func}`~BWindow::Hide` function).
- The view is made visible after being hidden (see {hclass}`BView`'s {cpp:func}`~BView::Hide` function).
- Obscured parts of the view are revealed, as when a window is moved from in front of the view or an image is dragged across it.
- The view is resized.
- The contents of the view are scrolled (see {cpp:func}`~BView::ScrollBy`).
- A child view is added, removed, or resized.
- A rectangle has been invalidated that includes at least some of the view (see {cpp:func}`~BView::Invalidate`).
- {cpp:func}`~BView::CopyBits` can't completely fill a destination rectangle within the view.

{hmethod}`Draw()` is also called from a
{cpp:class}`BPrintJob` object's
{cpp:func}`~BPrintJob::DrawView` function to
draw the view on a printed page.
{cpp:func}`~BView::IsPrinting`
returns {cpp:enum}`true` when the
{cpp:class}`BView`
is drawing for the printer and {cpp:enum}`false` when it's drawing to the screen.
When printing, you may want to recalculate layouts, substitute fonts,
turn antialiasing off, scale the size of a coordinate unit, or make other
adjustments to ensure the quality of the printed image.

When drawing to the screen, the {hparam}`updateRect` is the smallest rectangle that
encloses the current clipping region for the view. Since the Application
Server won't render anything on-screen that's outside the clipping
region, an application will be more efficient if it avoids producing
drawing instructions for images that don't intersect with the rectangle.
For still more efficiency and precision, you can ask for the clipping
region itself (by calling
{cpp:func}`~BView::GetClippingRegion`)
and confine drawing to images that intersect with it.

When printing, the {hparam}`updateRect` matches the rectangle passed to
{cpp:func}`~BPrintJob::DrawView`
and may lie outside the clipping region. The clipping region is not
enforced for printing, but the Print Server clips the BView's drawing to
the specified rectangle.

See also:
{cpp:func}`BWindow::UpdateIfNeeded`

::::

::::{abi-group}

:::{cpp:function} virtual void BView::DrawAfterChildren(BRect updateRect)
:::

This function is similar (in fact, almost identical) to
{cpp:func}`~BView::Draw`. The only
difference is that {hmethod}`DrawAfterChildren()`
is called after all children have drawn during a screen update.
This is in contrast to {cpp:func}`~BView::Draw`,
which draws before any children have drawn. In general,
{cpp:func}`~BView::Draw` will be used for
almost all of your drawing needs; {hmethod}`DrawAfterChildren()` is intended for use
in the rare circumstances where you wish a view to be able to draw on top
of its child views.

Other details are as for {cpp:func}`~BView::Draw`.

::::

::::{abi-group}

:::{cpp:function} virtual void BView::FrameMoved(BPoint newLocation)
:::

Implemented by derived classes to respond to a notification that the view
has moved within its parent's coordinate system. {hparam}`newLocation` gives the
new location, within the coordinate system of the view's window, of the
left top corner of the {hclass}`BView`'s frame rectangle.

{hmethod}`FrameMoved()` is called only if the
{cpp:enum}`B_FRAME_EVENTS` flag is set and the
{hclass}`BView` is attached to a window.

If the view is both moved and resized, {hmethod}`FrameMoved()` is called before
{cpp:func}`~BView::FrameResized`.
This might happen, for example, if the {hclass}`BView`'s automatic
resizing mode is a combination of {cpp:enum}`B_FOLLOW_TOP_BOTTOM`
and {cpp:enum}`B_FOLLOW_RIGHT`
and its parent is resized both horizontally and vertically.

{hclass}`BView`'s version of this function is empty.

Currently, {hmethod}`FrameMoved()` is also called when a hidden window is shown
on-screen.

See also:
{cpp:func}`~BView::MoveBy`,
{cpp:func}`BWindow::FrameMoved`,
{cpp:func}`~BView::SetFlags`

::::

::::{abi-group}

:::{cpp:function} virtual void BView::FrameResized(float width, float height)
:::

Implemented by derived classes to respond to a notification that the view
has been resized. The arguments state the new width and height of the
view. The resizing could have been the result of a user action (resizing
the window) or of a programmatic one (calling
{cpp:func}`~BView::ResizeTo` or
{cpp:func}`~BView::ResizeBy`).

{hmethod}`FrameResized()` is called only if the
{cpp:enum}`B_FRAME_EVENTS` flag is set and the
{hclass}`BView` is attached to a window.

{hclass}`BView`'s version of this function is empty.

See also:
{cpp:func}`BWindow::FrameResized`,
{cpp:func}`~BView::SetFlags`

::::

::::{abi-group}

:::{cpp:function} virtual void BView::GetPreferredSize(float* width, float* height)
:::
:::{cpp:function} virtual void BView::ResizeToPreferred()
:::

{hmethod}`GetPreferredSize()` is implemented by derived classes to write the
preferred width and height of the view into the variables the {hparam}`width` and
{hparam}`height` arguments refer to. Derived classes generally make this
calculation based on the view's contents. For example, a
{cpp:class}`BButton` object
reports the optimal size for displaying the button border and label given
the current font.

{hmethod}`ResizeToPreferred()` resizes the
{hclass}`BView`'s frame rectangle to the preferred
size, keeping its left and top sides constant.

See also:
{cpp:func}`~BView::ResizeTo`

::::

::::{abi-group}

:::{cpp:function} virtual void BView::KeyDown(const char* bytes, int32 numBytes)
:::

Implemented by derived classes to respond to a
{cpp:func}`~B::KEY` message
reporting keyboard input. Whenever a {hclass}`BView` is the focus view of the
active window, it receives a {hmethod}`KeyDown()` notification for each character
the user types, except for those that:

- Are produced while a Command key is held down. Command key events are interpreted as keyboard shortcuts.
- Are produced by the Tab key when an Option key is held down. Option+Tab events are invariably interpreted as instructions to change the focus view (for keyboard navigation); they work even where Tab alone does not.
- Can operate the default button in a window. The {cpp:class}`BButton` object's {cpp:func}`~BButton::KeyDown` function is called, rather than the focus view's.

The first argument, {hparam}`bytes`, is an array that encodes the character mapped
to the key the user pressed. The second argument, {hparam}`numBytes`, tells how
many bytes are in the array; there will always be at least one. The {hparam}`bytes`
value follows the character encoding of the {hclass}`BView`'s font. Typically, the
encoding is Unicode UTF-8 ({cpp:enum}`B_UNICODE_UTF8`), so there may be more than one
byte per character. The bytes array is not null-terminated; '0' is a
valid character value.

The character value takes into account any modifier keys that were held
down or keyboard locks that were on at the time of the keystroke. For
example, Shift+i
is reported as uppercase 'I' (0x49) and
Control+i is
reported as a {cpp:enum}`B_TAB` (0x09).

Single-byte characters can be tested against
ASCII
codes and these constants:

- {cpp:enum}`B_BACKSPACE`
- {cpp:enum}`B_ENTER`
- {cpp:enum}`B_RETURN`
- {cpp:enum}`B_SPACE`
- {cpp:enum}`B_TAB`
- {cpp:enum}`B_ESCAPE`
- {cpp:enum}`B_LEFT_ARROW`
- {cpp:enum}`B_RIGHT_ARROW`
- {cpp:enum}`B_UP_ARROW`
- {cpp:enum}`B_DOWN_ARROW`
- {cpp:enum}`B_INSERT`
- {cpp:enum}`B_DELETE`
- {cpp:enum}`B_HOME`
- {cpp:enum}`B_END`
- {cpp:enum}`B_PAGE_UP`
- {cpp:enum}`B_PAGE_DOWN`
- {cpp:enum}`B_FUNCTION_KEY`

{cpp:enum}`B_ENTER` and {cpp:enum}`B_RETURN`
are the same character, a newline ('\n').

Only keys that generate characters produce key-down events; the modifier
keys on their own do not.

You can determine which modifier keys were being held down at the time of
the event by calling
{cpp:class}`BLooper`'s
{cpp:func}`~BLooper::CurrentMessage`
function and looking up the "modifiers" entry in the
{cpp:class}`BMessage`
it returns. If the {hparam}`bytes` character
is {cpp:enum}`B_FUNCTION_KEY` and you want to know which key produced the character,
you can look up the "key" entry in the
{cpp:class}`BMessage`
and test it against these constants:

- {cpp:enum}`B_F1_KEY`
- {cpp:enum}`B_F1_KEY`
- {cpp:enum}`B_F2_KEY`
- {cpp:enum}`B_F3_KEY`
- {cpp:enum}`B_F4_KEY`
- {cpp:enum}`B_F5_KEY`
- {cpp:enum}`B_F6_KEY`
- {cpp:enum}`B_F7_KEY`
- {cpp:enum}`B_F8_KEY`
- {cpp:enum}`B_F9_KEY`
- {cpp:enum}`B_F10_KEY`
- {cpp:enum}`B_F11_KEY`
- {cpp:enum}`B_F12_KEY`
- {cpp:enum}`B_PRINT_KEY` (Print Screen)
- {cpp:enum}`B_SCROLL_KEY` (Scroll Lock)
- {cpp:enum}`B_PAUSE_KEY`

For example:

:::{code}
if ( bytes[0] == B_FUNCTION_KEY ) {
   BMessage *msg = Window()->CurrentMessage();
   if ( msg ) {
      int32 key;
      msg->FindInt32("key", &key);
      switch ( key ) {
      case B_F1_KEY:
         . . .
         break;
      case B_F2_KEY:
         . . .
         break;
      . . .
      }
   }
}
:::

The {hclass}`BView` version of {hmethod}`KeyDown()`
handles keyboard navigation from view to view through
{cpp:enum}`B_TAB` characters. If the view you define is navigable, its
{hmethod}`KeyDown()` function should permit
{cpp:enum}`B_SPACE` characters to operate the object
and perhaps allow the arrow keys to navigate inside the view. It should
also call the inherited version of
{hmethod}`KeyDown()` to enable between-view
navigation. For example:

:::{code}
void MyView::KeyDown(const char *bytes, int32 numBytes)
{
   if ( numBytes == 1 ) {
      switch ( bytes[0] ) {
      case B_SPACE:
         /* mimic a click in the view*/
         break;
      case B_RIGHT_ARROW:
         /* move one position to the right in the view*/
         break;
      case B_LEFT_ARROW:
         /* move one position to the left in the view*/
         break;
      default:
         baseClass::KeyDown(bytes, numBytes);
         break;
      }
   }
}
:::

If your {hclass}`BView` is navigable but needs to respond to {cpp:enum}`B_TAB`
characters—for example, if it permits users to insert tabs in a
text string—its {hmethod}`KeyDown()` function should simply grab the
characters and not pass them to the inherited function. Users will have
to rely on the
Option+Tab
combination to navigate from your view.

See also: the {ref}`Keyboard Information` special topic,
{cpp:func}`~B::KEY` in the
{ref}`Keyboard Messages` appendix,
{cpp:func}`BWindow::SetDefaultButton`,
{ref}`modifiers()`

::::

::::{abi-group}

:::{cpp:function} virtual void BView::KeyUp(const char* bytes, int32 numBytes)
:::

Implemented by derived classes to respond to a
{cpp:func}`~B::KEY`
message reporting that the user released a key on the keyboard.
The same set of keys that produce
{cpp:func}`~B::KEY`
messages when they're pressed produce
{cpp:func}`~B::KEY`
messages when they're released. The {hparam}`bytes`
and {hparam}`numBytes` arguments encode
the character mapped to the key the user released; they work exactly like
the same arguments passed to
{cpp:func}`~BView::KeyDown`.

Some {cpp:func}`~B::KEY`
messages are swallowed by the system and are never dispatched by calling
{cpp:func}`~BView::KeyDown`;
others are dispatched, but not to the focus view. In contrast, all
{cpp:func}`~B::KEY`
messages are dispatched by calling
{cpp:func}`~BView::KeyUp`
for the focus view of the active window. Since the focus view and
active window can change between the time a key is pressed and the time
it's released, this may or may not be the same {hclass}`BView` that was notified of
the {cpp:func}`~B::KEY`
message.

::::

::::{abi-group}

:::{cpp:function} virtual void BView::MessageReceived(BMessage* message)
:::

Augments the
{cpp:class}`BHandler` version of
{cpp:func}`~BHandler::MessageReceived`
to handle scripting messages for the {hclass}`BView`.

::::

::::{abi-group}

:::{cpp:function} virtual void BView::MouseDown(BPoint point)
:::

{hmethod}`MouseDown()` is a hook function that's invoked when the user depresses a
mouse button (or other pointing device button, not including joysticks).
The location of the cursor at the time of the event is given by {hparam}`point` in
the {hclass}`BView`'s coordinates. See
{cpp:func}`~B::MOUSE`
for the message format. Also see
{cpp:func}`~BView::SetMouseEventMask`
for information on extending the view's event mask while the mouse is being held down.

The {hclass}`BView` version of {hmethod}`MouseDown()` is empty.

::::

::::{abi-group}

:::{cpp:function} virtual void BView::MouseMoved(BPoint point, uint32 transit, const BMessage* message)
:::

Implemented by derived classes to respond to reports of mouse-moved
events associated with the view. As the user moves the cursor over a
window, the Application Server generates a continuous stream of messages
reporting where the cursor is located.

The first argument, {hparam}`point`, gives the cursor's
new location in the {hclass}`BView`'s
coordinate system. The second argument, {hparam}`transit`, is one of four constants,

- {cpp:enum}`B_ENTERED_VIEW`
- {cpp:enum}`B_INSIDE_VIEW`
- {cpp:enum}`B_EXITED_VIEW`
- {cpp:enum}`B_OUTSIDE_VIEW`

which explains whether the cursor has just entered the visible region of
the view, is now inside the visible region having previously entered, has
just exited from the view, or is currently outside the visible region of
the view. When the cursor passes from one view to another, {hmethod}`MouseMoved()`
is called on each of the {hclass}`BView`s, once with a transit code of
{cpp:enum}`B_EXITED_VIEW` and the other with a code of {cpp:enum}`B_ENTERED_VIEW`.

If the user is dragging a bundle of information from one location to
another, the final argument, {hparam}`message`, is a pointer to the
{cpp:class}`BMessage` object
that holds the information. If a message isn't being dragged,
{hparam}`message` is {cpp:enum}`NULL`.

The default version of {hmethod}`MouseMoved()` is empty.

::::

::::{abi-group}

:::{cpp:function} virtual void BView::MouseUp(BPoint point)
:::

Implemented by derived classes to respond to a message reporting a
mouse-up event within the view. The location of the cursor at the time of
the event is given by {hparam}`point` in the {hclass}`BView`'s coordinates.

::::

::::{abi-group}

:::{cpp:function} virtual void BView::Pulse()
:::

Implemented by derived classes to do something at regular intervals.
Pulses are regularly timed events, like the tick of a clock or the beat
of a steady pulse. A {hclass}`BView` receives
{hmethod}`Pulse()` notifications when no other
messages are pending, but only if it asks for them with the
{cpp:enum}`B_PULSE_NEEDED` flag.

The interval between {hmethod}`Pulse()` calls can be set with
{cpp:class}`BWindow`'s
{cpp:func}`~BWindow::SetPulseRate`
function. The default interval is around 500 milliseconds.
The pulse rate is the same for all views within a window, but can vary
between windows.

Derived classes can implement a {hmethod}`Pulse()` function to do something that
must be repeated continuously. However, for time-critical actions, you
should implement your own timing mechanism.

The {hclass}`BView` version of this function is empty.

See also:
{cpp:func}`~BView::SetFlags`
the {hclass}`BView`
{cpp:func}`~BView::Constructor`,

::::

::::{abi-group}

:::{cpp:function} virtual void BView::TargetedByScrollView(BScrollView* scroller)
:::

Implemented by derived classes to respond to a notification that the
{hclass}`BView` has become the target of the scroller
{cpp:class}`BScrollView`
object. This function is called when the
{cpp:class}`BScrollView`
sets its target, which it does on
construction. The target is the object whose contents will be scrolled.

{hclass}`BView`'s implementation of this function is empty.

See also: The various scrolling-related
functions in {hclass}`BView`
{cpp:func}`~BView::Input`.

::::

::::{abi-group}

:::{cpp:function} virtual void BView::WindowActivated(bool active)
:::

Implemented by derived classes to take whatever steps are necessary when
the {hclass}`BView`'s window becomes the active window, or when the window gives up
that status. If {hparam}`active` is {cpp:enum}`true`,
the window has become active. If {hparam}`active`
is {cpp:enum}`false`, it no longer is the active window.

All objects in the view hierarchy receive
{hmethod}`WindowActivated()`
notifications when the status of the window changes.

{hclass}`BView`'s version of this function is empty.

See also:
{cpp:func}`BWindow::WindowActivated`

::::

## General Functions
::::{abi-group}

:::{cpp:function} virtual status_t BView::Archive(BMessage* archive, bool deep = true) const
:::

Archives the {hclass}`BView` in the
{cpp:class}`BMessage` {hparam}`archive`.

See also:
{cpp:func}`BArchivable::Archive`,
{cpp:func}`~BView::Instantiate` static function

::::

::::{abi-group}

:::{cpp:function} BRect BView::Bounds() const
:::

Returns the {hclass}`BView`'s bounds rectangle.

::::

::::{abi-group}

:::{cpp:function} BPoint BView::ConvertToParent(BPoint localPoint) const
:::
:::{cpp:function} void BView::ConvertToParent(BPoint* localPoint) const
:::
:::{cpp:function} BRect BView::ConvertToParent(BRect localRect) const
:::
:::{cpp:function} void BView::ConvertToParent(BRect* localRect) const
:::
:::{cpp:function} BPoint BView::ConvertFromParent(BPoint parentPoint) const
:::
:::{cpp:function} void BView::ConvertFromParent(BPoint* parentPoint) const
:::
:::{cpp:function} BRect BView::ConvertFromParent(BRect parentRect) const
:::
:::{cpp:function} void BView::ConvertFromParent(BRect* parentRect) const
:::

These functions convert points and rectangles to and from the coordinate
system of the {hclass}`BView`'s parent.
{hmethod}`ConvertToParent()` converts {hparam}`localPoint` or
{hparam}`localRect` from the {hclass}`BView`'s coordinate system to the coordinate system of
its parent {hclass}`BView`.
{hmethod}`ConvertFromParent()` does the opposite; it converts
{hparam}`parentPoint` or {hparam}`parentRect` from the coordinate system of the {hclass}`BView`'s
parent to the {hclass}`BView`'s own coordinate system.

If the point or rectangle is passed by value, the function returns the
converted value. If a pointer is passed, the conversion is done in place.

Both functions fail if the {hclass}`BView` isn't attached to a window.

See also:
{cpp:func}`~BView::ConvertToScreen`

::::

::::{abi-group}

:::{cpp:function} BPoint BView::ConvertToScreen(BPoint localPoint) const
:::
:::{cpp:function} void BView::ConvertToScreen(BPoint* localPoint) const
:::
:::{cpp:function} BRect BView::ConvertToScreen(BRect localRect) const
:::
:::{cpp:function} void BView::ConvertToScreen(BRect* localRect) const
:::
:::{cpp:function} BPoint BView::ConvertFromScreen(BPoint screenPoint) const
:::
:::{cpp:function} void BView::ConvertFromScreen(BPoint* screenPoint) const
:::
:::{cpp:function} BRect BView::ConvertFromScreen(BRect screenRect) const
:::
:::{cpp:function} void BView::ConvertFromScreen(BRect* screenRect) const
:::

{hmethod}`ConvertToScreen()` converts
{hparam}`localPoint` or {hparam}`localRect` from the {hclass}`BView`'s
coordinate system to the global screen coordinate system.
{hmethod}`ConvertFromScreen()` makes the opposite conversion; it converts
{hparam}`screenPoint` or {hparam}`screenRect` from the screen coordinate system to the
{hclass}`BView`'s local coordinate system.

If the point or rectangle is passed by value, the function returns the
converted value. If a pointer is passed, the conversion is done in place.

The screen coordinate system has its origin, (0.0, 0.0), at the left top
corner of the main screen.

Neither function will work if the {hclass}`BView` isn't attached to a window.

See also:
{cpp:func}`BWindow::ConvertToScreen`,
{cpp:func}`~BView::ConvertToParent`

::::

::::{abi-group}

:::{cpp:function} BRect BView::Frame() const
:::

Returns the {hclass}`BView`'s frame rectangle. The frame rectangle is first set by
the {hclass}`BView` constructor and is altered only when the view is moved or
resized. It's stated in the coordinate system of the {hclass}`BView`'s parent.

::::

::::{abi-group}

:::{cpp:function} virtual void BView::Hide()
:::
:::{cpp:function} virtual void BView::Show()
:::

These functions hide a view and show it again.

{hmethod}`Hide()` makes the view invisible without removing it from the view
hierarchy. The visible region of the view will be empty and the {hclass}`BView`
won't receive update messages. If the {hclass}`BView` has children, they also are
hidden.

{hmethod}`Show()` unhides a view that had been hidden. This function doesn't
guarantee that the view will be visible to the user; it merely undoes the
effects of {hmethod}`Hide()`. If the view didn't have any visible area before being
hidden, it won't have any after being shown again (given the same
conditions).

Calls to {hmethod}`Hide()` and {hmethod}`Show()`
can be nested. For a hidden view to become
visible again, the number of {hmethod}`Hide()` calls must be matched by an equal
number of {hmethod}`Show()` calls.

However, {hmethod}`Show()` can only undo a previous {hmethod}`Hide()` call on the same view. If
the view became hidden when {hmethod}`Hide()` was called to hide the window it's in
or to hide one of its ancestors in the view hierarchy, calling {hmethod}`Show()` on
the view will have no effect. For a view to come out of hiding, its
window and all its ancestor views must be unhidden.

{hmethod}`Hide()` and {hmethod}`Show()`
can affect a view before it's attached to a window. The
view will reflect its proper state (hidden or not) when it becomes
attached. Views are created in an unhidden state.

See also:
{cpp:func}`BWindow::Hide`,
{cpp:func}`~BView::IsHidden`

::::

::::{abi-group}

:::{cpp:function} bool BView::IsFocus()
:::

Returns {cpp:enum}`true` if the {hclass}`BView`
is the current focus view for its window, and
{cpp:enum}`false` if it's not. The focus view changes as the user chooses one view to
work in and then another—for example, as the user moves from one
text field to another when filling out an on-screen form. The change is
made programmatically through the
{cpp:func}`~BView::MakeFocus` function.

See also:
{cpp:func}`BWindow::CurrentFocus`

::::

::::{abi-group}

:::{cpp:function} bool BView::IsHidden()
:::

Returns {cpp:enum}`true` if the view has been hidden by the
{cpp:func}`~BView::Hide` function, and
{cpp:enum}`false` otherwise.

This function returns {cpp:enum}`true` whether
{cpp:func}`~BView::Hide`
was called to hide the {hclass}`BView`
itself, to hide an ancestor view, or to hide the {hclass}`BView`'s window. When a
window is hidden, all its views are hidden with it. When a {hclass}`BView` is
hidden, all its descendants are hidden with it.

If the view has no visible region—perhaps because it lies outside
its parent's frame rectangle or is obscured by a window in
front—this function may nevertheless return {cpp:enum}`false`. It reports only
whether the {cpp:func}`~BView::Hide`
function has been called to hide the view, hide one of
the view's ancestors in the view hierarchy, or hide the window where the
view is located.

If the {hclass}`BView` isn't attached to a window,
{hmethod}`IsHidden()` returns the state
that it will assume when it becomes attached. By default, views are not
hidden.

::::

::::{abi-group}

:::{cpp:function} bool BView::IsPrinting() const
:::

Returns {cpp:enum}`true` if the {hclass}`BView`
is being asked to draw for the printer, and
{cpp:enum}`false` if the drawing it produces will be rendered on-screen (or if the
{hclass}`BView` isn't being asked to draw at all).

This function's result is only reliable when called from within
{cpp:func}`~BView::Draw` or
{cpp:func}`~BView::DrawAfterChildren`
to determine whether the drawing it does is destined for
the printer or the screen. When drawing to the printer, the {hclass}`BView` may
choose different parameters—such as fonts, bitmap images, or
colors—than when drawing to the screen.

:::{admonition} Note
:class: note
You should avoid calling this function from outside
{cpp:func}`~BView::Draw` and
{cpp:func}`~BView::DrawAfterChildren`;
however, if you absolutely have to do it, lock the view
first. Failure to do so may bring up the debugger—if not in BeOS 5,
it may in future versions of BeOS.
:::

See also:
the {cpp:class}`BPrintJob` class

::::

::::{abi-group}

:::{cpp:function} BPoint BView::LeftTop() const
:::

Returns the coordinates of the left top corner of the view—the
smallest x and y coordinate values within the bounds rectangle.

See also:
{cpp:func}`BRect::LeftTop`,
{cpp:func}`~BView::Bounds`

::::

::::{abi-group}

:::{cpp:function} void BView::MoveBy(float horizontal, float vertical)
:::
:::{cpp:function} void BView::MoveTo(BPoint point)
:::
:::{cpp:function} void BView::MoveTo(float x, float y)
:::

These functions move the view in its parent's coordinate system without
altering its size.

{hmethod}`MoveBy()` adds {hparam}`horizontal` coordinate units to the left and right
components of the frame rectangle and {hparam}`vertical` units to the top and
bottom components. If {hparam}`horizontal` and
{hparam}`vertical` are positive, the view
moves downward and to the right. If they're negative, it moves upward and
to the left.

{hmethod}`MoveTo()` moves the upper left corner of the view
to {hparam}`point` or to ({hparam}`x`, {hparam}`y`)
in the parent view's coordinate system and adjusts all
coordinates in the frame rectangle accordingly.

Neither function alters the {hclass}`BView`'s bounds rectangle or coordinate system.

None of the values passed to these functions should specify fractional
coordinates; the sides of a view must line up on screen pixels.
Fractional values will be rounded to the closest whole number.

If the {hclass}`BView` is attached to a window, these functions cause its parent
view to be updated, so the {hclass}`BView` is immediately displayed in its new
location. If it doesn't have a parent or isn't attached to a window,
these functions merely alter its frame rectangle.

See also:
{cpp:func}`~BView::FrameMoved`,
{cpp:func}`~BView::ResizeBy`,
{cpp:func}`~BView::Frame`

::::

::::{abi-group}

:::{cpp:function} void BView::ResizeBy(float horizontal, float vertical)
:::
:::{cpp:function} void BView::ResizeTo(float width, float height)
:::

These functions resize the view, without moving its left and top sides.
{hmethod}`ResizeBy()` adds {hparam}`horizontal`
coordinate units to the width of the view and
{hparam}`vertical` units to the height.
{hmethod}`ResizeTo()` makes the view {hparam}`width` units wide
and {hparam}`height` units high. Both functions adjust the right and bottom
components of the frame rectangle accordingly.

Since a {hclass}`BView`'s frame rectangle must be aligned on screen pixels, only
integral values should be passed to these functions. Values with
fractional components will be rounded to the nearest whole integer.

If the {hclass}`BView` is attached to a window, these functions cause its parent
view to be updated, so the {hclass}`BView` is immediately displayed in its new
size. If it doesn't have a parent or isn't attached to a window, these
functions merely alter its frame and bounds rectangles.

:::{admonition} Note
:class: note
If the view isn't attached to a window, its frame and bounds rectangles
are adjusted, but its children, if any, don't get corresponding
adjustments.
:::

See also:
{cpp:func}`~BView::FrameResized`,
{cpp:func}`~BView::MoveBy`,
{cpp:func}`~BView::Frame`,
{cpp:func}`BRect::Width`

::::

::::{abi-group}

:::{cpp:function} virtual void BView::SetFlags(uint32 mask)
:::
:::{cpp:function} uint32 BView::Flags() const
:::

These functions set and return the flags that inform the Application
Server about the kinds of notifications the {hclass}`BView` should receive. The
mask set by {hmethod}`SetFlags()` and the return value of
{hmethod}`Flags()` is formed from
combinations of the following constants:

- {cpp:enum}`B_WILL_DRAW`
- {cpp:enum}`B_FULL_UPDATE_ON_RESIZE`
- {cpp:enum}`B_FRAME_EVENTS`
- {cpp:enum}`B_PULSE_NEEDED`
- {cpp:enum}`B_NAVIGABLE`
- {cpp:enum}`B_NAVIGABLE_JUMP`
- {cpp:enum}`B_SUBPIXEL_PRECISE`

The flags are first set when the {hclass}`BView` is constructed; they're explained
in the description of the {hclass}`BView` constructor. The mask can be 0.

To set just one of the flags, combine it with the current setting:

:::{code}
myView->SetFlags(Flags() | B_FRAME_EVENTS);
:::

See also:
The {hclass}`BView` {cpp:func}`~BView::Constructor`,
{cpp:func}`~BView::SetResizingMode`

::::

::::{abi-group}

:::{cpp:function} void BView::SetOrigin(BPoint pt)
:::
:::{cpp:function} void BView::SetOrigin(float x, float y)
:::
:::{cpp:function} BPoint BView::Origin() const
:::

Sets and retrieves the local origin of the {hclass}`BView`'s coordinate system.

The actual origin used by the Application Server is the sum of the local
origin (as set by this method) and the origins stored on the state stack
(properly scaled).

::::

::::{abi-group}

:::{cpp:function} virtual void BView::SetResizingMode(uint32 mode)
:::
:::{cpp:function} uint32 BView::ResizingMode() const
:::

These functions set and return the {hclass}`BView`'s automatic
resizing mode. The resizing mode is first set when the
{hclass}`BView` is constructed. The various possible modes are
explained where the {cpp:func}`~BView::Constructor` is
described.

See also:
{cpp:func}`~BView::SetFlags`

::::

::::{abi-group}

:::{cpp:function} void BView::SetViewCursor(const BCursor* cursor, bool sync = true) const
:::

Sets the specified {hparam}`cursor` as the view's cursor; while the mouse is inside
the view, this cursor will be displayed (unless of course the cursor is
hidden or obscured).

If {hparam}`sync` is {cpp:enum}`true`, the
Application Server will be synchronized by this call, forcing the change to
take place immediately. If {hparam}`sync` is
{cpp:enum}`false`, the change will take place when the Application
Server naturally gets to the change in its queue of pending requests.

::::

::::{abi-group}

:::{cpp:function} BWindow* BView::Window() const
:::

Returns the {cpp:class}`BWindow`
to which the {hclass}`BView` belongs, or {cpp:enum}`NULL`
if the {hclass}`BView`
isn't attached to a window. This function returns the same object that
{cpp:func}`~BHandler::Looper`
(inherited from the {cpp:class}`BHandler`
class) does—except that
{hmethod}`Window()` returns it more specifically as a pointer to a
{cpp:class}`BWindow` and
{cpp:func}`~BHandler::Looper`
returns it more generally as a pointer to a
{cpp:class}`BLooper`.

See also:
{cpp:func}`BHandler::Looper` in the Application Kit,
{cpp:func}`~BView::AddChild`,
{cpp:func}`BWindow::AddChild`,
{cpp:func}`~BView::AttachedToWindow`

::::

## View Hierarchy Functions
::::{abi-group}

:::{cpp:function} void BView::AddChild(BView* aView, BView* sibling = NULL)
:::
:::{cpp:function} bool BView::RemoveChild(BView* aView)
:::

{hmethod}`AddChild()` makes {hparam}`aView` a
child of the {hclass}`BView`, provided that {hparam}`aView` doesn't
already have a parent. The new child is added to the
{hclass}`BView`'s list of children immediately before the
named {hparam}`sibling` {hclass}`BView`. If the
{hparam}`sibling` is {cpp:enum}`NULL` (as it is by
default), {hparam}`aView` isn't added in front of any other
view—in other words, it's added to the end of the list. If the
{hclass}`BView` is attached to a window,
{hparam}`aView` and all its descendants become attached to the
same window. Each of them is notified of this change through
{cpp:func}`~BView::AttachedToWindow` and
{cpp:func}`~BView::AllAttached`
function calls.

{hmethod}`AddChild()` fails if {hparam}`aView`
already belongs to a view hierarchy. A view can
live with only one parent at a time. It also fails if sibling is not
already a child of the {hclass}`BView`.

{hmethod}`RemoveChild()` severs the link between the
{hclass}`BView` and {hparam}`aView`, so that {hparam}`aView`
is no longer a child of the {hclass}`BView`;
{hparam}`aView` retains all its own children and
descendants, but they become an isolated fragment of a view hierarchy,
unattached to a window. Each removed view is notified of this change
through
{cpp:func}`~BView::DetachedFromWindow` and
{cpp:func}`~BView::AllDetached`
function calls.

A {hclass}`BView` must be removed from a window before it can be destroyed.

If it succeeds in removing {hparam}`aView`, {hmethod}`RemoveChild()`
returns {cpp:enum}`true`. If it
fails, it returns {cpp:enum}`false`. It will fail if {hparam}`aView`
is not, in fact, a current child of the {hclass}`BView`.

When a {hclass}`BView` object becomes attached to a
{cpp:class}`BWindow`, two other connections
are automatically established for it:

- The view is added to the {cpp:class}`BWindow`'s flat list of {cpp:class}`BHandler` objects, making it an eligible target for messages the {cpp:class}`BWindow` dispatches.
- The {hclass}`BView`'s parent view becomes its next handler. Messages that the {hclass}`BView` doesn't recognize will be passed to its parent.

Removing a {hclass}`BView` from a window's view hierarchy also removes it from the
{cpp:class}`BWindow`'s flat list of
{cpp:class}`BHandler`
objects; the {hclass}`BView` will no longer be
eligible to handle messages dispatched by the
{cpp:class}`BWindow`.

See also:
{cpp:func}`BWindow::AddChild`,
{cpp:func}`BLooper::AddHandler`,
{cpp:func}`BHandler::SetNextHandler`,
{cpp:func}`~BView::RemoveSelf`,
{cpp:func}`~BView::AttachedToWindow`,
{cpp:func}`~BView::DetachedFromWindow`

::::

::::{abi-group}

:::{cpp:function} BView* BView::FindView(const char* name) const
:::

Returns the {hclass}`BView` identified by {hparam}`name`,
or {cpp:enum}`NULL` if the view can't be found.
Names are assigned by the {hclass}`BView` constructor and can be modified by the
{cpp:func}`~BHandler::SetName` function inherited from
{cpp:class}`BHandler`.

{hmethod}`FindView()` begins the search by checking
whether the {hclass}`BView`'s name matches
{hparam}`name`. If not, it continues to search down the view hierarchy, among the
{hclass}`BView`'s children and more distant descendants. To search the entire view
hierarchy, use the
{cpp:class}`BWindow`
{cpp:func}`~BWindow::FindView` of this function.

::::

::::{abi-group}

:::{cpp:function} BView* BView::Parent() const
:::
:::{cpp:function} BView* BView::NextSibling() const
:::
:::{cpp:function} BView* BView::PreviousSibling() const
:::
:::{cpp:function} BView* BView::ChildAt(int32 index) const
:::
:::{cpp:function} int32 BView::CountChildren() const
:::

These functions provide various ways of navigating the view hierarchy.
{hmethod}`Parent()` returns the {hclass}`BView`'s
parent view, unless the parent is the top
view of the window, in which case it returns {cpp:enum}`NULL`.
It also returns {cpp:enum}`NULL`
if the {hclass}`BView` doesn't belong to a view hierarchy and has no parent.

All the children of the same parent are arranged in a linked list.
{hmethod}`NextSibling()` returns the next sibling of
the {hclass}`BView` in the list, or {cpp:enum}`NULL`
if the {hclass}`BView` is the last child of its parent.
{hmethod}`PreviousSibling()` returns
the previous sibling of the {hclass}`BView`, or {cpp:enum}`NULL`
if the {hclass}`BView` is the first
child of its parent.

{hmethod}`ChildAt()` returns the view at {hparam}`index`
in the list of the {hclass}`BView`'s children,
or {cpp:enum}`NULL` if the {hclass}`BView` has no such child.
Indices begin at 0 and there are
no gaps in the list. {hmethod}`CountChildren()` returns the number of children the
{hclass}`BView` has. If the {hclass}`BView` has no
children, {hmethod}`CountChildren()` returns {cpp:enum}`NULL`, as
will {hmethod}`ChildAt()` for all indices, including 0.

To scan the list of a {hclass}`BView`'s children, you can increment the {hparam}`index`
passed to {hmethod}`ChildAt()` until it returns
{cpp:enum}`NULL`. However, it's more efficient
to ask for the first child and then use {hmethod}`NextSibling()` to walk down the
sibling list. For example:

:::{code}
BView *child;
if ( child = myView->ChildAt(0) ) {
   while ( child ) {
      . . .
      child = child->NextSibling();
   }
}
:::
::::

::::{abi-group}

:::{cpp:function} bool BView::RemoveSelf()
:::

Removes the {hclass}`BView` from its parent and returns
{hparam}`true`, or returns {hparam}`false` if
the {hclass}`BView` doesn't have a parent or for some reason can't be removed from
the view hierarchy.

This function acts just like
{cpp:func}`~BView::RemoveChild`,
except that it removes the
{hclass}`BView` itself rather than one of its children.

See also:
{cpp:func}`~BView::AddChild`

::::

## Input Related Functions
::::{abi-group}

:::{cpp:function} void BView::BeginRectTracking(BRect rect, uint32 how = B_TRACK_WHOLE_RECT)
:::
:::{cpp:function} void BView::EndRectTracking()
:::

These functions instruct the Application Server to display a rectangular
outline that will track the movement of the cursor.
{hmethod}`BeginRectTracking()`
puts the rectangle on-screen and initiates tracking;
{hmethod}`EndRectTracking()`
terminates tracking and removes the rectangle. The initial rectangle,
{hparam}`rect`, is specified in the {hclass}`BView`'s coordinate system.

This function supports two kinds of tracking, depending on the constant
passed as the {hparam}`how` argument:

:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_TRACK_WHOLE_RECT`
	- The whole rectangle moves with the cursor. Its position changes, but its size remains fixed.
-
	- {cpp:enum}`B_TRACK_RECT_CORNER`
	- The left top corner of the rectangle remains fixed within the view while its right and bottom edges move with the cursor.
:::

Tracking is typically initiated from within a {hclass}`BView`'s
{cpp:func}`~BView::MouseDown`
function and is terminated in
{cpp:func}`~BView::MouseUp`

::::

::::{abi-group}

:::{cpp:function} void BView::DragMessage(BMessage* message, BRect rect, BHandler* replyTarget = NULL)
:::
:::{cpp:function} void BView::DragMessage(BMessage* message, BBitmap* bitmap, BPoint point, BHandler* replyTarget = NULL)
:::
:::{cpp:function} void BView::DragMessage(BMessage* message, BBitmap* image, drawing_mode dragMode, BPoint offset, BHandler* replyTarget = NULL)
:::

Initiates a drag-and-drop session.

{hparam}`message`, is a
{cpp:class}`BMessage`
object that bundles the information that will be
dragged and dropped on the destination view. The caller retains
responsibility for this object and can delete it after {hmethod}`DragMessage()`
returns (the {hclass}`BView` makes a copy of the message).

{hparam}`image`, is a bitmap that the user can drag. The bitmap is automatically
freed when the message is dropped.

:::{admonition} Note
:class: note
1 bit-per-pixel bitmaps aren't supported; you should avoid using them.
:::

{hparam}`point` locates the hotspot within image (in the bitmap's coordinate
system). This is the point that's aligned with the location passed to
{cpp:func}`~BView::MouseDown`
or returned by
{cpp:func}`~BView::GetMouse`.

{hparam}`rect` defines the dimensions of an outline rectangle that you can instead
of a bitmap. The rectangle is stated in the {hclass}`BView`'s coordinate system.

{hparam}`replyTarget`, names the object that you want to handle a message that
might be sent in reply to the dragged message. If
{hparam}`replyTarget` is {cpp:enum}`NULL`, as
it is by default, any reply that's received will be directed to the {hclass}`BView`
object that initiated the drag-and-drop session.

{hparam}`dragMode` defines the drawing_mode
which will be used to draw image as the
image is dragged around. This is provided primarily so that transparent
or partially transparent images can be dragged around (using the
{cpp:enum}`B_OP_ALPHA` drawing mode).

This function works only for {hclass}`BView`
objects that are attached to a window.

::::

::::{abi-group}

:::{cpp:function} void BView::GetMouse(BPoint* cursor, uint32* buttons, bool checkQueue = true)
:::

Provides the location of the cursor and the state of the mouse buttons.
The position of the cursor is recorded in the variable referred to by
{hparam}`cursor`; it's provided in the
{hclass}`BView`'s own coordinates. A bit is set in the
variable referred to by {hparam}`buttons` for each mouse button that's down. This
mask may be 0 (if no buttons are down) or it may contain one or more of
the following constants:

- {cpp:enum}`B_PRIMARY_MOUSE_BUTTON`
- {cpp:enum}`B_SECONDARY_MOUSE_BUTTON`
- {cpp:enum}`B_TERTIARY_MOUSE_BUTTON`

The cursor doesn't have to be located within the view for this function
to work; it can be anywhere on-screen. However, the {hclass}`BView` must be
attached to a window.

If the {hparam}`checkQueue` flag is set to {cpp:enum}`false`,
{hmethod}`GetMouse()` provides information
about the current state of the mouse buttons and the current location of
the cursor.

If {hparam}`checkQueue` is {cpp:enum}`true`, as it
is by default, this function first looks in
the message queue for any pending reports of mouse-moved or mouse-up
events. If it finds any, it takes the one that has been in the queue the
longest (the oldest message), removes it from the queue, and reports the
cursor location and button states that were recorded in the message. Each
{hmethod}`GetMouse()` call removes another message from the queue. If the queue
doesn't hold any {cpp:enum}`B_MOUSE_MOVED` or {cpp:enum}`B_MOUSE_UP`
messages, {hmethod}`GetMouse()` reports
the current state of the mouse and cursor, just as if {hparam}`checkQueue` were
{cpp:enum}`false`.

If {hparam}`checkQueue` is {cpp:enum}`true`,
and the view's parent window has pending update
events, {hmethod}`GetMouse()` causes those update events to be processed.

You shouldn't use this function to track the mouse; implement the
{cpp:func}`~BView::MouseMoved` function instead.

See also:
{ref}`modifiers()`

::::

::::{abi-group}

:::{cpp:function} virtual void BView::MakeFocus(bool focused = true)
:::

Makes the {hclass}`BView` the current focus view for its
window (if the {hparam}`focused`
flag is {cpp:enum}`true`), or causes it to give up that status
(if {hparam}`focused` is {cpp:enum}`false`).
The focus view is the view that displays the current selection and is
expected to handle reports of key-down events when the window is the
active window. There can be no more than one focus view per window at a
time.

When called to make a {hclass}`BView` the focus view, this function invokes
{hmethod}`MakeFocus()` for the previous focus view,
passing it an argument of {cpp:enum}`false`.
It's thus called twice—once for the new and once for the old focus
view.

Calling {hmethod}`MakeFocus()` is the only way to make a view the focus view; the
focus doesn't automatically change on mouse-down events. {hclass}`BView`s that can
display the current selection (including an insertion point) or that can
accept pasted data should call {hmethod}`MakeFocus()`in their
{cpp:func}`~BView::MouseDown` functions.

A derived class can override {hmethod}`MakeFocus()` to add code that takes note of
the change in status. For example, a {hclass}`BView` that displays selectable data
may want to highlight the current selection when it becomes the focus
view, and remove the highlighting when it's no longer the focus view. A
{hclass}`BView` that participates in the keyboard navigation system should visually
indicate that it can be operated from the keyboard when it becomes the
focus view, and remove that indication when the user navigates to another
view and it's notified that it's no longer the focus view.

If the {hclass}`BView` isn't attached to a window, this function has no effect.

See also:
{cpp:func}`BWindow::CurrentFocus`,
{cpp:func}`~BView::IsFocus`

::::

::::{abi-group}

:::{cpp:function} BScrollBar* BView::ScrollBar(orientation posture) const
:::

Returns a {cpp:class}`BScrollBar`
object that scrolls the {hclass}`BView` (that has the {hclass}`BView` as
its target). The requested scroll bar has the {hparam}`posture`
orientation—{cpp:enum}`B_VERTICAL` or {cpp:enum}`B_HORIZONTAL`.
If the {hclass}`BView` isn't the
target of a scroll bar with the specified orientation, this function
returns {cpp:enum}`NULL`.

See also:
{cpp:func}`BScrollBar::SetTarget`

::::

::::{abi-group}

:::{cpp:function} void BView::ScrollBy(float horizontal, float vertical)
:::
:::{cpp:function} virtual void BView::ScrollTo(BPoint point)
:::
:::{cpp:function} inline void BView::ScrollTo(float x, float y)
:::

These functions scroll the contents of the view, provided that the {hclass}`BView`
is attached to a window.

{hmethod}`ScrollBy()` adds {hparam}`horizontal`
to the left and right components of the
{hclass}`BView`'s bounds rectangle, and {hparam}`vertical`
to the top and bottom components.
This serves to shift the display {hparam}`horizontal` coordinate units to the left
and {hparam}`vertical` units upward. If {hparam}`horizontal`
and {hparam}`vertical` are negative, the
display shifts in the opposite direction.

{hmethod}`ScrollTo()` shifts the contents of the view as much as necessary to put
{hparam}`point`—or
({hparam}`x`, {hparam}`y`)—at the upper left corner of its bounds
rectangle. The point is specified in the {hclass}`BView`'s coordinate system.

Anything in the view that was visible before scrolling and also visible
afterwards is automatically redisplayed at its new location. The
remainder of the view is invalidated, so the {hclass}`BView`'s
{cpp:func}`~BView::Draw` function will
be called to fill in those parts of the display that were previously
invisible. The update rectangle passed to
{cpp:func}`~BView::Draw` will be the smallest
possible rectangle that encloses just these new areas. If the view is
scrolled in only one direction, the update rectangle will be exactly the
area that needs to be drawn.

If the {hclass}`BView` is the target of scroll bars,
{hmethod}`ScrollBy()` and {hmethod}`ScrollTo()`
notify the {cpp:func}`BScrollBar`
objects of the change in the display so they can
update themselves to match. If the contents were scrolled horizontally,
they call the horizontal
{cpp:func}`BScrollBar`'s
{cpp:func}`~BScrollBar::SetValue` function and pass it the
new value of the left side of the bounds rectangle. If they were scrolled
vertically, they call
{cpp:func}`~BScrollBar::SetValue`
for the vertical
{cpp:func}`BScrollBar`
and pass it the new value of the top of the bounds rectangle.

The `inline` version of {hmethod}`ScrollTo()`
works by creating a {cpp:class}`BPoint` object and
passing it to the version that's declared `virtual`. Therefore, if you want
to override either function, you should override the `virtual` version.
(However, due to the peculiarities of C++, overriding any version of an
overloaded function hides all versions of the function. For continued
access to the nonvirtual version without explicitly specifying the
"BView::" prefix, simply copy the `inline` code from
interface/View.h into
the derived class.)

::::

::::{abi-group}

:::{cpp:function} status_t BView::SetEventMask(uint32 events, uint32 options = 0)
:::
:::{cpp:function} status_t BView::SetMouseEventMask(uint32 events, uint32 options = 0)
:::
:::{cpp:function} uint32 BView::EventMask()
:::

{hmethod}`SetEventMask()` lets you extend the scope of the mouse and keyboard events
that the view can receive. If {hparam}`events` includes
{cpp:enum}`B_POINTER_EVENTS`, the view
will receive mouse events (aka pointer events) even when the mouse isn't
over the view; if it includes {cpp:enum}`B_KEYBOARD_EVENTS`, the view will receive
keyboard events even if the view isn't in focus. (We'll look at the
options argument below).

{hmethod}`SetMouseEventMask()` does the same thing as
{hmethod}`SetEventMask()`, except (1) it
can only be called from within an implementation of
{cpp:func}`~BView::MouseDown`, and (2)
the new {hparam}`events` value—which is added to the current event
mask—is only in effect until (and including) the following mouse up
event. When the mouse is released, the view's previous event mask (as set
through {hmethod}`SetEventMask()`) is re-established.

The {hparam}`option` arguments lets you request other event-handling modifications
(note that {hmethod}`SetEventMask()` only accepts the first of these options;
{hmethod}`SetMouseEventMask()` accepts all three):

:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_NO_POINTER_HISTORY`.
	- This tells the App Server to only send the most recent pointer moved (i.e. mouse moved) event to your view (all "old" events are thrown away). You use this option if your {cpp:func}`~BView::MouseMoved` implementation is too heavy to keep up with the mouse moved messages that are pouring in. Of course, your view may lose some mouse movement granularity, but that's the price you pay to stay in synch with the user.
-
	- {cpp:enum}`B_SUSPEND_VIEW_FOCUS`
	- ({hmethod}`SetMouseEventMask()` only). Events that are normally sent to the focus view are suppressed. In practice, this means that while the mouse is held down, the keyboard is turned off. Note that the view that's processing the {cpp:func}`~BView::MouseDown` messages doesn't have to be the focus view to suppress focused messages.
-
	- {cpp:enum}`B_LOCK_WINDOW_FOCUS`
	- ({hmethod}`SetMouseEventMask()` only). Prevents the view's window from losing focused status while the mouse is down, even if the mouse leaves the window's bounds.
:::
:::{admonition} Note
:class: note
To ask for an option without changing the event mask (or mouse event
mask), pass 0 as the events argument.
:::
:::{admonition} Note
:class: note
Both {hmethod}`SetEventMask()` and
{hmethod}`SetMouseEventMask()` require that the view be
attached to a window; they have no effect if the view isn't already
attached.
:::

{hmethod}`EventMask()` returns the view's event mask as set through
{hmethod}`SetEventMask()`.
It doesn't consider the mask set in {hmethod}`SetMouseEventMask()`.

::::

## Graphics State Functions
::::{abi-group}

:::{cpp:function} void BView::MovePenBy(float horizontal, float vertical)
:::
:::{cpp:function} void BView::MovePenTo(BPoint point)
:::
:::{cpp:function} void BView::MovePenTo(float x, float y)
:::
:::{cpp:function} BPoint BView::PenLocation() const
:::

These functions move the pen (without drawing a line) and report the
current pen location.

{hmethod}`MovePenBy()` moves the pen {hparam}`horizontal`
coordinate units to the right and {hparam}`vertical` units downward.
If {hparam}`horizontal` or {hparam}`vertical` are negative, the pen
moves in the opposite direction. {hmethod}`MovePenTo()` moves the pen to
{hparam}`point`—or to ({hparam}`x`, {hparam}`y`)—in
the {hclass}`BView`'s coordinate system.

Some drawing functions also move the pen—to the end of whatever
they draw. In particular, this is true of
{cpp:func}`~BView::StrokeLine`,
{cpp:func}`~BView::DrawString`, and
{cpp:func}`~BView::DrawChar`.
Functions that stroke a closed shape (such as
{cpp:func}`~BView::StrokeEllipse`)
don't move the pen.

The pen location is a parameter of the {hclass}`BView`'s graphics environment,
which is maintained by both the Application Server and the {hclass}`BView`. If the
{hclass}`BView` doesn't belong to a window,
{hmethod}`MovePenTo()` and {hmethod}`MovePenBy()` cache the
location, so that later, when the {hclass}`BView` becomes attached to a window, it
can be handed to the server to become the operable pen location for the
{hclass}`BView`. If the {hclass}`BView` belongs
to a window, these functions alter both the
server parameter and the client-side cache.

{hmethod}`PenLocation()` returns the point where the pen is currently positioned in
the {hclass}`BView`'s coordinate system. Because of the cache, this shouldn't
entail contacting the server. The default pen position is (0.0, 0.0).

See also:
{cpp:func}`~BView::SetPenSize`

::::

::::{abi-group}

:::{cpp:function} void BView::PushState()
:::
:::{cpp:function} void BView::PopState()
:::

Saves and restores the state from the state stack. A state consists of
the following: local and global origins, local and global scales, drawing
mode, line cap and join modes, miter limit, pen size and location,
foreground and background color, stipple pattern, local and global
clipping regions, and the font context. When a state is saved to the
stack, a new state context is created, with a local scale of zero, a
local origin at (0,0), and no clipping region.

:::{admonition} Warning
:class: warning
If the {hclass}`BView` isn't attached to a window, these functions will crash the
application.
:::
::::

::::{abi-group}

:::{cpp:function} void BView::SetLineMode(cap_mode lineCap, join_mode lineJoin, float miterLimit = B_DEFAULT_MITER_LIMIT)
:::
:::{cpp:function} cap_mode BView::LineCapMode() const
:::
:::{cpp:function} join_mode BView::LineJoinMode() const
:::
:::{cpp:function} float BView::LineMiterLimit() const
:::

These methods implement support for PostScript-style line cap and join
modes. The cap mode determines the shape of the endpoints of stroked
paths, while the join mode determines the shape of the corners of the
paths (i.e. where two lines meet).

The following values of cap_mode are defined:

:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_ROUND_CAP`
	- A semicircle is drawn around the endpoint. Its diameter is equal to the width of the line.
-
	- {cpp:enum}`B_BUTT_CAP`
	- The line is squared off and does not extend beyond the endpoint.
-
	- {cpp:enum}`B_SQUARE_CAP`
	- The line is squared off, extending past the endpoint for a distance equal to half the width of the line.
:::

Additionally, the following values of join_mode are defined:

:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_ROUND_JOIN`
	- Acts identically to {cpp:enum}`B_ROUND_CAP`, except applied to joins.
-
	- {cpp:enum}`B_MITER_JOIN`
	- The lines are extended until they touch. If they meet at an angle greater than `2*arcsin(1/miterLimit)`, a bevel join is used instead.
-
	- {cpp:enum}`B_BEVEL_JOIN`
	- Butt end caps are used at the common endpoint and the empty area between the caps is filled with a triangle.
-
	- {cpp:enum}`B_BUTT_JOIN`
	- Acts identically to {cpp:enum}`B_BUTT_CAP`, except applied to joins.
-
	- {cpp:enum}`B_SQUARE_JOIN`
	- Acts identically to {cpp:enum}`B_SQUARE_CAP`, except applied to joins.
:::

{hmethod}`SetLineMode()` sets the line and join modes and the miter limit while
{hmethod}`LineCapMode()`, {hmethod}`LineJoinMode()`,
and {hmethod}`LineMiterLimit()` return them. The line
mode affects all of the {hmethod}`Stroke…()` methods except for
{cpp:func}`~BView::StrokeArc`,
{cpp:func}`~BView::StrokeEllipse`, and
{cpp:func}`~BView::StrokeRoundRect`.

::::

::::{abi-group}

:::{cpp:function} void BView::SetScale(float ratio)
:::

Scales the coordinate system the view uses for drawing. The default scale
is 1.0; smaller ratio values reduce the size of the drawing coordinate
system; larger numbers magnify the system. For example, a ratio of 0.5
makes a subsequent drawing twice as small and moves the drawing closer to
the origin, and 2.0 makes it twice as big and moves it away, as shown
below.


:::{admonition} Note
:class: note
The scaling ratio only affects subsequent drawing operations! Changing
the scale doesn't affect the graphics already displayed in the view, the
view's frame rectangle and clipping region, the placement and size of
subviews, translation of mouse coordinates to and from view space, and so
forth.
:::

Multiple {hmethod}`SetScale()` calls don't compound within the same graphics state,
but they do compound across pushed states:

:::{code}
aview->SetScale(0.5);
aview->SetScale(0.5);
/* aview's scaling is 0.5. */
bview->SetScale(0.5);
bview->PushState();
bview->SetScale(0.5);
/* view's scaling is 0.25. */
:::
:::{admonition} Warning
:class: warning
The {hclass}`BView` must be attached to a window
before you call this function.
:::
::::

::::{abi-group}

:::{cpp:function} virtual void BView::SetPenSize(float size)
:::
:::{cpp:function} float BView::PenSize() const
:::

{hmethod}`SetPenSize()` sets the size of the {hclass}`BView`'s pen—the graphics
parameter that determines the thickness of stroked lines—and
{hmethod}`PenSize()` returns the current pen size. The pen size is stated in
coordinate units, but is translated to a device-specific number of pixels
for each output device.

The pen tip can be thought of as a brush that's centered on the line path
and held perpendicular to it. If the brush is broader than one pixel, it
paints roughly the same number of pixels on both sides of the path.

The default pen size is 1.0 coordinate unit. It can be set to any
nonnegative value, including 0.0. If set to 0.0, the size is translated
to one pixel for all devices. This guarantees that it will always draw
the thinnest possible line no matter what the resolution of the device.

Thus, lines drawn with pen sizes of 1.0 and 0.0 will look alike on the
screen (one pixel thick), but the line drawn with a pen size of 1.0 will
be 1/72 of an inch thick when printed, however many printer pixels that
takes, while the line drawn with a 0.0 pen size will be just one pixel
thick.

The pen size is a parameter of the {hclass}`BView`'s graphics
environment maintained by the Application Server and cached by the
{hclass}`BView`. If the {hclass}`BView` isn't
attached to a window, {hmethod}`SetPenSize()` records the
size so that later, when the {hclass}`BView` is added to a
window and becomes known to the server, the cached value can automatically
be established as the operable pen size for the
{hclass}`BView`. If the {hclass}`BView` belongs
to a window, this function changes both the server and the cache.

See also:
"{cpp:func}`~TheInterfaceKit::Drawing`"
in the chapter overview,
{cpp:func}`~BView::StrokeArc`,
{cpp:func}`~BView::MovePenBy`

::::

::::{abi-group}

:::{cpp:function} virtual void BView::SetHighColor(rgb_color color)
:::
:::{cpp:function} inline void BView::SetHighColor(uchar red, uchar green, uchar blue, uchar alpha = 255)
:::
:::{cpp:function} rgb_color BView::HighColor() const
:::
:::{cpp:function} virtual void BView::SetLowColor(rgb_color color)
:::
:::{cpp:function} inline void BView::SetLowColor(uchar red, uchar green, uchar blue, uchar alpha = 255)
:::
:::{cpp:function} rgb_color BView::LowColor() const
:::

These functions set and return the current high and low colors of the
{hclass}`BView`. These colors combine to form a pattern that's passed as an
argument to the {hmethod}`Stroke…()` and {hmethod}`Fill…()` drawing functions. The
{cpp:enum}`B_SOLID_HIGH` pattern is the high color alone, and {cpp:enum}`B_SOLID_LOW` is the low
color alone.

The default high color is black—red, green, and blue values all
equal to 0. The default low color is white—red, green, and blue
values all equal to 255.

The `inline` versions of {hmethod}`SetHighColor()`
and {hmethod}`SetLowColor()` take separate
arguments for the red, blue, and green color components; they work by
creating an rgb_color data structure and passing it to the corresponding
function that's declared `virtual`. Therefore, if you want to override
either function, you should override the virtual version. (However, due
to the peculiarities of C++, overriding any version of an overloaded
function hides all versions of the function. For continued access to the
nonvirtual version without explicitly specifying the "BView::" prefix,
simply copy the inline code from interface/View.h into the derived class.)

The high and low colors are parameters of the {hclass}`BView`'s graphics
environment, which is kept in the {hclass}`BView`'s shadow counterpart in the
Application Server and cached in the {hclass}`BView`.
If the {hclass}`BView` isn't attached
to a window, {hmethod}`SetHighColor()` and
{hmethod}`SetLowColor()` cache the color value so
that later, when the {hclass}`BView` is placed in a window and becomes known to the
server, the cached value can automatically be registered as the current
high or low color for the view. If the {hclass}`BView` belongs to a window, these
functions alter both the client-side and the server-side values.

{hmethod}`HighColor()` and {hmethod}`LowColor()`
return the {hclass}`BView`'s current high and low
colors. Because of the cache, this shouldn't entail contacting the
Application Server.

See also:
"{cpp:func}`~TheInterfaceKit::Drawing`"
"in the {ref}`Drawing`" section of this chapter,
{cpp:func}`~BView::SetViewColor`

::::

::::{abi-group}

:::{cpp:function} virtual void BView::SetViewColor(rgb_color color)
:::
:::{cpp:function} inline void BView::SetViewColor(uchar red, uchar green, uchar blue, uchar alpha = 255)
:::
:::{cpp:function} rgb_color BView::ViewColor() const
:::

These functions set and return the view's background color. This is the
color that's displayed when a view is erased during an update, or when
the view is resized to expose new areas. The default view color is white
(255,255,255). If you don't want the view to be erased in an update, set
the view color to {cpp:enum}`B_TRANSPARENT_COLOR`. (Despite the name this doesn't
actually make the view transparent.)

The `inline` version of {hmethod}`SetViewColor()`
calls the `virtual` version. Thus,
overriding the `virtual` version affects both versions. However, due to the
peculiarities of C++, overriding any version of an overloaded function
hides all versions of the function. To fix this, simply copy the `inline`
code from View.h into your subclass.

{hmethod}`ViewColor()` returns the current background color.

See also:
"{cpp:func}`~TheInterfaceKit::Drawing`" in the
"{ref}`Drawing`" section of this chapter,
{cpp:func}`~BView::SetHighColor`,
{cpp:func}`~BView::SetViewBitmap`

::::

::::{abi-group}

:::{cpp:function} virtual void BView::SetBlendingMode(source_alpha alphaSrcMode, alpha_function alphaFncMode)
:::
:::{cpp:function} virtual void BView::GetBlendingMode(source_alpha* alphaSrcMode, alpha_function* alphaFncMode)
:::

These two functions set and retrieve the graphics state variables which
control the details of alpha transparency drawing. These variables will
have an effect on drawing in the view only if the drawing mode has been
set to {cpp:enum}`B_OP_ALPHA` by
{cpp:func}`~BView::SetDrawingMode`.

{hparam}`alphaSrcMode` is one of the following two constants, with associated
meanings:

:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_CONSTANT_ALPHA`
	- Use the alpha channel of the current high color as the transparency value for whatever is being drawn.
-
	- {cpp:enum}`B_PIXEL_ALPHA`
	- When drawing a bitmap, use the alpha value associated with each pixel as the transparency value for that pixel. This can be used to obtain some interesting variable transparency effects.
:::

{hparam}`alphaFncMode` is one of the following two constants, with associated
meanings:

:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_ALPHA_OVERLAY`
	- The "normal" mode, used when drawing a transparent image or shape over an opaque background.
-
	- {cpp:enum}`B_ALPHA_COMPOSITE`
	- Used when blending two or more transparent images together offscreen, to produce a new transparent image that will later be drawn onscreen using the {cpp:enum}`B_ALPHA_OVERLAY` setting.
:::
::::

::::{abi-group}

:::{cpp:function} virtual void BView::SetDrawingMode(drawing_mode mode)
:::
:::{cpp:function} drawing_mode BView::DrawingMode() const
:::

These functions set and return the {hclass}`BView`'s drawing mode, which can be any
of the following eleven constants:

- {cpp:enum}`B_OP_COPY`
- {cpp:enum}`B_OP_OVER`
- {cpp:enum}`B_OP_ERASE`
- {cpp:enum}`B_OP_INVERT`
- {cpp:enum}`B_OP_SELECT`
- {cpp:enum}`B_OP_ALPHA`
- {cpp:enum}`B_OP_MIN`
- {cpp:enum}`B_OP_MAX`
- {cpp:enum}`B_OP_ADD`
- {cpp:enum}`B_OP_SUBTRACT`
- {cpp:enum}`B_OP_BLEND`

The drawing mode is an element of the {hclass}`BView`'s graphics environment, which
both the Application Server and the {hclass}`BView`
keep track of. If the {hclass}`BView`
isn't attached to a window, {hmethod}`SetDrawingMode()` caches the mode. When the
{hclass}`BView` is placed in a window and becomes known to the server, the cached
value is automatically set as the current drawing mode. If the {hclass}`BView`
belongs to a window, {hmethod}`SetDrawingMode()` makes the change in both the server
and the cache.

{hmethod}`DrawingMode()` returns the current mode. Because of the cache, this
generally doesn't entail a trip to the server.

The default drawing mode is {cpp:enum}`B_OP_COPY`. It and the other modes are
explained under
"{cpp:func}`~TheInterfaceKit::Drawing`" in the
"{ref}`Drawing`"
section of this chapter.

::::

::::{abi-group}

:::{cpp:function} void BView::ForceFontAliasing(bool enable)
:::

{hmethod}`ForceFontAliasing()` is used in conjunction with printing. When called
with a value of {cpp:enum}`true`, if causes subsequent printing to be done without
antialiasing printed characters. This is normally what is desired with
high-resolution printers, to guarantee that the edges of printed
characters appear sharp. Calling {hmethod}`ForceFontAliasing()` with an argument of
{cpp:enum}`false` turns antialiasing back on, which may be desirable with
lower-resolution printers.

Note that {hmethod}`ForceFontAliasing()` does not affect characters or strings drawn
to the screen.

See also:
The {cpp:class}`BPrintJob` class.

::::

::::{abi-group}

:::{cpp:function} void BView::GetFontHeight(font_height* fontHeight) const
:::

Gets the height of the {hclass}`BView`'s font. This function provides the same
information as {cpp:class}`BFont`'s
{cpp:func}`~BFont::GetHeight`. The following code

:::{code}
font_height height;
myView->GetFontHeight(&height);
:::

is equivalent to:

:::{code}
font_height height;
BFont font;
myView->GetFont(&font);
font.GetHeight(&height);
:::

See the {cpp:class}`BFont`
class for more information.

::::

::::{abi-group}

:::{cpp:function} void BView::SetFont(const BFont* font, uint32 properties = B_FONT_ALL)
:::
:::{cpp:function} void BView::GetFont(BFont* font)
:::

{hmethod}`SetFont()` sets the {hclass}`BView`'s
current font so that it matches the specified
properties of the {hparam}`font`
{cpp:class}`BFont` object.
The {hparam}`properties` mask is formed by
combining the following constants:

- {cpp:enum}`B_FONT_FAMILY_AND_STYLE`
- {cpp:enum}`B_FONT_SPACING`
- {cpp:enum}`B_FONT_SIZE`
- {cpp:enum}`B_FONT_ENCODING`
- {cpp:enum}`B_FONT_SHEAR`
- {cpp:enum}`B_FONT_FACE`
- {cpp:enum}`B_FONT_ROTATION`
- {cpp:enum}`B_FONT_FLAGS`

Each constant corresponds to a settable property of the
{cpp:class}`BFont` object. The
default mask, {cpp:enum}`B_FONT_ALL`, is a shorthand for all the properties
(including any that might be added in future releases). If the mask is 0,
{hmethod}`SetFont()` won't set the {hclass}`BView`'s font.

{hmethod}`GetFont()` copies the {hclass}`BView`'s
current font to the {cpp:class}`BFont` object passed as
an argument. Modifying this copy doesn't modify the {hclass}`BView`'s font; it
takes an explicit {hmethod}`SetFont()` call to affect the {hclass}`BView`.

For example, this code changes the size of a {hclass}`BView`'s font and turns
antialiasing off:

:::{code}
BFont font;
myView->GetFont(&font);
font.SetSize(67.0);
font.SetFlags(B_DISABLE_ANTIALIASING);
myView->SetFont(&font, B_FONT_SIZE | B_FONT_FLAGS);
:::

Since the {cpp:class}`BFont`
object that this example code alters is a copy of the
{hclass}`BView`'s current font, it's not strictly necessary to name the properties
that are different when calling {hmethod}`SetFont()`. However, it's more efficient
and better practice to do so.

The font is part of the {hclass}`BView`'s graphic environment. Like other elements
in the environment, it can be set whether or not the {hclass}`BView` is attached to
the window. Graphics parameters are kept by the Application Server and
also cached by the {hclass}`BView` object.

See also:
{cpp:func}`~get::font`

::::

::::{abi-group}

:::{cpp:function} void BView::SetFontSize(float points)
:::

Sets the size of the {hclass}`BView`'s font to {hparam}`points`.
This function is a shorthand
for a {hmethod}`SetFont()` call that just alters the font size. For example, this
line of code

:::{code}
myView->SetFontSize(12.5);
:::

does the same thing as:

:::{code}
BFont font;
font.SetSize(12.5);
myView->SetFont(&font, B_FONT_SIZE);
:::

See also: the {cpp:class}`BFont` class

::::

::::{abi-group}

:::{cpp:function} float BView::StringWidth(const char* string) const
:::
:::{cpp:function} float BView::StringWidth(const char* string, int32 length) const
:::
:::{cpp:function} void BView::GetStringWidths(char* stringArray[], int32 lengthArray[], int32 numStrings, float widthArray[]) const
:::

These functions measure how much room is required to draw a string, or a
group of strings, in the {hclass}`BView`'s current font. They're equivalent to the
identically named set of functions defined in the
{cpp:class}`BFont` class, except
that they assume the {hclass}`BView`'s font. For example, this line of code

:::{code}
float width;
width = myView->StringWidth("Be"B_UTF8_REGISTERED);
:::

produces the same result as:

:::{code}
float width;
BFont font;
myView->GetFont(&font);
width = font.StringWidth("Be"B_UTF8_REGISTERED);
:::

See also:
{cpp:func}`BFont::StringWidth`,
{cpp:func}`BFont::GetEscapements`

::::

::::{abi-group}

:::{cpp:function} void BView::TruncateString(BString* inOutString, uint32 mode, float width) const
:::

Truncates the {cpp:class}`BString`
{hparam}`inOutString` to be no wider than {hparam}`width` pixels. The
{hparam}`mode` flags control how the string is truncated.

:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_TRUNCATE_BEGINNING`
	- Cut from the beginning of the string until it fits within the specified width.
-
	- {cpp:enum}`B_TRUNCATE_MIDDLE`
	- Cut from the middle of the string.
-
	- {cpp:enum}`B_TRUNCATE_END`
	- Cut from the end of the string.
-
	- {cpp:enum}`B_TRUNCATE_SMART`
	- Cut anywhere, but do so intelligently, so that all the strings remain different after being cut. For example, if a set of similar path names are passed in the {hparam}`inputStringArray`, this mode would attempt to cut from the identical parts of the path names and preserve the parts that are different. This mode also pays attention to word boundaries, separators, punctuation, and the like. However, it's not implemented for the current release.
:::
::::

::::{abi-group}

:::{cpp:function} void BView::ClipToPicture(BPicture* picture, BPoint where = B_ORIGIN, bool sync = true)
:::
:::{cpp:function} void BView::ClipInverseToPicture(BPicture* picture, BPoint where = B_ORIGIN, bool sync = true)
:::

Modifies the view's clipping region by intersecting the current clipping
region with the pixels drawn by {hparam}`picture` (in the case of
{hmethod}`ClipToPicture()`) or
with everything outside the pixels drawn by {hparam}`picture` (in the case of
{hmethod}`ClipToInversePicture()`), to produce the new clipping region.

Note that {cpp:class}`BPicture`
instances are, by their nature, resolution
independent; when the {hmethod}`ClipToPicture()`
or {hmethod}`ClipToInversePicture()` command is
invoked, {hparam}`picture` is effectively drawn at the same resolution as the
invoking view, and the bitmap produced by that action is used to modify
the clipping region. You may think of {hparam}`picture` as executing its drawing
instructions on a surface that starts out as completely transparent; at
the end of the process, each pixel on the drawing surface will either be
either completely transparent, or will be at least somewhat opaque. The
pixels which are at least somewhat opaque are those which were "drawn" by
{hparam}`picture`.

If {hparam}`sync` is {cpp:enum}`false`, the
functions will execute asynchronously; normally
they execute synchronously (i.e. wait for the drawing actions to be
completed by the Application Server.)

See also:
{cpp:func}`~BView::BeginPicture`

::::

::::{abi-group}

:::{cpp:function} virtual void BView::ConstrainClippingRegion(BRegion* region)
:::

Restricts the drawing that the {hclass}`BView` can do to {hparam}`region`.

The Application Server keeps track of a clipping region for each {hclass}`BView`
that's attached to a window. It clips all drawing the {hclass}`BView` does to that
region; the {hclass}`BView` can't draw outside of it.

By default, the clipping region contains only the visible area of the
view and, during an update, only the area that actually needs to be
drawn. By passing a {hparam}`region` to this function, an application can further
restrict the clipping region. When calculating the clipping region, the
server intersects it with the region provided. The {hclass}`BView` can draw only in
areas common to the region passed and the clipping region as the server
would otherwise calculate it. The {hparam}`region` passed can't expand the clipping
region beyond what it otherwise would be.

The clipping region is additionally affected by any items on the state
stack. If any saved states contain clipping regions, then the actual
clipping region used by the Application Server is the intersection of the
local clipping region (as set by this method) and the regions stored on
the state stack.

If called during an update, {hmethod}`ConstrainClippingRegion()` restricts the
clipping region only for the duration of the update.

Calls to {hmethod}`ConstrainClippingRegion()` are not additive; each region that's
passed replaces the one that was passed in the previous call. Passing a
{cpp:enum}`NULL` pointer removes the previous region without replacing it. The
function works only for {hclass}`BView`s that are attached to a window.

See also:
{cpp:func}`~BView::Draw`

::::

::::{abi-group}

:::{cpp:function} void BView::GetClippingRegion(BRegion* region) const
:::

Modifies the {cpp:class}`BRegion`
object passed as an argument so that it describes
the current local clipping region of the {hclass}`BView`, the region where the
{hclass}`BView` is allowed to draw. It's most efficient to allocate temporary
{cpp:class}`BRegion`s on the stack:

:::{code}
BRegion clipper;
GetClippingRegion(&clipper);
. . .
:::

Ordinarily, the clipping region is the same as the visible region of the
view, the part of the view currently visible on-screen. The visible
region is equal to the view's bounds rectangle minus:

- The frame rectangles of its children,
- Any areas that are clipped because the view doesn't lie wholly within the frame rectangles of all its ancestors in the view hierarchy, and
- Any areas that are obscured by other windows or that lie in a part of the window that's off-screen.

The clipping region can be smaller than the visible region if the program
restricted it by calling
{cpp:func}`~BView::ConstrainClippingRegion`.
It will exclude any
area that doesn't intersect with the region passed to
{cpp:func}`~BView::ConstrainClippingRegion`.

The clipping region is additionally modified by any items on the state
stack. If any saved states contain clipping regions, then the actual
clipping region used by the Application Server is the intersection of the
local clipping region (as set by
{cpp:func}`~BView::ConstrainClippingRegion`)
and the regions stored on the state stack.

While the {hclass}`BView` is being updated, the clipping region contains just those
parts of the view that need to be redrawn. This may be smaller than the
visible region, or the region restricted by
{cpp:func}`~BView::ConstrainClippingRegion`,
if:

- The update occurs during scrolling. The clipping region will exclude any of the view's visible contents that the Application Server is able to shift to their new location and redraw automatically.
- The view rectangle has grown (because, for example, the user resized the window larger) and the update is needed only to draw the new parts of the view.
- The update was caused by {cpp:func}`~BView::Invalidate` and the rectangle passed to {cpp:func}`~BView::Invalidate` didn't cover all of the visible region.
- The update was necessary because {cpp:func}`~BView::CopyBits` couldn't fill all of a destination rectangle.

If, while updating is ongoing, you call the view's parent's
{hmethod}`GetClippingRegion()` function, the resulting region indicates only the
area of that view that requries updating, and so forth. In other words,
this change in behavior (from returning the true clipping region to
returning the update region) is recursive up the view hierarchy.

This function works only if the {hclass}`BView` is attached to a window. Unattached
{hclass}`BView`s can't draw and therefore have no clipping region.

See also:
{cpp:func}`~BView::ConstrainClippingRegion`,
{cpp:func}`~BView::Draw`,
{cpp:func}`~BView::Invalidate`

::::

## Drawing Related Functions
::::{abi-group}

:::{cpp:function} void BView::DrawBitmap(const BBitmap* image)
:::
:::{cpp:function} void BView::DrawBitmap(const BBitmap* image, BPoint point)
:::
:::{cpp:function} void BView::DrawBitmap(const BBitmap* image, BRect destination)
:::
:::{cpp:function} void BView::DrawBitmap(const BBitmap* image, BRect source, BRect destination)
:::
:::{cpp:function} void BView::DrawBitmapAsync(const BBitmap* image)
:::
:::{cpp:function} void BView::DrawBitmapAsync(const BBitmap* image, BPoint point)
:::
:::{cpp:function} void BView::DrawBitmapAsync(const BBitmap* image, BRect destination)
:::
:::{cpp:function} void BView::DrawBitmapAsync(const BBitmap* image, BRect source, BRect destination)
:::
These functions place a bitmap {hparam}`image` in the
view at the current pen position, at the {hparam}`point`
specified, or within the designated {hparam}`destination`
rectangle. The {hparam}`point` and the
{hparam}`destination` rectangle are stated in the
{hclass}`BView`'s coordinate system.
If a {hparam}`source` rectangle is given, only that part
of the bitmap image is drawn. Otherwise, the entire bitmap is placed in the
view. The {hparam}`source` rectangle is stated in the internal
coordinates of the
{cpp:class}`BBitmap`
object.
If the source image is bigger than the
{hparam}`destination` rectangle, it's scaled to fit.
The two functions differ in only one respect:
{hmethod}`DrawBitmap()` waits for the Application Server to
finish rendering the image before it returns.
{hmethod}`DrawBitmapAsync()` doesn't wait; it passes the
image to the server and returns immediately. The latter function can be
more efficient in some cases—for example, you might use an
asynchronous function to draw several bitmaps and then call
{cpp:func}`~BView::Sync`
to wait for them all to finish rather than wait for each one individually:
:::{code}
DrawBitmapAsync(bitmapOne, firstPoint);
DrawBitmapAsync(bitmapTwo, secondPoint);
DrawBitmapAsync(bitmapThree, thirdPoint);
Sync();
:::
Or, if you can cram some useful work between the time you send the
bitmap to the Application Server and the time you need to be sure that it
has appeared on-screen, {hmethod}`DrawBitmapAsync()` will
free your thread to do that work immediately:
:::{code}
DrawBitmapAsync(someBitmap, somePoint);
/* do something else */
Sync();
:::
See also:
The "{ref}`Drawing`"
in the chapter overview, the
{cpp:class}`BBitmap`
class
::::

::::{abi-group}

:::{cpp:function} void BView::DrawChar(char c)
:::
:::{cpp:function} void BView::DrawChar(char c, BPoint point)
:::
Draws the character {hparam}`c` at the current pen
position—or at the {hparam}`point` specified—and
moves the pen to a position immediately to the right of the character. This
function is equivalent to passing a string of one character to
{cpp:func}`~BView::DrawString`.
The point is specified in the {hclass}`BView`'s coordinate
system.
::::

::::{abi-group}

:::{cpp:function} void BView::DrawString(const char* string, escapement_delta* delta = NULL)
:::
:::{cpp:function} void BView::DrawString(const char* string, int32 length, escapement_delta* delta = NULL)
:::
:::{cpp:function} void BView::DrawString(const char* string, BPoint point, escapement_delta* delta = NULL)
:::
:::{cpp:function} void BView::DrawString(const char* string, int32 length, BPoint point, escapement_delta* delta = NULL)
:::
Draws the characters encoded in {hparam}`length` bytes
of {hparam}`string`—or, if the number of bytes isn't
specified, all the characters in the string, up to the null terminator
('\0'). Characters are drawn in the {hclass}`BView`'s current
font. The font's direction determines whether the string is drawn
left-to-right or right-to-left. Its rotation determines the angle of the
baseline (horizontal for an unrotated font). The spacing mode of the font
determines how characters are positioned within the string and the string
width.
This function places the characters on a baseline that begins one
pixel above the current pen position—or one pixel above the specified
point in the {hclass}`BView`'s coordinate system. It draws the
characters to the right (assuming an unrotated font) and moves the pen to
the baseline immediately past the characters drawn. For a left-to-right
font, the pen will be in position to draw the next character, as shown
below:

The characters are drawn in the opposite direction for a right-to-left
font, but the pen still moves left-to-right:

:::{admonition} Note
:class: note
The BeOS draws text one pixel above the logical baseline to maintain
compatibility with an earlier version of one of our most commonly-used
font rasterizers. This affects both fonts and
{cpp:class}`BShape`s
representing glyphs (see
{cpp:func}`BFont::GetGlyphShapes`.
To draw text at the right place, add one to
the Y coordinate when calling
{cpp:func}`~BView::MovePenTo`
or specifying a {cpp:class}`BPoint` at which
to begin drawing.
:::
For a font that's read from left-to-right, a series of simple
{hmethod}`DrawString()` calls (with no point specified) will
produce a continuous string. For example, these two lines of code,
:::{code}
DrawString("tog");
DrawString("ether");
:::
will produce the same result as this one,
:::{code}
DrawString("together");
:::
except if the spacing mode is {cpp:enum}`B_STRING_SPACING`.
Under {cpp:enum}`B_STRING_SPACING`, character placements are
adjusted keeping the string width constant. The adjustments are
contextually dependent on the string and may therefore differ depending on
whether there are two strings ("tog" and "ether") or
just one ("together").
If a {hparam}`delta` argument is provided,
{hmethod}`DrawString()` adds the additional amounts
specified in the escapement_delta structure to the width of each
character. This structure has two fields:
:::{list-table}
---
header-rows: 1
---
-
	- Field
	- Description
-
	- floatnonspace
	- The amount to add to the width of characters that have visible glyphs (that put ink on the printed page).
-
	- floatspace
	- The amount to add to the width of characters that have escapements, but don't have visible glyphs (characters that affect the position of surrounding characters but don't put ink on the page).
:::

When drawing to the screen, {hmethod}`DrawString()` uses antialiasing—unless
the {hclass}`BView`'s font disables it or the font size is large enough (over
1,000.0 points) so that its benefits aren't required. Antialiasing
produces colors at the margins of character outlines that are
intermediate between the color of the text (the {hclass}`BView`'s high color) and
the color of the background against which the text is drawn. When drawing
in {cpp:enum}`B_OP_COPY` mode, antialiasing requires the
{hclass}`BView`'s low color to match the background color.

It's much faster to draw a string in {cpp:enum}`B_OP_COPY` mode than in any other
mode. If you draw the same string repeatedly in the same location in
{cpp:enum}`B_OP_OVER` mode without erasing, antialiasing will produce different, and
worse, results each time as the intermediate color it previously produced
is treated as the new background each time. Antialiasing doesn't produce
pleasing results in {cpp:enum}`B_OP_SELECT` mode.

This is a graphical drawing function, so any character that doesn't have
an escapement or a visible representation (including white space) is
replaced by an undefined character that can be drawn (currently an empty
box). This includes all control characters (those with values less than
{cpp:enum}`B_SPACE`, 0x20).

{hmethod}`DrawString()` doesn't erase before drawing.

See also:
{cpp:func}`~BView::MovePenBy`,
{cpp:func}`~BView::SetFont`,
the {cpp:class}`BFont` class

::::

::::{abi-group}

:::{cpp:function} void BView::FillRegion(BRegion* region, pattern aPattern = B_SOLID_HIGH) const
:::

Fills the region with the pattern specified by {hparam}`aPattern`—or, if no
pattern is specified, with the current high color. Filling a region is
equivalent to filling all the rectangles that define the region.

See also:
The {cpp:class}`BRegion` class

::::

::::{abi-group}

:::{cpp:function} void BView::StrokeBezier(BPoint* controlPoints, pattern aPattern = B_SOLID_HIGH) const
:::
:::{cpp:function} void BView::FillBezier(BPoint* controlPoints, pattern aPattern = B_SOLID_HIGH) const
:::

These functions draw a third degree Bezier curve. {hmethod}`StrokeBezier()` strokes
a line along the path of the curve; the width of the line is determined
by the current pen size. {hmethod}`FillBezier()` fills in the region defined by the
path of the curve and the line joining the two endpoints.

{hparam}`controlPoints` points to an array of the four points for the curve. Both
functions draw using the pattern specified by {hparam}`aPattern`—or, if no
pattern is specified, in the current high color. Neither function alters
the current pen position.

See also:
{cpp:func}`~BView::StrokeEllipse`,
{cpp:func}`~BView::SetPenSize`,
{cpp:func}`~BView::StrokeRoundRect`

::::

::::{abi-group}

:::{cpp:function} void BView::StrokeEllipse(BRect rect, pattern aPattern = B_SOLID_HIGH)
:::
:::{cpp:function} void BView::StrokeEllipse(BPoint center, float xRadius, float yRadius, pattern aPattern = B_SOLID_HIGH)
:::
:::{cpp:function} void BView::FillEllipse(BRect rect, pattern aPattern = B_SOLID_HIGH)
:::
:::{cpp:function} void BView::FillEllipse(BPoint center, float xRadius, float yRadius, pattern aPattern = B_SOLID_HIGH)
:::
:::{cpp:function} void BView::StrokeArc(BRect rect, float angle, float span, pattern aPattern = B_SOLID_HIGH)
:::
:::{cpp:function} void BView::StrokeArc(BPoint center, float xRadius, float yRadius, float angle, float span, pattern aPattern = B_SOLID_HIGH)
:::
:::{cpp:function} void BView::FillArc(BRect rect, float angle, float span, pattern aPattern = B_SOLID_HIGH)
:::
:::{cpp:function} void BView::FillArc(BPoint center, float xRadius, float yRadius, float angle, float span, pattern aPattern = B_SOLID_HIGH)
:::

These functions draw all or part of the ellipse that's inscribed in {hparam}`rect`
or that has its center at {hparam}`center` and has horizontal and vertical radii
{hparam}`xRadius` and {hparam}`yRadius`. The ellipse is always aligned with the x and y axes.
A more flexible curve-drawing mechanism is given by
{cpp:func}`~BView::StrokeBezier` and
{cpp:func}`~BView::FillBezier`.

{hmethod}`StrokeEllipse()` strokes a line around the entire perimeter of the ellipse
and {hmethod}`FillEllipse()` fills the area the ellipse encloses.

{hmethod}`StrokeArc()` and {hmethod}`FillArc()`
stroke and fill a section of the ellipse,
starting at {hparam}`angle` (where 0 ° points right along the x-axis) and
proceeding (counterclockwise) span degrees. In the illustration below,
the red arc is the result of {hmethod}`StrokeArc()` with an angle of 10° and span
of 235°; the blue area is the same arc filled through {hmethod}`FillArc()`. The
center of the ellipse (the yellow dot) is drawn for reference.


:::{admonition} Warning
:class: warning
Currently, angle and span measurements in fractions of a degree are not
supported.
:::

For the stroking functions, the width of the stroked line is determined
by the current pen size. All functions draw using {hparam}`aPattern` or, if no
pattern is specified, the current high color. The functions neither
depend on nor alter the current pen position.

::::

::::{abi-group}

:::{cpp:function} void BView::StrokeArc(BPoint start, BPoint end, pattern aPattern = B_SOLID_HIGH)
:::
:::{cpp:function} void BView::StrokeArc(BPoint end, pattern aPattern = B_SOLID_HIGH)
:::

Draws a straight line between the {hparam}`start` and {hparam}`end` points—or, if no
starting point is given, between the current pen position and end
point—and leaves the pen at the end point.

This function draws the line using the current pen size and the specified
pattern. If no pattern is specified, the line is drawn in the current
high color. The points are specified in the {hclass}`BView`'s coordinate system.

See also:
{cpp:func}`~BView::SetPenSize`
{cpp:func}`~BView::BeginLineArray`

::::

::::{abi-group}

:::{cpp:function} void BView::StrokePolygon(BPolygon polygon, bool isClosed = true, pattern aPattern = B_SOLID_HIGH)
:::
:::{cpp:function} void BView::StrokePolygon(BPoint* pointList, int32 numPoints, bool isClosed = true, pattern aPattern = B_SOLID_HIGH)
:::
:::{cpp:function} void BView::StrokePolygon(BPoint* pointList, int32 numPoints, BRect rect, bool isClosed = true, pattern aPattern = B_SOLID_HIGH)
:::
:::{cpp:function} void BView::FillPolygon(BPolygon polygon, bool isClosed = true, pattern aPattern = B_SOLID_HIGH)
:::
:::{cpp:function} void BView::FillPolygon(BPoint* pointList, int32 numPoints, bool isClosed = true, pattern aPattern = B_SOLID_HIGH)
:::
:::{cpp:function} void BView::FillPolygon(BPoint* pointList, int32 numPoints, BRect rect, bool isClosed = true, pattern aPattern = B_SOLID_HIGH)
:::

These functions draw a polygon with an arbitrary number of sides.
{hmethod}`StrokePolygon()` strokes a line around the edge of the polygon using the
current pen size. If a {hparam}`pointList` is specified rather than a
{cpp:class}`BPolygon`
object, this function strokes a line from point to point, connecting the
first and last points if they aren't identical. However, if the {hparam}`isClosed`
flag is {cpp:enum}`false`, {hmethod}`StrokePolygon()` won't stroke the line connecting the first
and last points that define the
{cpp:class}`BPolygon`
(or the first and last points in
the {hparam}`pointList`). This leaves the polygon open—making it not appear
to be a polygon at all, but rather a series of straight lines connected
at their end points. If {hparam}`isClosed` is {cpp:enum}`true`, as it is by default, the
polygon will appear to be a polygon, a closed figure.

{hmethod}`FillPolygon()` is a simpler function; it fills in the entire area enclosed
by the polygon.

Both functions must calculate the frame rectangle of a polygon
constructed from a point list—that is, the smallest rectangle that
contains all the points in the polygon. If you know what this rectangle
is, you can make the function somewhat more efficient by passing it as
the {hparam}`rect` parameter.

Both functions draw using the specified pattern—or, if no pattern
is specified, in the current high color. Neither function alters the
current pen position.

See also:
{cpp:func}`~BView::SetPenSize`

::::

::::{abi-group}

:::{cpp:function} void BView::StrokeRect(BRect rect, pattern aPattern = B_SOLID_HIGH)
:::
:::{cpp:function} void BView::FillRect(BRect rect, pattern aPattern = B_SOLID_HIGH)
:::

These functions draw a rectangle. {hmethod}`StrokeRect()` strokes a line around the
edge of the rectangle; the width of the line is determined by the current
pen size. {hmethod}`FillRect()` fills in the entire rectangle.

Both functions draw using the pattern specified by {hparam}`aPattern`—or, if
no pattern is specified, in the current high color. Neither function
alters the current pen position.

See also:
{cpp:func}`~BView::SetPenSize`,
{cpp:func}`~BView::StrokeRoundRect`

::::

::::{abi-group}

:::{cpp:function} void BView::StrokeRoundRect(BRect rect, float xRadius, float yRadius, pattern aPattern = B_SOLID_HIGH)
:::
:::{cpp:function} void BView::FillRoundRect(BRect rect, float xRadius, float yRadius, pattern aPattern = B_SOLID_HIGH)
:::

These functions draw a rectangle with rounded corners. The corner arc is
one-quarter of an ellipse, where the ellipse would have a horizontal
radius equal to {hparam}`xRadius` and a vertical radius equal to {hparam}`yRadius`.

Except for the rounded corners of the rectangle, these functions work
exactly like
{cpp:func}`~BView::StrokeRect` and
{cpp:func}`~BView::FillRect`.

Both functions draw using the pattern specified by {hparam}`aPattern`—or, if
no pattern is specified, in the current high color. Neither function
alters the current pen position.

See also:
{cpp:func}`~BView::StrokeEllipse`

::::

::::{abi-group}

:::{cpp:function} void BView::StrokeShape(BShape* shape, pattern aPattern = B_SOLID_HIGH)
:::
:::{cpp:function} void BView::FillShape(BShape* shape, pattern aPattern = B_SOLID_HIGH)
:::

These functions draw a shape. {hmethod}`StrokeShape()` strokes a line around the
edge of the shape; the width of the line is determined by the current pen
size. {hmethod}`FillShape()` fills in the entire shape.

Both functions draw using the pattern specified by {hparam}`aPattern`—or, if
no pattern is specified, in the current high color. Neither function
alters the current pen position.

See also:
{cpp:func}`~BView::SetPenSize`

::::

::::{abi-group}

:::{cpp:function} void BView::StrokeTriangle(BPoint firstPoint, BPoint secondPoint, BPoint thirdPoint, pattern aPattern = B_SOLID_HIGH)
:::
:::{cpp:function} void BView::StrokeTriangle(BPoint firstPoint, BPoint secondPoint, BPoint thirdPoint, BRect rect, pattern aPattern = B_SOLID_HIGH)
:::
:::{cpp:function} void BView::FillTriangle(BPoint firstPoint, BPoint secondPoint, BPoint thirdPoint, pattern aPattern = B_SOLID_HIGH)
:::
:::{cpp:function} void BView::FillTriangle(BPoint firstPoint, BPoint secondPoint, BPoint thirdPoint, BRect rect, pattern aPattern = B_SOLID_HIGH)
:::

These functions draw a triangle, a three-sided polygon.
{hmethod}`StrokeTriangle()` strokes a line the width of the
current pen size from the first point to the second, from the second point
to the third, then back to the first point.
{hmethod}`FillTriangle()` fills in the area that the three
points enclose.

Each function must calculate the smallest rectangle that contains the
triangle. If you know what this rectangle is, you can make the function
marginally more efficient by passing it as the {hparam}`rect` parameter.

Both functions do their drawing using the pattern specified by
{hparam}`aPattern`—or, if no pattern is specified, in the current high color.
Neither function alters the current pen position.

See also:
{cpp:func}`~BView::SetPenSize`

::::

::::{abi-group}

:::{cpp:function} void BView::BeginLineArray(int32 count)
:::
:::{cpp:function} void BView::AddLine(BPoint start, BPoint end, rgb_color color)
:::
:::{cpp:function} void BView::EndLineArray()
:::

These functions provide a more efficient way of drawing a large number of
lines than repeated calls to
{cpp:func}`~BView::StrokeLine`.
{hmethod}`BeginLineArray()`
signals the beginning of a series of up to count
{hmethod}`AddLine()` calls;
{hmethod}`EndLineArray()`
signals the end of the series. Each
{hmethod}`AddLine()`
call defines a line from
the start point to the end point, associates it with a particular {hparam}`color`,
and adds it to the array. The lines can each be a different color; they
don't have to be contiguous. When
{hmethod}`EndLineArray()`
is called, all the lines
are drawn—using the then current pen size—in the order that
they were added to the array.

These functions don't change any graphics parameters. For example, they
don't move the pen or change the current high and low colors. Parameter
values that are in effect when
{hmethod}`EndLineArray()`
is called are the ones used
to draw the lines. The high and low colors are ignored in favor of the
{hparam}`color` specified for each line.

The {hparam}`count` passed to
{hmethod}`BeginLineArray()`
is an upper limit on the number of
lines that can be drawn. Keeping the count close to accurate and within
reasonable bounds helps the efficiency of the line-array mechanism. It's
a good idea to keep it less than 256; above that number, memory
requirements begin to impinge on performance.

See also:
{cpp:func}`~BView::StrokeLine`

::::

::::{abi-group}

:::{cpp:function} void BView::BeginPicture(BPicture* picture)
:::
:::{cpp:function} void BView::AppendToPicture(BPicture* picture)
:::
:::{cpp:function} BPicture* BView::EndPicture()
:::

{hmethod}`BeginPicture()` starts a new "picture recording" session: Subsequent
drawing instructions invoked upon the view are recorded in the
{cpp:class}`BPicture`
argument. {hmethod}`AppendToPicture()` does the same, but doesn't clear the argument
first—it tacks additional instructions on to the end of the
{cpp:class}`BPicture`.
{hmethod}`EndPicture()` ends the recording session; it returns the object
that was passed to {hmethod}`BeginPicture()` or {hmethod}`AppendToPicture()`.

While it's recording a picture, the {hclass}`BView`
doesn't display anything to the screen. To render the drawing, you use the
{cpp:func}`~BView::DrawPicture`
function.

The picture captures only primitive graphics operations such as
{cpp:func}`~BView::DrawString`,
{cpp:func}`~BView::FillArc`,
and {cpp:func}`~BView::SetFont`.
Furthermore, only instructions
performed by this view are recorded; the drawing done by the view's
children is not recorded.

A {cpp:class}`BPicture`
can be recorded only if the {hclass}`BView` is attached to a window. The
window can be off-screen and the view itself can be hidden or reside
outside the current clipping region.

::::

::::{abi-group}

:::{cpp:function} void BView::CopyBits(BRect source, BRect destination)
:::

Copies the image displayed in the {hparam}`source`
rectangle to the {hparam}`destination`
rectangle, where both rectangles lie within the view and are stated in
the {hclass}`BView`'s coordinate system.

If the two rectangles aren't the same size, the source image is scaled to
fit.

If not all of the {hparam}`destination` rectangle lies
within the {hclass}`BView`'s visible
region, the {hparam}`source` image is clipped rather than scaled.

If not all of the {hparam}`source` rectangle lies within
the {hclass}`BView`'s visible
region, only the visible portion is copied. It's mapped to the
corresponding portion of the destination rectangle. The {hclass}`BView` is then
invalidated so its
{cpp:func}`~BView::Draw`
function will be called to update the part of
the destination rectangle that can't be filled with the source image.

The {hclass}`BView` must be attached to a window.

::::

::::{abi-group}

:::{cpp:function} void BView::DrawPicture(const BPicture* picture)
:::
:::{cpp:function} void BView::DrawPicture(const BPicture* picture, BPoint point)
:::
:::{cpp:function} void BView::DrawPicture(const char* filename, off_t offset, BPoint point)
:::
:::{cpp:function} void BView::DrawPictureAsync(const BPicture* picture)
:::
:::{cpp:function} void BView::DrawPictureAsync(const BPicture* picture, BPoint point)
:::
:::{cpp:function} void BView::DrawPictureAsync(const char* filename, off_t offset, BPoint point)
:::

Draws the previously recorded picture at the current pen
position—or at the specified point in the {hclass}`BView`'s coordinate
system. The point or pen position is taken as the coordinate origin for
all the drawing instructions recorded in the
{cpp:class}`BPicture`. The last form of
the method plays a picture from an arbitrary offset of a file.

The two functions differ in only one respect: {hmethod}`DrawPicture()` waits for the
Application Server to finish rendering the image before it returns.
{hmethod}`DrawPictureAsync()`
doesn't wait; it passes the image to the server and
returns immediately. The latter function can be more efficient in some
cases—for example, you might use an asynchronous function to draw
several bitmaps and then call
{cpp:func}`~BView::Sync`
to wait for them all to finish rather than wait for each one individually:

Nothing that's done in the
{cpp:class}`BPicture`
can affect anything in the {hclass}`BView`'s
graphics state—for example, the
{cpp:class}`BPicture` can't reset the current
high color or the pen position. Conversely, nothing in the {hclass}`BView`'s
current graphics state affects the drawing instructions captured in the
picture. The graphics parameters that were in effect when the picture was
recorded determine what the picture looks like.

See also:
{cpp:func}`~BView::BeginPicture`

::::

::::{abi-group}

:::{cpp:function} void BView::Flush() const
:::
:::{cpp:function} void BView::Sync() const
:::

These functions flush the window's connection to the Application Server.
If the {hclass}`BView` isn't attached to a window,
{hmethod}`Flush()` does nothing.

:::{admonition} Warning
:class: warning
If the {hclass}`BView` isn't attached to a window, {hmethod}`Sync()` will crash the
application.
:::

For reasons of efficiency, the window's connection to the Application
Server is buffered. Drawing instructions destined for the server are
placed in the buffer and dispatched as a group when the buffer becomes
full. Flushing empties the buffer, sending whatever it contains to the
server, even if it's not yet full.

The buffer is automatically flushed on every update. However, if you do
any drawing outside the update mechanism—in response to interface
messages, for example—you need to explicitly flush the connection
so that drawing instructions won't languish in the buffer while waiting
for it to fill up or for the next update. You should also flush it if you
call any drawing functions from outside the window's thread.

{hmethod}`Flush()` simply flushes the buffer and returns. It does the same work as
{cpp:class}`BWindow`'s
{cpp:func}`~BWindow::Flush` of the same name.

{hmethod}`Sync()` flushes the connection, then waits until the server has executed
the last instruction that was in the buffer before returning. This
alternative to {hmethod}`Flush()` prevents the application from getting ahead of the
server (ahead of what the user sees on-screen) and keeps both processes
synchronized.

It's a good idea, for example, to call {hmethod}`Sync()`,
rather than {hmethod}`Flush()`, after
employing {hclass}`BView`s to produce a bitmap image (a
{cpp:class}`BBitmap` object).
{hmethod}`Sync()` is
the only way you can be sure the image has been completely rendered
before you attempt to draw with it.

(Note that all {hclass}`BView`s attached to a window share the same connection to
the Application Server. Calling {hmethod}`Flush()`
or {hmethod}`Sync()` for any one of them
flushes the buffer for all of them.)

::::

::::{abi-group}

:::{cpp:function} void BView::Invalidate(BRect rect)
:::
:::{cpp:function} void BView::Invalidate()
:::

Invalidates the {hparam}`rect` portion of the view, causing update
messages—and consequently
{cpp:func}`~BView::Draw` notifications—to be
generated for the {hclass}`BView` and all descendants that lie wholly or partially
within the rectangle. The rectangle is stated in the {hclass}`BView`'s coordinate
system.

If no rectangle is specified, the {hclass}`BView`'s entire bounds rectangle is
invalidated.

Since only {hclass}`BView`s that are attached to a window can draw, only attached
{hclass}`BView`s can be invalidated.

See also:
{cpp:func}`~BView::Draw`,
{cpp:func}`~BView::GetClippingRegion`,
{cpp:func}`BWindow::UpdateIfNeeded`

::::

::::{abi-group}

:::{cpp:function} void BView::InvertRect(BRect rect)
:::

Inverts all the colors displayed within the {hparam}`rect` rectangle. A subsequent
{hmethod}`InvertRect()` call on the same rectangle restores the original colors.
This operation can be used to "highlight" a selection made as the user
drags the mouse.

The rectangle is stated in the {hclass}`BView`'s coordinate system.

See also:
{cpp:func}`BScreen::ColorMap`

::::

::::{abi-group}

:::{cpp:function} void BView::SetViewBitmap(const BBitmap* bitmap, uint32 follow = B_FOLLOW_TOP | B_FOLLOW_LEFT, uint32 options = B_TILE_BITMAP)
:::
:::{cpp:function} void BView::SetViewBitmap(const BBitmap* bitmap, BRect source, BRect destination, uint32 follow = B_FOLLOW_TOP | B_FOLLOW_LEFT, uint32 options = B_TILE_BITMAP)
:::
:::{cpp:function} void BView::ClearViewBitmap()
:::

{hmethod}`SetViewBitmap()` sets the background bitmap for the view. The view bitmap
is a background image for the view; all drawing in the view occurs over
this bitmap. The background color is used to fill in the visible regions
not covered by the background bitmap.

The background bitmap is passed in {hparam}`bitmap`.
The caller can delete {hparam}`bitmap`
after the function returns.

If a {hparam}`source` rectangle is given, only that part of the bitmap is used.
Otherwise, the entire bitmap is used as the background bitmap. The
{hparam}`destination` rectangle, if given, specifies the placement of the bitmap in
the view. It need not be the same size as the source rectangle; scaling
is performed automatically by the application server. If no destination
is given, the image will be placed, unscaled, at the upper left corner of
the view.

{hparam}`follow` determines the behavior of destination as the view is resized; see
the {hclass}`BView` {cpp:func}`~BView::Constructor`
for specifics. {hparam}`options` specifies additional view
options. Currently, only one option, {cpp:enum}`B_TILE_BITMAP`, is defined. If set,
the view bitmap is tiled across the view.

{hmethod}`ClearViewBitmap()` clears the background bitmap for the view.

See also:
"{cpp:func}`~TheInterfaceKit::Drawing`"
in the "{ref}`Drawing`"
section of this chapter,
{cpp:func}`~BView::SetViewColor`

::::

::::{abi-group}

:::{cpp:function} void BView::SetViewOverlay(const BBitmap* bitmap, rgb_color* colorKey, uint32 follow = B_FOLLOW_TOP | B_FOLLOW_LEFT, uint32 options = 0)
:::
:::{cpp:function} void BView::SetViewOverlay(const BBitmap* bitmap, BRect source, BRect destination, rgb_color* colorKey, uint32 follow = B_FOLLOW_TOP | B_FOLLOW_LEFT, uint32 options = 0)
:::
:::{cpp:function} void BView::ClearViewOverlay()
:::

{hmethod}`SetViewOverlay()` sets the overlay bitmap for the view. The overlay bitmap
is superimposed on top of the view's contents. The {hparam}`colorKey` is used to
determine which color in the overlay should be treated as transparent,
allowing the view's contents to be visible.

The overlay bitmap is passed in {hparam}`bitmap`. The
caller can delete {hparam}`bitmap`
after the function returns.

If a {hparam}`source` rectangle is given, only that part of the bitmap is used.
Otherwise, the entire bitmap is used as the overlay bitmap. The
{hparam}`destination` rectangle, if given, specifies the placement of the overlay
bitmap in the view. It need not be the same size as the {hparam}`source` rectangle;
scaling is performed automatically by the application server. If no
{hparam}`destination` is given, the image will be placed, unscaled, at the upper
left corner of the view.

{hparam}`follow` determines the behavior of destination as the view is resized; see
the {hclass}`BView` {cpp:func}`~BView::Constructor`
for specifics. {hparam}`options` specifies additional view
options. The same options allowed by
{cpp:func}`~BView::SetViewBitmap` are allowed here.

:::{admonition} Note
:class: note
You can't use both a background bitmap and an overlay in the same view.
:::

{hmethod}`ClearViewOverlay()` clears the overlay bitmap for the view.

::::

## Static Functions
::::{abi-group}

:::{cpp:function} static BArchivable* BView::Instantiate(BMessage* archive)
:::

Returns a new {hclass}`BView` object, allocated by new and created with the version
of the constructor that takes a
{cpp:class}`BMessage` archive. However, if the message
doesn't contain archived data for a {hclass}`BView`,
{hmethod}`Instantiate()` returns {cpp:enum}`NULL`.

See also:
{cpp:func}`BArchivable::Instantiate`,
{cpp:func}`~instantiate::object`

::::

## Scripting Support
::::{abi-group}

FrameThe Frame property represents the frame rectangle of the view. The frame is passed as a {cpp:class}`BRect` ({cpp:enum}`B_RECT_TYPE`).MessageSpecifiersDescriptionB_GET_PROPERTYB_DIRECT_SPECIFIERReturns the view's frame rectangle.B_SET_PROPERTYB_DIRECT_SPECIFIERSets the view's frame rectangle.
HiddenThe "Hidden" property determines the visibility of the view. The messages are equivalent to manipulating the view with the {cpp:func}`~BView::IsHidden`, {cpp:func}`~BView::Hide`, and {cpp:func}`~BView::Show`. Note that this differs slightly from {cpp:class}`BWindow`'s {cpp:func}`~BWindow::Scripting` property, where multiple hides or shows are not nested.MessageSpecifiersDescriptionB_GET_PROPERTYB_DIRECT_SPECIFIERReturns true if the view is hidden; false otherwise.B_SET_PROPERTYB_DIRECT_SPECIFIERHides or shows the view.
ViewThe "View" property represents the child views of the current view. For all messages except {cpp:enum}`B_COUNT_PROPERTIES`, the current specifier is popped off the specifier stack before the scripting message is passed to the target view. Views can be specified either by index (as found by {cpp:func}`~BView::ChildAt`), or name (as found by {cpp:func}`~BView::FindView`).MessageSpecifiersDescriptionB_COUNT_PROPERTIESB_DIRECT_SPECIFIERReturns the number of of child views.anyB_INDEX_SPECIFIER, B_REVERSE_INDEX_SPECIFIER, B_NAME_SPECIFIERDirects the scripting message to the specified view.
::::

::::{abi-group}

ShelfThe "Shelf" property pops the current specifier off the specifier stack and then passes the scripting message to the shelf. If no shelf is present, an error is returned.MessageSpecifiersDescriptionanyB_DIRECT_SPECIFIERDirects the scripting message to the shelf.
::::

## Archived Fields