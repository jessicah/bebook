:::{cpp:class} BMessageFilter
:::

# BMessageFilter

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BMessageFilter::BMessageFilter(message_delivery delivery, message_source source, uint32 command, filter_hook filter = NULL)
:::

:::{cpp:function} BMessageFilter::BMessageFilter(message_delivery delivery, message_source source, filter_hook filter = NULL)
:::

:::{cpp:function} BMessageFilter::BMessageFilter(uint32 command, filter_hook filter = NULL)
:::

:::{cpp:function} BMessageFilter::BMessageFilter(const BMessageFilter& object)
:::

:::{cpp:function} BMessageFilter::BMessageFilter(const BMessageFilter* object)
:::

Creates and returns a new {hclass}`BMessageFilter`. The first three
arguments define the types of messages that the object wants to see:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Parameter

	- Description

-
	- delivery
	- Specifies how the message must arrive: drag-and-drop
		({cpp:enumerator}`B_DROPPED_DELIVERY`), programmatically
		({cpp:enumerator}`B_PROGRAMMED_DELIVERY`), or either
		({cpp:enumerator}`B_ANY_DELIVERY`). The default is
		{cpp:enumerator}`B_ANY_DELIVERY`.
-
	- source
	- Specifes whether the sender of the message must be local vis-a-vis this
		app ({cpp:enumerator}`B_LOCAL_SOURCE`), remote
		({cpp:enumerator}`B_REMOTE_SOURCE`), or either
		({cpp:enumerator}`B_ANY_SOURCE`). The default is
		{cpp:enumerator}`B_ANY_SOURCE`.
-
	- command
	- Is a command constant. If supplied, the {hparam}`what` value of the
		incoming message must match this value.

:::

Messages that don't fit the definition won't be sent to the object's
filter function.

The {hparam}`filter` argument is a pointer to a {cpp:func}`filter_hook
<filter::hook>` function. This is the function that's invoked when a
message needs to be examined (see {cpp:func}`filter_hook <filter::hook>`
for the protocol). You don't have to supply a {cpp:func}`filter_hook
<filter::hook>` function; instead, you can implement
{hclass}`BMessageFilter`'s {cpp:func}`Filter() <BMessageFilter::Filter>`
function in a subclass.

For more information, refer to the description of the member
{cpp:func}`Filter() <BMessageFilter::Filter>` function.
::::

::::{abi-group}
:::{cpp:function} virtual BMessageFilter::~BMessageFilter()()
:::

Does nothing.
::::

## Hook Functions

::::{abi-group}
:::{cpp:function} virtual filter_result BMessageFilter::Filter(BMessage* message, BHandler** target)
:::

Implemented by derived classes to examine an arriving message just before
it's dispatched. The first two arguments are the {hparam}`message` that's
being considered, and the proposed {cpp:class}`BHandler` {hparam}`target`.
You can alter the contents of the message, and alter or even replace the
handler. If you replace the handler, the new handler must belong to the
same looper as the original. The new handler is given an opportunity to
filter the message before it's dispatched.

The return value must be one of these two values:

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
	- {cpp:enumerator}`B_DISPATCH_MESSAGE`.
	- The {hparam}`message` and {hparam}`handler` are passed (by the caller) to
		the looper's {cpp:func}`DispatchMessage() <BLooper::DispatchMessage>`
		function.
-
	- {cpp:enumerator}`B_SKIP_MESSAGE`.
	- The message goes no further—it's immediately thrown away by the caller.

:::

The default version of this function returns
{cpp:enumerator}`B_DISPATCH_MESSAGE`.

It's possible to call your {hmethod}`Filter()` function yourself (i.e.
outside the message-passing mechanism), but keep in mind that it's the
caller's responsibility to interpret the return value.

Rather than implement the  function, you can supply the
{hclass}`BMessageFilter` with a {cpp:func}`filter_hook <filter::hook>`
callback when you construct the object. If you do both, the
{cpp:func}`filter_hook <filter::hook>` (and not {hmethod}`Filter()`) will
be invoked when the object is asked to examine a message.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} uint32 BMessageFilter::Command() const
:::

:::{cpp:function} bool BMessageFilter::FiltersAnyCommand() const
:::

{hmethod}`Command()` returns the command constant (the
{cpp:class}`BMessage` {hparam}`what` value) that an arriving message must
match for the filter to apply. {hmethod}`FiltersAnyCommand()` returns
{cpp:expr}`true` if the filter applies to all messages, and
{cpp:expr}`false` if it's limited to a specific command.

Because all command constants are valid, including negative numbers and 0,
{hmethod}`Command()` returns a reliable result only if
{hmethod}`FiltersAnyCommand()` returns {cpp:expr}`false`.
::::

::::{abi-group}
:::{cpp:function} BLooper* BMessageFilter::Looper() const
:::

Returns the {cpp:class}`BLooper` whose messages this object filters, or
{cpp:expr}`NULL` if the {hclass}`BMessageFilter` hasn't yet been assigned
to a {cpp:class}`BHandler` or {cpp:class}`BLooper`. To attach a
{hclass}`BMessageFilter` to a looper or handler, use
{cpp:func}`BLooper::AddCommonFilter` or {cpp:func}`BHandler::AddFilter`.
::::

::::{abi-group}
:::{cpp:function} message_delivery BMessageFilter::MessageDelivery() const
:::

:::{cpp:function} message_source BMessageFilter::MessageSource() const
:::

These functions return constants, set when the {hclass}`BMessageFilter`
object was constructed, that describe the categories of messages that can
be filtered. {hmethod}`MessageDelivery()` returns a constant that specifies
how the message must be delivered ({cpp:enumerator}`B_DROPPED_DELIVERY`,
{cpp:enumerator}`B_PROGRAMMED_DELIVERY`, or
{cpp:enumerator}`B_ANY_DELIVERY`). {hmethod}`MessageSource()` returns how
the source of the message is constrained ({cpp:enumerator}`B_LOCAL_SOURCE`,
{cpp:enumerator}`B_REMOTE_SOURCE`, or {cpp:enumerator}`B_ANY_SOURCE`).
::::

## Operators

::::{abi-group}
:::{cpp:function} BMessageFilter BMessageFilter::operator=(const BMessageFilter& from)
:::

Copies the filtering criteria and filter_hook pointer (if any) from the
right-side object into the left-side object.
::::

## Defined Types

::::{abi-group}
:::{cpp:function} filter_result (*filter_hook)(BMessage* message, BHandler** target, BMessageFilter* messageFilter)
:::

:::{code} cpp
typedef enum filter_result {
    B_SKIP_MESSAGE,
    B_DISPATCH_MESSAGE
}
:::

filter_hook defines the protocol for message-filtering functions. The
first two arguments are the {hparam}`message` that's being considered, and
the proposed {cpp:class}`BHandler` target. You can alter the contents of
the message, and alter or even replace the handler. If you replace the
handler, the new handler must belong to the same looper as the original.
The new handler is given an opportunity to filter the message before it's
dispatched.

{hparam}`messageFilter` is a pointer to the object on whose behalf this
function is being called; you mustn't delete this object. More than one
{hclass}`BMessageFilter` can use the same filter_hook function.

The return value of type {htype}`filter_result` must be one of these two
values:

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
	- {cpp:enumerator}`B_DISPATCH_MESSAGE`.
	- The {hparam}`message` and {hparam}`handler` are passed (by the caller) to
		the looper's {cpp:func}`DispatchMessage() <BLooper::DispatchMessage>`
		function.
-
	- {cpp:enumerator}`B_SKIP_MESSAGE`.
	- The message goes no further–it's immediately thrown away by the caller.

:::

It's possible to call your filter function yourself (i.e. outside the
message-passing mechanism), but keep in mind that it's the caller's
responsibility to interpret the return value.

You supply a {hclass}`BMessageFilter` with a filter_hook function when you
constuct the object. Alternatively, you can subclass
{hclass}`BMessageFilter` and provide an implementation of
{cpp:func}`Filter() <BMessageFilter::Filter>`. If you do both, the
filter_hook (and not {cpp:func}`Filter() <BMessageFilter::Filter>`) will be
invoked when the object is asked to examine a message.
::::

### message_delivery

:::{code} cpp
typedef enum message_delivery {
    B_ANY_DELIVERY,
    B_DROPPED_DELIVERY,
    B_PROGRAMMED_DELIVERY
}
:::

This type enumerates the delivery criteria for filtering a message.

See also: The {hclass}`BMessageFilter` {cpp:func}`constructor
<BMessageFilter::BMessageFilter()>`

### message_source

:::{code} cpp
typedef enum message_source {
    B_ANY_SOURCE,
    B_REMOTE_SOURCE,
    B_LOCAL_SOURCE
}
:::

This type enumerates the source criteria for filtering a message.

See also: The {hclass}`BMessageFilter` {cpp:func}`constructor
<BMessageFilter::BMessageFilter()>`
