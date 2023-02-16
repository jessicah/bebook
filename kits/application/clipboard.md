:::{cpp:class} BClipboard
:::

# BClipboard

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BClipboard::BClipboard(const char* name, bool discard = false)
:::

Creates a new {hclass}`BClipboard` object that refers to the
{hparam}`name` clipboard. The clipboard itself is created if a clipboard of
that name doesn't already exist.

The {hparam}`discard` flag is currently unused.
::::

::::{abi-group}
:::{cpp:function} virtual BClipboard::~BClipboard()
:::

Destroys the {hclass}`BClipboard` object. The clipboard itself and the
data it contains are not affected by the object's destruction.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} status_t BClipboard::Clear()
:::

:::{cpp:function} status_t BClipboard::Commit()
:::

:::{cpp:function} status_t BClipboard::Revert()
:::

These functions are used when you're writing data to the clipboard.
{hmethod}`Clear()` prepares your {hclass}`BClipboard` for writing. You call
{hmethod}`Clear()` just before you add new data to your clipboard message.
{hmethod}`Commit()` copies your {hclass}`BClipboard` data back to the
clipboard. See "{ref}`Writing to the Clipboard`" for an example of these
functions.

{hmethod}`Revert()` refreshes the {hclass}`BClipboard`'s data message by
uploading it from the clipboard. The function is provided for the (rare)
case where you alter your {hclass}`BClipboard`'s data message, and then
decide to back out of the change. In this case, you should call
{hmethod}`Revert()` (rather than {hmethod}`Commit()`). If you don't revert,
your {hclass}`BClipboard`'s message will still contain your unwanted
change, even if you unlock and then re-lock the object.

All three functions return {cpp:enumerator}`B_ERROR` if the
{hclass}`BClipboard` isn't locked, and {cpp:enumerator}`B_OK` otherwise.
::::

::::{abi-group}
:::{cpp:function} BMessage* BClipboard::Data() const
:::

Returns the {cpp:class}`BMessage` object that holds the
{hclass}`BClipboard`'s data, or {cpp:expr}`NULL` if the
{hclass}`BClipboard` isn't locked. You're expected to read and write the
{cpp:class}`BMessage` directly; however, you may not free it or dispatch it
like a normal {cpp:class}`BMessage`. If you change the
{cpp:class}`BMessage` and want to write it back to the clipboard, you have
to call {hmethod}`Commit()` after you make the change.

See "{ref}`The Clipboard Message`" for more information.
::::

::::{abi-group}
:::{cpp:function} BMessenger BClipboard::DataSource() const
:::

Returns a {cpp:class}`BMessenger` that targets the
{cpp:class}`BApplication` object of the application that last committed
data to the clipboard. The {hclass}`BClipboard` needn't be locked.
::::

::::{abi-group}
:::{cpp:function} uint32 BClipboard::LocalCount() const
:::

:::{cpp:function} uint32 BClipboard::SystemCount() const
:::

These functions return the clipboard count. {hmethod}`LocalCount()` uses a
cached count, while {hmethod}`SystemCount()` asks the Application Server
for the more accurate system counter.
::::

::::{abi-group}
:::{cpp:function} bool BClipboard::Lock()
:::

:::{cpp:function} void BClipboard::Unlock()
:::

:::{cpp:function} bool BClipboard::IsLocked()
:::

{hmethod}`Lock()` uploads data from the clipboard into your
{hclass}`BClipboard` object, and locks the object so no other thread in
your application can use it. You must call {hmethod}`Lock()` before reading
or writing the {hclass}`BClipboard`. {hmethod}`Lock()` blocks if the object
is already locked. It returns {cpp:expr}`true` if the lock was acquired,
and {cpp:expr}`false` if the {hclass}`BClipboard` object was deleted while
{hmethod}`Lock()` was blocked.

:::{admonition} Warning
:class: warning
There's no way to tell {hmethod}`Lock()` to time out.
:::

{hmethod}`Unlock()` unlocks the object so other threads in your
application can use it.

{hmethod}`IsLocked()` hardly needs to be documented.
::::

::::{abi-group}
:::{cpp:function} const char* BClipboard::Name() const
:::

Returns the name of the clipboard. The object needn't be locked.
::::

::::{abi-group}
:::{cpp:function} status_t BClipboard::StartWatching(BMessenger target)
:::

:::{cpp:function} status_t BClipboard::StopWatching(BMessenger target)
:::

If you want to be alerted when the clipboard changes, call
{hmethod}`StartWatching()`, passing a {cpp:class}`BMessenger` to be the
target for the notification. When the clipboard changes, a
{cpp:enumerator}`B_CLIPBOARD_CHANGED` message will be sent to the target.

{hmethod}`StopWatching()` stops monitoring the clipboard for changes.

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`B_OK`.
	- No error.
-
	- Other errors.
	- You get the idea.

:::
::::

## Global Variables

### be_clipboard

:::{code} cpp
BClipboard* be_clipboard
:::

This variable gives applications access to the system clipboard—the shared
repository of data for cut, copy, and paste operations. It's initialized at
startup.
