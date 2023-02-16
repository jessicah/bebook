# BMediaEventLooper

The {cpp:class}`BMediaEventLooper` class provides a control thread that
automatically queues received media events and calls the
{cpp:func}`HandleEvent() <BMediaEventLooper::HandleEvent>` function you
implement to process them as necessary. This takes a lot of the drudgery
out of writing nodes:

-   You don't have to write a service thread to receive and process incoming
messages; {cpp:class}`BMediaEventLooper` does this for you (much like a
{cpp:class}`BLooper`, hence the similarity in names).

-   You don't have to write code to queue up events until it's time to handle
them, since {cpp:class}`BMediaEventLooper` maintains a
{cpp:class}`BTimedEventQueue` for you. Just push events onto the queue as
you receive them and the {cpp:class}`BMediaEventLooper` pops them off for
you at the appropriate times and asks you to handle them.

-   If all your node needs to do is know when {cpp:func}`Start()
<BTimeSource::Start>`, {cpp:func}`Stop() <BTimeSource::Stop>`, and
{cpp:func}`Seek() <BTimeSource::Seek>` requests come due, your node doesn't
even have to override these functions—{cpp:class}`BMediaEventLooper`
automatically intercepts them and pushes them onto the queue for you.

-   The {cpp:class}`BTimedEventQueue` employed by
{cpp:class}`BMediaEventLooper` automatically provides support for queueing
multiple start, stop, and seek events.

{cpp:class}`BMediaEventLooper` maintains two queues: one for real-time
events, and one for normal events. Events in the real-time queue are
handled according to their real time, while events in the other queue are
handled based on their performance time. So the values of the time stamps
on events in these two queues are handled differently; keep this in mind if
you need to peek into the queues yourself.

## Implementing a Node (the Easy Way)

Although {cpp:class}`BMediaEventLooper` does take away a lot of the
complicated node construction work, there's still work to be done. There
are still plenty of hooks you have to implement yourself (which ones,
exactly, depend on whether you're a producer or a consumer).

You can study a specific example of how to implement a node using
{cpp:class}`BMediaEventLooper` by reading "{ref}`A BMediaEventLooper
Example`".
