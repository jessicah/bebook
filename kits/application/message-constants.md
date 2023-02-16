# Message Constants

The following sections describe Application Kit constants which can be
either used as a return value from a method or as a {hparam}`what` data
member of a {cpp:class}`BMessage`.

## Application Messages

These constants represent the system messages that are recognized and
given special treatment by {cpp:class}`BApplication`. Application messages
concern the application as a whole, rather than any particular window
thread. See the introduction to this chapter and the
{cpp:class}`BApplication` class for details.

::::{abi-group}
:::{cpp:enumerator} B_ABOUT_REQUESTED
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

	- App-defined; typically {cpp:var}`be_app`.

-
	- Hook:

	- {cpp:func}`BApplication::AboutRequested` if the target is
{cpp:var}`be_app`.


:::

The message should be assigned to an About... menu item, such that the
message is sent when the user clicks the item. Your application is expected
to put up an "About This Application" panel when it receives this message.
::::

::::{abi-group}
:::{cpp:enumerator} B_APP_ACTIVATED
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

	- {cpp:var}`be_app`

-
	- Hook:

	- {cpp:func}`BApplication::AppActivated`


:::

Sent when an application becomes active or inactive.

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
	- {hparam}`active`

	- {cpp:enumerator}`B_BOOL_TYPE`

	- {cpp:expr}`true` if the app has become active; otherwise
{cpp:expr}`false`.


:::
::::

::::{abi-group}
:::{cpp:enumerator} B_ARGV_RECEIVED
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

	- {cpp:var}`be_app`

-
	- Hook:

	- {cpp:func}`BApplication::ArgvReceived`


:::

Forwards arguments that (a) the user passes while launching the app from
the command line, or (b) are passed to {cpp:func}`BRoster::Launch`. Most
apps treat command line arguments as filenames that should be opened. If
the filename is relative (if it doesn't start with "/"), you should append
it to the {hparam}`cwd` field to reconstruct the full path.

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
	- {hparam}`argc`

	- {cpp:enumerator}`B_INT32_TYPE`

	- The number of arguments.

-
	- {hparam}`argv` [{hparam}`argc`]

	- {cpp:enumerator}`B_STRING_TYPE`

	- The arguments.

-
	- {hparam}`cwd`

	- {cpp:enumerator}`B_STRING_TYPE`

	- The path name of the current working directory.


:::
::::

::::{abi-group}
:::{cpp:enumerator} B_PULSE
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

	- {cpp:var}`be_app` or {cpp:class}`BWindow` object.

-
	- Hook:

	- {cpp:func}`BApplication::Pulse` and {cpp:func}`BView::Pulse`


:::

Sent at regular intervals, but with no particular intent. You can
implement {hmethod}`Pulse()` to do whatever you want. The message is to the
{cpp:class}`BWindow` only if a {cpp:class}`BView` within the window
declares {cpp:enumerator}`B_PULSE_NEEDED` in its constructor flags.
::::

::::{abi-group}
:::{cpp:enumerator} B_READY_TO_RUN
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

	- {cpp:var}`be_app`

-
	- Hook:

	- {cpp:func}`BApplication::ReadyToRun`


:::

Sent when an application has finished configuring itself and is ready to
start running.

(No Be-defined fields)
::::

::::{abi-group}
:::{cpp:enumerator} B_REFS_RECEIVED
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

	- {cpp:var}`be_app`, or other app-defined target.

-
	- Hook:

	- {cpp:func}`BApplication::RefsReceived`


:::

Automatically sent to be_app when (a) the user double-clicks a file that
has a type that's supported by the app, and (b) when the user confirms some
files (or directories) in an Open File panel (the target is be_app by
default; it can be changed in {cpp:func}`BFilePanel::SetTarget`). You can
also create, stuff, and send a {cpp:enumerator}`B_REFS_RECEIVED` message
yourself. When it receives this message, an app is expected to open the
files that the message refers to.

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
	- {hparam}`refs` [i]

	- {cpp:enumerator}`B_REF_TYPE`

	- {htype}`entry_ref` items, one for each file or directory.


:::
::::

See also: "{ref}`Application Messages`"

## BLooper Messages

::::{abi-group}
:::{cpp:enumerator} B_QUIT_REQUESTED
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

	- {cpp:var}`be_app`, {cpp:class}`BWindow` closed by the user, or other
{cpp:class}`BLooper` object.

-
	- Hook:

	- {cpp:func}`BLooper::QuitRequested`.


:::

Automatically sent (a) to {cpp:var}`be_app` when the user types
{hkey}`Command`+{hkey}`q`, and (b) to a {cpp:class}`BWindow` when the user
clicks the window's close box. Applications can also manufacture and send
the message themselves. A looper that receives this message is expected to
quit, or at least consider quitting.

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
	- {hparam}`shortcut`

	- {cpp:enumerator}`B_BOOL_TYPE`

	- {cpp:expr}`true` if the user typed {hkey}`Command`+{hkey}`q`.


:::
::::

## Scripting Messages

The scripting system defines four generic messages that can operate on the
specific properties of an object and two meta-messages that query an object
about the messages it can handle. See "{ref}`Scripting`" in The Application
Kit chapter for a full explanation.

::::{abi-group}
:::{cpp:enumerator} B_COUNT_PROPERTIES
:::

This message requests the number of properties supported by the receiver.
It contains no data, but the reply message should contain one field:

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
	- {hparam}`result`

	- {cpp:enumerator}`B_INT32_TYPE`

	- The number of properties supported.


:::
::::

::::{abi-group}
:::{cpp:enumerator} B_GET_SUPPORTED_SUITES
:::

This message requests the names of all message suites that the receiver
supports. It doesn't contain any data, but the message that's sent in reply
has one field:

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
	- {hparam}`suites`

	- {cpp:enumerator}`B_STRING_TYPE`

	- An array of suite names.


:::

A suite is a named set of messages and specifiers. A {cpp:class}`BHandler`
supports the suite if it can respond to the messages and resolve the
specifiers.
::::

::::{abi-group}
:::{cpp:enumerator} B_SET_PROPERTY
:::

These messages—as their names state—target a particular property under the
control of the target handler. They have the following data fields:

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
	- {hparam}`specifiers`

	- {cpp:enumerator}`B_MESSAGE_TYPE`

	- An array of one or more {cpp:class}`BMessage`s that specify the targeted
property. See {cpp:func}`AddSpecifier() <BMessage::AddSpecifier>` in the
{cpp:class}`BMessage` class of the Application Kit for details on the
contents of a specifier.

-
	- {hparam}`data`

	- __variable__

	- For {cpp:enumerator}`B_SET_PROPERTY` messages only, the data that should
be set. The data type depends on the targeted property.


:::
::::

## Reply Messages

The following three messages are sent as replies to other messages.

::::{abi-group}
:::{cpp:enumerator} B_MESSAGE_NOT_UNDERSTOOD
:::

This message doesn't contain any data. The system sends it as a reply to a
message that the receiving thread's chain of {cpp:class}`BHandler` does not
recognize. See {cpp:func}`MessageReceived() <BHandler::MessageReceived>`
and {cpp:func}`ResolveSpecifier() <BHandler::ResolveSpecifier>` in the
{cpp:class}`BHandler` class of the Application Kit.
::::

::::{abi-group}
:::{cpp:enumerator} B_NO_REPLY
:::

This message doesn't contain any data. It's sent as a default reply to
another message when the original message is about to be deleted. The
default reply is sent only if a synchronous reply is expected and none has
been sent. See the {cpp:func}`SendReply() <BMessage::SendReply>` function
in the {cpp:class}`BMessage` class of the Application Kit.
::::

::::{abi-group}
:::{cpp:enumerator} B_REPLY
:::

This constant identifies a message as being a reply to a previous message.
The data in the reply depends on the circumstances and, particularly, on
the original message. For replies to scripting messages, it generally has a
{hparam}`result` field with requested data and an {hparam}`error` field
with an error code reporting the success or failure of the scripted
request.
::::

## General Messages

::::{abi-group}
:::{cpp:enumerator} B_CLIPBOARD_CHANGED
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

	- The Application Server.

-
	- Target:

	- Selected {cpp:class}`BMessenger`.


:::

If you've called {cpp:func}`BClipboard::StartWatching` to monitor a
clipboard for changes, this message is sent to the specified
{cpp:class}`BMessenger` when the clipboard changes.
::::

::::{abi-group}
:::{cpp:enumerator} B_OBSERVER_NOTICE_CHANGE
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

	- Application-defined target.

-
	- Hook:

	- 


:::

Sent by {cpp:class}`BHandler`s to all targets that have been registered
with the {cpp:class}`BHandler`'s {cpp:func}`StartWatching()
<BHandler::StartWatching>` or {cpp:func}`StartWatchingAll()
<BHandler::StartWatchingAll>` function.

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
	- {hparam}`be:observe_change_what`

	- {cpp:enumerator}`B_INT32_TYPE`

	- The {hparam}`what` code of the message being broadcast.

-
	- {hparam}`be:observe_orig_what`

	- {cpp:enumerator}`B_INT32_TYPE`

	- The original {hparam}`what` code of the message, before it was altered by
the broadcasting mechanism.


:::

The message may have other fields, depending on what the broadcast message
is. Messages are sent to targets in response to the
{cpp:func}`BHandler::SendNotices` function. The logic is:

1.    Take the message to broadcast and place its what code into the
{hparam}`be:observe_change_orig_what` field.

2.    Add the {hparam}`be:observe_change_what` field, which is set to the
{hparam}`what` code specified by the call to {cpp:func}`SendNotices()
<BHandler::SendNotices>`.

3.    Set the message's {hparam}`what` code to
{cpp:enumerator}`B_OBSERVER_NOTICE_CHANGE`.

The resulting message is then sent to all interested parties.
::::

::::{abi-group}
:::{cpp:enumerator} B_SILENT_RELAUNCH
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

	- {cpp:var}`be_app`

-
	- Hook:

	- 


:::

Sent to a single-launch application when it's activated by being launched
(for example, if the user double-clicks its icon in Tracker).

(No Be-defined fields)
::::

::::{abi-group}
:::{cpp:enumerator} B_SOME_APP_ACTIVATED
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

	- The Roster Monitor.

-
	- Target:

	- App-defined.

-
	- Hook:

	- 


:::

Sent as apps are launched, activated, or quit. You get these messages by
invoking {cpp:func}`BRoster::StartWatching` passing a one or more of
{cpp:enumerator}`B_REQUEST_ACTIVATED`,
{cpp:enumerator}`B_REQUEST_LAUNCHED`, and {cpp:enumerator}`B_REQUEST_QUIT`.

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
	- {hparam}`mime_sig`

	- {cpp:enumerator}`B_STRING_TYPE`

	- The app signature.

-
	- {hparam}`team`

	- {cpp:enumerator}`B_INT32_TYPE`

	- The app's team id.

-
	- {hparam}`thread`

	- {cpp:enumerator}`B_INT32_TYPE`

	- The id of the app's main thread.

-
	- {hparam}`flags`

	- {cpp:enumerator}`B_INT32_TYPE`

	- The app's app flags ({cpp:enumerator}`B_SINGLE_LAUNCH`,
{cpp:enumerator}`B_BACKGROUND_APP`, etc).

-
	- {hparam}`ref`

	- {cpp:enumerator}`B_REF_TYPE`

	- The {htype}`entry_ref` of the app's executable.


:::
::::

### B_CANCEL

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

	- The Application Kit.

-
	- Target:

	- Application Server.


:::

Used to cancel an ongoing operation. The Application Kit sends this
message to the Application Server to cancel a shutdown if a window refuses
to quit.
