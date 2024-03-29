# BInputDevice

A {cpp:class}`BInputDevice` object is a "downstream" representation of an
Input Server device, such as a mouse or a keyboard, within a "regular"
application. The {cpp:class}`BInputDevice` can
{cpp:func}`~BInputDevice::Start()` and {cpp:func}`~BInputDevice::Stop()`
the device it represents, and can send it input device control messages
through its {cpp:func}`~BInputDevice::Control()` function.

You never create {cpp:class}`BInputDevice` objects yourself; instead, you
ask the system to return one or more instances to you through the
{cpp:func}`find_input_device()` or {cpp:func}`get_input_devices()`
functions. Alternatively, you can work without an object by invoking the
static versions of {cpp:func}`~BInputDevice::Start()`,
{cpp:func}`~BInputDevice::Stop()`, and
{cpp:func}`~BInputDevice::Control()`. Note, however, that the static
functions control all devices of a given type, whereas a
{cpp:class}`BInputDevice` instance can talk to a specific device.

{cpp:class}`BInputDevice` objects don't live in the Input Server—they're
used in "normal" applications as a means to control an Input Server device
add-on.

The {cpp:class}`BInputDevice` object is provided, primarily, to let an
application talk to a custom input device.

You never subclass {cpp:class}`BInputDevice`.
