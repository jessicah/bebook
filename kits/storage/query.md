:::{cpp:class} BQuery
:::

# BQuery

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BQuery::BQuery()
:::

Creates a new {hclass}`BQuery` object. To use the object, you have to set
its predicate and volume, and then tell it to {cpp:func}`Fetch()
<BQuery::Fetch>`. If you want to fetch again, you have to call
{cpp:func}`Clear() <BQuery::Clear>` first (and re-set the predicate and
volume.)
::::

::::{abi-group}
:::{cpp:function} BQuery::~BQuery()
:::

Destroys the {hclass}`BQuery`. If the query is live, the query is shot
dead. You stop receiving live query updates when you delete the
{hclass}`BQuery` object.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} status_t BQuery::Clear()
:::

Erases the {hclass}`BQuery`'s predicate, sets the volume and target to
{cpp:expr}`NULL`, and turns off live query updates (if the query is live).
You call {hmethod}`Clear()` if you want to {cpp:func}`Fetch()
<BQuery::Fetch>` more than once: You have to {hmethod}`Clear()` before each
{cpp:func}`Fetch() <BQuery::Fetch>` (except the first).

{hmethod}`Clear()` always return {cpp:enumerator}`B_OK`.
::::

### CountEntries(), Rewind()

:::{admonition} Warning
:class: warning
Don't use these functions. They're no-ops for the {hclass}`BQuery` class.
:::

::::{abi-group}
:::{cpp:function} status_t BQuery::Fetch()
:::

Tells the {hclass}`BQuery` to go fetch the entries that satisfy the
predicate. After you've fetched, you can retrieve the set of "static"
entries through calls to {cpp:func}`GetNextEntry() <BQuery::GetNextEntry>`,
{cpp:func}`GetNextRef() <BQuery::GetNextRef>`, or
{cpp:func}`GetNextDirents() <BQuery::GetNextDirents>`.

If you've set the {hclass}`BQuery`'s target, then this query is live. The
live query update messages start rolling in when you tell the object to
{hmethod}`Fetch()`. They stop when you {cpp:func}`Clear() <BQuery::Clear>`
or destroy the object.

The fetch fails if the object's predicate or volume isn't set, or if
you've already fetched but haven' {cpp:func}`Clear() <BQuery::Clear>`'d
since then.

:::{admonition} Warning
:class: warning
Every query must include at least one indexed attribute. If your predicate
includes no indexed attributes, {hmethod}`Fetch()` will not balk—it returns
{cpp:enumerator}`B_OK` (given that it doesn't otherwise fail). However, no
entries will have been retrieved, and your subsequent {hmethod}`GetNext…()`
call will fail ({cpp:enumerator}`B_BAD_VALUE`).
:::

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
	- The fetch is running.
-
	- {cpp:enumerator}`B_NO_INIT`.
	- The volume or predicate isn't set.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- The predicate is improper.
-
	- {cpp:enumerator}`B_NOT_ALLOWED`.
	- You've already fetched; {cpp:func}`Clear() <BQuery::Clear>` the object and
		start again.

:::
::::

::::{abi-group}
:::{cpp:function} virtual status_t BQuery::GetNextEntry(BEntry* entry, bool traverse = false)
:::

:::{cpp:function} virtual status_t BQuery::GetNextRef(entry_ref* ref)
:::

:::{cpp:function} virtual int32 BQuery::GetNextDirents(dirent* buf, size_t bufsize, int32 count = INT_MAX)
:::

These functions return the next entry in the "static" entry list; the list
is created when you tell your (well-formed) {hclass}`BQuery` to
{cpp:func}`Fetch() <BQuery::Fetch>`. You can retrieve the entry as a
{cpp:class}`BEntry`, {htype}`entry_ref`, or {htype}`dirent` structure. The
static entry list is the set of entries that initially satisfy the
predicate; entries found by the live query mechanism are not included in
this list.

When you reach the end of the entry list, the {hmethod}`Get…()` function
returns an indicative value:

-   {hmethod}`GetNextRef()` and {hmethod}`GetNextEntry()` return
{cpp:enumerator}`B_ENTRY_NOT_FOUND`.

-   {hmethod}`GetNextDirents()` returns 0.

You can only cycle over the list once; the {cpp:func}`Rewind()
<BQuery::Rewind>` function is not defined for {hclass}`BQuery`. See the
{cpp:class}`BEntryList` class for more information on these functions.

{hmethod}`GetNextDirents()` returns the number of dirents it retrieved
(currently, it can only retrieve one at a time. The other two functions
return these codes:

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
	- The entry was retrieved.
-
	- {cpp:enumerator}`B_ENTRY_NOT_FOUND`.
	- You're at the end of the list.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- The predicate includes unindexed attributes.
-
	- {cpp:enumerator}`B_FILE_ERROR`.
	- The {hclass}`BQuery` hasn't fetched.

:::
::::

::::{abi-group}
:::{cpp:function} void BQuery::PushAttr(const char* attr_name)
:::

:::{cpp:function} void PushOp(query_op operator)
:::

:::{cpp:function} void BQuery::PushUInt32(uint32 value)
:::

:::{cpp:function} void BQuery::PushInt32(int32 value)
:::

:::{cpp:function} void BQuery::PushUInt64(uint64 value)
:::

:::{cpp:function} void BQuery::PushInt64(int64 value)
:::

:::{cpp:function} void BQuery::PushFloat(float value)
:::

:::{cpp:function} void BQuery::PushDouble(double value)
:::

:::{cpp:function} void BQuery::PushString(const char* attr_name, bool case_insensitive = false)
:::

You use these functions to construct the {hclass}`BQuery`'s predicate.
They create a predicate expression by pushing attribute names, operators,
and values in Reverse Polish Notation (post-fix) order.

-   {hmethod}`PushAttr()` pushes an attribute name.

-   {hmethod}`PushOp()` pushes one of the {cpp:func}`query_op <query::op>`
operators.

-   The rest of the functions push values of the designated types.

For details on how the push method works, see "{ref}`Constructing a
Predicate`."

The predicate that you construct through these functions can be returned
as a string through the {cpp:func}`GetPredicate() <BQuery::GetPredicate>`
function.
::::

::::{abi-group}
:::{cpp:function} status_t BQuery::SetTarget(BMessenger target)
:::

:::{cpp:function} bool BQuery::IsLive() const
:::

Sets the {hclass}`BQuery`'s target. The target identifies the
{cpp:class}`BLooper`/{cpp:class}`BHandler` pair (a la the
{cpp:class}`BInvoker` target protocol) that will receive subsequent live
query update messages. Calling this function declares the query to be live.

If {hparam}`target` is {cpp:expr}`NULL`, the {hclass}`BQuery` is told to
be "not live". However, you can only turn off liveness (in this way) before
you {cpp:func}`Fetch() <BQuery::Fetch>`. In other words, if you set the
target, and then call {cpp:func}`Fetch() <BQuery::Fetch>` and then call
`SetTarget(NULL)`, the {hclass}`BQuery` will think that it (itself) is not
live, but it really is.

{hmethod}`IsLive()` tells you if the {hclass}`BQuery` is live. The
"liveness" needn't be actuated yet—live queries don't start operating until
you tell the {hclass}`BQuery` to {cpp:func}`Fetch() <BQuery::Fetch>`. The
live query is killed when you delete or {cpp:func}`Clear() <BQuery::Clear>`
the {hclass}`BQuery` object.

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
	- The {hparam}`target` was set (including set to {cpp:expr}`NULL`).
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- {hparam}`target` doesn't identify a proper looper/handler pair.
-
	- {cpp:enumerator}`B_NOT_ALLOWED`.
	- You've already {cpp:func}`Fetch() <BQuery::Fetch>`'d; you need to
		{cpp:func}`Clear() <BQuery::Clear>`.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BQuery::SetPredicate(const char* expr)
:::

:::{cpp:function} status_t BQuery::GetPredicate(char* buf, size_t length)
:::

:::{cpp:function} size_t BQuery::PredicateLength()
:::

{hmethod}`SetPredicate()` sets the {hclass}`BQuery`'s predicate as a
string. Predicate strings can be simple, single comparison expressions:

:::{code} sh
"name = fido"
:::

Or they can be more complex:

:::{code} sh
"((name = fid*) || (size > 500)) && (last_modified < 243567)"
:::

For the complete rules on setting the predicate as a string, see
"{ref}`Constructing a Predicate`."

You can also set the predicate through the {hmethod}`Push…()` functions.
You can't combine the methods: Pushing the predicate always takes
precedence over {hmethod}`SetPredicate()`, regardless of the order in which
the methods are deployed.

{hmethod}`GetPredicate()` copies the predicate into {hparam}`buf`;
{hparam}`length` gives the length of {hparam}`buf`, in bytes. If you want
to find out how much storage you need to allocate to accommodate the
predicate, call {hmethod}`PredicateLength()` first.

If you set the predicate through the {hmethod}`Push…()` functions,
{hmethod}`GetPredicate()` converts the pushed construction into a string,
and returns a copy of the string to you.

{hmethod}`PredicateLength()` returns the length of the predicate string,
regardless of how it's created.

:::{admonition} Warning
:class: warning
{hmethod}`GetPredicate()` and {hmethod}`PredicateLength()` both clear the
push stack. This is important, because it means that you can't build up a
portion of your predicate, then call {hmethod}`GetPredicate()`, build a
little more, look again, build some more, etc. When you call
{hmethod}`GetPredicate()`, you're done. Your next step should be a
{cpp:func}`Fetch() <BQuery::Fetch>`
:::

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
	- The predicate was successfully set or gotten.
-
	- {cpp:enumerator}`B_NO_INIT`.
	- ({hmethod}`Get`) The predicate isn't set.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- ({hmethod}`Get`) length is shorter than the predicate's length.
-
	- {cpp:enumerator}`B_NOT_ALLOWED`.
	- ({hmethod}`Set`) You've already {cpp:func}`Fetch() <BQuery::Fetch>`'d; you
		have to {cpp:func}`Clear() <BQuery::Clear>`.
-
	- {cpp:enumerator}`B_NO_MEMORY`.
	- ({hmethod}`Set`) Not enough memory to store the predicate string.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BQuery::SetVolume(const BVolume* volume)
:::

A query can only look in one volume at a time. This is where you set the
volume that you want to look at.

:::{admonition} Warning
:class: warning
Currently, {hmethod}`SetVolume()` doesn't complain if volume is invalid.
However, the subsequent {cpp:func}`Fetch() <BQuery::Fetch>` will fail
({cpp:enumerator}`B_NO_INIT`).
:::

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
	- The volume was set.
-
	- {cpp:enumerator}`B_NOT_ALLOWED`.
	- You've already fetched, you need to {cpp:func}`Clear() <BQuery::Clear>`
		before you can reset the volume.

:::
::::

## Constants

### Query Operation Codes

These constants define the operations that can be used to specify a query.
They are used in conjunction with the push functions for constructing a
query.

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Constant

	- Operation

-
	- {cpp:enumerator}`B_EQ`

	- =

-
	- {cpp:enumerator}`B_NE`

	- !=

-
	- {cpp:enumerator}`B_GT`

	- >

-
	- {cpp:enumerator}`B_LT`

	- <

-
	- {cpp:enumerator}`B_GE`

	- >=

-
	- {cpp:enumerator}`B_LE`

	- <=

-
	- {cpp:enumerator}`B_CONTAINS`

	- string contains value ("*value*")

-
	- {cpp:enumerator}`B_BEGINS_WITH`

	- string begins with value ("value*")

-
	- {cpp:enumerator}`B_ENDS_WITH`

	- string ends with value ("*value")

-
	- {cpp:enumerator}`B_AND`

	- &&

-
	- {cpp:enumerator}`B_OR`

	- ||

-
	- {cpp:enumerator}`B_NOT`

	- !


:::
