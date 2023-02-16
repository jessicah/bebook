:::{cpp:class} BEntryList
:::

# BEntryList

## Member Functions

::::{abi-group}
:::{cpp:function} virtual int32 BEntryList::CountEntries() = 0
:::

Returns the number of entries that are in the entry list.

:::{admonition} Warning
:class: warning
For {cpp:class}`BQuery` this is a no-op. Also, {cpp:class}`BDirectory`'s
implementation manipulates the entry list pointer; thus, you shouldn't call
{hmethod}`CountEntries()` while you're iterating through the directory's
entries.
:::
::::

::::{abi-group}
:::{cpp:function} virtual status_t BEntryList::GetNextEntry(BEntry* entry, bool traverse = false) = 0
:::

:::{cpp:function} virtual status_t BEntryList::GetNextRef(entry_ref* ref) = 0
:::

:::{cpp:function} virtual int32 BEntryList::GetNextDirents(dirent* buf, size_t bufsize, int32 count = INT_MAX) = 0
:::

These functions return the "next" entry in the entry list as a
{cpp:class}`BEntry`, {htype}`entry_ref`, or {htype}`dirent` structure. The
end of the list is signalled by…

-   {hmethod}`GetNextEntry()` and {hmethod}`GetNextRef()` return
{cpp:enumerator}`B_ENTRY_NOT_FOUND`.

-   {hmethod}`GetNextDirents()` returns 0.

If the {hparam}`traverse` argument is {cpp:expr}`true`, symlinks are
traversed.

See the {ref}`class overview` for more information.
::::

::::{abi-group}
:::{cpp:function} virtual status_t BEntryList::Rewind() = 0
:::

Rewinds the entry list pointer so it points to the first element in the
list.

:::{admonition} Warning
:class: warning
For {cpp:class}`BQuery` this is a no-op.
:::
::::
