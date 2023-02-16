:::{cpp:class} BTimedEventQueue
:::

# BTimedEventQueue

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BTimedEventQueue::BTimedEventQueue()
:::

Initializes a new, empty, timed event queue.
::::

::::{abi-group}
:::{cpp:function} virtual BTimedEventQueue::~BTimedEventQueue()
:::

Flushes the queue and deallocates memory allocated by the object.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} status_t BTimedEventQueue::AddEvent(const media_timed_event& event)
:::

Adds the specified event to the queue.

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
	- {cpp:enumerator}`B_OK`
	- The event was added.
-
	- {cpp:enumerator}`B_BAD_VALUE`
	- Unknown or invalid event type (you can't use {cpp:enumerator}`B_NO_EVENT`
		or {cpp:enumerator}`B_ANY_EVENT`).
-
	- {cpp:enumerator}`B_NO_INIT`
	- The queue hasn't been initialized.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BTimedEventQueue::DoForEach(for_each_hook hook, void* context, bigtime_t time, time_direction direction, bool inclusive = true, int32 event = B_ANY_EVENT)
:::

For each event in the queue matching the specified parameters, the hook
function is called. The {hparam}`context` pointer is passed through to the
hook function, and may point to anything your hook function requires.

-   Setting {hparam}`direction` to {cpp:enumerator}`B_ALWAYS` indicates that
all events of the type indicated by {hparam}`event` should be processed.
The {hparam}`time` and {hparam}`inclusive` arguments are ignored.

-   Setting {hparam}`direction` to {cpp:enumerator}`B_BEFORE_TIME` indicates
that all matching events occurring before the specified {hparam}`time`
should be processed. If {hparam}`inclusive` is {cpp:expr}`true`, events
occurring at {hparam}`time` are also processed.

-   Setting {hparam}`direction` to {cpp:enumerator}`B_AT_TIME` processes all
matching events scheduled at the specified {hparam}`time`. The
{hparam}`inclusive` argument is ignored.

-   If {hparam}`direction` is {cpp:enumerator}`B_AFTER_TIME`, all matching
events scheduled to occur after the specified {hparam}`time` are processed.
If {hparam}`inclusive` is {cpp:expr}`true`, events scheduled to occur at
{hparam}`time` are also processed.

This provides a means for you to scan through the queue and perform a
particular act on every node (or all nodes of a certain type, or that occur
at certain times). If you want to process all events, you can specify a
{hparam}`time` of {cpp:enumerator}`B_INFINITE_TIMEOUT` and a
{hparam}`direction` of {cpp:enumerator}`B_BEFORE_TIME`.

The hook function should return a {ref}`queue_action` value.

:::{code} cpp
queue_action MyHook(media_timed_event* event, void* context) {
   if (event->data == 0) {
      /* countdown finished, do something */
      return BTimedEventQueue::B_REMOVE_EVENT;
   }
   event->data--;
   return BTimedEventQueue::B_NO_ACTION;
}
:::

In this example, the hook function processes the event (and indicates on
return that it should be removed from the queue) if the {hparam}`data`
field of the event structure is zero; otherwise {hparam}`data` is
decremented and the event is left alone.

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
	- {cpp:enumerator}`B_OK`
	- The events were processed.
-
	- {cpp:enumerator}`B_ERROR`
	- An undefined error occurred.

:::
::::

::::{abi-group}
:::{cpp:function} int32 BTimedEventQueue::EventCount() const
:::

Returns the number of events in the queue.
::::

::::{abi-group}
:::{cpp:function} const media_timed_event* BTimedEventQueue::FindFirstMatch(bigtime_t eventTime, time_direction direction, bool inclusive = true, int32 event = B_ANY_EVENT)
:::

Searches the event queue for the first event matching the given
specifications. The search begins at the time specified by
{hparam}`eventTime`, and progresses in the specified {hparam}`direction`.

-   Setting {hparam}`direction` to {cpp:enumerator}`B_ALWAYS` indicates that
all events of the type indicated by {hparam}`event` should be scanned. The
{hparam}`eventTime` and {hparam}`inclusive` arguments are ignored.

-   Setting {hparam}`direction` to {cpp:enumerator}`B_BEFORE_TIME` indicates
that all matching events occurring before the specified {hparam}`eventTime`
should be scanned. If {hparam}`inclusive` is {cpp:expr}`true`, events
occurring at {hparam}`eventTime` are also scanned.

-   Setting {hparam}`direction` to {cpp:enumerator}`B_AT_TIME` scans all
matching events scheduled at the specified {hparam}`eventTime`. The
{hparam}`inclusive` argument is ignored.

-   If {hparam}`direction` is {cpp:enumerator}`B_AFTER_TIME`, all matching
events scheduled to occur after the specified {hparam}`eventTime` are
scanned. If {hparam}`inclusive` is {cpp:expr}`true`, events scheduled to
occur at {hparam}`eventTime` are also scanned.

If you want to scan all events, you can specify a time of
{cpp:enumerator}`B_INFINITE_TIMEOUT` and a direction of
{cpp:enumerator}`B_BEFORE_TIME`.

If no matching event is found, {cpp:expr}`NULL` is returned.
::::

::::{abi-group}
:::{cpp:function} const media_timed_event* BTimedEventQueue::FirstEvent() const
:::

:::{cpp:function} bigtime_t BTimedEventQueue::FirstEventTime() const
:::

{hmethod}`FirstEvent()` returns the first event in the queue, without
removing it from the queue.

{hmethod}`FirstEventTime()` returns the first event's time, in
microseconds.

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
	- {cpp:enumerator}`B_OK`
	- No error occurred.
-
	- {cpp:enumerator}`B_NO_INIT`
	- The queue hasn't been initialized.
-
	- {cpp:enumerator}`B_INFINITE_TIMEOUT`
	- The queue is empty ({hmethod}`FirstEventTime()` only).

:::
::::

::::{abi-group}
:::{cpp:function} status_t BTimedEventQueue::FlushEvents(bigtime_t time, time_direction direction, bool inclusive = true, int32 event = B_ANY_EVENT) const
:::

Flushes the specified events from the queue. You specify which events to
flush by indicating a {hparam}`time` from which events should be flushed, a
{hparam}`direction` in which to search for events to flush, and the type of
events to flush:

-   Setting {hparam}`direction` to {cpp:enumerator}`B_ALWAYS` indicates that
all events of the type indicated by {hparam}`event` should be flushed. The
{hparam}`eventTime` and {hparam}`inclusive` arguments are ignored.

-   Setting {hparam}`direction` to {cpp:enumerator}`B_BEFORE_TIME` indicates
that all matching events occurring before the specified {hparam}`eventTime`
should be flushed. If {hparam}`inclusive` is {cpp:expr}`true`, events
occurring at {hparam}`eventTime` are also flushed.

-   Setting {hparam}`direction` to {cpp:enumerator}`B_AT_TIME` flushes all
matching events scheduled at the specified {hparam}`eventTime`. The
{hparam}`inclusive` argument is ignored.

-   If {hparam}`direction` is {cpp:enumerator}`B_AFTER_TIME`, all matching
events scheduled to occur after the specified {hparam}`eventTime` are
flushed. If {hparam}`inclusive` is {cpp:expr}`true`, events scheduled to
occur at {hparam}`eventTime` are also flushed.

If you want to flush all events, you can specify a time of
{cpp:enumerator}`B_INFINITE_TIMEOUT` and a direction of
{cpp:enumerator}`B_BEFORE_TIME`.

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
	- {cpp:enumerator}`B_OK`
	- The events were flushed.
-
	- {cpp:enumerator}`B_ERROR`
	- An undefined error occurred.

:::
::::

::::{abi-group}
:::{cpp:function} bool BTimedEventQueue::HasEvents()
:::

Returns {cpp:expr}`true` if there are events in the queue, otherwise
returns {cpp:expr}`false`.
::::

::::{abi-group}
:::{cpp:function} const media_timed_event* BTimedEventQueue::LastEvent() const
:::

:::{cpp:function} bigtime_t BTimedEventQueue::LastEventTime() const
:::

{hmethod}`LastEvent()` returns the last event in the queue, without
removing it from the queue.

{hmethod}`LastEventTime()` returns the last event's time, in microseconds.

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
	- {cpp:enumerator}`B_OK`
	- No error occurred.
-
	- {cpp:enumerator}`B_NO_INIT`
	- The queue hasn't been initialized.
-
	- {cpp:enumerator}`B_INFINITE_TIMEOUT`
	- The queue is empty ({hmethod}`LastEventTime()` only).

:::
::::

::::{abi-group}
:::{cpp:function} status_t BTimedEventQueue::RemoveEvent(const media_timed_event* event)
:::

:::{cpp:function} status_t BTimedEventQueue::RemoveFirstEvent(const media_timed_event* event = NULL)
:::

{hmethod}`RemoveEvent()` removes the specified event from the queue.

{hmethod}`RemoveFirstEvent()` removes the first event from the queue. If
{hparam}`outEvent` isn't {hparam}`NULL`, the specified buffer is filled
with a copy of the event that's been removed.

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
	- {cpp:enumerator}`B_OK`
	- The event was removed.
-
	- {cpp:enumerator}`B_NO_INIT`
	- The queue hasn't been initialized.

:::
::::

::::{abi-group}
:::{cpp:function} void BTimedEventQueue::SetCleanupHook(cleanup_hook hook, void* context)
:::

Sets up the cleanup hook function specified by hook to be called for
events as they're removed from the queue. The hook will be called only for
events with {ref}`cleanup_flag` values of {cpp:enumerator}`B_DELETE` or
{cpp:enumerator}`B_USER_CLEANUP` or greater.
::::

## Constants

### cleanup_flag

Declared in: media/TimedEventQueue.h

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
	- {cpp:enumerator}`B_NO_CLEANUP`
	- Don't clean up when the event is removed from the queue.
-
	- {cpp:enumerator}`B_RECYCLE_BUFFER`
	- {hclass}`BTimedEventQueue` should recycle the buffer when the buffer event
		is removed from the queue.
-
	- {cpp:enumerator}`B_EXPIRE_TIMER`
	- Call {cpp:func}`TimerExpired() <BMediaNode::TimerExpired>` on the event's
		data field.
-
	- {cpp:enumerator}`B_USER_CLEANUP`
	- Base value for user-defined cleanup types.

:::

These values define how {hclass}`BTimedEventQueue` should handle removing
events from the queue. If the flag is {cpp:enumerator}`B_USER_CLEANUP` or
greater, the cleanup hook function is called when the event is removed.

### event_type

Declared in: media/TimedEventQueue.h

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
	- {cpp:enumerator}`B_NO_EVENT`
	- Don't push buffers of this type. It's a return value only.
-
	- {cpp:enumerator}`B_ANY_EVENT`
	- Don't push buffers of this type; it's used in searches only.
-
	- {cpp:enumerator}`B_START`
	- A start event.
-
	- {cpp:enumerator}`B_STOP`
	- A stop event.
-
	- {cpp:enumerator}`B_SEEK`
	- A seek event.
-
	- {cpp:enumerator}`B_WARP`
	- A warp event.
-
	- {cpp:enumerator}`B_TIMER`
	- A timer event.
-
	- {cpp:enumerator}`B_HANDLE_BUFFER`
	- Represents a buffer queued to be handled. The event's pointer is a pointer
		to a {cpp:class}`BBuffer` object.
-
	- {cpp:enumerator}`B_DATA_STATUS`
	- Represents a data status event.
-
	- {cpp:enumerator}`B_HARDWARE`
	- A hardware event.
-
	- {cpp:enumerator}`B_PARAMETER`
	- The buffer contains changes to parameter values; pass it to
		{cpp:func}`BControllable::ApplyParameterData`.
-
	- {cpp:enumerator}`B_USER_EVENT`
	- Base value for user-defined events.

:::

These values describe type types of events that a
{hclass}`BTimedEventQueue` can handle.

### queue_action

Declared in: media/TimedEventQueue.h

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
	- {cpp:enumerator}`B_DONE`
	- End the {cpp:func}`DoForEach() <BTimedEventQueue::DoForEach>` pass.
-
	- {cpp:enumerator}`B_NO_ACTION`
	- Do nothing for this event.
-
	- {cpp:enumerator}`B_REMOVE_EVENT`
	- Remove the event.
-
	- {cpp:enumerator}`B_RESORT_QUEUE`
	- Sort the queue again to ensure that events are still in the right order.

:::

These queue action values are returned by the hook function used by
{cpp:func}`DoForEach() <BTimedEventQueue::DoForEach>`; these values
indicate what {cpp:func}`DoForEach() <BTimedEventQueue::DoForEach>` should
do to the event after the hook has processed it.

### time_direction

Declared in: media/TimedEventQueue.h

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
	- {cpp:enumerator}`B_ALWAYS`
	- Matches events occurring at any time.
-
	- {cpp:enumerator}`B_BEFORE_TIME`
	- Matches events occurring before a specified time.
-
	- {cpp:enumerator}`B_AT_TIME`
	- Matches events occurring at a specified time.
-
	- {cpp:enumerator}`B_AFTER_TIME`
	- Matches events occurring after a specified time.

:::

These values are used to indicate a search direction through the time
continuum.

## Defined Types

### cleanup_hook

Declared in: media/TimedEventQueue.h

:::{code} c
typedef queue_action (*cleanup_hook)(media_timed_event* event,
                                     void* context);
:::

The {htype}`cleanup_hook` type is used to define a hook function called
while removing an event from the queue; it's set by calling
{cpp:func}`SetCleanupHook() <BTimedEventQueue::SetCleanupHook>`.

### for_each_hook

Declared in: media/TimedEventQueue.h

:::{code} c
typedef queue_action (*for_each_hook)(media_timed_event* event,
                                      void* context);
:::

The {htype}`for_each_hook` type is used to define a hook function called
by {cpp:func}`DoForEach() <BTimedEventQueue::DoForEach>`.

### media_timed_event

Declared in: media/TimedEventQueue.h

:::{code} cpp
struct media_timed_event {
   media_timed_event();
   media_timed_event(bigtime_t inTime, int32 inType);
   media_timed_event(bigtime_t inTime, int32 inType, void* inPointer,
            uint32 inCleanup);
   media_timed_event(bigtime_t inTime, int32 inType,
            void* inPointer, uint32 inCleanup,
            int32 inData, int64 inBigdata,
            char* inUserData, size_t dataSize = 0);

   media_timed_event(const media_timed_event& clone);
   void operator=(const media_timed_event& clone);

   ~media_timed_event();

   bigtime_t event_time;
   int32 type;
   void* pointer;
   uint32 cleanup;
   int32 data;
   int64 bigdata;
   char user_data[64];
   uint32 _reserved_media_timed_event_[8];
};
:::

Describes a media event:

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
	- event_time
	- Indicates the time at which the event is scheduled to occur.
-
	- type
	- Indicates the type of event, as an event_type.
-
	- pointer
	- Is a pointer to event-specific data owned by the event.
-
	- cleanup
	- Is the cleanup_flag value for the event.
-
	- data
	- Is an event-specific 32-bit value.
-
	- bigdata
	- Is an event-specific 64-bit value.
-
	- user_data
	- Is user-defined data.

:::
