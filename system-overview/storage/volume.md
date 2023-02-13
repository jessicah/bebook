# BVolume

The {hclass}`BVolume` class lets you ask questions about specific
"volumes," where a volume is any independent file system. Most applications
are usually only interested in "persistent" volumes, such as hard disks,
floppies, or CD-ROMs, but you can also create {hclass}`BVolume`s to virtual
file systems, such as /pipe.

Here's what a {hclass}`BVolume` knows:

- The volume's name, device ID, and "root directory."

- Its storage capacity, and the currently available storage.

- If the volume is on a media that's removable.

- If the volume's storage is persistent (as opposed to the ephemeral storage
you get with virtual file systems).

- If the volume is accessed through the network.

- If the file system uses MIME as file types, if it responds to queries, and
if it knows about attributes.

## Initializing a BVolume

There are two ways to initialize a {hclass}`BVolume`:



## Mount and Unmount

A {hclass}`BVolume` object can't tell you directly whether the device that
it represents is still mounted. If you want to ask, you can call a
{htype}`status_t`-returning {hclass}`BVolume` function; if the function
returns {cpp:enum}`B_BAD_VALUE`, the device is no longer mounted.

Furthermore, you can't ask a {hclass}`BVolume` to unmount itself. If you
want to be told when devices are mounted and unmounted, you have to ask the
Node Monitor to help you. Call {cpp:func}`~watch::node` thus:

:::{code}
watch_node(NULL, B_WATCH_MOUNT, messenger);
:::

messenger is a {cpp:class}`BMessenger` object that acts as the target of
subsequent mount and unmount notifications. See "{ref}`The Node Monitor`"
section of this chapter for details.
