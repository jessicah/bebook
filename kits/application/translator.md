# BTranslator

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} ~BTranslator::BTranslator()
:::

The constructor must create and return a new instance of your {hclass}`BTranslator` subclass. Note
that the constructor doesn't {hmethod}`Acquire()` the object it returns.
::::

::::{abi-group}
:::{cpp:function} BTranslator::~BTranslator()
:::

Note that the destructor is protected; you can only delete a {hclass}`BTranslator` object from
within the implementation of the subclass. From outside the class, you call {hmethod}`Release()`.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} BTranslator* BTranslator::Acquire()
:::
:::{cpp:function} BTranslator* BTranslator::Release()
:::
:::{cpp:function} int32 BTranslator::ReferenceCount()
:::

:::{admonition} Warning
:class: warning
{hmethod}`ReferenceCount()` is for debugging use only!
:::

{hmethod}`Acquire()` and {hmethod}`Release()` increment and decrement the object's reference count.
The count starts at 1 (i.e. the object is implicitly acquired when it's created); if the count falls
to 0, the object is deleted.

When you add a {hclass}`BTranslator` to a {cpp:class}`BTranslatorRoster`, the
{hclass}`BTranslator` is automatically {hmethod}`Acquire()`'d. When the
{cpp:class}`BTranslatorRoster` is deleted, its {hclass}`BTranslator`s are {hmethod}`Release()`'d.
Thus, when you instantiate a {hclass}`BTranslator` and add it to a {cpp:class}`BTranslatorRoster`,
you and the Roster maintain joint ownership of the object. To give up ownership (such that the
{cpp:class}`BTranslatorRoster` will destroy the object when the Roster itself is destroyed), call
{hmethod}`Release()` after adding the {hclass}`BTranslator` to the Roster.

{hmethod}`Acquire()` and {hmethod}`Release()` both return a pointer to the {hclass}`BTranslator`
that was just acquired or released. If {hmethod}`Release()` caused the object to be deleted, it
returns {cpp:expr}`NULL`.

{hmethod}`ReferenceCount()`, which returns the current reference count value, is meant for
debugging purposes only. It is not thread-safe! Don't predicate your code on the value it returns.
::::
