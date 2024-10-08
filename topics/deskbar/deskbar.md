:::{cpp:class} BDeskbar
:::

# BDeskbar

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BDeskbar::BDeskbar()
:::

The constructor creates and returns a new {hclass}`BDeskbar` object.
::::

::::{abi-group}
:::{cpp:function} BDeskbar::BDeskbar()
:::

Deletes the {hclass}`BDeskbar` object.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} status_t BDeskbar::AddItem(BView* view, int32* id = NULL)
:::

:::{cpp:function} status_t BDeskbar::AddItem(entry_ref* addon, int32* id = NULL)
:::

:::{cpp:function} status_t BDeskbar::RemoveItem(int32 id)
:::

:::{cpp:function} status_t BDeskbar::RemoveItem(const char* name)
:::

:::{cpp:function} int32 BDeskbar::CountItems() const
:::

:::{cpp:function} bool BDeskbar::HasItem(int32 id) const
:::

:::{cpp:function} bool BDeskbar::HasItem(const char* name) const
:::

:::{cpp:function} status_t BDeskbar::GetItemInfo(int32 for_id, const char** found_name)
:::

:::{cpp:function} status_t BDeskbar::GetItemInfo(const char* for_name, const int32* found_id)
:::

:::{admonition} Warning
:class: warning
A view that's sitting on the Deskbar's shelf may not call any of these
functions.
:::

The Deskbar contains a shelf that contains replicants (archivable
{cpp:class}`BView`s). Typically, these replicants monitor or control some
service. For example, the BeOS provides shelf items that monitor and
control the input method mechanism, PPP, and the mail daemon (the date/time
view is not a shelf replicant):

![The BDeskbar Shelf](./_static/images/Shelf.png)

{hmethod}`AddItem()` puts a new item on the Deskbar's shelf.
{hparam}`view`, the {cpp:class}`BView` that will be displayed on the shelf,
must be archivable (see {cpp:class}`BArchivable`). An item on the shelf is
identified by name and an integer id. The name is that of the view itself
(i.e., as assigned in the {cpp:class}`BView` constructor); the id is
generated by the Deskbar and is guaranteed to be unique. {hparam}`id`, if
supplied, is set to the added item's unique id number.

You can also add an item to the Deskbar by passing an {htype}`entry_ref`,
{hparam}`addon`, to the Deskbar add-on to place there.

{hmethod}`RemoveItem()` removes the shelf item identified by {hparam}`name`
or {hparam}`id`.

{hmethod}`CountItems()` returns the number of items currently on the shelf
(keep in mind that it doesn't count the date/time view).

{hmethod}`HasItem()` returns {cpp:expr}`true` if the Deskbar shelf contains
the item identified by {hparam}`name` or {hparam}`id`.

{hmethod}`GetItemInfo()` points *{hparam}`found_name` to the name of the
item identified by {hparam}`for_id`, or sets {hparam}`found_id` of the item
identified by {hparam}`for_nam`e.

:::{admonition} Warning
:class: warning
The caller is responsible for freeing found_name.
:::

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`B_OK`.
	- The request to add, remove, or get info on the item was successfully
		communicated to the Deskbar. Note that this doesn't mean that the function
		actually did what it was supposed to do.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- ({hmethod}`GetItemInfo()`) *{hparam}`found_name` is {cpp:expr}`NULL`.
-
	- Negative values.
	- A message-sending error occurred.

:::
::::

::::{abi-group}
:::{cpp:function} BRect BDeskbar::Frame() const
:::

Returns the Deskbar's frame in screen coordinates.
::::

::::{abi-group}
:::{cpp:function} deskbar_location BDeskbar::Location(bool* isExpanded = NULL) const
:::

:::{cpp:function} bool BDeskbar::IsExpanded() const
:::

:::{cpp:function} status_t BDeskbar::SetLocation(deskbar_location location, bool isExpanded = false)
:::

:::{cpp:function} status_t BDeskbar::Expand(bool expand)
:::

{hmethod}`Location()` returns a symbolic description of the Deskbar's
current location; see {cpp:any}`deskbar_location` for the list of
pre-defined locations. {hparam}`isExpanded` (if supplied) is set to
{cpp:expr}`true` if the Deskbar is expanded, and {cpp:expr}`false` if it's
contracted; {hmethod}`IsExpanded()` returns the expansion value directly.
Expansion and contraction is variable only if the Deskbar's location is
left-top or right-top; for all other locations, the expansion state is
hard-wired. See {cpp:any}`deskbar_location` for illustrations.

{hmethod}`SetLocation()` sets the Deskbar's location and expands/contracts
the Deskbar; for some locations, the expansion/contraction is hard-wired.
{hmethod}`Expand()` expands/contracts the Deskbar (if the setting isn't
hard-wired) without setting its location. You should very rarely need to
call these functions. Moving and expanding the Deskbar is in the user's
domain.

{hmethod}`SetLocation()` and {hmethod}`Expand()` return…

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`B_OK`.
	- The new location or expansion request was successfully communicated to the
		Deskbar. Whether the parameters were actually enforced isn't indicated.
-
	- Negative values.
	- The Deskbar isn't running, or some other message-sending error occurred.

:::
::::

## Deskbar Types

### Deskbar Location

:::{code} cpp
enum deskbar_location;
:::

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Constant

	- Description

-
	- {cpp:enumerator}`B_DESKBAR_TOP`

	- Expanded (only) along the top.

-
	- {cpp:enumerator}`B_DESKBAR_BOTTOM`

	- Expanded (only) along the bottom.

-
	- {cpp:enumerator}`B_DESKBAR_LEFT_BOTTOM`

	- Contracted (only) in bottom left corner.

-
	- {cpp:enumerator}`B_DESKBAR_RIGHT_BOTTOM`

	- Contracted (only) in bottom right corner.

-
	- {cpp:enumerator}`B_DESKBAR_LEFT_TOP`

	- In the top left corner (expanded or contracted).

-
	- {cpp:enumerator}`B_DESKBAR_RIGHT_TOP`

	- In the top right corner (expanded or contracted).


:::

The {htype}`deskbar_location` constants are used to set and return the
Deskbar's location (see {cpp:func}`~BDeskbar::Location()`). The six
locations are shown in the two illustrations below:

![BDeskbar At Top And Bottom](./_static/images/TopBottom.png)

![BDeskbar At Left And Right](./_static/images/Corners.png)

The {htype}`deskbar_location` value affects the Deskbar's expanded state:
The Deskbar can be expanded or contracted in
{cpp:enumerator}`B_DESKBAR_LEFT_TOP` and
{cpp:enumerator}`B_DESKBAR_RIGHT_TOP` locations only. In the other
locations, the expansion/contraction is hard-wired. The illustration below
shows a left-top Deskbar in its expanded and contracted states:


