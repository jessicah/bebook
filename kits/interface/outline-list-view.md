:::{cpp:class} BOutlineListView
:::

# BOutlineListView

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BOutlineListView::BOutlineListView(BRect frame, const char* name, list_view_type type = B_SINGLE_SELECTION_LIST, uint32 resizingMode = B_FOLLOW_LEFT | B_FOLLOW_TOP, uint32 flags = B_WILL_DRAW | B_FRAME_EVENTS | B_NAVIGABLE)
:::

:::{cpp:function} BOutlineListView::BOutlineListView(BMessage* archive)
:::

Initializes the {hclass}`BOutlineListView`. This constructor matches the
{cpp:class}`BListView` constructor in every detail, including default
arguments. All argument values are passed to the {cpp:class}`BListView`
{cpp:func}`constructor <BListView::BListView()>` without change. The
{hclass}`BOutlineListView` class doesn't do any initialization of its own.
::::

::::{abi-group}
:::{cpp:function} virtual BOutlineListView::~BOutlineListView()
:::

Does nothing; this class relies on the {cpp:class}`BListView`
{cpp:func}`constructor <BListView::BListView()>` destructor.
::::

## Hook Functions

::::{abi-group}
:::{cpp:function} virtual void BOutlineListView::KeyDown(const char* bytes, int32 numBytes)
:::

Augments the inherited version of {cpp:func}`KeyDown()
<BListView::KeyDown>` to allow users to navigate the outline hierarchy
using the arrow keys and to expand or collapse sections of the outline
using Control—arrow key combinations.
::::

::::{abi-group}
:::{cpp:function} virtual void BOutlineListView::MouseDown(BPoint point)
:::

Augments the inherited version of {cpp:func}`MouseDown()
<BView::MouseDown>` to permit users to expand and collapse sections of the
outline by clicking on an item's latch.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} virtual bool BOutlineListView::AddItem(BListItem* item)
:::

:::{cpp:function} virtual bool BOutlineListView::AddItem(BListItem* item, int32 index)
:::

:::{cpp:function} virtual bool BOutlineListView::AddUnder(BListItem* item, BListItem* superitem)
:::

These functions add an {hparam}`item` to the list. {hmethod}`AddItem()`
adds the item at {hparam}`index`—where the index counts all items assigned
to the {hclass}`BOutlineListView`—or, if an {hparam}`index` isn't
specified, at the end of the list. The two versions of this function
override their {cpp:class}`BListView` counterparts to ensure that the item
is correctly entered into the outline. If the item is added to a portion of
the list that is collapsed, it won't be visible.

{hmethod}`AddUnder()` adds an {hparam}`item` immediately after another
item in the list and at one outline level deeper. The level of the
{hparam}`item` is modified accordingly. Thus, the item already in the list
becomes the superitem for the newly added {hparam}`item`. If its new
superitem is collapsed or is in a collapsed part of the list, the item will
not be visible.

Unlike {hmethod}`AddUnder()`, {hmethod}`AddItem()` respects the outline
level of the item. By setting the item's level before calling
{hmethod}`AddItem()`, you can add it as a subitem to an item at a higher
outline level or insert it as a superitem to items at a lower level.

See also: the {cpp:class}`BListItem` class
::::

::::{abi-group}
:::{cpp:function} virtual bool BOutlineListView::AddList(BList* newItems)
:::

:::{cpp:function} virtual bool BOutlineListView::AddList(BList* newItems, int32 index)
:::

Adds a group of items to the list just as {cpp:func}`AddItem()
<BOutlineListView::AddItem>` adds a single item. The {hparam}`index` counts
all items assigned to the {hclass}`BOutlineListView`. The
{hparam}`newItems` {cpp:class}`BList` must contain pointers to
{cpp:class}`BListItem` objects.

See also: {cpp:func}`BListView::AddList`
::::

::::{abi-group}
:::{cpp:function} virtual status_t BOutlineListView::Archive(BMessage* archive, bool deep = true) const
:::

Archives the {hclass}`BOutlineListView` object much as the
{cpp:func}`Archive() <BListView::Archive>` function in the
{cpp:class}`BListView` class does, but makes sure that all items are
archived, including items in collapsed sections of the list, when the
{hparam}`deep` flag is {cpp:expr}`true`.

See also: {cpp:func}`BListView::Archive`, {cpp:func}`Instantiate()
<BOutlineListView::Instantiate>` static function
::::

::::{abi-group}
:::{cpp:function} void BOutlineListView::Collapse(BListItem* item)
:::

:::{cpp:function} void BOutlineListView::Expand(BListItem* item)
:::

These functions collapse and expand the section of the list controlled by
the {hparam}`item` superitem. If {hparam}`item` isn't a superitem, it is
nevertheless flagged as expanded or collapsed so that it will behave
appropriately in case it does become a superitem.

See also: {cpp:func}`BListItem::SetExpanded`
::::

::::{abi-group}
:::{cpp:function} int32 BOutlineListView::CountItemsUnder(BListItem* underItem, bool oneLevelOnly) const
:::

Counts the items located under the {hparam}`underItem` superitem and
returns that value. If the {hparam}`oneLevelOnly` argument is
{cpp:expr}`true`, only items directly contained within the specified
superitem are considered. If {hparam}`oneLevelOnly` is {cpp:expr}`false`,
all subitems of the specified item are considered, as are all subitems of
those subitems and so forth.

:::{admonition} Note
:class: note
When {hparam}`oneLevelOnly` is {cpp:expr}`false`,
{hmethod}`CountItemsUnder()` acts just like {cpp:func}`FullListCountItems()
<BOutlineListView::FullListCountItems>`, except the first item in the list
that's considered is {hparam}`underItem` instead of the first item in the
full list.
:::

See also: {cpp:func}`BListView::CountItems`
::::

::::{abi-group}
:::{cpp:function} BListItem* BOutlineListView::EachItemUnder(BListItem* underItem, bool oneLevelOnly, BListItem* (*eachFunc) (BListItem*, void* ), void* data)
:::

Calls the function {hparam}`eachFunc` for every item located under the
{hparam}`underItem` superitem. If {hparam}`oneLevelOnly` is
{cpp:expr}`true`, {hparam}`eachFunc` is only called for items located
directly under the {hparam}`underItem`; if {hparam}`oneLevelOnly` is
{cpp:expr}`false`, the {hparam}`eachFunc` is called once for every subitem
of {hparam}`underItem`, including subitems of subitems, recursively.

The {hparam}`data` argument is passed through to each call to the
{hparam}`eachFunc` function as the second argument to that function, and
may be used for whatever purpose your {hparam}`eachFunc` requires.

If the {hparam}`eachFunc` function returns a pointer to a
{cpp:class}`BListItem` (rather than {cpp:expr}`NULL`), processing is
stopped immediately, even if there are items still unvisited. The
{cpp:class}`BListItem` pointer returned by the {hparam}`eachFunc` function
is returned by {hmethod}`EachItemUnder()`.

:::{admonition} Note
:class: note
When {hparam}`oneLevelOnly` is {cpp:expr}`false`,
{hmethod}`EachItemUnder()` acts just like {cpp:func}`FullListDoForEach()
<BOutlineListView::FullListDoForEach>`, except the first item in the list
that's considered is {hparam}`underItem` instead of the first item in the
full list.
:::

See also: {cpp:func}`BListView::DoForEach`
::::

::::{abi-group}
:::{cpp:function} int32 BOutlineListView::FullListCountItems() const
:::

:::{cpp:function} int32 BOutlineListView::FullListCurrentSelection(int32 index = 0) const
:::

:::{cpp:function} BListItem* BOutlineListView::FullListFirstItem() const
:::

:::{cpp:function} BListItem* BOutlineListView::FullListLastItem() const
:::

:::{cpp:function} int32 BOutlineListView::FullListIndexOf(BPoint point) const
:::

:::{cpp:function} int32 BOutlineListView::FullListIndexOf(BListItem* item) const
:::

:::{cpp:function} BListItem* BOutlineListView::FullListItemAt(int32 index) const
:::

:::{cpp:function} bool BOutlineListView::FullListHasItem(BListItem* item) const
:::

:::{cpp:function} bool BOutlineListView::FullListIsEmpty() const
:::

:::{cpp:function} void BOutlineListView::FullListDoForEach(bool (*func)(BListItem*))
:::

:::{cpp:function} void BOutlineListView::FullListDoForEach(bool (*func)(BListItem*), void* ))
:::

:::{cpp:function} void BOutlineListView::FullListDoForEach(bool (*func)(BListItem*), void* ), void* )
:::

:::{cpp:function} void BOutlineListView::FullListSortItems(int (*compareFunc)(const BListItem *, const BListItem *))
:::

These functions parallel a similar set of functions defined in the
{cpp:class}`BListView` class. The {cpp:class}`BListView` functions have
identical names, but without the {hmethod}`FullList…()` prefix. When
applied to a {hclass}`BOutlineListView` object, the inherited functions
consider only items in sections of the outline that can be displayed
on-screen—that is, they skip over items in collapsed portions of the list.

These {hclass}`BOutlineListView` functions, on the other hand, consider
all items in the list. For example, {cpp:func}`IndexOf()
<BListView::IndexOf>` and {hmethod}`FullListIndexOf()` both return an index
to a given item. However, for {cpp:func}`IndexOf() <BListView::IndexOf>`
the index is to the position of the item in the list that can be currently
displayed, but for {hmethod}`FullListIndexOf()` it's to the item's position
in the full list, including collapsed sections.
::::

::::{abi-group}
:::{cpp:function} bool BOutlineListView::IsExpanded(int32 index)
:::

Returns {cpp:expr}`true` if the item at {hparam}`index` is marked as
controlling an expanded section of the list, and {cpp:expr}`false` if it's
marked as controlling a collapsed section or if there's no item at that
index. If a superitem is expanded, the {hclass}`BOutlineListView` can
display its subitems; if not, the subitems are hidden.

The {hparam}`index` passed to this function is to the full list of items
assigned to the {hclass}`BOutlineListView`.

See also: {cpp:func}`BListItem::IsExpanded`
::::

::::{abi-group}
:::{cpp:function} BListItem* BOutlineListView::ItemUnderAt(BListItem* underItem, bool oneLevelOnly, int32 index) const
:::

Returns a pointer to the {hparam}`index`th item under the specified
{hparam}`underItem`. If {hparam}`oneLevelOnly` is {cpp:expr}`true`, only
items located directly under the {hparam}`underItem` are considered. If
{hparam}`oneLevelOnly` is {cpp:expr}`false`, subitems are scanned
recursively to locate the appropriate index.

:::{admonition} Note
:class: note
When {hparam}`oneLevelOnly` is {cpp:expr}`false`, {hmethod}`ItemUnderAt()`
acts just like {cpp:func}`FullListItemAt()
<BOutlineListView::FullListItemAt>`, except the first item in the list
that's considered is {hparam}`underItem` instead of the first item in the
full list.
:::
::::

::::{abi-group}
:::{cpp:function} virtual void BOutlineListView::MakeEmpty()
:::

Overrides the {cpp:class}`BListView` version of {cpp:func}`MakeEmpty()
<BListView::MakeEmpty>` to remove all items from the list. The
{cpp:class}`BListView` version of this function won't work as advertised on
a {hclass}`BOutlineListView`.
::::

::::{abi-group}
:::{cpp:function} virtual bool BOutlineListView::RemoveItem(BListItem* item)
:::

:::{cpp:function} virtual BListItem* BOutlineListView::RemoveItem(int32 index)
:::

:::{cpp:function} virtual bool BOutlineListView::RemoveItems(int32 index, int32 count)
:::

These functions work like their {cpp:class}`BListView` counterparts,
except that:

-   They can remove items from any part of the list, including collapsed
sections. The index counts all items assigned to the
{hclass}`BOutlineListView`; the specified item can be hidden.

-   If the item being removed is a superitem, they also remove all of its
subitems.

:::{admonition} Warning
:class: warning
The {cpp:class}`BListView` versions of these functions will not produce
reliable results when applied to a {hclass}`BOutlineListView`, even if the
item being removed is in an expanded section of the list and is not a
superitem.
:::

See also: {cpp:func}`BListView::RemoveItem`
::::

::::{abi-group}
:::{cpp:function} void BOutlineListView::SortItemsUnder(BListItem* underItem, bool oneLevelOnly, int (*compareFunc)(const BListItem *, const BListItem *))
:::

Sorts the items located under the specified {hparam}`underItem`. If
{hparam}`oneLevelOnly` is {cpp:expr}`true`, only items located directly
under the {hparam}`underItem` are considered. If {hparam}`oneLevelOnly` is
{cpp:expr}`false`, subitems are scanned recursively and sorted.

The hierarchy of the list is ignored when sorting with
{hparam}`oneLevelOnly` set to {cpp:expr}`false`; items can (and will) be
moved from one level to another. If you want to sort without moving items
from one level to another, you should call {hmethod}`SortItemsUnder()` once
for each superitem with {hparam}`oneLevelOnly` set to {cpp:expr}`true`.

:::{admonition} Note
:class: note
When {hparam}`oneLevelOnly` is {cpp:expr}`false`,
{hmethod}`SortItemsUnder()` acts just like {cpp:func}`FullListSortItems()
<BOutlineListView::FullListSortItems>`, except the first item in the list
that's considered is {hparam}`underItem` instead of the first item in the
full list.
:::
::::

::::{abi-group}
:::{cpp:function} BListItem* BOutlineListView::Superitem(const BListItem* item)
:::

Returns the superitem for the {hparam}`item` passed as an argument—that
is, the item under which the argument {hparam}`item` is grouped—or
{cpp:expr}`NULL` if the {hparam}`item` is at the outermost level of the
outline (level 0) or isn't in the list.
::::

## Static Functions

::::{abi-group}
:::{cpp:function} static BArchivable* BOutlineListView::Instantiate(BMessage* archive)
:::

Returns a new {hclass}`BOutlineListView` object, allocated by new and
created with the version of the constructor that takes a
{cpp:class}`BMessage` archive. However, this function returns
{cpp:expr}`NULL` if the specified {hparam}`archive` doesn't contain data
for a {hclass}`BOutlineListView` object.

See also: {cpp:func}`BArchivable::Instantiate`,
{cpp:func}`instantiate_object() <instantiate::object>`,
{cpp:func}`Archive() <BOutlineListView::Archive>`
::::
