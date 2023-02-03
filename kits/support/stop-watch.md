# BStopWatch

## Constructor and Desctructor

::::{abi-group}
:::{cpp:function} BStopWatch::BStopWatch(const char* name, bool silent = false)
:::

Creates a {hclass}`BStopWatch` object, names it, and starts its timer. If {hparam}`silent` is
{cpp:expr}`false` (the default), the object will print its elapsed time when it's destroyed;
otherwise the message isn't printed. To get the elapsed time from a silent {hclass}`BStopWatch`,
call {cpp:func}`~BStopWatch::ElapsedTime()`.
::::

::::{abi-group}
:::{cpp:function} BStopWatch::~BStopWatch()
:::

Stops the object's timer, prints a timing message to standard out (unless it's running silently),
and then destroys the object. By default the timing messages looks like this:

:::{code}
StopWatch "name": f usecs.
:::

If you've recorded some lap points (through the {cpp:func}`~BStopWatch::Lap()` function), you'll
also see the lap times as well:

:::{code}
StopWatch "name": f usecs.
[Lap#: soFar#thisLap] [Lap#: soFar#thisLap] [Lap#: soFar#this]...
:::

... where _Lap#_ is the number of the lap, _soFar_ was the total elapsed time at that lap, and
_thisLap_ was the time it took to complete the lap.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} bigtime_t BStopWatch::ElapsedTime() const
:::

Returns the elapsed time, in microseconds, since the object was created or last {hmethod}`Reset()`.
This function doesn't print the time message, nor does it touch the timer (the timer keeps
running---unless it's {cpp:func}`~BStopWatch::Suspend()`ed).

:::{code}
BStopWatch watch("Timer 0");
// ...
printf("Elapsed time: %Ld\n", watch.ElapsedTime());
:::
::::

::::{abi-group}
:::{cpp:function} bigtime_t BStopWatch::Lap()
:::

Records a "lap point" and returns the total elapsed time so far. The lap point times are printed
individually when the object is destroyed, provided the object isn't silent. You can record as many
as eight lap points; if you ask for a ninth lap point, the lap isn't recorded and this function
returns 0. See {cpp:func}`~BStopWatch::~BStopWatch()` for a description of what the lap points look
like when they're printed.
::::

::::{abi-group}
:::{cpp:function} const char* BStopWatch::Name() const
:::

Returns the name of the object, as set in the constructor.
::::

::::{abi-group}
:::{cpp:function} void BStopWatch::Suspend()
:::
:::{cpp:function} void BStopWatch::Resume()
:::
:::{cpp:function} void BStopWatch::Reset()
:::

These functions affect the object's timer:

- {hmethod}`Suspend()` stops the timer but doesn't reset it.
- {hmethod}`Resume()` starts the timer running again.
- {hmethod}`Reset()` sets the elapsed time to 0, but doesn't stop the timer. You can call
  {hmethod}`Reset()` at any time, regardless of whether the object is running or suspended.
::::
