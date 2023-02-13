# Constants And Defined Types

Declared in: drivers/Drivers.h

This section covers constants and types defined for use by kernel drivers
and modules.

## Constants

### Current Driver API Version

:::{code}
#define B_CUR_DRIVER_API_VERSION N
:::

The {cpp:enum}`B_CUR_DRIVER_API_VERSION` constant indicates what version
of the driver API your driver will be built to.

See also: "{cpp:func}`~DeviceDrivers::SymbolsDriversExport`"

### Driver Control Opcodes

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-

	- Constant

	- Description

-

	- {cpp:enum}`B_GET_DEVICE_SIZE`

	- Returns a {htype}`size_t` indicating the device size in bytes.

-

	- {cpp:enum}`B_SET_DEVICE_SIZE`

	- Sets the device size to the value pointed to by data.

-

	- {cpp:enum}`B_SET_NONBLOCKING_IO`

	- Sets the device to use nonblocking I/O.

-

	- {cpp:enum}`B_SET_BLOCKING_IO`

	- Sets the device to use blocking I/O.

-

	- {cpp:enum}`B_GET_READ_STATUS`

	- Returns {cpp:enum}`true` if the device can read without blocking,
otherwise {cpp:enum}`false`.

-

	- {cpp:enum}`B_GET_WRITE_STATUS`

	- Returns {cpp:enum}`true` if the device can write without blocking,
otherwise {cpp:enum}`false`.

-

	- {cpp:enum}`B_GET_GEOMETRY`

	- Fills out the specified {cpp:func}`~device::geometry` structure to
describe the device.

-

	- {cpp:enum}`B_GET_DRIVER_FOR_DEVICE`

	- Returns the path of the driver executable handling the device.

-

	- {cpp:enum}`B_GET_PARTITION_INFO`

	- Returns a {cpp:func}`~partition::info` structure for the device.

-

	- {cpp:enum}`B_SET_PARTITION`

	- Creates a user-defined partition. data points to a
{cpp:func}`~partition::info` structure.

-

	- {cpp:enum}`B_FORMAT_DEVICE`

	- Formats the device. data should point to a boolean value: If
{cpp:enum}`true`, the device is formatted low-level. If it's
{cpp:enum}`false`, the formatting is <<??>>

-

	- {cpp:enum}`B_EJECT_DEVICE`

	- Ejects the device.

-

	- {cpp:enum}`B_GET_ICON`

	- Fills out the specified {cpp:func}`~device::icon` {htype}`` structure to
describe the device's icon.

-

	- {cpp:enum}`B_GET_BIOS_GEOMETRY`

	- Fills out a {cpp:func}`~device::geometry` structure to describe the device
as the BIOS sees it.

-

	- {cpp:enum}`B_GET_MEDIA_STATUS`

	- Gets the status of the media in the device by placing a status_t at the
location pointed to by data.B_GET_MEDIA_STATUS returns one of these values
in data:B_NO_ERROR.The media is ready.B_DEV_NO_MEDIA.No media in the
deviceB_DEV_NOT_READY.The device isn't ready.B_DEV_MEDIA_CHANGED.The media
changed since the time that the device was opened, or since the time of the
last B_GET_MEDIA_STATUS request.B_DEV_MEDIA_CHANGE_REQUEST.The user wants
to remove the media.B_DEV_DOOR_OPEN.The drive "door" is open.

-

	- {cpp:enum}`B_LOAD_MEDIA`

	- Loads the media.

-

	- {cpp:enum}`B_GET_BIOS_DRIVE_ID`

	- Returns the BIOS ID for the device.

-

	- {cpp:enum}`B_SET_UNINTERRUPTABLE_IO`

	- Prevents {hkey}`control`+{hkey}`C` from interrupting I/O.

-

	- {cpp:enum}`B_SET_INTERRUPTABLE_IO`

	- Allows {hkey}`control`+{hkey}`C` to interrupt I/O.

-

	- {cpp:enum}`B_FLUSH_DRIVE_CACHE`

	- Flushes the drive's cache.

-

	- {cpp:enum}`B_GET_NEXT_OPEN_DEVICE`

	- Iterates through open devices; data points to an
{htype}`open_device_iterator`.

-

	- {cpp:enum}`B_ADD_FIXED_DRIVER`

	- For internal use only.

-

	- {cpp:enum}`B_REMOVE_FIXED_DRIVER`

	- For internal use only.

-

	- {cpp:enum}`B_AUDIO_DRIVER_BASE`

	- Base for codes in audio_driver.h.

-

	- {cpp:enum}`B_MIDI_DRIVER_BASE`

	- Base for codes in midi_driver.h.

-

	- {cpp:enum}`B_JOYSTICK_DRIVER_BASE`

	- Base for codes in joystick.h.

-

	- {cpp:enum}`B_GRAPHIC_DRIVER_BASE`

	- Base for codes in graphic_driver.h.

-

	- {cpp:enum}`B_DEVICE_OP_CODES_END`

	- End of Be-defined control IDs.
:::

## Defined Types

### device_geometry

:::{code}
typedef struct {
    uint32 bytes_per_sector;
    uint32 sectors_per_track;
    uint32 cylinder_count;
    uint32 head_count;
    uchar device_type;
    bool removable;
    bool read_only;
    bool write_once;
} device_geometry
:::

The device_geometry structure is returned by the
{cpp:enum}`B_GET_GEOMETRY` driver control function. Its fields are:

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

	- bytes_per_sector

	- Indicates how many bytes each sector of the disk contains.

-

	- sectors_per_track

	- Indicates how many sectors each disk track contains.

-

	- cylinder_count

	- Indicates the number of cylinders the disk contains.

-

	- head_count

	- Indicates how many heads the disk has.

-

	- device_type

	- Specifies the type of device; there's a list of device type definitions
below.

-

	- removable

	- Is {cpp:enum}`true` if the device's media can be removed from the drive,
and is {cpp:enum}`false` otherwise.

-

	- read_only

	- Is {cpp:enum}`true` if the media is read-only (such as CD-ROM), or
{cpp:enum}`false` if the media can be both read from and written.

-

	- write_once

	- Is {cpp:enum}`true` if the media can only be written to once (such as
CD-recordable), or {cpp:enum}`false` if there's no limit to the number of
times the media can be written to.
:::

If you need to compute the total size of the device in bytes, you can
obtain this figure using the following simple formula:

:::{code}
disk_size = geometry.cylinder_count * geometry.sectors_per_track *
geometry.head_count * geometry.bytes_per_sector;
:::

The device type returned in device_type is one of:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-

	- Constant

	- Description

-

	- {cpp:enum}`B_DISK`

	- Hard disk, floppy disk, etc.

-

	- {cpp:enum}`B_TAPE`

	- Tape drive.

-

	- {cpp:enum}`B_PRINTER`

	- Printer.

-

	- {cpp:enum}`B_CPU`

	- CPU device.

-

	- {cpp:enum}`B_WORM`

	- Write-once, read-many device (such as CD-recordable).

-

	- {cpp:enum}`B_CD`

	- CD-ROM.

-

	- {cpp:enum}`B_SCANNER`

	- Scanner.

-

	- {cpp:enum}`B_OPTICAL`

	- Optical device

-

	- {cpp:enum}`B_JUKEBOX`

	- Jukebox device.

-

	- {cpp:enum}`B_NETWORK`

	- Network device.
:::

### device_hooks

:::{code}
typedef struct {
    device_open_hook open;
    device_close_hook close;
    device_free_hook free;
    device_control_hook control;
    device_read_hook read;
    device_write_hook write;
    device_select_hook select;
    device_deselect_hook deselect;
    device_readv_hook readv;
    device_writev_hook writev;
} device_hooks
:::

This structure is used by device drivers to export their function hooks to
the kernel.

### device_icon

:::{code}
typedef struct {
    int32 icon_size;
    void*icon_data;
} device_icon
:::

When you want to obtain an icon for a specific device, call ioctl() on the
open device, specifying the {cpp:enum}`B_GET_ICON` opcode. Pass in data a
pointer to a {htype}`device_icon` structure in which icon_size indicates
the size of icon you want and icon_data points to a buffer large enough to
receive the icon's data.

icon_size can be either {cpp:enum}`B_MINI_ICON`, in which case the buffer
pointed to by icon_data should be large enough to receive a 16x16 8-bit
bitmap (256-byte), or {cpp:enum}`B_LARGE_ICON`, in which case the buffer
should be large enough to receive a 32x32 8-bit bitmap (1024-byte). The
most obvious way to set up this buffer would be to create a
{cpp:class}`BBitmap` of the appropriate size and color depth and use its
buffer, like this:

:::{code}
BBitmap bits(BRect(0, 0, B_MINI_ICON-1, B_MINI_ICON-1, 0, B_CMAP8));
device_icon iconrec;

iconrec.icon_size = B_MINI_ICON;
iconrec.icon_data = bits.Bits();
status_t err = ioctl(dev_fd, B_GET_ICON, &iconrec);

if (err == B_OK) {
   /* enjoy the icon */
   ...
   view->DrawBitmap(bits);
} else {
   /* I don't like icons anyway */
}
:::

### driver_path

:::{code}
typedef char driver_path[256];
:::

Used by the {cpp:enum}`B_GET_DRIVER_FOR_DEVICE` control function to return
the pathname of the specified device.

### open_device_iterator

:::{code}
typedef struct {
    uint32 cookie;
    char device[256];
} open_device_iterator
:::

Used by the {cpp:enum}`B_GET_NEXT_OPEN_DEVICE` control function. The first
time you call this function, your {htype}`open_device_iterator` should have
cookie initialized to 0. Then just keep calling it over and over; each time
you'll get the name of the next open device. When an error is returned,
you're done.

### partition_info

:::{code}
typedef struct {
    off_t offset;
    off_t size;
    int32 logical_block_size;
    int32 session;
    int32 partition;
    char device[256];
} partition_info
:::

The {htype}`partition_info` structure describes a disk partition, and is
used by the {cpp:enum}`B_GET_PARTITION_INFO` and
{cpp:enum}`B_SET_PARTITION` control commands.

The fields are:

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

	- offset

	- Is the offset, in bytes, from the beginning of the disk to the beginning
of the partition.

-

	- size

	- Is the size, in bytes, of the partition.

-

	- logical_block_size

	- Is the block size with which the file system was written to the partition.

-

	- sessionandpartition

	- Are the session and partition ID numbers for the partition.

-

	- device

	- Is the pathname of the physical device on which the partition is located.
:::
