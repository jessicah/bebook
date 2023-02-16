:::{cpp:class} BVolume
:::

# BVolume

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BVolume::BVolume()
:::

:::{cpp:function} BVolume::BVolume(dev_t device)
:::

:::{cpp:function} BVolume::BVolume(BVolume& volume)
:::

Creates a new {hclass}`BVolume` object and initializes it according to the
argument. The status of the initialization is recorded by the
{cpp:func}`InitCheck() <BVolume::InitCheck>` function.

-   The default constructor does nothing and sets {cpp:func}`InitCheck()
<BVolume::InitCheck>` to {cpp:enumerator}`B_NO_INIT`.

-   The device constructor sets the {hclass}`BVolume` to point to the volume
represented by the argument. See the {cpp:func}`SetTo() <BVolume::SetTo>`
function for status codes.

-   The copy constructor sets the object to point to the same device as does
the argument.
::::

::::{abi-group}
:::{cpp:function} BVolume::~BVolume()
:::

Destroys the {hclass}`BVolume` object.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} off_t BVolume::Capacity() const
:::

:::{cpp:function} off_t BVolume::FreeBytes() const
:::

Returns the volume's total storage capacity and the amount of storage
that's currently unused. Both measurements are in bytes.
::::

::::{abi-group}
:::{cpp:function} dev_t BVolume::Device() const
:::

Returns the object's {htype}`dev_t` number.
::::

::::{abi-group}
:::{cpp:function} status_t BVolume::GetIcon(BBitmap* icon, icon_size which) const
:::

Returns the volume's icon in {hparam}`icon`. which specifies the icon to
retrieve, either {cpp:enumerator}`B_MINI_ICON` (16x16) or
{cpp:enumerator}`B_LARGE_ICON` (32x32).

See also: {ref}`get_device_icon()`
::::

::::{abi-group}
:::{cpp:function} status_t BVolume::GetName(char* buffer) const
:::

Copies the name of the volume into {hparam}`buffer`.
::::

::::{abi-group}
:::{cpp:function} status_t BVolume::GetRootDirectory(BDirectory* dir) const
:::

Initializes {hparam}`dir` (which must be allocated) to refer to the
volume's "root directory." The root directory stands at the "root" of the
volume's file hierarchy. Note that this isn't necessarily the root of the
entire file hierarchy.
::::

::::{abi-group}
:::{cpp:function} status_t BVolume::InitCheck() const
:::

Returns the status of the last initialization (from either the constructor
or {cpp:func}`SetTo() <BVolume::SetTo>`).
::::

::::{abi-group}
:::{cpp:function} bool BVolume::IsPersistent() const
:::

:::{cpp:function} bool BVolume::IsRemovable() const
:::

:::{cpp:function} bool BVolume::IsReadOnly() const
:::

:::{cpp:function} bool BVolume::IsShared() const
:::

These functions answer media-related questions about the volume:

-   {hmethod}`IsPersistent()`. Is the storage persistent (such as on a floppy
or hard disk)?

-   {hmethod}`IsRemovable()`. Can the media be removed?

-   {hmethod}`IsReadOnly()`. Can it be read but not written to?

-   {hmethod}`IsShared()`. Is it accessed through the network (as opposed to
being directly connected to this computer)?
::::

::::{abi-group}
:::{cpp:function} bool BVolume::KnowsAttr() const
:::

:::{cpp:function} bool BVolume::KnowsMime() const
:::

:::{cpp:function} bool BVolume::KnowsQuery() const
:::

These functions answer questions about the file system on the volume:

-   {hmethod}`KnowsAttr()`. Do its files accept attributes?

-   {hmethod}`KnowsMime()`. Does it use MIME to type files?

-   {hmethod}`KnowsQuery()`. Can it respond to queries?
::::

::::{abi-group}
:::{cpp:function} status_t BVolume::SetTo(dev_t dev)
:::

:::{cpp:function} void BVolume::Unset()
:::

{hmethod}`SetTo()` initializes the {hclass}`BVolume` object to represent
the volume (device) identified by the argument.

{hmethod}`Unset()` uninitializes the {hclass}`BVolume`.
::::

## Operators

::::{abi-group}
:::{cpp:function} BVolume& operator =(const BEntry& volume)
:::

In the expression

:::{code} cpp
BVolume a = b;
:::

{hclass}`BVolume` {hparam}`a` is initialized to refer to the same volume
as {hparam}`b`. To gauge the success of the assignment, you should call
{cpp:func}`InitCheck() <BVolume::InitCheck>` immediately afterwards.
Assigning a {hclass}`BVolume` to itself is safe.

Assigning from an uninitialized {hclass}`BVolume` is "successful": The
assigned-to {hclass}`BVolume` will also be uninitialized
({cpp:enumerator}`B_NO_INIT`).
::::

::::{abi-group}
:::{cpp:function} bool operator ==(const BVolume& volume) const
:::

:::{cpp:function} bool operator !=(const BVolume& volume) const
:::

Two {hclass}`BVolume` objects are said to be equal if they refer to the
same volume, or if they're both uninitialized.
::::
