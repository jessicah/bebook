# BList

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BList::BList(int32 count = 20)
:::
:::{cpp:function} BList::BList(const BList& anotherList)
:::

Initializes the {hclass}`BList` by allocating enough memory to hold {hparam}`count` items. As the
list grows and shrinks, additional memory is allocated and freed in blocks of the same size.

The copy constructor creates an independent list of data pointers, but it doesn't copy the
pointed-to data. For example:

:::{code} cpp
BList* newList = new BList(oldList);
:::

Here, the contents of `oldList` and `newList`---the actual data pointers---are separate and
independent. Adding, removing, or reordering items in `oldList` won't affect the number or order of
items in `newList`. But if you modify the data than an item in `oldList` points to, the modification
will be seen through the analogous item in `newList`.

The block size of a {hclass}`BList` that's created through the copy constructor is the same as that
of the original {hclass}`BList`.
::::


::::{abi-group}
:::{cpp:function} virtual BList::~BList()
:::

Frees the list of data pointers, but doesn't free the data that they point to. To destroy the data,
you need to free each item individually:

:::{code} cpp
void* item;
for (int32 i = 0; item = list->ItemAt(i); ++i)
	delete item;

delete list;
:::

See also: {cpp:func}`~BList::MakeEmpty()`
::::

## Member Functions

::::{abi-group}
:::{cpp:function} bool BList::AddItem(void* item)
:::
:::{cpp:function} bool BList::AddItem(void* item, int32 index)
:::

Adds an {hparam}`item` to the {hclass}`BList` at {hparam}`index`---or, if no index is supplied, at the end of
the list. If necessary, additional memory is allocated to accommodate the new item.

Adding an item never removes an item already in the list. If the item is added at an index that's
already occupied, items currently in the list are bumped down one slot to make room.

If {hparam}`index` is out of range (greater than the current item count, or less than zero), the
function fails and returns {cpp:expr}`false`. Otherwise it returns {cpp:expr}`true`.
::::

::::{abi-group}
:::{cpp:function} bool BList::AddList(BList* items)
:::
:::{cpp:function} bool BList::AddList(BList* items, int32 index)
:::

Adds the contents of another {hclass}`BList` to this {hclass}`BList`. The items from the other
{hclass}`BList` are inserted at {hparam}`index`---or, if no index is given, they're appended to the
end of the list. if the index is out of range, the function fails and returns {cpp:expr}`false`. if
successful, it returns {cpp:expr}`true`.

See also: {cpp:func}`~BList::AddItem()`
::::

::::{abi-group}
:::{cpp:function} int32 BList::CountItems()
:::

Returns the number of items currently in the list.
::::

::::{abi-group}
:::{cpp:function} void BList::DoForEach(bool (*func)(void*))
:::
:::{cpp:function} void BList::DoForEach(bool (*func)(void*), void* arg2)
:::

Calls the {hparam}`func` function once for each item in the {hclass}`BList`. Items are visited in
order, beginning with the first one in the list (index 0) and ending with the last. If a call to
{hparam}`func` returns {cpp:expr}`true`, the iteration is stopped, even if some items have not yet
been visited.

{hparam}`func` must be a function that takes one or two arguments. THe first argument is the
currently-considered item from the list; the second argument, if {hparam}`func` requires one, is
passed to {hmethod}`DoForEach()` as {hparam}`arg2`.
::::

::::{abi-group}
:::{cpp:function} void* BList::FirstItem() const
:::

Returns the first item in the list, or {cpp:expr}`NULL` if the list is empty. This function doesn't
remove the item from the list.

See also: {cpp:func}`~BList::LastItem()`, {cpp:func}`~BList::ItemAt()`
::::

::::{abi-group}
:::{cpp:func} bool BList::HasItem() const
:::

Returns {cpp:expr}`true` if item is in the list, and {cpp:expr}`false` if not.
::::

::::{abi-group}
:::{cpp:function} int32 BList::IndexOf(void* item) const
:::

Returns the index where a particular item is located in the list, or a negative number if the item
isn't in the list. If the item is in the list more than once, the index returned will be the
position of its first occurrence.
::::

::::{abi-group}
:::{cpp:function} bool BList::IsEmpty() const
:::

Returns {cpp:expr}`true` if the list is empty (if it contains no items), and {cpp:expr}`false`
otherwise.

See also: {cpp:func}`~BList::MakeEmpty()`
::::

::::{abi-group}
:::{cpp:function} void* BList::ItemAt(in32 index) const
:::

Returns the item at {hparam}`index`, or {cpp:expr}`NULL` if the index is out of range. This function
doesn't remove the item from the list.

See also: {cpp:func}`~BList::Items()`, {cpp:func}`~BList::FirstItem()`,
{cpp:func}`~BList::LastItem()`
::::

::::{abi-group}
:::{cpp:function} void* BList::Items() const
:::

Returns a pointer to the {hclass}`BList`'s list. You can index directly into the list if you're
certain that the index is in range:

:::{code} cpp
myType* item = (myType*)Items()[index];
:::
::::

::::{abi-group}
:::{cpp:function} void* BList::LastItem() const
:::

Returns the last item in the list without removing it. If the list is empty, this function returns
{cpp:expr}`NULL`.

See also: {cpp:func}`~BList::RemoveItem()`, {cpp:func}`~BList::FirstItem()`
::::

::::{abi-group}
:::{cpp:function} void BList::MakeEmpty()
:::

Empties the {hclass}`BList` of all its items, without freeing the data that they point to.

See also: {cpp:func}`~BList::IsEmpty()`, {cpp:func}`~BList::RemoveItem()`
::::

::::{abi-group}
:::{cpp:function} bool BList::RemoveItem(void* item)
:::
:::{cpp:function} void* BList::RemoveItem(int32 index)
:::
:::{cpp:function} bool BList::RemoveItems(int32 index, int32 count)
:::

{hmethod}`RemoveItem()` removes an item from the list. If passed an {hparameter}`item`, the function
looks for the item in the list, removes it, and returns {cpp:expr}`true`. If it can't find the item,
it returns {cpp:expr}`false`. If the item is in the list more than once, this function removes only
its first occurrence.

If passed an {hparam}`index`, {hmethod}`RemoveItem()` removes the item at that index and returns it.
If there's no item at the index, it returns {cpp:expr}`NULL`.

{hmethod}`RemoveItems()` removes a group of {hparam}`count` items from the list, beginning with the
item at {hparam}`index`. If the index is out of range, it fails and returns {cpp:expr}`false`.
Otherwise, it removes the items, without checking to be sure that the list actually holds that many
items at the index, and returns {cpp:expr}`true`.

The list is compacted after an item is removed. Because of this, you mustn't try to empty a list (or
a range within a list) by removing items at monotonically increasing indices. You should either
start with the highest index and move towards the head of the list, or remove at the same index (the
lowest in the range) some number of times. As an example of the latter, the following code removes
the first five items in the list:

:::{code} cpp
for (int32 i = 0; i < 5; ++i)
	list->RemoveItem(0);
:::

See also: {cpp:func}`~BList::MakeEmpty()`
::::

::::{abi-group}
:::{cpp:function} void* BList::SortItems(int (*compareFunc)(const void* first, const void* second))
:::

Rearranges the items in the list. The items are sorted using the {hparam}`compareFunc` comparison
function passed as an argument. This function should return a negative number if the first item is
ordered before the second, a positive number if the second is ordered before the first, and 0 if the
two items are ordered equivalently.

The arguments passed to the comparison function are declared to be `void*`; however they should be
regarded as pointers to the items in the list---in other words, as pointers to pointers.
::::

## Operators

::::{abi-group}
:::{cpp:function} BList& operator=(const BList& from)
:::

Copies the contents of one {hclass}`BList` object into another:

:::{code} cpp
BList newList = oldList;
:::

After the assignment, each object has its own independent copy of list data; destroying one of the
objects won't affect the other.

Only the items in the list are copied, not the data they point to.
::::
