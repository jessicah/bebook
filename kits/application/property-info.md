:::{cpp:class} BPropertyInfo
:::

# BPropertyInfo

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BPropertyInfo::BPropertyInfo(property_info* p = NULL, bool free_on_delete = false)
:::

Initializes the object with the specified zero-terminated array
{hparam}`p` of {cpp:func}`property_info <property::info>`. Passing
{cpp:expr}`true` in {hparam}`free_on_delete` instructs the object to free
the memory associated with the {cpp:func}`property_info <property::info>`
when the object is destroyed. {hclass}`BPropertyInfo` does not copy the
array, so it is important that the array is not deleted or otherwise
destroyed while the {hclass}`BPropertyInfo` is in use.
::::

::::{abi-group}
:::{cpp:function} BPropertyInfo::~BPropertyInfo()
:::

If {hparam}`free_on_delete` is set to {cpp:expr}`true` in the constructor,
the destructor frees all memory associated with the
{cpp:func}`property_info <property::info>`. Otherwise, it does nothing.
::::

## Member Functions

### AllowsTypeCode()

See {cpp:func}`BFlattenable::AllowsTypeCode`.

::::{abi-group}
:::{cpp:function} int32 BPropertyInfo::FindMatch(BMessage* msg, int32 index, BMessage* spec, int32 form, const char* prop, void* data = NULL) const
:::

Passed a property name in {hparam}`prop`, a specifier in {hparam}`form`,
and a command in {hparam}`msg`->{hparam}`what`, searches the
{cpp:func}`property_info <property::info>` array for an item supporting the
specified scripting request. If {hparam}`index` is nonzero, then
{hmethod}`FindMatch()` only searches those {cpp:func}`property_info
<property::info>` structures with the wildcard command (first element of
command array equal to 0). Otherwise, it searches through all available
{cpp:func}`property_info <property::info>` structures for a match. If a
match is found, it fills the memory at {hparam}`data` with the contents of
the {hparam}`extra_data` field of the match and returns the index of the
match in the array. Otherwise, it returns {cpp:enumerator}`B_ERROR`.
::::

### Flatten()

See {cpp:func}`BFlattenable::Flatten`.

### FlattenedSize()

See {cpp:func}`BFlattenable::FlattenedSize`.

### IsFixedSize()

See {cpp:func}`BFlattenable::IsFixedSize`.

### TypeCode()

See {cpp:func}`BFlattenable::TypeCode`.

::::{abi-group}
:::{cpp:function} void BPropertyInfo::PrintToStream() const
:::

Prints information about the {hclass}`BPropertyInfo` to standard output.
::::

::::{abi-group}
:::{cpp:function} const property_info* BPropertyInfo::PropertyInfo() const
:::

Returns the {cpp:func}`property_info <property::info>` list associated
with the object.
::::

### Unflatten()

See {cpp:func}`BFlattenable::Unflatten`.

## Defined Types

### property_info

:::{code}
struct property_info {
    char*  name;
    uint32 commands[10];
    uint32 specifiers[10];
    char*  usage;
    uint32 extra_data;
};
:::

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Field

	- Description

-
	- name
	- Provides the name of the property this structure describes.
-
	- commands
	- Is a zero-terminated array of commands understood by the property, i.e.
		{cpp:enumerator}`B_GET_PROPERTY`. If the first element is 0, it represents
		a wildcard matching all possible commands.
-
	- specifiers
	- Is a zero-terminated array of the specifiers understood by the property,
		i.e. {cpp:enumerator}`B_DIRECT_SPECIFIER`. If the first element is 0, it
		represents a wildcard matching all possible specifiers.
-
	- usage
	- Gives a human-readable string describing the property and its allowable
		commands and specifiers.
-
	- extra_data
	- Is an area free for general use; the operating system does not touch its
		contents.

:::
