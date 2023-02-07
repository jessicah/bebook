# BListItem
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BListItem::BListItem(uint32 level = 0, bool expanded = true)
:::
:::{cpp:function} BListItem::BListItem(BMessage* archive)
:::

The constructors create a new {hclass}`BListItem` object. The level and expanded
arguments are only used if the item is added to a
{cpp:class}`BOutlineListView`
object; see
{cpp:func}`BOutlineListView::AddItem`
for more information.

::::

::::{abi-group}

:::{cpp:function} BListItem::~BListItem()
:::

The destructor is empty.

::::

## Hook Functions
::::{abi-group}

:::{cpp:function} virtual void BListItem::DrawItem(BView* owner, BRect itemRect, bool drawEverything = false) = 0
:::

Hook function that's invoked when the item's owner (a
{cpp:class}`BListView` object)
needs to draw this item. {hparam}`itemRect` is the area within the owner to which
the item's drawing is clipped. If {hparam}`drawEverything` is
{cpp:enum}`true`, this function
should touch every pixel in {hparam}`itemRect`; if it's
{cpp:enum}`false`, the function can
assume that the background color for the item is already painted.
{hmethod}`DrawItem()` should be implemented to visually reflect the state of the
item, highlighting it if it's selected, dimming it if it's disabled, and
so on.

The owner view provides the drawing environment for this item. All
drawing instructions should be invoked on owner.
See
"{cpp:func}`~BListItem::Overview`"
for an example {hmethod}`DrawItem()` function.

::::

::::{abi-group}

:::{cpp:function} virtual void BListItem::Update(BView* owner, const BFont* font)
:::

Hook function that's called whenever the item's {hparam}`owner` changes in a way
that could affect the appearance of this item. It's always called when
the item is added to a list view.

The default implementation sets the item's width to that of the owner,
and sets its height so it will accommodate {hparam}`font` (the owner's current
{cpp:class}`BFont` setting).

::::

## Member Functions
::::{abi-group}

:::{cpp:function} uint32 BListItem::OutlineLevel() const
:::

Returns the outline level of the item; this is only meaningful if the
item is in a {cpp:class}`BOutlineListView`.

::::

::::{abi-group}

:::{cpp:function} void BListItem::Select()
:::
:::{cpp:function} void BListItem::Deselect()
:::
:::{cpp:function} bool BListItem::IsSelected() const
:::

{hmethod}`Select()` and {hmethod}`Deselect()`
set the item's selected state; {hmethod}`IsSelected()`
returns the state. The setting functions don't automatically update the
item's display: After calling {hmethod}`Select()` or
{hmethod}`Deselect()`, you must tell the
owner to redrawn this item (see
{cpp:func}`BListView::InvalidateItem`).

Also, {hmethod}`Select()` doesn't deselect the current selection. If this item is
part of a single-selection list view, you have to deselect the current
selection yourself.

:::{admonition} Note
:class: note
If possible, you should use {cpp:class}`BListView`'s versions of these functions
(see
{cpp:func}`BListView::Select`.
They update the view and manage the selection for you.
:::
::::

::::{abi-group}

:::{cpp:function} void BListItem::SetEnabled(bool enabled)
:::
:::{cpp:function} bool BListItem::IsEnabled() const
:::

{hmethod}`SetEnabled()` sets the list item's enabled state; {hmethod}`IsEnabled()` returns the
state. A disabled item can't be selected by the user or by
{cpp:func}`BListView::Select`
, but it can be selected through
{cpp:func}`BListItem::Select`.
If an item is already selected, {hmethod}`SetEnabled`({cpp:enum}`false`)
doesn't deselect it.

After calling {hmethod}`SetEnabled()`, you must tell the owner list view to redraw
the item (see
{cpp:func}`BListView::InvalidateItem`).

Note that {cpp:class}`BListView`
doesn't provide smart versions of these functions (as it does for
{hmethod}`Select()`).

::::

::::{abi-group}

:::{cpp:function} void BListItem::SetExpanded(bool expanded)
:::
:::{cpp:function} bool BListItem::IsExpanded() const
:::

These functions set and return the item's expanded state. This is only
meaningful if the item is part of a
{cpp:class}`BOutlineListView`.
The item is not automatically redrawn; you must tell the
{cpp:class}`BOutlineListView`
to redraw the item (and its sublist) through
{cpp:func}`BListView::InvalidateItem`.

:::{admonition} Note
:class: note
If possible, you should use
{cpp:class}`BOutlineListView`'s
{cpp:func}`~BOutlineListView::Expand` and
{cpp:func}`~BOutlineListView::Collapse`
functions instead of {hmethod}`SetExpanded()`. The
{cpp:class}`BOutlineListView`
functions redraw the affected part of the list for you.
:::
::::

::::{abi-group}

:::{cpp:function} void BListItem::SetHeight(float height)
:::
:::{cpp:function} void BListItem::SetWidth(float height)
:::
:::{cpp:function} float BListItem::Height() const
:::
:::{cpp:function} float BListItem::Width() const
:::

These functions set and return the width and height of the item. The
item's dimensions are adjusted when
{cpp:func}`~BListItem::Update`
is called.

::::

## Archived Fields