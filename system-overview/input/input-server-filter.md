# BInputServerFilter

{cpp:class}`BInputServerFilter` is a base class for input filters; these
are instances of {cpp:class}`BInputServerFilter` that modify, generate, or
eat input events. An input filter add-on is privy to all the events that
pass through the Input Server's event stream. A filter is similar to the
Interface Kit's {cpp:class}`BMessageFilter`, but at a much lower level. The
{cpp:class}`BInputServerFilter` also sees all events, while a
{cpp:class}`BMessageFilter` only sees the events targeted at its
{cpp:class}`BLooper`. {cpp:class}`BMessageFilter`s can also generate
additional events in place of, or in addition to, the original input event.

{cpp:class}`BInputServerFilter` objects are created and deleted by the
Input Server only—you never create or delete these objects in your code.

## Creating

To create a new input filter, you must:

- create a subclass of {cpp:class}`BInputServerFilter`

- implement the {cpp:func}`~instantiate::input` C function to create an
instance of your {cpp:class}`BInputServerFilter` subclass

- compile the class and function as an add-on

- install the add-on in one of the input filter directories

At boot time (or whenever the Input Server is restarted; see
"{cpp:func}`~TheInputServer::Introduction`" in The Input Server), the Input
Server loads the add-ons it finds in the input filter directories. For each
add-on it finds, the Server invokes {cpp:func}`~instantiate::input` to get
a pointer to the add-ons's {cpp:class}`BInputServerFilter` object. After
constructing the object, the Server calls
{cpp:func}`~BInputServerFilter::InitCheck` to give the add-on a chance to
bail out if the constructor failed.

## Installing an Input Filter

The input server looks for input filters in the input_server/filters
subdirectories of {cpp:enum}`B_BEOS_ADDONS_DIRECTORY`,
{cpp:enum}`B_COMMON_ADDONS_DIRECTORY`, and
{cpp:enum}`B_USER_ADDONS_DIRECTORY`.

- You can install your input devices in the latter two directories—i.e.
those under {cpp:enum}`B_COMMON_ADDONS_DIRECTORY`, and
{cpp:enum}`B_USER_ADDONS_DIRECTORY`.

- The {cpp:enum}`B_BEOS_ADDONS_DIRECTORY` is reserved for add-ons that are
supplied with BeOS.
