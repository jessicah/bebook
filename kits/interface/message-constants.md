# Message Constants

## Container Messages

- {cpp:enumerator}`B_MIME_DATA`

- {cpp:enumerator}`B_SIMPLE_DATA`

A few constants identify messages as data containers. The system currently
uses the {cpp:enumerator}`B_MIME_DATA` and {cpp:enumerator}`B_SIMPLE_DATA`
constants to mark the containers it constructs for drag-and-drop
operations.

::::{abi-group}
:::{cpp:enumerator} B_MIME_DATA
:::

This message constant indicates that all the data in the message is
identified by MIME type names. The type code of every data field is
{cpp:enumerator}`B_MIME_TYPE` and the name of each field is the MIME type
string.

As an example, a {cpp:class}`BTextView` object puts together a
{cpp:enumerator}`B_MIME_DATA` message for drag-and-drop operations. The
message has the text itself in a field named "text/plain"; the
{ref}`text_run_array` structure that describes the character formats of the
text is in a field named "application/x-vnd.Be-text_run_array".
::::

::::{abi-group}
:::{cpp:enumerator} B_SIMPLE_DATA
:::

This message is a package for a single data element. If there are multiple
data fields in the message, they present the same data in various formats.

For example, when the user drags selected files and directories from a
Tracker window, the Tracker packages {htype}`entry_ref` references to them
in a {cpp:enumerator}`B_SIMPLE_DATA` message. The references are in a
{hparam}`refs` array with a type code of {cpp:enumerator}`B_REF_TYPE`. In
other words, the message has the same structure as a
{cpp:enumerator}`B_REFS_RECEIVED` message, but a different what constant.
::::

## Selection Messages

- {cpp:enumerator}`B_CUT`

- {cpp:enumerator}`B_COPY`

- {cpp:enumerator}`B_PASTE`

- {cpp:enumerator}`B_SELECT_ALL`

Declared in: app/AppDefs.h

These messages are sent to {cpp:class}`BTextView` and {cpp:class}`BWindow`
classes (which normally passes the message to a {cpp:class}`BTextView`
instance) to cut, copy, paste and select all items respectively.

::::{abi-group}
:::{cpp:enumerator} B_CUT
:::

Removes the selected items and moves it to the clipboard.

The {hkey}`Command`+{hkey}`X` key combination is normally mapped to
{hclass}`B_CUT`
::::

::::{abi-group}
:::{cpp:enumerator} B_COPY
:::

Copies the selected items to the clipboard.

The {hkey}`Command`+{hkey}`C` key combination is normally mapped to
{hclass}`B_COPY`
::::

::::{abi-group}
:::{cpp:enumerator} B_PASTE
:::

Pastes items stored in the clipboard into the view.

The {hkey}`Command`+{hkey}`V` key combination is normally mapped to
{hclass}`B_PASTE`
::::

::::{abi-group}
:::{cpp:enumerator} B_SELECT_ALL
:::

Selects all the items in the clipboard into the view.

The {hkey}`Command`+{hkey}`A` key combination is normally mapped to
{hclass}`B_SELECT_ALL`
::::

## Status Bar Messages

::::{abi-group}
:::{cpp:enumerator} B_UPDATE_STATUS_BAR
:::

:::{list-table}
---
header-rows: 0
align: left
widths: auto
---
-
	- Purpose:

	- Deliverable

-
	- Source:

	- Your app.

-
	- Target:

	- The {cpp:class}`BStatusBar` you're updating.

-
	- Hook:

	- {cpp:func}`BStatusBar::Update`


:::

You construct and send this message to a {cpp:class}`BStatusBar` object to
tell it to (asynchronously) update its progress. To send the message,
invoke {cpp:class}`BWindow`'s {cpp:func}`PostMessage()
<BLooper::PostMessage>` naming the target {cpp:class}`BStatusBar` as the
handler:

:::{code} cpp
statusBar->Window()->PostMessage(theMessage, statusBar);
:::

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
	- {hparam}`delta`

	- {cpp:enumerator}`B_FLOAT_TYPE`

	- An increment to the object's current value.

-
	- {hparam}`text`

	- {cpp:enumerator}`B_STRING_TYPE`

	- The object's new text ({cpp:expr}`NULL`-terminated).

-
	- {hparam}`trailing_text`

	- {cpp:enumerator}`B_STRING_TYPE`

	- The object's new trailing text ({cpp:expr}`NULL`-terminated)..


:::
::::

::::{abi-group}
:::{cpp:enumerator} B_RESET_STATUS_BAR
:::

:::{list-table}
---
header-rows: 0
align: left
widths: auto
---
-
	- Purpose:

	- Deliverable

-
	- Source:

	- Your app.

-
	- Target:

	- {cpp:func}`Reset() <BStatusBar::Reset>`

-
	- Hook:

	- The {cpp:class}`BStatusBar` you're resetting.


:::

You construct and send this message to a {cpp:class}`BStatusBar` object to
tell it to (asynchronously) reset itself. The message also lets you reset
the object's labels. To send the message, invoke {cpp:class}`BWindow`'s
{cpp:func}`PostMessage() <BLooper::PostMessage>` naming the target
{cpp:class}`BStatusBar` as the handler:

:::{code} cpp
statusBar->Window()->PostMessage(theMessage, statusBar);
:::

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
	- {hparam}`label`

	- {cpp:enumerator}`B_STRING_TYPE`

	- The object's new label (NULL-terminated).

-
	- {hparam}`trailing_label`

	- {cpp:enumerator}`B_STRING_TYPE`

	- The object's new trailing label ({cpp:expr}`NULL`-terminated)..


:::
::::

## General Constants

::::{abi-group}
:::{cpp:enumerator} B_CONTROL_INVOKED
:::

:::{list-table}
---
header-rows: 0
align: left
widths: auto
---
-
	- Purpose:

	- Deliverable

-
	- Source:

	- A {cpp:class}`BControl`.

-
	- Target:

	- Selected {cpp:class}`BMessenger`.


:::

This message is sent to the targeted messenger when a
{cpp:class}`BControl`-derived object is invoked.
::::

## Keyboard Messages

::::{abi-group}
:::{cpp:enumerator} B_KEY_DOWN
:::

:::{list-table}
---
header-rows: 0
align: left
widths: auto
---
-
	- Purpose:

	- Deliverable

-
	- Source:

	- The system.

-
	- Target:

	- The focus view's {cpp:class}`BWindow`.

-
	- Hook:

	- {cpp:func}`BView::KeyDown` ({cpp:enumerator}`B_KEY_DOWN`)
{cpp:func}`BView::KeyUp` ({cpp:enumerator}`B_KEY_UP`)   (The
...{cpp:enumerator}`UNMAPPED`... messages don't map to hook functions.)


:::

{cpp:enumerator}`B_KEY_DOWN` is sent when the user presses (or holds down)
a key that's mapped to a character; {cpp:enumerator}`B_KEY_UP` is sent when
the user releases the key. {cpp:enumerator}`B_UNMAPPED_KEY_DOWN` and
{cpp:enumerator}`B_UNMAPPED_KEY_UP` are sent if the key isn't mapped to a
character. This doesn't include modifier keys, which are reported in the
{cpp:enumerator}`B_MODIFIERS_CHANGED` message.

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
	- {hparam}`when`

	- {cpp:enumerator}`B_INT64_TYPE`

	- Event time, in microseconds since 01/01/70

-
	- {hparam}`key`

	- {cpp:enumerator}`B_INT32_TYPE`

	- The code for the physical key that was pressed. See <x> for the key map.

-
	- {hparam}`be:key_repeat` ({cpp:enumerator}`B_KEY_DOWN` only)

	- {cpp:enumerator}`B_INT32_TYPE`

	- The "iteration number" of this key down. When the user holds the key down,
successive messages are sent with increasing key repeat values. This field
isn't present in the initial event; the first repeat message (i.e., the
second key down message) has a key repeat value of 1.

-
	- {hparam}`modifiers`

	- {cpp:enumerator}`B_INT32_TYPE`

	- The modifier keys that were in effect at the time of the event. See <x>
for a list of values.

-
	- {hparam}`states`

	- {cpp:enumerator}`B_UINT8_TYPE`

	- The state of all keys at the time of the event. See <x>.

-
	- {hparam}`byte` [3] ({cpp:enumerator}`B_KEY_DOWN` and
{cpp:enumerator}`B_KEY_UP` only)

	- {cpp:enumerator}`B_INT8_TYPE`

	- The UTF8 data that's generated

-
	- {hparam}`bytes` ({cpp:enumerator}`B_KEY_DOWN` and
{cpp:enumerator}`B_KEY_UP` only)

	- {cpp:enumerator}`B_STRING_TYPE`

	- The string that's generated. (The string usually contains a single
character.)

-
	- {hparam}`raw_char` ({cpp:enumerator}`B_KEY_DOWN` and
{cpp:enumerator}`B_KEY_UP` only)

	- {cpp:enumerator}`B_INT32_TYPE`

	- Modifier-independent ASCII code for the character.


:::
::::

::::{abi-group}
:::{cpp:enumerator} B_MODIFIERS_CHANGED
:::

:::{list-table}
---
header-rows: 0
align: left
widths: auto
---
-
	- Purpose:

	- Deliverable

-
	- Source:

	- The system.

-
	- Target:

	- The focus view's window.

-
	- Hook:

	- 


:::

Sent when the user presses or releases a modifier key.

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
	- {hparam}`when`

	- {cpp:enumerator}`B_INT64_TYPE`

	- Event time, in microseconds since 01/01/70

-
	- {hparam}`modifiers`

	- {cpp:enumerator}`B_INT32_TYPE`

	- The current modifier keys.

-
	- {hparam}`be:old_modifiers`

	- {cpp:enumerator}`B_INT32_TYPE`

	- The previous modifier keys.

-
	- {hparam}`states`

	- {cpp:enumerator}`B_UINT8_TYPE`

	- The state of all keys at the time of the event. See <x>.


:::
::::

## Mouse Messages

::::{abi-group}
:::{cpp:enumerator} B_MOUSE_DOWN
:::

:::{list-table}
---
header-rows: 0
align: left
widths: auto
---
-
	- Purpose:

	- Deliverable

-
	- Source:

	- The system.

-
	- Target:

	- The {cpp:class}`BWindow` of the view the mouse is pointing to.

-
	- Hook:

	- {cpp:func}`BView::MouseDown`


:::

Sent when the user presses a mouse button. This message is only sent if no
other mouse button is already down.

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
	- {hparam}`when`

	- {cpp:enumerator}`B_INT64_TYPE`

	- Event time, in microseconds since 01/01/70

-
	- {hparam}`where`

	- {cpp:enumerator}`B_POINT_TYPE`

	- Mouse location in the view's coordinate system.

-
	- {hparam}`modifiers`

	- {cpp:enumerator}`B_INT32_TYPE`

	- The modifier keys that were in effect at the time of the event.

-
	- {hparam}`buttons`

	- {cpp:enumerator}`B_INT32_TYPE`

	- The mouse button that was pressed, one of:
{cpp:enumerator}`B_PRIMARY_MOUSE_BUTTON`,
{cpp:enumerator}`B_SECONDARY_MOUSE_BUTTON`,
{cpp:enumerator}`B_TERTIARY_MOUSE_BUTTON`

-
	- {hparam}`clicks`

	- {cpp:enumerator}`B_INT32_TYPE`

	- 1 for a single-click, 2 for double-click, 3 for triple-click, and so on.
The counter is reset if the time between clicks exceeds the "Double-click
speed" set by the user in the Mouse preferences. Note that the counter is
not reset if the mouse moves between clicks.


:::
::::

::::{abi-group}
:::{cpp:enumerator} B_MOUSE_MOVED
:::

:::{list-table}
---
header-rows: 0
align: left
widths: auto
---
-
	- Purpose:

	- Deliverable

-
	- Source:

	- The system.

-
	- Target:

	- The {cpp:class}`BWindow` of the view the mouse is pointing to.

-
	- Hook:

	- {cpp:func}`BView::MouseMoved`


:::

Sent when the user moves the mouse.

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
	- {hparam}`when`

	- {cpp:enumerator}`B_INT64_TYPE`

	- Event time, in microseconds since 01/01/70

-
	- {hparam}`where`

	- {cpp:enumerator}`B_POINT_TYPE`

	- The mouse's new location in window coordinates.

-
	- {hparam}`buttons`

	- {cpp:enumerator}`B_INT32_TYPE`

	- The mouse buttons that are down. Zero or more of:
{cpp:enumerator}`B_PRIMARY_MOUSE_BUTTON`,
{cpp:enumerator}`B_SECONDARY_MOUSE_BUTTON`,
{cpp:enumerator}`B_TERTIARY_MOUSE_BUTTON`


:::
::::

::::{abi-group}
:::{cpp:enumerator} B_MOUSE_UP
:::

:::{list-table}
---
header-rows: 0
align: left
widths: auto
---
-
	- Purpose:

	- Deliverable

-
	- Source:

	- The system.

-
	- Target:

	- {cpp:class}`BWindow` of the view the mouse is pointing to.

-
	- Hook:

	- {cpp:func}`BView::MouseUp`


:::

Sent when the user releases a mouse button. It's only sent if no other
mouse button remains down.

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
	- {hparam}`when`

	- {cpp:enumerator}`B_INT64_TYPE`

	- Event time, in microseconds since 01/01/70

-
	- {hparam}`where`

	- {cpp:enumerator}`B_POINT_TYPE`

	- Mouse location in the view's coordinate system.

-
	- {hparam}`modifiers`

	- {cpp:enumerator}`B_INT32_TYPE`

	- The modifier keys that were in effect at the time of the event.


:::
::::

::::{abi-group}
:::{cpp:enumerator} B_MOUSE_WHEEL_CHANGED
:::

:::{list-table}
---
header-rows: 0
align: left
widths: auto
---
-
	- Purpose:

	- Deliverable

-
	- Source:

	- The system.

-
	- Target:

	- The {cpp:class}`BWindow` of the view the mouse is pointing to.

-
	- Hook:

	- 


:::

Sent when the user moves the mouse wheel (on mice that have them).

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
	- {hparam}`when`

	- {cpp:enumerator}`B_INT64_TYPE`

	- Event time, in microseconds since 01/01/70

-
	- {hparam}`be:wheel_delta_x`

	- {cpp:enumerator}`B_FLOAT_TYPE`

	- How much the Y value of the wheel has changed.

-
	- {hparam}`be:wheel_delta_y`

	- {cpp:enumerator}`B_FLOAT_TYPE`

	- How much the Y value of the wheel has changed.


:::

The standard mouse driver that comes with BeOS only supports a Y-oriented
wheel.
::::

## B_PRINTER_CHANGED



:::{list-table}
---
header-rows: 0
align: left
widths: auto
---
-
	- Purpose:

	- Deliverable

-
	- Source:

	- The Print Server.

-
	- Target:

	- Everyone.

-
	- Hook:

	- 


:::

Sent whenever the user changes printers. Applications that support
printing should watch for this message, and if they receive it, they should
suggest that the user check their page setup the next time they choose to
print.

## B_SCREEN_CHANGED



:::{list-table}
---
header-rows: 0
align: left
widths: auto
---
-
	- Purpose:

	- Deliverable

-
	- Source:

	- The system.

-
	- Target:

	- Every {cpp:class}`BWindow` in the screen that changed (even hidden
windows).

-
	- Hook:

	- {cpp:func}`BWindow::ScreenChanged`


:::

Sent when the screen's dimensions or color space changes—because the user
played with the Screen preferences app, for example.

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
	- {hparam}`when`

	- {cpp:enumerator}`B_INT64_TYPE`

	- Event time, in microseconds since 01/01/70

-
	- {hparam}`frame`

	- {cpp:enumerator}`B_RECT_TYPE`

	- The screen's dimensions.

-
	- {hparam}`mode`

	- {cpp:enumerator}`B_INT32_TYPE`

	- The screen's color space: {cpp:enumerator}`B_CMAP8`,
{cpp:enumerator}`B_RGB15`, {cpp:enumerator}`B_RGB15`, or
{cpp:enumerator}`BRGB32`.


:::

## B_VALUE_CHANGED



:::{list-table}
---
header-rows: 0
align: left
widths: auto
---
-
	- Purpose:

	- Deliverable

-
	- Source:

	- The system.

-
	- Target:

	- The manipulated scrollbar's {cpp:class}`BWindow`.

-
	- Hook:

	- {cpp:func}`BScrollBar::ValueChanged`


:::

Sent when the user plays with a scrollbar.

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
	- {hparam}`when`

	- {cpp:enumerator}`B_INT64_TYPE`

	- Event time, in microseconds since 01/01/70

-
	- {hparam}`value`

	- {cpp:enumerator}`B_INT32_TYPE`

	- The scrollbar's new value.


:::

## View Messages

::::{abi-group}
:::{cpp:enumerator} B_VIEW_MOVED
:::

:::{list-table}
---
header-rows: 0
align: left
widths: auto
---
-
	- Purpose:

	- Deliverable

-
	- Source:

	- The system.

-
	- Target:

	- The moved view's {cpp:class}`BWindow`.

-
	- Hook:

	- {cpp:func}`BView::FrameMoved`


:::

Sent when a view's origin (left top corner) changes relative to the origin
of its parent. The message isn't sent if the view doesn't have the
{cpp:enumerator}`B_FRAME_EVENTS` flag set.

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
	- {hparam}`when`

	- {cpp:enumerator}`B_INT64_TYPE`

	- Event time, in microseconds since 01/01/70

-
	- {hparam}`where`

	- {cpp:enumerator}`B_POINT_TYPE`

	- The view's new origin in the coordinate system of its parent.


:::
::::

::::{abi-group}
:::{cpp:enumerator} B_VIEW_RESIZED
:::

:::{list-table}
---
header-rows: 0
align: left
widths: auto
---
-
	- Purpose:

	- Deliverable

-
	- Source:

	- The system.

-
	- Target:

	- The resized view's {cpp:class}`BWindow`.

-
	- Hook:

	- {cpp:func}`BView::FrameResized`


:::

Sent when the size of the view's frame changes. The message isn't sent if
the view doesn't have the {cpp:enumerator}`B_FRAME_EVENTS` flag set.

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
	- {hparam}`when`

	- {cpp:enumerator}`B_INT64_TYPE`

	- Event time, in microseconds since 01/01/70

-
	- {hparam}`width`

	- {cpp:enumerator}`B_INT32_TYPE`

	- The view's new width.

-
	- {hparam}`height`

	- {cpp:enumerator}`B_INT32_TYPE`

	- The view's new height.

-
	- {hparam}`where`

	- {cpp:enumerator}`B_POINT_TYPE`

	- The view's new origin expressed in the coordinate system of its parent.
This field is only included if the view actually moved while being resized,
and can always be ignored: If the view did move, you'll hear about it in a
separate {cpp:enumerator}`B_VIEW_MOVED` {cpp:class}`BMessage`.


:::
::::

## Window Messages

::::{abi-group}
:::{cpp:enumerator} B_WINDOW_ACTIVATED
:::

:::{list-table}
---
header-rows: 0
align: left
widths: auto
---
-
	- Purpose:

	- Deliverable

-
	- Source:

	- The system.

-
	- Target:

	- The activated/deactivated {cpp:class}`BWindow`.

-
	- Hook:

	- {cpp:func}`BWindow::WindowActivated` and
{cpp:func}`BView::WindowActivated`


:::

Sent just after a window is activated or deactivated. Note that the
{cpp:class}`BWindow` invokes {cpp:func}`WindowActivated()
<BView::WindowActivated>` on each of its views.

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
	- {hparam}`when`

	- {cpp:enumerator}`B_INT64_TYPE`

	- Event time, in microseconds since 01/01/70

-
	- {hparam}`active`

	- {cpp:enumerator}`B_BOOL_TYPE`

	- {cpp:expr}`true` if the window is now active; {cpp:expr}`false` if not.


:::
::::

::::{abi-group}
:::{cpp:enumerator} B_WINDOW_MOVE_BY
:::

:::{list-table}
---
header-rows: 0
align: left
widths: auto
---
-
	- Purpose:

	- Deliverable.

-
	- Source:

	- Your application.

-
	- Target:

	- The {cpp:class}`BWindow` to be moved.

-
	- Hook:

	- 


:::

You can send this message to a window to resize it by the specified
deltas.

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
	- {hparam}`data`

	- {cpp:enumerator}`B_POINT_TYPE`

	- The amount by which to move the window's X and Y coordinates.


:::
::::

::::{abi-group}
:::{cpp:enumerator} B_WINDOW_MOVE_TO
:::

:::{list-table}
---
header-rows: 0
align: left
widths: auto
---
-
	- Purpose:

	- Deliverable.

-
	- Source:

	- Your application.

-
	- Target:

	- The {cpp:class}`BWindow` to be moved.

-
	- Hook:

	- 


:::

You can send this message to a window to resize it to the specified size.

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
	- {hparam}`data`

	- {cpp:enumerator}`B_POINT_TYPE`

	- The width and height (in X and Y) to resize the window to.


:::
::::

::::{abi-group}
:::{cpp:enumerator} B_WINDOW_MOVED
:::

:::{list-table}
---
header-rows: 0
align: left
widths: auto
---
-
	- Purpose:

	- Deliverable

-
	- Source:

	- The system.

-
	- Target:

	- {cpp:class}`BWindow` that moved.

-
	- Hook:

	- {cpp:func}`BWindow::FrameMoved`


:::

Sent when a window's origin (left top corner) changes within the screen
coordinate system.

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
	- {hparam}`when`

	- {cpp:enumerator}`B_INT64_TYPE`

	- Event time, in microseconds since 01/01/70

-
	- {hparam}`where`

	- {cpp:enumerator}`B_POINT_TYPE`

	- The window's new origin in screen coordinates.


:::
::::

::::{abi-group}
:::{cpp:enumerator} B_WINDOW_RESIZED
:::

:::{list-table}
---
header-rows: 0
align: left
widths: auto
---
-
	- Purpose:

	- Deliverable

-
	- Source:

	- The system.

-
	- Target:

	- The resized {cpp:class}`BWindow`.

-
	- Hook:

	- {cpp:func}`BWindow::FrameResized`


:::

Sent when the size of the window's frame changes. Note that the
{hparam}`width` and {hparam}`height` fields measure the window's content
area—they don't include the window border or window tab.

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
	- {hparam}`when`

	- {cpp:enumerator}`B_INT64_TYPE`

	- Event time, in microseconds since 01/01/70

-
	- {hparam}`width`

	- {cpp:enumerator}`B_INT32_TYPE`

	- The width of the window's content area.

-
	- {hparam}`height`

	- {cpp:enumerator}`B_INT32_TYPE`

	- The height of the window's content area.


:::
::::

::::{abi-group}
:::{cpp:enumerator} B_WORKSPACE_ACTIVATED
:::

:::{list-table}
---
header-rows: 0
align: left
widths: auto
---
-
	- Purpose:

	- Deliverable

-
	- Source:

	- The system.

-
	- Target:

	- Every {cpp:class}`BWindow` in the activated and deactivated workspaces.

-
	- Hook:

	- {cpp:func}`BWindow::WorkspaceActivated`


:::

Sent when the active workspace changes.

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
	- {hparam}`when`

	- {cpp:enumerator}`B_INT64_TYPE`

	- Event time, in microseconds since 01/01/70

-
	- {hparam}`workspace`

	- {cpp:enumerator}`B_INT32_TYPE`

	- The index of the window's workspace.

-
	- {hparam}`active`

	- {cpp:enumerator}`B_BOOL_TYPE`

	- {cpp:expr}`true` if the workspace is now active; {cpp:expr}`false` if not.


:::
::::

::::{abi-group}
:::{cpp:enumerator} B_WORKSPACES_CHANGED
:::

:::{list-table}
---
header-rows: 0
align: left
widths: auto
---
-
	- Purpose:

	- Deliverable

-
	- Source:

	- The system.

-
	- Target:

	- The {cpp:class}`BWindow` whose set of workspaces changed.

-
	- Hook:

	- {cpp:func}`BWindow::WorkspacesChanged`


:::

Sent when there's a change to the set of workspaces in which a window can
appear.

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
	- {hparam}`when`

	- {cpp:enumerator}`B_INT64_TYPE`

	- Event time, in microseconds since 01/01/70

-
	- {hparam}`old`

	- {cpp:enumerator}`B_INT32_TYPE`

	- The window's old workspace set, given as a vector of workspace indices.

-
	- {hparam}`new`

	- {cpp:enumerator}`B_INT32_TYPE`

	- The window's new workspace set, given as a vector of workspace indices.


:::
::::

::::{abi-group}
:::{cpp:enumerator} B_ZOOM
:::

:::{list-table}
---
header-rows: 0
align: left
widths: auto
---
-
	- Purpose:

	- Deliverable

-
	- Source:

	- The system.

-
	- Target:

	- The {cpp:class}`BWindow` that was zoomed.

-
	- Hook:

	- {cpp:func}`BWindow::Zoom`


:::

Sent when the user clicks a window's zoom button.

The message has just one data field:

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
	- {hparam}`when`

	- {cpp:enumerator}`B_INT64_TYPE`

	- Event time, in microseconds since 01/01/70


:::
::::

::::{abi-group}
:::{cpp:enumerator} B_OPEN_IN_WORKSPACE
:::

:::{list-table}
---
header-rows: 0
align: left
widths: auto
---
-
	- Purpose:

	- Deliverable

-
	- Source:

	- The system.

-
	- Target:

	- {cpp:class}`BApplication`.

-
	- Hook:

	- 


:::

Sent to an application when it's first launched to tell it to open in a
specific workspace. The message will be handled during the construction of
the {cpp:class}`BApplication` object.

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
	- {hparam}`be:workspace`

	- {cpp:enumerator}`B_INT32_TYPE`

	- Workspace number into which the application should open.


:::
::::

::::{abi-group}
:::{cpp:enumerator} B_MINIMIZE
:::

:::{list-table}
---
header-rows: 0
align: left
widths: auto
---
-
	- Purpose:

	- Deliverable

-
	- Source:

	- The system or your app.

-
	- Target:

	- The {cpp:class}`BWindow` that's hidden/unhidden.

-
	- Hook:

	- {cpp:func}`BWindow::Minimize`


:::

Sent when the user double-clicks a window's title bar (to hide the
window), or selects a window from the DeskBar's window list (to unhide the
window).

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
	- {hparam}`when`

	- {cpp:enumerator}`B_INT64_TYPE`

	- Event time, in microseconds since 01/01/70.

-
	- {hparam}`minimize`

	- {cpp:enumerator}`B_BOOL_TYPE`

	- {cpp:expr}`true` if the window is being hidden; {cpp:expr}`false` if it's
being unhidden.


:::
::::

## BShelf Messages

::::{abi-group}
:::{cpp:enumerator} B_ARCHIVED_OBJECT
:::

:::{list-table}
---
header-rows: 0
align: left
widths: auto
---
-
	- Purpose:

	- Deliverable and format

-
	- Source:

	- A dragged replicant, or your app.

-
	- Target:

	- A (remote) application.

-
	- Hook:

	- {cpp:func}`BShelf::CanAcceptReplicantMessage`


:::

#### As a deliverable:

The replicant system uses this message as a deliverable. If you're using
{cpp:class}`BDragger` and {cpp:class}`BShelf` objects, the message is
created and delivered for you. You can also simulate a dragged replicant by
archiving a view, setting the archive message's command to
{cpp:enumerator}`B_ARCHIVED_OBJECT`, and sending the message to a remote
application. If the remote application has a {cpp:class}`BShelf` object,
the {cpp:class}`BShelf` will pick up the message (through a
{cpp:class}`BMessageFilter`) and pass it to the hook function.

To create a simulated replicant message, you call {cpp:func}`Archive()
<BView::Archive>` on the view that you want to replicate, and add (at
least) the {hparam}`add_on` field to the archive message.

See {cpp:class}`BShelf` and {cpp:class}`BDragger` for more information
about replicants.

#### As a format:

{cpp:enumerator}`B_ARCHIVED_OBJECT` should be used as the command constant
for all archive messages. When you archive an object, the {hparam}`class`
field is automatically added to the archive message. All other fields must
be added by your archiving code. See the {cpp:class}`BArchivable` class for
more information about archiving.

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
	- {hparam}`class` [ ]

	- {cpp:enumerator}`B_STRING_TYPE`

	- An array of class names that gives the class hierarchy of the archived
object.

-
	- {hparam}`add_on`

	- {cpp:enumerator}`B_STRING_TYPE`

	- The signature of the library or application that knows how to create the
archived object.

-
	- {hparam}`be:add_on_version`

	- {cpp:enumerator}`B_INT32_TYPE`

	- The version of the add_on.

-
	- {hparam}`be:load_each_time`

	- {cpp:enumerator}`B_BOOL_TYPE`

	- {cpp:expr}`true`: The add_on is loaded each time the object is unarchived.
{cpp:expr}`false`: The add_on is loaded only if it isn't already loaded.

-
	- {hparam}`be:unload_on_delete`

	- {cpp:enumerator}`B_BOOL_TYPE`

	- Is the add_on unloaded when the unarchived object is deleted?

-
	- {hparam}`shelf_type` (replicants only; optional)

	- {cpp:enumerator}`B_STRING_TYPE`

	- The {hparam}`type` of shelf that you want to have display the replicant. A
shelf's type is its name, as assigned when it's created.


:::
::::
