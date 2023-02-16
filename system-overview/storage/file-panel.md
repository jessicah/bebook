# BFilePanel

{hclass}`BFilePanel` knows how to create and display an "Open File" or
"Save File" panel, and provides the means for filtering and responding to
the user's actions on the panel. The Save Panel looks like this:

![File Save Panel](./images/TheStorageKit/FilePanel1.png)

The Open Panel looks pretty much the same, but without the text view in
the lower left corner.

## Creating and Using a BFilePanel

To create and use a {hclass}`BFilePanel`, follow these steps:

1.    Construct a {hclass}`BFilePanel` object in response to the user's request
(most likely, a click on an "Open" or "Save"/"Save As" menu item). When you
construct the panel, you have to specify its "mode" (Open or Save).

2.    Fine-tune the panel by telling it which directory to display, whether it
allows multiple selection, whether it can open a directory, which target it
should send notifications to, and so on. (Most of these parameters can also
be set in the constructor.)

3.    Invoke {hmethod}`Show()` on the panel, and then wait for the user to
confirm a selection (or close the panel).

4.    Receive a message. When the user confirms a selection (or cancels the
panel), the panel disappears and a notification message (Open, Save, or
Cancel) is sent to the panel's target. The message identifies the confirmed
file(s).

5.    Delete the {hclass}`BFilePanel` object…or don't. When the user closes a
file panel, the object is not automatically deleted; you have to do it
yourself. But you may not want to. If you don't delete the panel, you can
simply call {hmethod}`Show()` the next time you want to display it; the
state from the previous invocation (the panel's size and location, the
directory it points to) is remembered.

## Constructing and Fine-tuning the Panel

The {hclass}`BFilePanel` constructor has about two thousand arguments.
They all have default values, and most of the parameters that they control
can be set through individual functions. The following sections list and
describe the constructor arguments and tell you if there's an analogous
function.

### Panel Mode

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Argument

	- Default

	- Function

-
	- {htype}`file_panel_mode` {hparam}`mode`

	- {cpp:enumerator}`B_OPEN_PANEL`

	- –


:::

There are two file panel modes: {cpp:enumerator}`B_OPEN_PANEL` and
{cpp:enumerator}`B_SAVE_PANEL`. You've got to make up your mind in the
constructor.

### Target

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Argument

	- Default

	- Function

-
	- {htype}`BMessenger*` {hparam}`target`

	- {hparam}`be_app_messenger`

	- {cpp:func}`SetTarget() <BFilePanel::SetTarget>`


:::

The {hparam}`target` represents the
{cpp:class}`BLooper`/{cpp:class}`BHandler` that will receive the Open,
Save, and Cancel messages.

### Panel Directory

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Argument

	- Default

	- Function

-
	- {htype}`entry_ref*` {hparam}`panel_directory`

	- cwd

	- SetPanelDirectory()


:::

When a panel is first displayed, it has to show the contents of some
directory; this is called the "panel directory." The panel directory
defaults to the current working directory.

### Confirmable Node Flavors

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Argument

	- Default

	- Function

-
	- {htype}`uint32` {hparam}`node_flavors`

	- {cpp:enumerator}`B_FILE_NODE`

	- –


:::

:::{admonition} Note
:class: note
This parameter applies to Open panels only.
:::

There are three node flavors: {cpp:enumerator}`B_FILE_NODE`,
{cpp:enumerator}`B_DIRECTORY_NODE`, and {cpp:enumerator}`B_SYMLINK_NODE`.
You combine these constants to declare the flavors that you want the user
to be able to confirm. Before describing the flavor settings, keep this in
mind…

-   Double-clicking a directory in the file list always enters the directory,
regardless of the panel's flavor setting.

If you understand the following, you can save yourself some reading:

-   If your app wants to open files only, then stick with the default
({cpp:enumerator}`B_FILE_NODE`); the user will be able to confirm files and
symlinks to files. If you want directories as well (for example, a
compression app might want to work on files and directories) then add in
{cpp:enumerator}`B_DIRECTORY_NODE` (symlinks to directories are okay, as
well). If you only want directories (unusual, but possible), then leave
{cpp:enumerator}`B_FILE_NODE` out of it.

If you're not convinced, read on:

-   If the setting includes {cpp:enumerator}`B_FILE_NODE` and the user selects
and confirms a file or a symlink to a file, the file (or symlink) is
delivered to your target. If it doesn't include
{cpp:enumerator}`B_FILE_NODE` and the user selects a file (or symlink to a
file), the Open button is disabled.

-   If the setting includes {cpp:enumerator}`B_DIRECTORY_NODE` and the user
selects and Opens (i.e. clicks the Open button) a directory or a symlink to
a directory, the directory (or symlink) is delivered to your target. If it
doesn't include {cpp:enumerator}`B_DIRECTORY_NODE` and the user Opens a
directory (or symlink to a directory), the directory is entered (the
contents of the directory are displayed in the file list).

-   If the setting includes {cpp:enumerator}`B_SYMLINK_NODE` and the user
confirms a symlink, the symlink is delivered to your target. If it doesn't
include {cpp:enumerator}`B_SYMLINK_NODE` and the user selects symlink, the
panel's response depends on the inclusion of the other two flavors. Note
that including {cpp:enumerator}`B_SYMLINK_NODE` is an odd thing to do—it
only makes sense if it's not combined with either of the other two flavors,
and even then it doesn't make much sense.

As implied by the here, when the user confirms a symlink (regardless of
the flavor setting), you always receive the symlink itself in the Open
message—you don't get the file or directory it points to.

### Multiple Selection

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Argument

	- Default

	- Function

-
	- {htype}`bool` {hparam}`allow_multiple_selection`

	- {cpp:expr}`true`

	- –


:::

This parameter determines whether the user is allowed to select more than
one item at a time. Save panels should set this to {cpp:expr}`false`.

### Notification Message

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Argument

	- Default

	- Function

-
	- {htype}`BMessage*` {hparam}`message`

	- a default {cpp:class}`BMessage`

	- {cpp:func}`SetMessage() <BFilePanel::SetMessage>`


:::

By default, the format of the message that's sent to your target when the
user confirms or cancels is defined by the file panel (the default formats
are defined later). You can override the default by specifying your own
{cpp:class}`BMessage`. The {cpp:class}`BMessage` is copied by the
{hclass}`BFilePanel` object. You can change this message using the
{cpp:func}`SetMessage() <BFilePanel::SetMessage>` function.

### Ref Filter

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Argument

	- Default

	- Function

-
	- {htype}`BRefFilter*` {hparam}`filter`

	- {cpp:expr}`NULL`

	- {cpp:func}`SetRefFilter() <BFilePanel::SetRefFilter>`


:::

When panel directory changes (this includes when the panel is constructed,
and when the panel's {cpp:func}`Refresh() <BFilePanel::Refresh>` function
is called), or when a new entry is added to the existing directory, the new
entries are passed, one-by-one, to the panel's {cpp:class}`BRefFilter`
object through a {cpp:class}`BRefFilter` hook function. In your
implementation of the hook function, you can reject individual entries;
rejected entries won't be displayed in the file list.

By default, a file panel has no {cpp:class}`BRefFilter`. To supply one,
you have to subclass {cpp:class}`BRefFilter` (in order to implement the
hook function) and pass it in.

-   Note that the ref filter isn't asked to "re-review" the entry list when
the file panel is Show()'d after being hidden.

### Is Modal?

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Argument

	- Default

	- Function

-
	- {htype}`bool`

	- {cpp:expr}`false`

	- –


:::

A modal file panel can't be closed; to get rid of the panel, the user has
to click a button. By default, file panels are not modal.

### Hide When Done

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Argument

	- Default

	- Function

-
	- {htype}`bool` {hparam}`hide_when_done`

	- {cpp:expr}`true`

	- {cpp:func}`SetHideWhenDone() <BFilePanel::SetHideWhenDone>`


:::

By default, a file panel is hidden when the user confirms or Cancels. If
you set {hparam}`hide_when_done` to {cpp:expr}`false`, the panel remains on
the screen. Clicking the panel's close box always hides the panel

## The Target and the Messages it Sees

When the user confirms a selection or cancels a file panel, a
{cpp:class}`BMessage` is constructed and sent to the target of the
{hclass}`BFilePanel` object. By default, the target is
{cpp:var}`be_app_messenger`. You can specify a different target (as a
{cpp:class}`BMessenger`) through the {hclass}`BFilePanel` constructor, or
through the {cpp:func}`SetTarget() <BFilePanel::SetTarget>` function.

The format of the {cpp:class}`BMessage` that the target receives depends
on whether the user is opening, saving, or canceling.

## Open Notification

If the target is {cpp:var}`be_app_messenger` and the {cpp:var}`what` field
is {cpp:enumerator}`B_REFS_RECEIVED`, the {cpp:class}`BMessage` shows up in
the {cpp:func}`RefsReceived() <BApplication::RefsReceived>` function.
Otherwise it's sent to the target's {cpp:func}`MessageReceived()
<BHandler::MessageReceived>`.

-   By default, the {cpp:var}`what` field is
{cpp:enumerator}`B_REFS_RECEIVED`. You can override the default by
supplying your own {cpp:class}`BMessage` ({cpp:func}`SetMessage()
<BFilePanel::SetMessage>`).

-   The {hparam}`refs` field (type {cpp:enumerator}`B_REF_TYPE`) contains
{htype}`entry_ref` structures, one for each entry that the user has
confirmed.

-   The message may contain other fields, as copied from the
{cpp:class}`BMessage` you (optionally) supplied. The data in these fields
won't be changed.

Keep in mind that the refs that you receive through this message point to
the literal entries that the user confirmed. In other words, if the
confirmed selection is a symlink to a file, you'll receive a ref for the
symlink, not the file (and similarly for a link to a directory). It's up to
you to turn the symlink into a file (which is probably what you want).

If you want a {cpp:class}`BEntry` object, all you have to do is pass
{cpp:expr}`true` as the {hparam}`traverse` argument to
{cpp:class}`BEntry`'s constructor or {cpp:func}`SetTo() <BEntry::SetTo>`:

:::{code} cpp
/* We'll assume that 'ref' was just plucked from an
   open notification. */
BEntry entry(ref, true);
:::

You don't even have to check to see if the ref is a symlink.

If you want to turn a symlink ref into a ref to the pointed-to file, just
add this line:

:::{code} cpp
entry.GetRef(&ref);
:::

## Save Notification

Save notifications are always sent to the target's
{cpp:func}`MessageReceived() <BHandler::MessageReceived>` function.

-   By default, the {cpp:var}`what` field is
{cpp:enumerator}`B_SAVE_REQUESTED`. You can override the default by
supplying your own {cpp:class}`BMessage` ({cpp:func}`SetMessage()
<BFilePanel::SetMessage>`).

-   The {hparam}`directory` field (type {cpp:enumerator}`B_REF_TYPE`) contain
a single {htype}`entry_ref` structure that points to the directory in which
the user has requested the entry be saved (in other words, the ref refers
to the panel directory).

-   The {hparam}`name` field ({cpp:enumerator}`B_STRING_TYPE`) is the text the
user typed in the Save Panel's text view.

-   The message may contain other fields, as copied from the
{cpp:class}`BMessage` you (optionally) supplied. The data in these fields
won't be changed.

Note that if the user confirms a name that collides with an existing file,
an alert is automatically displayed. The user can then back out of the
confirmation and return to the Save Panel, or clobber the existing file.
The save notification is sent after (and only if) the user agrees to
clobber the file.

:::{admonition} Note
:class: note
The file __isn't__ clobbered by the system; it's up to you (as the
receiver of the save notification) to do the dirty work.
:::

## Cancel Notification

A cancel notification is sent __whenever__ the file panel is hidden. This
includes the Cancel button being clicked, the panel being closed, and the
panel being hidden after an open or a save (given that the panel is in
hide-when-done mode).

Cancel notifications are always sent to the target's
{cpp:func}`MessageReceived() <BHandler::MessageReceived>` function.

-   The {cpp:var}`what` field is always {cpp:enumerator}`B_CANCEL`, even if
you supplied your own {cpp:class}`BMessage`.

-   The {hparam}`old_what` field ({cpp:enumerator}`B_UINT32_TYPE`) records the
"previous" what value. This is only useful (and dependable) if you supplied
your own {cpp:class}`BMessage`: The {cpp:var}`what` from your message is
moved to the {hparam}`old_what` field. If you didn't supply a
{cpp:var}`what`, you should ignore this field (it could contain garbage).

-   The {hparam}`source` ({cpp:enumerator}`B_POINTER_TYPE`) is a pointer to
the {hclass}`BFilePanel` object that was closed.

-   The message may contain other fields, as copied from the
{cpp:class}`BMessage`: you (optionally) supplied. The data in these fields
won't be changed.

Keep in mind that when a file panel is closed—regardless of how it's
closed—the {hclass}`BFilePanel` object is not destroyed. It's merely
hidden.

## Modifying the Look of the File Panel

There are two ways you can modify the look of your {hclass}`BFilePanel`
object.

-   You can do some simple text twiddling by calling the label- and
text-setting functions SetButtonLabel() and SetSaveText().

-   If you need to really change the look, you can get a handle on the panel's
BWindow and BView objects in order to move them around, add your own, or
whatever. You get the window through the Window() function. Finding
specific views within the window is described below.

### Finding Views in the Panel

The views in the panel are (mostly) named, as listed and shown below

-   "MenuBar" is the window's menu bar.

-   "DirMenuField" is the path popup.

-   "TitleView" is the bar that holds the attribute titles.

-   "PoseView" is the scrollable list of files.

-   "VScrollBar" and "HScrollBar" are the vertical and horizontal scroll bars.

-   "CountVw" is the item counter to the left of the horizontal scroll bar.

-   "text view" is where the user types a file name (Save Panel only).

-   "default button" is the Save or Open button.

-   "cancel button" is the Cancel button.

![File Panel Views](./images/TheStorageKit/FilePanel2.png)

The background view doesn't have a name, but it's always the first in the
window's list of views:

:::{code} cpp
BView* background = filepanel->Window()->ChildAt(0);
:::

The other views can be found by name, reckoning off of the background
view. For example, here we get the "PoseView" view (the view that contains
the file list):

:::{code} cpp
BView* files = background->FindView("PoseView");
:::

## The C Functions

You can also display Open and Save Panels through the global C functions
run_open_panel() and run_save_panel() (which are declared in FilePanel.h).
The functions create {hclass}`BFilePanel` objects using the default
constructor settings (modulo the {htype}`file_panel_mode`, of course).

The C functions create a new file panel each time they're called, and
delete the panel when the user is finished with it.
