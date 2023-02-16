:::{cpp:class} BBitmap
:::

# BBitmap

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BBitmap::BBitmap(BRect bounds, color_space space, bool acceptsViews = false, bool needsContiguousMemory = false)
:::

:::{cpp:function} BBitmap::BBitmap(BMessage* archive)
:::

Creates a new {hclass}`BBitmap` object that can hold a bitmap whose size
and depth are described by {hparam}`bounds` and {hparam}`space`. The bitmap
data is uninitialized; you set the data through {cpp:func}`Bits()
<BBitmap::Bits>` / {cpp:func}`SetBits() <BBitmap::SetBits>`, or by drawing
into an attached {cpp:class}`BView` (see "{ref}`Using a View to Draw into a
Bitmap`").

:::{admonition} Warning
:class: warning
The {hclass}`BBitmap` class insists that a {cpp:class}`BApplication`
object be present (but not necessarily running).
:::

If {cpp:class}`BView`s are to be used, the {hparam}`acceptsViews` argument
must be set to {cpp:expr}`true`. Furthermore (in this case), the origin of
the {hparam}`bounds` rectangle must be 0.0

If the {hparam}`needsContiguousMemory` flag is {cpp:expr}`true`, the
{hclass}`BBitmap` will make sure that the (physical) memory it allocates is
one contiguous physical chunk. This should matter only to drivers doing
direct DMA into physical memory.

The possible color spaces are enumerated in the section "{ref}`Color
Spaces`".
::::

::::{abi-group}
:::{cpp:function} virtual BBitmap::~BBitmap()
:::

Frees all memory allocated to hold image data, deletes any
{cpp:class}`BView`s used to create the image, gets rid of the off-screen
window that held the views, and severs the {hclass}`BBitmap`'s connection
to the Application Server.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} virtual void BBitmap::AddChild(BView* aView)
:::

Adds {hparam}`aView` (and all its children) to this {hclass}`BBitmap`'s
view hierarchy, and causes {cpp:func}`AttachedToWindow()
<BView::AttachedToWindow>` to be sent to the newly add children.

:::{admonition} Warning
:class: warning
If {hparam}`aView` already has a parent, the application may crash. Be
sure to remove the view from a previous parent before trying to add it to a
bitmap.
:::

{hmethod}`AddChild()` fails if the {hclass}`BBitmap` was not constructed
to accept views.

See also: {cpp:func}`BWindow::AddChild`,
{cpp:func}`BView::AttachedToWindow`, {cpp:func}`RemoveChild()
<BBitmap::RemoveChild>`, the {hclass}`BBitmap` {cpp:func}`constructor
<BBitmap::BBitmap()>`
::::

::::{abi-group}
:::{cpp:function} virtual status_t BBitmap::Archive(BMessage* archive, bool deep = true) const
:::

Calls the inherited version of {cpp:func}`Archive()
<BArchivable::Archive>` and stores the {hclass}`BBitmap` in the
{cpp:class}`BMessage` archive.

See also: {cpp:func}`BArchivable::Archive`, {cpp:func}`Instantiate()
<BBitmap::Instantiate>` static function
::::

::::{abi-group}
:::{cpp:function} void* BBitmap::Bits() const
:::

Returns a pointer to the bitmap data. The length of the data can be
obtained by calling {cpp:func}`BitsLength() <BBitmap::BitsLength>`—or it
can be calculated from the height of the bitmap (the number of rows) and
{cpp:func}`BytesPerRow() <BBitmap::BytesPerRow>`.

The data is in the format specified by {cpp:func}`ColorSpace()
<BBitmap::ColorSpace>`.

This pointer is valid throughout the entire lifespan of the object.

See also: {cpp:func}`Bounds() <BBitmap::Bounds>`, {cpp:func}`BytesPerRow()
<BBitmap::BytesPerRow>`, {cpp:func}`BitsLength() <BBitmap::BitsLength>`
::::

::::{abi-group}
:::{cpp:function} int32 BBitmap::BitsLength() const
:::

Returns the number of bytes that were allocated to store the bitmap data.

See also: {cpp:func}`Bits() <BBitmap::Bits>`, {cpp:func}`BytesPerRow()
<BBitmap::BytesPerRow>`
::::

::::{abi-group}
:::{cpp:function} BRect BBitmap::Bounds() const
:::

Returns the bounds rectangle that defines the size and coordinate system
of the bitmap. This should be identical to the rectangle used in
constructing the object.
::::

::::{abi-group}
:::{cpp:function} int32 BBitmap::BytesPerRow() const
:::

Returns how many bytes of data are required to specify a row of pixels.
This may include slop space required by the graphics hardware; you should
always use this call to determine the width of a row of pixels in bytes
instead of assuming that it will be the number of pixels multiplied by the
size of a pixel in bytes.
::::

::::{abi-group}
:::{cpp:function} BView* BBitmap::ChildAt(int32 index) const
:::

:::{cpp:function} int32 BBitmap::CountChildren() const
:::

{hmethod}`ChildAt()` returns the child {cpp:class}`BView` at
{hparam}`index`, or {cpp:expr}`NULL` if there's no child at
{hparam}`index`. Indices begin at 0 and count only {cpp:class}`BView`s that
were added to the {hclass}`BBitmap` (added as children of the top view of
the {hclass}`BBitmap`'s off-screen window) and not subsequently removed.

{hmethod}`CountChildren()` returns the number of {cpp:class}`BView`s the
{hclass}`BBitmap` currently has. (It counts only {cpp:class}`BView`s that
were added directly to the {hclass}`BBitmap`, not {cpp:class}`BView`s
farther down the view hierarchy.)

These functions fail if the {hclass}`BBitmap` wasn't constructed to accept
views.
::::

::::{abi-group}
:::{cpp:function} color_space BBitmap::ColorSpace() const
:::

Returns the color space of the data being stored (not necessarily the
color space of the data passed to the {cpp:func}`SetBits()
<BBitmap::SetBits>` function). Once set by the {hclass}`BBitmap`
constructor, the color space doesn't change.
::::

::::{abi-group}
:::{cpp:function} BView* BBitmap::FindView(BPoint point) const
:::

:::{cpp:function} BView* BBitmap::FindView(const char* name) const
:::

Returns the {cpp:class}`BView`  at {hparam}`point` within the bitmap or
the {cpp:class}`BView` tagged with {hparam}`name`. The point must be
somewhere within the {hclass}`BBitmap`'s bounds rectangle, which must have
the coordinate origin, (0.0, 0.0), at its left top corner.

If the {hclass}`BBitmap` doesn't accept views, this function fails. If no
view draws at the {hparam}`point` given, or no view associated with the
{hclass}`BBitmap` has the {hparam}`name` given, it returns
{cpp:expr}`NULL`.
::::

::::{abi-group}
:::{cpp:function} bool BBitmap::IsValid() const
:::

Returns {cpp:expr}`true` if there's memory for the bitmap (if the address
returned by {cpp:func}`Bits() <BBitmap::Bits>` is valid), and
{cpp:expr}`false` if not.
::::

::::{abi-group}
:::{cpp:function} bool BBitmap::Lock()
:::

:::{cpp:function} void BBitmap::Unlock()
:::

:::{cpp:function} bool BBitmap::IsLocked() const
:::

These functions lock and unlock the off-screen window where
{cpp:class}`BView`s associated with the {hclass}`BBitmap` draw. Locking
works for this window and its views just as it does for ordinary on-screen
windows.

{hmethod}`Lock()` returns {cpp:expr}`false` if the {hclass}`BBitmap`
doesn't accept views or if its off-screen window is unlockable (and
therefore unusable) for some reason. Otherwise, it doesn't return until it
has the window locked and can return {cpp:expr}`true`.

{hmethod}`IsLocked()` returns {cpp:expr}`false` if the {hclass}`BBitmap`
doesn't accept views. Otherwise, it returns the lock status of its
off-screen window.
::::

::::{abi-group}
:::{cpp:function} virtual bool BBitmap::RemoveChild(BView* aView)
:::

Removes {hparam}`aView` from the hierarchy of views associated with the
{hclass}`BBitmap`, but only if {hparam}`aView` was added to the hierarchy
by calling {hclass}`BBitmap`'s version of the {cpp:func}`AddChild()
<BView::AddChild>` function.

If {hparam}`aView` is successfully removed, {hmethod}`RemoveChild()`
returns {cpp:expr}`true`. If not, it returns {cpp:expr}`false`.
::::

::::{abi-group}
:::{cpp:function} void BBitmap::SetBits(const void* data, int32 length, int32 offset, color_space mode)
:::

Assigns {hparam}`length` bytes of {hparam}`data` to the {hclass}`BBitmap`
object. The new data is copied into the bitmap beginning {hparam}`offset`
bytes (not pixels) from the start of allocated memory. To set data
beginning with the first (left top) pixel in the image, the
{hparam}`offset` should be 0; to set data beginning with, for example, the
sixth pixel in the first row of a {cpp:enumerator}`B_RGB32` image, the
offset should be 20. The offset counts any padding required to align rows
of data.

This function is intended to be used for importing existing data from a
different format rather than for setting individual pixels in the bitmap.
If you're interested in coloring individual pixels, use {cpp:func}`Bits()
<BBitmap::Bits>` to obtain direct access to the bitmap data.

The source data is specified in the {hparam}`mode` color space, which may
or may not be the same as the color space that the {hclass}`BBitmap` uses
to store the data. If not, the following conversions are automatically
made:

-   {cpp:enumerator}`B_GRAY1` and {cpp:enumerator}`B_RGB32` to
{cpp:enumerator}`B_CMAP8`.

-   {cpp:enumerator}`B_CMAP8` and {cpp:enumerator}`B_GRAY1` to
{cpp:enumerator}`B_RGB32`.

:::{admonition} Note
:class: note
These are the only color conversions {hmethod}`SetBits()` understands; all
other conversions must be performed manually.
:::

Colors may be dithered in a conversion to {cpp:enumerator}`B_CMAP8` so
that the resulting image will match the original as closely as possible,
despite the lost information.

If the color space {hparam}`mode` is {cpp:enumerator}`B_RGB32`, the
{hparam}`data` should be triplets of three 8-bit components—red, green, and
blue, in that order—without an alpha component. Although stored as 32-bit
quantities with the components in BGRA order, the input data is only 24
bits in RGB order. Rows of source data do not need to be aligned.

However, if the source data is in any {hparam}`mode` other than
{cpp:enumerator}`B_RGB32`, padding must be added so that each row is
aligned on a {htype}`int32` word boundary.

:::{admonition} Warning
:class: warning
{hmethod}`SetBits()` works only on {hclass}`BBitmap`s in
{cpp:enumerator}`B_GRAY1`, {cpp:enumerator}`B_CMAP8`, and
{cpp:enumerator}`B_RGB32` color spaces; all other conversions must be
carried out manually.
:::

This function works for all {hclass}`BBitmap`s, whether or not
{cpp:class}`BView`s are also enlisted to produce the image.
::::

## Static Functions

::::{abi-group}
:::{cpp:function} static BArchivable* BBitmap::Instantiate(BMessage* archive)
:::

Returns a new {hclass}`BBitmap` object—or {cpp:expr}`NULL`, if the
{hparam}`archive` message doesn't contain data for a {hclass}`BBitmap`
object. The new object is allocated by new and created with the version of
the constructor that takes a {cpp:class}`BMessage` archive.

See also: {cpp:func}`BArchivable::Instantiate`,
{cpp:func}`instantiate_object() <instantiate::object>`,
{cpp:func}`Archive() <BBitmap::Archive>`
::::

## Archived Fields

The {cpp:func}`Archive() <BBitmap::Archive>` function adds the following
fields to its {cpp:class}`BMessage` argument:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Field

	- Type code

	- Description

-
	- {hparam}`_frame`

	- {cpp:enumerator}`B_RECT_TYPE`

	- The {hclass}`BBitmap`'s bounds rectangle.

-
	- {hparam}`_cspace`

	- {cpp:enumerator}`B_INT32_TYPE`

	- The color_space of the data.

-
	- {hparam}`_view_ok`

	- {cpp:enumerator}`B_BOOL_TYPE`

	- Always {cpp:expr}`true`, indicating the {hclass}`BBitmap` accepts views
(only present in deep copy archives of {hclass}`BBitmap`s accepting views).

-
	- {hparam}`_data`

	- {cpp:enumerator}`B_RAW_TYPE`

	- The bitmap data (present only if {hparam}`_view_ok` not present).

-
	- {hparam}`_continguous`

	- {cpp:enumerator}`B_BOOL_TYPE`

	- Whether the {hclass}`BBitmap` requires memory in one contiguous chunk.


:::

If the {hparam}`_view_ok` field is present, the child views of the BBitmap
are additionally archived in the {hparam}`_views` array of
{cpp:class}`BMessages`. See the description of the {cpp:class}`BView`
{cpp:func}`Archived Fields <BView::ArchivedFields>` for more information on
those fields.
