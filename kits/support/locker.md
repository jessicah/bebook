# BLocker

## Constructor and Destructor

::::{abi-group}

:::{cpp:function} BLocker::BLocker()
:::
:::{cpp:function} BLocker::BLocker(const char* name)
:::
:::{cpp:function} BLocker::BLocker(bool benaphore_style)
:::
:::{cpp:function} BLocker::BLocker(const char* name, bool benaphore_style)
:::

Sets up the object, creating a semaphore to implement the locking mechanism. The optional {hparam}`name` is for diagnostics and debugging.

By default, a {hclass}`BLocker` is implemented as a benaphore---a hybrid integer mutex and semaphore. This allows for faster performance when there is little contention for the lock. If you'd rather use a pure semaphore for locking, then pass {cpp:expr}`false` as the {hparam}`benaphore_style` argument.
::::

::::{abi-group}

:::{cpp:function} BLocker::~BLocker()
:::

Destroys the lock, deleting the controlling semaphore. If there are any threads blocked waiting to lock the object, they're immediately unblocked.
::::

## Member Functions

::::{abi-group}

:::{cpp:function} bool BLocker::Lock()
:::
:::{cpp:function} status_t BLocker::LockWithTimeout(bigtime_t timeout)
:::
:::{cpp:function} void BLocker::Unlock()
:::

{hmethod}`Lock()` tries to lock the {hclass}`BLocker`. The function returns a) when the lock is acquired (return = {cpp:expr}`true`), or b) immediately if the {hclass}`BLocker`s semaphore is deleted, most commonly as a result of deleting the object (return = {cpp:expr}`false`). A thread can nest {hmethod}`Lock()` calls, but each call must be balanced by a concomitant {hmethod}`Unlock()`.

{hmethod}`LockWithTimeout()` lets you declare a time limit, specified in microseconds. If {hmethod}`LockWithTimeout()` can't acquire the lock before the time limit expires, it returns {cpp:enum}`B_TIMED_OUT`. If the timeout is 0, this function immediately returns {cpp:enum}`B_OK` (if it locked the {hclass}`BLocker`) or {cpp:enum}`B_ERROR` (if it failed to obtain the lock). If the timeout is {cpp:enum}`B_INFINITE_TIMEOUT`, it blocks without limit, just as {hmethod}`Lock()` does. Note that if {hmethod}`Lock()` returns 0 ({cpp:expr}`false`), it has failed to lock the {hclass}`BLocker`, but if {hmethod}`LockWithTimeout()` returns 0 ({cpp:enum}`B_OK`), it has succeeded.

{hmethod}`Unlock()` releases one level of nested locks and returns immediately. If there are threads blocked waiting for the lock when the lock is released, the thread that's been waiting the longest acquires the lock.

Any thread can call {hmethod}`Unlock()` on any {hclass}`BLocker`---the thread needn't be the lock's current holder. Call {hmethod}`IsLocked()` before calling {hmethod}`Unlock()` if you want to make sure you own a lock before you unlock it.
::::

::::{abi-group}

:::{cpp:function} thread_id BLocker::LockingThread() const
:::
:::{cpp:function} bool BLocker::IsLocked() const
:::
:::{cpp:function} int32 BLocker::CountLocks() const
:::
:::{cpp:function} int32 BLocker::CountLockRequests() const
:::
:::{cpp:function} sem_id BLocker::Sem() const
:::

These functions provide information that may be useful for debugging purposes.

{hmethod}`LockingThread()` returns the thread that currently has the {hclass}`BLocker` locked, or {cpp:enum}`B_ERROR` if the {hclass}`BLocker` isn't locked.

{hmethod}`IsLocked()` returns {cpp:expr}`true` if the calling thread currently has the {hclass}`BLocker` locked (if it's the locking thread) and {cpp:expr}`false` if not (if some other thread is the locking thread of the {hclass}`BLocker` isn't locked).

{hmethod}`CountLocks()` returns the number of times the locking thread has locked the {hclass}`BLocker`---the number of {hmethod}`Lock()` (or {hmethod}`LockWithTimeout()`) calls that have not yet been balanced by matching {hmethod}`Unlock()` calls.

{hmethod}`CountLockRequests()` returns the number of threads currently trying to lock the {hclass}`BLocker`. The count includes the thread that currently holds the lock plus all threads currently waiting to acquire it.

{hmethod}`Sem()` returns the sem_id for the semaphore that the {hclass}`BLocker` uses to implement the locking mechanism.
::::
