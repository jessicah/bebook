```{cpp:class} BTranslator

# BTranslator

---

## Constructor and Destructor

### BTranslator()

{cpp:member}`~BTranslator::BTranslator()`
: The constructor must create and return a new instance of your {cpp:expr}`BTranslator` subclass.
Note that the constructor doesn't {cpp:func}`Acquire()` the object it returns.

### ~BTranslator()

{cpp:member}`~BTranslator::~BTranslator()`
: Note that the destructor is protected; you can only delete a {cpp:expr}`BTranslator` object from
within the implementation of the subclass. From outside the class, you call {cpp:func}`Release()`.

---

## Member Functions

### Acquire(), Release(), ReferenceCount()

{cpp:member}`BTranslator* Acquire()`<br>{cpp:expr}`BTranslator* Release();`<br>{cpp:expr}`int32 ReferenceCount();`
: :::{warning}
  {cpp:expr}`ReferenceCount()` is for debugging use only!
  :::

: {cpp:expr}`Acquire()` and {cpp:expr}`Release()` increment and decrement the object's reference
count. The count starts at 1 (i.e. the object is implicitly acquired when it's created); if the
count falls to 0, the object is deleted.

: When you add a {cpp:expr}`BTranslator` to a {cpp:class}`BTranslatorRoster`, the
{cpp:expr}`BTranslator` is automatically {cpp:expr}`Acquire()`'d. When the
{cpp:class}`BTranslatorRoster` is deleted, its {cpp:expr}`BTranslator`s are {cpp:expr}`Release()`'d.
Thus, when you instantiate a {cpp:expr}`BTranslator` and add it to a {cpp:class}`BTranslatorRoster`,
you and the Roster maintain joint ownership of the object. To give up ownership (such that the
{cpp:class}`BTranslatorRoster` will destroy the object when the Roster itself is destroyed), call
{cpp:expr}`Release()` after adding the {cpp:expr}`BTranslator` to the Roster.

: {cpp:expr}`Acquire()` and {cpp:expr}`Release()` both return a pointer to the {cpp:expr}`BTranslator`
that was just acquired or released. If {cpp:expr}`Release()` caused the object to be deleted, it
returns {cpp:enum}`NULL`.

: {cpp:expr}`ReferenceCount()`, which returns the current reference count value, is meant for
debugging purposes only. It is not thread-safe! Don't predicate your code on the value it returns.
