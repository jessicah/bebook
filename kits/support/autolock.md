# BAutolock

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} inline BAutolock::BAutolock(BLooper* looper)
:::
:::{cpp:function} inline BAutolock::BAutolock(BLocker* locker)
:::
:::{cpp:function} inline BAutolock::BAutolock(BLocker& locker)
:::

Locks the target {hparameter}`looper` or {hparameter}`locker` object.
::::

::::{abi-group}
:::{cpp:function} inline BAutolock::~BAutolock()
:::

Unlocks the target {cpp:class}`BLooper` or {cpp:class}`BLocker`.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} inline bool IsLocked()
:::

Returns {cpp:enum}`true` if the target {cpp:class}`BLooper` or {cpp:class}`BLocker` is locked, and {cpp:enum}`false` if not.
::::
