# BTimedEventQueue

The {cpp:class}`BTimedEventQueue` class provides an easy way to queue a
sequence of events within your node. You can use it to queue up start,
stop, and seek requests, and to queue up incoming data buffers in
preparation for handling them. Each queue element is tagged with the time
at which the event should be processed, and functions are provided for
locating the next event that should be handled.

:::{admonition} Note
:class: note
Although you shouldn't need to subclass {cpp:class}`BTimedEventQueue`,
there's no reason you can't do it.
:::

## Cleaning Up After Nodes

Each event has a cleanup flag associated with it that indicates what sort
of special action needs to be performed when the event is removed from the
queue. If this value is {cpp:enumerator}`B_NO_CLEANUP`, nothing is done. If
it's {cpp:enumerator}`B_RECYCLE`, and the event is a
{cpp:enumerator}`B_HANDLE_BUFFER` event, {cpp:class}`BTimedEventQueue` will
automatically recycle the buffer associated with the event.

If the cleanup flag is {cpp:enumerator}`B_DELETE` or is
{cpp:enumerator}`B_USER_CLEANUP` or greater, the cleanup hook function will
be called. You can implement and establish a cleanup hook function to
handle deleting event data yourself. The hook function is of type
{htype}`cleanup_hook`:

:::{code}
typedef void (*cleanup_hook)(void *context, bigtime_t time, int32 what,
         void *pointer, uint32 pointerCleanup, int64 data);
:::

You specify the cleanup hook function by calling
{cpp:func}`SetCleanupHook() <BTimedEventQueue::SetCleanupHook>`, like this:

:::{code}
SetCleanupHook(MyCleanupFunction, contextPtr);
:::

The {hparam}`contextPtr` is a pointer that your cleanup hook function
uses, and can contain whatever data you require.
