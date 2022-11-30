# Semaphores

A semaphore acts as a key that a thread must acquire in order to continue execution. Any thread that
can identify a particular semaphore can attempt to acquire it by passing its `sem_id` identifier---a
system-wide number that's assigned when the semaphore is created---to the {cpp:func}`acquire_sem()`
function. The function blocks until the semaphore is actually acquired.

:::{admonition} Note
:class: information

An alternate function, {cpp:func}`acquire_sem_etc()` lets you specify the amount of time you're
willing to wait for the semaphore to be acquired, and let you acquire the semaphore more than once
in a single go. Unless otherwise noted, characteristics ascribed to {cpp:func}`acquire_sem()` apply
to {cpp:func}`acquire_sem_etc()` as well.
:::

When a thread acquires a semaphore, that semaphore (typically) becomes unavailable for acquisition
by other threads. The semaphore remains unavailable until it's passed in a cell to the
{cpp:func}`release_sem()` function.

The code that a semaphore "protects" lies between the calls to {cpp:func}`acquire_sem()` and
{cpp:func}`release_sem()`. The disposition of these functions in your code usually follows this
pattern:

:::{code} cpp
if (acquire_sem(my_semaphore) == B_NO_ERROR)
{
	/* Protected code goes here. */
	release_sem(my_semaphore);
}
:::

Keep in mind that...

- The calls to the acquire and release functions needn't be locally balanced (although this is by
  far the most common use.) A semaphore can be acquired within one function and released in another.
  Acquisition and release of the same semaphore can even be performed by two different threads.

- Checking the value returned by {cpp:func}`acquire_sem()` is extremely important. If an
  acquire-blocked thread is unblocked by a signal (a return of {cpp:enum}`B_INTERRUPTED`), the
  thread shouldn't procede to the critical section.

## The Thread Queue

Every semaphore has its own thread queue: This is a list that identifies the threads that are
waiting to acquire the semaphore. A thread that attempts to acquire an unavailable semaphore is
placed at the tail of the semaphore's thread queue, where it sits blocked in the
{cpp:func}`acquire_sem()` call. Each call to {cpp:func}`release_sem()` unblocks the thread at the
head of that semaphore's queue, thus allowing the thread to return from its call to
{cpp:func}`acquire_sem()`.

Semaphores don't discriminate between acquisitive threads---they don't prioritize or otherwise
reorder the threads in their queues---the oldest waiting thread is always the next to acquire the
semaphore.

## The Thread Count

To assess availability, a semaphore looks at its thread count. This is a counting variable that's
initialized when the semaphore is created. Ostensibly, a thread count's initial value (which is
passed as the first argument to {cpp:func}`create_sem()`) is the number of threads that can acquire
the semaphore at a time. (As we'll see later, this isn't the entire story, but it's good enough for
now.) For example, a semaphore that's used as a mutually exclusive lock takes an initial thread
count of 1---in other words, only one thread can acquire the semaphore at a time.

:::{admonition} Note
:class: information

An initial thread count of 1 is by far the most common use; a thread count of 0 is also useful.
Other counts are much less common.
:::

Calls to {cpp:func}`acquire_sem()` and {cpp:func}`release_sem()` alter the semaphore's thread
acount: {cpp:func}`acquire_sem()` decrements the count, and {cpp:func}`release_sem()` increments it.
When you call {cpp:func}`acquire_sem()`, the function looks at the thread count (before decrementing
it) to determine if the semaphore is available:

- If the count is greater than zero, the semaphore is available for acquisition, so the function
  returns immediately.

- If the count is zero or less, the semaphore is unavailable, and the thread is placed in the
  semaphore's thread queue.

The initial thread count isn't an inviolable limit on the number of threads that can acquire a given
semaphore---it's simply the initial value for the semaphore's thread count variable. For example, if
you create a semaphore with an initial thread count of 1 and then immediately call
{cpp:func}`release_sem()` five times, the semaphore's thread count will increase to 6. Furthermore,
although you can't initialize the thread count to less-than-zero, an initial value of zero itself is
common---it's an integral part os using semaphores to impose an execution order (as demonstrated
later).

Summarizing the description above, there are three significant thread count value ranges:

- A positive thread count (_n_) means that there are no threads in the semaphore's queue, and the
  next _n_ {cpp:func}`acquire_sem()` calls will return without blocking.

- If the count is 0, there are no queued threads, but the next {cpp:func}`acquire_sem()` call will
  block.

- A negative count (_-n_) means there are _n_ threads in the semaphore's thread queue, and the next
  call to {cpp:func}`acquire_sem()` will block.

Although it's possible to retrieve the value of a semaphore's thread count (by looking at a field in
the semaphore's `sem_info` structure, as described later), you should only do so for
amusement---while you're debugging, for example.

:::{admonition} Warning
:class: warning

You should never predicate your code on the basis of a semaphore's thread count.
:::

## Deleting a Semaphore

Every semaphore is owned by a team (the team of the thread that called {cpp:func}`create_sem()`).
WHen the last thread in a team dies, it takes the team's semaphores with it.

Prior to the death of a team, you can explicitly delete a semaphore through the
{cpp:func}`delete_sem()` call. Note, however, that {cpp:func}`delete_sem()` must be called from a
thread that's a member of the team that owns the semaphore---you can't delete another team's
semaphores.

You're allowed to delete a semaphore even if it still has threads in its queue. However, you usually
want to avoid this, so deleting a semaphore may require some thought: When you delete a semaphore
(or when it dies naturally), all its queued threads are immediately allowed to continue---they all
return from {cpp:func}`acquire_sem()` at once. You can distinguish between a "normal" acquisition
and a "semaphore deleted" acquisition by the value that's returned by {cpp:func}`acquire_sem()` (the
specific return values are listed in the function descriptions).

## Inter-application Semaphores

The `sem_id` number that identifies a semaphore is a system-wide token---the `sem_id` values that
you create in your application will identify your semaphores in all other applications as well. It's
possible, therefore, to broadcast the `sem_id` numbers of the semaphores that you create and so
allow other applications to acquire and release them---but it's not a very good idea.

:::{admonition} Warning
:class: warning

A semaphore is best controlled if it's created, acquired, released, and deleted within the same
team.
:::

If you want to provide a protected service or resource to other applications, you should accept
messages from other applications and then spawn threads that acquire and release the appropriate
semaphores.

## Semaphore Examples

The following sections provides examples of typical semaphore use.

### Semaphore Example 1: Locking

The most typical use of a semaphore is to protect a chunk of code that can only be executed by one
thread at a time. The semaphore acts a s a lock; {cpp:func}`acquire_sem()` locks the code,
{cpp:func}`release_sem()` releases it. Semaphores that are used as locks are (almost always) created
with a thread tcount of 1.

As a simple example, let's say you keep track of a maximum value like this:

:::{code} cpp

/* max_val is a global. */
uint32 max_val = 0;
...

/* bump_max() resets the max value, if necessary. */
void bump_max(uint32 new_value)
{
   if (new_value > max_value)
      max_value = new_value;
}
:::

`bump_max()` isn't thread safe; there's a race condition between the comparison and the assignment.
So we protect it with a semaphore:

:::{code} cpp

sem_id max_sem;
uint32 max_val = 0;

...
/* Initialize the semaphore during a setup routine. */
status_t init()
{
   if ((max_sem = create_sem(1, "max_sem")) < B_NO_ERROR)
      return B_ERROR;
   ...
}
void bump_max(uint32 new_value)
{
   if (acquire_sem(max_sem) != B_NO_ERROR)
      return;
   if (new_value > max_value)
      max_value = new_value;
   release_sem();
}
:::

### Semaphore Example 2: Benaphores

A "benaphore" is a combination of an atomic variable and a semaphore that can improve locking
efficiency. If you're using a semaphore as shown in the previous example, you should consider using
a benaphore instead (if you can).

Here's the example re-written to use a benaphore:

:::{code} cpp

sem_id max_sem;
uint32 max_val = 0;
int32 ben_val = 0;

status_t init()
{
   /* This time we initialized the semaphore to 0. */
   if ((max_sem = create_sem(0, "max_sem")) < B_NO_ERROR)
      return B_ERROR;
   ...
}
void bump_max(uint32 new_value)
{
   int32 previous = atomic_add(&ben_val, 1);
   if (previous >= 1)
      if (acquire_sem(max_sem) != B_NO_ERROR)
         goto get_out;

   if (new_value > max_value)
      max_value = new_value;

get_out:
   previous = atomic_add(&ben_val, -1);
   if (previous > 1)
      release_sem(max_sem);
}
:::

The point, here, is that {cpp:func}`acquire_sem()` is called only if it's known (by checking the
previous value of `ben_val`) that some other thread is in the middle of the critical section. On the
releasing end, the {cpp:func}`release_sem()` is called only if some other thread has since entered
the function (and is now blocked in the {cpp:func}`acquire_sem()` call). An important point, here,
is that the semaphore is initialized to 0.

### Semaphore Example 3: Imposing an Execution Order

Semaphores can also be used to coordinate threads that are performing separate operations, but that
need to perform these operations in a particular order. In the following example, we have a global
buffer that's accessed through separate reading and writing functions. Furthermore, we want writes
and reads to alternate, with a write going first.

We can lock the entire buffer with a single semaphore, but to enforce alternation we need two
semaphores:

:::{code} cpp

sem_id write_sem, read_sem;
char buffer[1024];

/* Initialize the semaphores */
status_t init()
{
   if ((write_sem = create_sem(1, "write")) < B_NO_ERROR) {
      return;
   if ((read_sem = create_sem(0, "read")) < B_NO_ERROR) {
      delete_sem(write_sem);
      return;
   }
}

status_t write_buffer(const char *src)
{
   if (acquire_sem(write_sem) != B_NO_ERROR)
      return B_ERROR;

   strncpy(buffer, src, 1024);

   release_sem(read_sem);
}

status_t read_buffer(char *dest, size_t len)
{
   if (acquire_sem(read_sem) != B_NO_ERROR)
      return B_ERROR;

   strncpy(dest, buffer, len);

   release_sem(write_sem);
}
:::

The initial thread counts ensure that the buffer will be written to before it's read: If a reader
arrives before a writer, the reader will block until the writer releases the `read_sem` semaphore.
