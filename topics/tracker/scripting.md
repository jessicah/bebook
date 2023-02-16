# Scripting

Each Tracker window defines a "Poses" property representing the contents
of the window. Each poses, in turn, defines the two properties "Entry" and
"Selection". An "Entry" is an item in the window, e.g. either a file or a
directory, while a "Selection" represents a selected "Entry".

When a Tracker window receives a scripting message with a "Poses"
property, it pops the current specifier off the specifier stack and then
forwards the scripting message to the view handling the "Poses" property.
From there, the "Entry" and "Selection" properties are processed. For
example, the following function returns the number of entries present in a
given Tracker window:

:::{code} cpp
int32 CountEntries(const char *name)
{
    int32 count;
    BMessage message, reply;

    // form scripting request
    message.what = B_COUNT_PROPERTIES;
    message.AddSpecifier("Entry");
    message.AddSpecifier("Poses");
    message.AddSpecifier("Window", name);

    // deliver request and fetch response
    BMessenger("application/x-vnd.Be-TRAK").SendMessage(&message,
    &reply);

    // return result
    if (reply.FindInt32("result", &count) == B_OK)
        return count;

    return -1;
}
:::

The Tracker scripting API defines a number of ways of specifying entries
in a Poses. These methods are summarized below:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Specifier

	- Description

-
	- {cpp:enumerator}`B_DIRECT_SPECIFIER`

	- Used for specifying the entire Poses or selection as appropriate.

-
	- {cpp:enumerator}`B_INDEX_SPECIFIER`

	- "index" contains {htype}`int32` index of file in the Poses. Ranges are
specified with a pair of indices.

-
	- 'sref'

	- "refs" contains {htype}`entry_ref`s of specified files.

-
	- 'sprv'

	- Refers to item immediately following file whose {htype}`entry_ref` is
found in "data."

-
	- 'snxt'

	- Refers to item immediately preceeding file whose {htype}`entry_ref` is
found in "data."


:::

Always remember that other programs (or the user) may also be adding or
removing entries to the view and selection, so do not rely upon indices as
a safe method of referring to a specific file. Instead, use
{htype}`entry_refs`.

## The Entry Property

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Message

	- Specifiers

	- Description

-
	- {cpp:enumerator}`B_COUNT_PROPERTIES`

	- {cpp:enumerator}`B_DIRECT_SPECIFIER`

	- Counts entries in a Poses.

-
	- {cpp:enumerator}`B_DELETE_PROPERTY`

	- 'sref', {cpp:enumerator}`B_INDEX_SPECIFIER`

	- Moves the specified entry to the Trash.

-
	- {cpp:enumerator}`B_EXECUTE_PROPERTY`

	- 'sref', {cpp:enumerator}`B_INDEX_SPECIFIER`

	- Perform the equivalent action of opening the specified items in the
Tracker.

-
	- {cpp:enumerator}`B_GET_PROPERTY`

	- {cpp:enumerator}`B_DIRECT_SPECIFIER`

	- Returns {htype}`entry_ref`s of all entries in current Poses.

-
	- {cpp:enumerator}`B_GET_PROPERTY`

	- {cpp:enumerator}`B_INDEX_SPECIFIER`

	- Returns specified {htype}`entry_ref`.

-
	- {cpp:enumerator}`B_GET_PROPERTY`

	- 'sprv', 'snxt'

	- Returns {htype}`entry_ref` of entry prior to or following specified
{htype}`entry_ref`. Also returns index of file in "index."


:::

## The Selection Property

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Message

	- Specifiers

	- Description

-
	- {cpp:enumerator}`B_COUNT_PROPERTIES`

	- {cpp:enumerator}`B_DIRECT_SPECIFIER`

	- Counts the number of selected items in the Poses.

-
	- {cpp:enumerator}`B_CREATE_PROPERTY`

	- {cpp:enumerator}`B_DIRECT_SPECIFIER`

	- Adds items to the current selection. These can be specified as either
{htype}`entry_ref`s or {htype}`int32`s in the "data" array.

-
	- {cpp:enumerator}`B_DELETE_PROPERTY`

	- 'sref', {cpp:enumerator}`B_INDEX_SPECIFIER`

	- Removes items from the current selection.

-
	- {cpp:enumerator}`B_GET_PROPERTY`

	- {cpp:enumerator}`B_DIRECT_SPECIFIER`

	- Returns {htype}`entry_ref`s of items in selection.

-
	- {cpp:enumerator}`B_GET_PROPERTY`

	- 'sprv', 'snxt'

	- Returns {htype}`entry_ref` of file prior to or following given item.
Returns the index of the file in "index."

-
	- {cpp:enumerator}`B_SET_PROPERTY`

	- {cpp:enumerator}`B_DIRECT_SPECIFIER`

	- Clears the current selection and set it to the range given in "data." Also
accepts {htype}`entry_ref`s in "data" to determined the new selection.

-
	- {cpp:enumerator}`B_SET_PROPERTY`

	- 'sprv', 'snxt'

	- Clears the current selection and sets it to the {htype}`entry_ref`s prior
to or following those specified in "data."


:::
