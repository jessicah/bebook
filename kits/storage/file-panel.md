# BFilePanel
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BFilePanel::BFilePanel(file_panel_mode mode = B_OPEN_PANEL, BMessenger* target = NULL, entry_ref* panel_directory = NULL, uint32 node_flavors = 0, bool allow_multiple_selection = true, BMessage* message = NULL, BRefFilter* filter = NULL, bool modal = false, bool hide_when_done = true)
:::

The constructor creates a new {hclass}`BFilePanel` object and initializes it
according to the arguments. The panel isn't displayed until you invoke
{cpp:func}`~BFilePanel::Show`.
The arguments are thoroughly described in
"{cpp:func}`~BFilePanel::Constructing`."

:::{admonition} Note
:class: note
You may notice that some of the default arguments shown here don't jibe
with the defaults listed in the section "{cpp:func}`~BFilePanel::Constructing`".
In particular, the {hparam}`node_flavors` argument was described as
defaulting to {cpp:enum}`B_FILE_NODE`, but is shown here as 0. The "Constructing…"
descriptions are correct: The default values shown here are caught and
converted by the {hclass}`BFilePanel` constructor.
:::
::::

::::{abi-group}

:::{cpp:function} virtual BFilePanel::~BFilePanel()
:::

Destroys the {hclass}`BFilePanel`. The object's target and
{cpp:class}`BRefFilter` are not
touched by this destruction. If the object is currently displaying a file
panel, the panel is closed.

::::

## Hook Functions
::::{abi-group}

:::{cpp:function} virtual void BFilePanel::SelectionChanged()
:::

This hook function is invoked whenever the user changes the set of
selected files. Within your implementation of this function, you iterate
over
{cpp:func}`~BFilePanel::GetNextSelectedRef`
to retrieve refs to the currently selected files.

::::

::::{abi-group}

:::{cpp:function} virtual void BFilePanel::WasHidden()
:::

{hmethod}`WasHidden()` is a hook function that's invoked whenever the user's actions
causes the file panel to be hidden. If you call
{cpp:func}`~BFilePanel::Hide` yourself,
{hmethod}`WasHidden()` is not invoked.

::::

## Member Functions
::::{abi-group}

:::{cpp:function} status_t BFilePanel::GetNextSelectedRef(entry_ref* ref)
:::
:::{cpp:function} void BFilePanel::Rewind()
:::

{hmethod}`GetNextSelectedRef()` initializes its arguments to point to the "next" ref
in the file panel's set of currently selected items. The function returns
{cpp:enum}`B_ENTRY_NOT_FOUND` when it reaches the end of the list.
{hmethod}`Rewind()` gets you back to the top of the list.

Although you can call these functions anytime you want, they're intended
to be used in implementations of the
{cpp:func}`~BFilePanel::SelectionChanged`
hook function.

::::

::::{abi-group}

:::{cpp:function} file_panel_mode BFilePanel::PanelMode() const
:::

Returns the object's mode, either {cpp:enum}`B_OPEN_PANEL` or {cpp:enum}`B_SAVE_PANEL`. The mode
is set in the constructor and can't be changed thereafter.

::::

::::{abi-group}

:::{cpp:function} void BFilePanel::Refresh()
:::

{hmethod}`Refresh()` tells the file panel to re-read the contents of the panel
directory, which causes the directory's entries to be re-run through the
ref filter.

You don't have to call {hmethod}`Refresh()` in order to keep the panel in sync with
the directory's contents—the directory and file panel are kept in
sync automatically.

::::

::::{abi-group}

:::{cpp:function} virtual void BFilePanel::SendMessage(BMessenger* messenger, BMessage* message)
:::

Sends {cpp:class}`BMessage`
{hparam}`message` to the
{cpp:class}`BHandler` targeted by {hparam}`messenger`.

See Also:
{cpp:func}`BMessenger::SendMessage`

::::

::::{abi-group}

:::{cpp:function} void BFilePanel::SetButtonLabel(file_panel_button which_button, const char* label)
:::
:::{cpp:function} void BFilePanel::SetSaveText(const char* label)
:::

{hmethod}`SetButtonLabel()` lets you set the label that's displayed in the panel's
buttons. The button that a specific invocation affects depends on the
value of {hparam}`which_button`:

:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_DEFAULT_BUTTON`
	- Is the Open button for an Open Panel and the Save button for a Save Panel.
-
	- {cpp:enum}`B_CANCEL_BUTTON`
	- Is the "Cancel" button.
:::

{hmethod}`SetSaveText()` sets the text that's displayed in the Save Panel's text
view (the area in which the user types and confirms a file name).

::::

::::{abi-group}

:::{cpp:function} void BFilePanel::SetHideWhenDone(bool hide_when_done)
:::
:::{cpp:function} bool BFilePanel::HidesWhenDone() const
:::

By default, a file panel is hidden when the user confirms or Cancels. You
can control this behavior using the {hmethod}`SetHideWhenDone()` function. If you
set {hparam}`hide_when_done` to {cpp:enum}`false`, the panel remains on the screen; if you
specify {cpp:enum}`true`, the panel hides when the user confirms or Cancels. Clicking
the panel's close box always hides the panel.

{hmethod}`HidesWhenDone()` returns the current setting of this
option: {cpp:enum}`true` if the
panel hides when the user is done with it or {cpp:enum}`false` if it remains on the
screen.

::::

::::{abi-group}

:::{cpp:function} void BFilePanel::SetMessage(BMessage* message)
:::

{hmethod}`SetMessage()` allows you to set the format of the file panel's
notification messages. The message can also be set through the
constructor. See "{cpp:func}`~BFilePanel::The`" for more
information.

A copy is made of the {cpp:class}`BMessage`,
so it is your responsibility to delete {hparam}`msg` when you no longer need it.

::::

::::{abi-group}

:::{cpp:function} void BFilePanel::SetPanelDirectory(BEntry* dirEntry)
:::
:::{cpp:function} void BFilePanel::SetPanelDirectory(BDirectory* dirObj)
:::
:::{cpp:function} void BFilePanel::SetPanelDirectory(entry_ref* dirRef)
:::
:::{cpp:function} void BFilePanel::SetPanelDirectory(const char* dirStr)
:::
:::{cpp:function} void BFilePanel::GetPanelDirectory(entry_ref* ref) const
:::

The {hmethod}`SetPanelDirectory()` function sets the panel's "panel directory." This
is the directory whose contents are displayed in the panel's file list.
You can also set the panel directory through the constructor. If you
don't supply a directory, the current working directory is used.

{hmethod}`GetPanelDirectory()` initializes {hparam}`ref` to point to the current panel
directory. The argument must be allocated.

::::

::::{abi-group}

:::{cpp:function} void BFilePanel::SetRefFilter(BRefFilter* filter)
:::
:::{cpp:function} BRefFilter* BFilePanel::RefFilter() const
:::

Whenever the file panel's panel directory is changed or refreshed
({cpp:func}`~BFilePanel::Refresh`),
or when a new entry is added to the current panel directory,
the "new" entries are run through the panel's "ref filter." The
{cpp:class}`BRefFilter` class
defines a single boolean hook function called
{cpp:func}`~BRefFilter::Filter`.
The function receives the entries, one-by-one, and can reject specific
entries (because they're the wrong file type, for example). Rejected
entries are not shown in the panel's file list.

The {hmethod}`SetRefFilter()` function sets the panel's ref filter. You can also set
it through the constructor. Ownership of the filter is not handed to the
panel. You mustn't delete the ref filter while the panel is still extant.

{hmethod}`RefFilter()` returns a pointer to the panel's ref filter.

::::

::::{abi-group}

:::{cpp:function} void BFilePanel::SetTarget(BMessenger bellhop)
:::
:::{cpp:function} BMessenger BFilePanel::Messenger() const
:::

{hmethod}`SetTarget()` sets the target of the file panel's notification messages.
The target can also be set through the constructor. If you don't set a
target, be_app_messenger is used. See the
{cpp:class}`BInvoker` class (in the
Application Kit) for an explanation of how a
{cpp:class}`BMessenger` can be used as a
target.

A copy is made of the {cpp:class}`BMessenger`,
so it is your responsibility to delete
{hparam}`bellhop` when you no longer need it.

{hmethod}`Messenger()` returns (a copy of) the messenger that's used as the file
panel's target.

::::

::::{abi-group}

:::{cpp:function} void BFilePanel::Show()
:::
:::{cpp:function} void BFilePanel::Hide()
:::
:::{cpp:function} bool BFilePanel::IsShowing() const
:::

These functions show and hide the file panel, and tell if you the panel
is currently showing.

::::

::::{abi-group}

:::{cpp:function} BWindow* BFilePanel::Window() const
:::

Returns a pointer to the file panel's window. If you want to mess around
with the window's views, see
"{cpp:func}`~BFilePanel::Modifying`."

::::
