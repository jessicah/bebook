# Writing Drivers

A device driver is an add-on that communicates with a specific device or
type of device. Usually this communication involves some form of
device-specific protocol. For example, an add-on that specifically
addresses an Ethernet card or graphics card is a device driver. Likewise,
add-ons that know how to talk to a class such as SCSI disks, ATA devices,
ATAPI disks, or USB input devices is also a device driver.

A driver's job is to recognize the device and provide a means for
applications to talk to it.

:::{admonition} Warning
:class: warning
We can't stress this enough: a bug in a device driver can bring down the
entire system. Be very careful, and be sure to test your work well.
:::

To reduce the risk of the system being adversely affected by a bug in your
code, you should put as much of your code into user space as possible.

This section covers the structure of device drivers, and provides some
examples of how to write them.

## Symbols Drivers Export

The kernel communicates with drivers by calling certain known entry
points, which the driver must implement and export. These entry points are:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Symbol

	- Description

-
	- api_version
	- This exported value tells the kernel what version of the driver API it was
		written to, and should always be set to
		{cpp:enumerator}`B_CUR_DRIVER_API_VERSION` in your source code.
-
	- init_hardware()
	- Called when the system is booted, to let the driver detect and reset the
		hardware.
-
	- init_driver()
	- Called when the driver is loaded, so it can allocate needed system
		resources.
-
	- uninit_driver()
	- Called just before the driver is unloaded, so it can free allocated
		resources.
-
	- publish_devices()
	- Called to obtain a list of device names supported by the driver.
-
	- find_device()
	- Called to obtain a list of pointers to the hook functions for a specified
		device.

:::

## Constants

### api_version

:::{code} c
int32 api_version;
:::

This variable defines the API version to which the driver was written, and
should be set to {cpp:enumerator}`B_CUR_DRIVER_API_VERSION` at compile
time. The value of this variable will be changed with every revision to the
driver API; the value with which your driver was compiled will tell devfs
how it can communicate with the driver.

## Functions

::::{abi-group}
:::{cpp:function} status_t init_hardware()
:::

This function is called when the system is booted, which lets the driver
detect and reset the hardware it controls. The function should return
{cpp:enumerator}`B_OK` if the initialization is successful; otherwise, an
appropriate error code should be returned. If this function returns an
error, the driver won't be used.
::::

::::{abi-group}
:::{cpp:function} status_t init_driver()
:::

Drivers are loaded and unloaded on an as-needed basis. When a driver is
loaded by devfs, this function is called to let the driver allocate memory
and other needed system resources. Return {cpp:enumerator}`B_OK` if
initialization succeeds, otherwise return an appropriate error code.

:::{admonition} TODO
:class: note
what happens if this returns an error?
:::
::::

::::{abi-group}
:::{cpp:function} void uninit_driver()
:::

This function is called by devfs just before the driver is unloaded from
memory. This lets the driver clean up after itself, freeing any resources
it allocated.
::::

::::{abi-group}
:::{cpp:function} const char** publish_devices()
:::

Devfs calls publish_devices() to learn the names, relative to /dev, of the
devices the driver supports. The driver should return a
{cpp:expr}`NULL`-terminated array of strings indicating all the installed
devices the driver supports. For example, an ethernet device driver might
return:

:::{code} c
static char*devices[] = {
   "net/ether",
   NULL
};
:::

In this case, devfs will then create the pseudo-file /dev/net/ether,
through which all user applications can access the driver.

Since only one instance of the driver will be loaded, if support for
multiple devices of the same type is desired, the driver must be capable of
supporting them. If the driver senses (and supports) two ethernet cards, it
might return:

:::{code} c
static char*devices[] = {
   "net/ether1",
   "net/ether2",
   NULL
};
:::
::::

::::{abi-group}
:::{cpp:function} device_hooks* find_device(const char* name)
:::

When a device published by the driver is accessed, devfs communicates with
it through a series of hook functions that handle the requests.The
find_device() function is called to obtain a list of these hook functions,
so that devfs can call them. The {htype}`device_hooks` structure returned
lists out the hook functions.

The device_hooks structure, and what each hook does, is described in the
next section.
::::

## Device Hooks

The hook functions specified in the device_hooks function returned by the
driver's {cpp:func}`find_device() <find::device>` function handle requests
made by devfs (and through devfs, from user applications). These are
described in this section.

The structure itself looks like this:

:::{code} c
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
} device_hooks;
:::

In all cases, return {cpp:enumerator}`B_OK` if the operation is
successfully completed, or an appropriate error code if not.

::::{abi-group}
:::{cpp:function} status_t open_hook(const char* name, uint32 flags, void** cookie)
:::

This hook function is called when a program opens one of the devices
supported by the driver. The name of the device (as returned by
{cpp:func}`publish_devices() <publish::devices>`) is passed in name, along
with the flags passed to the Posix open() function. {hparam}`cookie` points
to space large enough for you to store a single pointer. You can use this
to store state information specific to the open() instance. If you need to
track information on a per-open() basis, allocate the memory you need and
store a pointer to it in *{hparam}`cookie`.
::::

::::{abi-group}
:::{cpp:function} status_t close_hook(void** cookie)
:::

This hook is called when an open instance of the driver is closed using
the close() Posix function. Note that because of the multithreaded nature
of the BeOS, it's possible there may still be transactions pending, and you
may receive more calls on the device. For that reason, you shouldn't free
instance-wide system resources here. Instead, you should do this in
{cpp:func}`free_hook() <free::hook>`. However, if there are any blocked
transactions pending, you should unblock them here.
::::

::::{abi-group}
:::{cpp:function} status_t free_hook(void** cookie)
:::

This hook is called once all pending transactions on an open (but closing)
instance of your driver are completed. This is where your driver should
release instance-wide system resources. free_hook() doesn't correspond to
any Posix function.
::::

::::{abi-group}
:::{cpp:function} status_t read_hook(void* cookie, off_t position, void* data, size_t* len)
:::

This hook handles the Posix read() function for an open instance of your
driver. Implement it to read {hparam}`len` bytes of data starting at the
specified byte {hparam}`position` on the device, storing the read bytes at
{hparam}`data`. Exactly what this does is device-specific (disk devices
would read from the specified offset on the disk, but a graphics driver
might have some other interpretation of this request).

Before returning, you should set {hparam}`len` to the actual number of
bytes read into the buffer. Return {cpp:enumerator}`B_OK` if data was read
(even if the number of returned bytes is less than requested), otherwise
return an appropriate error.
::::

::::{abi-group}
:::{cpp:function} status_t readv_hook(void* cookie, off_t position, const struct iovec* vec, size_t count, size_t* len)
:::

This hook handles the Posix readv() function for an open instance of your
driver. This is a scatter/gather read function; given an array of
{htype}`iovec` structures describing address/length pairs for a group of
destination buffers, your implementation should fill each successive buffer
with bytes, up to a total of {hparam}`len` bytes. The {hparam}`vec` array
has {hparam}`count` items in it.

As with {cpp:func}`read_hook() <read::hook>`, set {hparam}`len` to the
actual number of bytes read, and return an appropriate result code.
::::

::::{abi-group}
:::{cpp:function} status_t write_hook(void* cookie, off_t position, void* data, size_t* len)
:::

This hook handles the Posix write() function for an open instance of your
driver. Implement it to write {hparam}`len` bytes of data starting at the
specified byte {hparam}`position` on the device, from the buffer pointed to
by {hparam}`data`. Exactly what this does is device-specific (disk devices
would write to the specified offset on the disk, but a graphics driver
might have some other interpretation of this request).

Return {cpp:enumerator}`B_OK` if data was read (even if the number of
returned bytes is less than requested), otherwise return an appropriate
error.
::::

::::{abi-group}
:::{cpp:function} status_t writev_hook(void* cookie, off_t position, const struct iovec* vec, size_t count, size_t* len)
:::

This hook handles the Posix writev() function for an open instance of your
driver. This is a scatter/gather write function; given an array of
{htype}`iovec` structures describing address/length pairs for a group of
source buffers, your implementation should write each successive buffer to
disk, up to a total of {hparam}`len` bytes. The {hparam}`vec` array has
{hparam}`count` items in it.

Before returning, set {hparam}`len` to the actual number of bytes written,
and return an appropriate result code.
::::

::::{abi-group}
:::{cpp:function} status_t control_hook(void* cookie, uint32 op, void* data, size_t* len)
:::

This hook handles the ioctl() function for an open instance of your
driver. The control hook provides a means to perform operations that don't
map directly to either read() or write(). It receives the {hparam}`cookie`
for the open instance, plus the command code {hparam}`op` and the
{hparam}`data` and {hparam}`len` arguments specified by ioctl()'s caller.
These arguments have no inherent relationship; they're simply arguments to
ioctl() that are forwarded to your hook function. Their definitions are
defined by the driver. Common command codes can be found in
drivers/Drivers.h.

:::{admonition} Note
:class: note
The {hparam}`len` argument is only valid when ioctl() is called from user
space; the kernel always sets it to 0.
:::
::::

::::{abi-group}
:::{cpp:function} status_t select_hook(uint8 event, uint32 ref, selectsync* sync)
:::

:::{cpp:function} status_t deselect_hook(uint8 event, uint32 ref, selectsync* sync)
:::

These hooks are reserved for future use. Set the corresponding entries in
your {htype}`device_hooks` structure to {cpp:expr}`NULL`.
::::

## Driver Rules

Keep the following rules in mind for each instance of your driver:

-   open() will be called first, and no other hooks will be called until
open() returns.

-   close() may be called while other requests are pending. As previously
mentioned, if you have blocked transactions, you must unblock them when
close() is called. Further calls to other driver hooks my continue to occur
after close() is called; however, you should return an error to any such
requests.

-   free() isn't called until all pending transactions for the open instance
are completed.

-   Multiple threads may be accessing the driver's hooks simultaneously, so be
sure to lock and unlock where appropriate.
