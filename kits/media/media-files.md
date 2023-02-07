# BMediaFiles
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BMediaFiles::BMediaFiles()
:::
Constructor.
::::

::::{abi-group}

:::{cpp:function} virtual BMediaFiles::~BMediaFiles()()
:::
Destructor.
::::

## Member Functions
::::{abi-group}

:::{cpp:function} virtual status_t BMediaFiles::GetNextRef(BString* outType, entry_ref outRef = NULL)
:::
Returns the next media type in {hparam}`outType`.
These types include things like "sound" and "bitmap."
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- No error.
-
	- {cpp:enum}`B_BAD_INDEX`
	- No more entry_refs to get.
-
	- {cpp:enum}`B_BAD_VALUE`
	- {hparam}`outType` is {cpp:enum}`NULL`.
:::
::::

::::{abi-group}

:::{cpp:function} virtual status_t BMediaFiles::GetNextType(BString* outType) const
:::
Returns the next media type in {hparam}`outType`.
These types include things like "sound" and "bitmap."
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- No error.
-
	- {cpp:enum}`B_BAD_INDEX`
	- No more types to get.
:::
::::

::::{abi-group}

:::{cpp:function} virtual status_t BMediaFiles::GetRefFor(const char* type, const char* item, entry_ref* outRef)
:::
:::{cpp:function} virtual status_t BMediaFiles::SetRefFor(const char* type, const char* item, entry_ref& outRef)
:::
:::{cpp:function} virtual status_t BMediaFiles::RemoveRefFor(const char* type, const char* item, entry_ref& outRef)
:::
{hmethod}`GetRefFor()` returns the
entry_ref for the media file that's been assigned
to the specified {hparam}`type` and {hparam}`item`
name pair. For example, if you wanted to
retrieve the sound file that's been assigned as the system startup sound,
you might specify type as "sound" and item as "startup sound."
{hmethod}`SetRefFor()` sets, by entry_ref,
the file to be used for the specified
{hparam}`type`/{hparam}`item` pairing.
{hmethod}`RemoveRefFor()` removes the specified
entry_ref for the given
{hparam}`type`/{hparam}`item` pairing.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- No error.
-
	- {cpp:enum}`B_ENTRY_NOT_FOUND`
	- ({hmethod}`GetRefFor()` only) the specified {hparam}`type`/{hparam}`item` pair isn't assigned.
:::
::::

::::{abi-group}

:::{cpp:function} virtual status_t BMediaFiles::RewindRefs(const char* type)
:::
Rewinds the entry_ref list for the specified media
type, so you can start scanning from the beginning of the list.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- No error.
-
	- {cpp:enum}`B_BAD_VALUE`
	- {hparam}`type` is {cpp:enum}`NULL`.
-
	- Other errors.
	- Unable to rewind; the Media Server may not be  responding.
:::
::::

::::{abi-group}

:::{cpp:function} virtual status_t BMediaFiles::RemoveItem(const char* type)
:::
Removes an entrire entry from the media files database. Unlike
{hmethod}`RemoveRefFor()`, which removes an
entry_ref from an entry, this function
actually deletes the entire entry.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- No error.
-
	- Other errors.
	- Unable to remove the item; the Media Server may not be responding.
:::
::::

::::{abi-group}

:::{cpp:function} virtual status_t BMediaFiles::RewindTypes()
:::
Rewinds to the beginning of the media type list. If you've been using a
{hclass}`BMediaFiles` object and want to begin scanning again from the beginning of
the media type list, you should call this function.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- No error.
-
	- Other errors.
	- Unable to rewind; the Media Server may not be responding.
:::
::::
