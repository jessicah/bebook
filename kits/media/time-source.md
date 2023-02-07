# BTimeSource
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BTimeSource::BTimeSource()
:::
The standard {hclass}`BTimeSource` constructor. You should never directly
instantiate a {hclass}`BTimeSource`; instead, you should create a node class
derived from {hclass}`BTimeSource` (and possibly other
{cpp:class}`BMediaNode`-derived
classes as well) and use the
{cpp:class}`BMediaRoster`
to instantiate the node as desired.
::::

## Member Functions
::::{abi-group}

:::{cpp:function} void BTimeSource::BroadcastTimeWarp(bigtime_t atRealTime, bigtime_t newPerformanceTime)
:::
Whenever time jumps suddenly (for instance, when a seek operation
occurs), call this function to inform all slaved nodes that time has
jumped in a discontinuous manner. You should also call this function if
the time from which your time source derives its time jumps.
At the real time specified by {hparam}`atRealTime`, the performance time will
instantaneously jump to {hparam}`newPerformanceTime`.
::::

::::{abi-group}

:::{cpp:function} status_t BTimeSource::GetStartLatency(bigtime_t* outLatency)
:::
Returns in {hparam}`outLatency` the amount of time, in microseconds, needed for the
time source to start up, including the time needed to start up any slaved
nodes that are started.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- The latency value was returned successfully.
-
	- {cpp:enum}`B_NO_INIT`
	- The time source has not been initialized.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BTimeSource::GetTime(bigtime_t* performanceTime, bigtime_t* realTime, float* drift)
:::
Returns the most recently published time information for this time
source; this information specifies the performance time and real time of
the last published time stamp, as well as the {hparam}`drift` value, which can be
used to interpolate the true current performance time, given a more
accurate real time, as follows:
:::{code}
bigtime_t performanceTime;
bigtime_t realTime;
float drift;
while (GetTime(&performanceTime, &realTime, &drift) != B_OK);
performanceTime = performanceTime + (RealTime() - realTime) * drift;
:::
Note, however, that the resulting
{hparam}`performanceTime` is the same value you would have
gotten by calling {hmethod}`PerformanceTimeFor()`, which
you should use instead.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- The returned information is accurate.
-
	- Other values.
	- The returned information is unreliable.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BTimeSource::HandleMessage(int32 code, const void* message, size_t size)
:::
Given a {hparam}`message` received on the control
port, this function dispatches the message to the appropriate
{hclass}`BTimeSource` hook function. If the message
doesn't correspond to a hook function, an appropriate error be
returned.
If your node derives from {hclass}`BTimeSource`,
your implementation of {hmethod}`HandleMessage()` should
call all inherited forms of
{hmethod}`HandleMessage()`.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- The message was dispatched.
-
	- Other values.
	- The message couldn't be dispatched, possibly because it doesn't correspond to a hook function.
:::
::::

::::{abi-group}

:::{cpp:function} bool BTimeSource::IsRunning()
:::
Returns {cpp:enum}`true` if the
{hclass}`BTimeSource` is currently progressing through time or
{cpp:enum}`false` if it's stopped.
::::

::::{abi-group}

:::{cpp:function} bigtime_t BTimeSource::Now()
:::
:::{cpp:function} bigtime_t BTimeSource::PerformanceTimeFor(bigtime_t realTime)
:::
:::{cpp:function} bigtime_t BTimeSource::PerformanceTimeFor(bigtime_t performanceTime, bigtime_t withLatency)
:::
{hmethod}`Now()` returns an approximation
of what the current performance time is.
{hmethod}`PerformanceTimeFor()` returns
an estimate of the performance time
represented by the specified real time (as returned by
{cpp:func}`BTimeSource::RealTime`).
{hmethod}`RealTimeFor()`, given a
performance time, returns an approximation of the
corresponding real time, adjusted by the given latency.
::::

::::{abi-group}

:::{cpp:function} void BTimeSource::PublishTime(bigtime_t performanceTime, bigtime_t realTime, float drift)
:::
While your time source is running, you should repeatedly call this
function in order to constantly refresh the mapping between real time and
performance time. When your time source is stopped, you should call this
function once with values of zero for all three arguments.
The arguments have the following meanings:
:::{list-table}
---
header-rows: 1
---
-
	- Parameter
	- Description
-
	- performanceTime.
	- Is the precise current performance time.
-
	- realTime.
	- Is the current real time.
-
	- drift.
	- Indicates the value which indicates the rate at which the performance time changes compared to real time.
:::
The {hparam}`drift` value makes it possible to
interpolate intermediate values. For instance, if playback of a video
source is progressing at normal speed, the {hparam}`drift`
value would be 1.0, indicating that performance time and real time progress
at the same rate.
However, if the movie is playing at half-speed,
{hparam}`drift` would be 0.5, so that for every one unit of
real time that passes, only a half-unit of performance time would pass.
This information is used to compute times without having to query the time
source each time an update must occur.
The data furnished by this function (which you should try to call about
20 times a second, although variations in frequency are acceptable as
long as the drift value doesn't change much) may be the only information
the rest of the world sees from your node.
::::

::::{abi-group}

:::{cpp:function} static bigtime_t BTimeSource::RealTime()
:::
Returns the current absolute real time reference that all time sources
measure themselves against. This is the only call that you should rely
upon to obtain this value (don't use the Kernel Kit's
{cpp:func}`~system::time`
function).
As of this time, {hmethod}`RealTime()` and
{cpp:func}`~system::time`
do return the same value;
however, you shouldn't rely upon this relationship. When doing media
stuff, you should always use {hmethod}`RealTime()`.
::::

::::{abi-group}

:::{cpp:function} virtual void BTimeSource::Seek(bigtime_t performanceTime, bigtime_t atRealTime)
:::
Implement this function to handle a seek request. When a {hclass}`BTimeSource`'s
performance time is adjusted, it needs to broadcast the change to all
nodes slaved to it; call
{cpp:func}`~BTimeSource::BroadcastTimeWarp`
to do this.
Be sure to queue at least one seek request, so seek operations can be
requested in advance. The seek request should occur at the real time
specified by {hparam}`atRealTime`.
::::

::::{abi-group}

:::{cpp:function} void BTimeSource::SendRunMode(run_mode mode)
:::
This function transmits the specified mode to all the nodes slaved
to this node, so they know that their time source's run mode has changed.
This function is called by
{cpp:func}`~BTimeSource::SetRunMode`;
it may or may not make sense to call it elsewhere, depending on your
{hclass}`BTimeSource` implementation.
::::

::::{abi-group}

:::{cpp:function} virtual void BTimeSource::SetRunMode(run_mode mode)
:::
This hook function is called when someone requests that your node's run
mode be changed. Be sure to call through to either
{cpp:func}`BMediaNode::SetRunMode` or
{hmethod}`BTimeSource::SetRunMode()`.
::::

::::{abi-group}

:::{cpp:function} virtual void BTimeSource::SnoozeUntil(bigtime_t performanceTime, bigtime_t withLatency = 0, bool retrySignals = false)
:::
Waits until the specified {hparam}`performanceTime` (specified in performance time)
arrives in real time. If {hparam}`withLatency` is non-zero, {hmethod}`SnoozeUntil()` waits
until {hparam}`withLatency` microseconds (in real time) prior to the specified
performance time; this lets you have time for setup prior to starting
some operation.
:::{admonition} Note
:class: note
Because {hparam}`performanceTime` is specified in
performance time, and {hparam}`withLatency` is specified
in real time, you can't just subtract
{hparam}`withLatency` microseconds from
{hparam}`performanceTime` and snooze until that time,
because {hparam}`performanceTime` may be passing at a rate
faster than or slower than real time (if, for example, the time source is
running at double-speed).
:::
If {hparam}`retrySignals` is
{cpp:enum}`false` (as is the default),
{hmethod}`SnoozeUntil()` returns
{cpp:enum}`B_INTERRUPTED` if it's interrupted by a signal
before {hparam}`performanceTime`; if
{hparam}`retrySignals` is {cpp:enum}`true`,
the function will go right back to sleep and not return until the time has
actually arrived.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- No error; the snooze has completed without incident.
-
	- {cpp:enum}`B_MEDIA_TIME_SOURCE_STOPPED`
	- The time source is stopped; snoozing on a stopped time source is a bad thing.
:::
::::

::::{abi-group}

:::{cpp:function} virtual void BTimeSource::Start(bigtime_t realTime)
:::
This function is called when someone wants the
{hclass}`BTimeSource` to begin running; the
{hparam}`realTime` argument indicates the real time at
which the time source should start. Implement the function to queue the
request as necessary.
Be sure to queue at least one start request, so that start requests can
be filed in advance.
:::{admonition} Note
:class: note
A {hclass}`BTimeSource` measures start and stop
times in real time, not in performance time, because
{hclass}`BTimeSource`s are the objects used to perform the
mapping between real time and performance time.
:::
::::

::::{abi-group}

:::{cpp:function} virtual void BTimeSource::Stop(bigtime_t realTime)
:::
{hmethod}`Stop()` is called when someone wants
the {hclass}`BTimeSource` to stop; the
{hparam}`realTime` argument indicates the real time at
which the time source should stop running. Implement the function to queue
the request.
Be sure to queue at least one stop request, so stop requests can be
filed in advance.
:::{admonition} Note
:class: note
A {hclass}`BTimeSource` measures start and stop
times in real time, not in performance time, because
{hclass}`BTimeSource`s are the objects used to perform the
mapping between real time and performance time.
:::
::::

::::{abi-group}

:::{cpp:function} virtual status_t BTimeSource::TimeSourceOp(const time_source_op_info& op, void* _reserved = 0)
:::
This function is called by the
{cpp:func}`BMediaNode::Start`,
{cpp:func}`BMediaNode::Stop`, and
{cpp:func}`BMediaNode::Seek`
functions to perform the requested activities.
You must implement this function to handle these requests.
Return {cpp:enum}`B_OK` if the request was handled
successfully; otherwise, return an appropriate error code.
::::

## Constants
::::{abi-group}

:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_TIMESOURCE_START`
	- Start the time source.
-
	- {cpp:enum}`B_TIMESOURCE_STOP`
	- Stop the time source.
-
	- {cpp:enum}`B_TIMESOURCE_STOP_IMMEDIATELY`
	- Stop the time source immediately.
-
	- {cpp:enum}`B_TIMESOURCE_SEEK`
	- Seek the time source.
:::
These constants identify the various operations
{cpp:func}`~BTimeSource::TimeSourceOp`
will be called upon to handle.
::::

## Defined Types
::::{abi-group}


:::{code}
struct time_source_op_info {
   time_source_op op;
   int32 _reserved1;
   bigtime_t real_time;
   bigtime_t performance_time;
   int32 _reserved2[6];
};
:::
Describes a request to
{cpp:func}`~BTimeSource::TimeSourceOp`.
:::{list-table}
---
header-rows: 1
---
-
	- Field
	- Description
-
	- op
	- Indicates the operation to be performed.
-
	- real_time
	- Indicates the time at which the request is to be filled (this is the {hparam}`atRealTime` argument passed to the {cpp:class}`BMediaRoster` functions {cpp:func}`~BMediaRoster::SeekTimeSource`, {cpp:func}`~BMediaRoster::StopTimeSource`, or {cpp:func}`~BMediaRoster::StartTimeSource`).
-
	- performance_time
	- Is the {hparam}`newPerformanceTime` argument passed to {cpp:func}`~BMediaRoster::SeekTimeSource`.
:::
::::
