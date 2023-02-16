:::{cpp:class} BVolumeRoster
:::

# BVolumeRoster

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BVolumeRoster::BVolumeRoster()
:::

Creates a new {hclass}`BVolumeRoster` object. You don't have to
"initialize" the object before using it (as you do with most other Storage
Kit classes). You can call {cpp:func}`GetNextVolume()
<BVolumeRoster::GetNextVolume>` (or whatever) immediately after
constructing.
::::

::::{abi-group}
:::{cpp:function} virtual BVolumeRoster::~BVolumeRoster()
:::

Destroys the object. If this {hclass}`BVolumeRoster` object was watching
volumes, the watch is called off.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} status_t BVolumeRoster::GetBootVolume(BVolume* boot_vol)
:::

Initializes {hparam}`boot_vol` to refer to the "boot volume." This is the
volume that was used to boot the computer. {hparam}`boot_vol` must be
allocated before you pass it in. If the boot volume can't be found, the
argument is uninitialized.

(Currently, this function looks for the volume that's mounted at /boot.
The only way to fool the system into thinking that there isn't a boot
volume is to rename /boot—not a smart thing to do.)

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
	- {cpp:enumerator}`B_NO_ERROR`.
	- The boot volume was successfully retrieved.
-
	- {cpp:enumerator}`B_ENTRY_NOT_FOUND`.
	- The boot volume wasn't found.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BVolumeRoster::GetNextVolume(BVolume* volume)
:::

:::{cpp:function} void BVolumeRoster::Rewind()
:::

{hmethod}`GetNextVolume()` retrieves the "next" volume from the volume
list and uses it to initialize the argument (which must be allocated). When
the function return {cpp:enumerator}`B_BAD_VALUE`, you've reached the end
of the list.

{hmethod}`Rewind()` rewinds the volume list such that the next
{hmethod}`GetNextVolume()` will return the first element in the list.

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
	- {cpp:enumerator}`B_NO_ERROR`.
	- The next volume was successfully retrieved.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- You've reached the end of the volume list.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BVolumeRoster::StartWatching(BMessenger* messenger = be_app_messenger )
:::

:::{cpp:function} void BVolumeRoster::StopWatching()
:::

:::{cpp:function} BMessenger BVolumeRoster::Messenger() const
:::

These functions start and stop the {hclass}`BVolumeRoster`'s
volume-watching facility. (This is actually just a convenient cover for the
Node Monitor.)

-   {hmethod}`StartWatching()` registers a request for notifications of volume
mounts and unmounts. The notifications are sent (as {cpp:class}`BMessage`s)
to the {cpp:class}`BHandler` / {cpp:class}`BLooper` pair specified by the
argument. There are separate messages for mounting and unmounting; their
formats are described below. The caller retains possession of the
{cpp:class}`BHandler` / {cpp:class}`BLooper` that the
{cpp:class}`BMessenger` represents. The volume watching continues until
this {hclass}`BVolumeRoster` object is destroyed, or until you call…

-   {hmethod}`StopWatching()`. This function tells the volume-watcher to stop
watching. In other words, notifications of volume mounts and unmounts are
no longer sent to the {hclass}`BVolumeRoster`'s target.

-   {hmethod}`Messenger()` returns a copy of the {cpp:class}`BMessenger`
object that was set in the previous {hmethod}`StartWatching()` call.

There are separate notifications ({cpp:class}`BMessage`s) for
volume-mounted and volume-unmounted events. See the
{cpp:enumerator}`B_DEVICE_MOUNTED` and {cpp:enumerator}`B_DEVICE_UNMOUNTED`
descriptions in "{ref}`The Node Monitor`" section of this chapter.

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
	- {cpp:enumerator}`B_NO_ERROR`.
	- The volume-watcher was successfully started or stopped.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- Poorly formed {cpp:class}`BMessenger`.
-
	- {cpp:enumerator}`B_NO_MEMORY`.
	- Couldn't allocate resources.

:::
::::
