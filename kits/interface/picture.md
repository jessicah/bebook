:::{cpp:class} BPicture
:::

# BPicture

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BPicture::BPicture()
:::

:::{cpp:function} BPicture::BPicture(const BPicture& picture)
:::

:::{cpp:function} BPicture::BPicture(BMessage* archive)
:::

Initializes the {hclass}`BPicture` object by ensuring that it's empty, or
by copying data from another picture or archive of a {hclass}`BPicture`
object.
::::

::::{abi-group}
:::{cpp:function} virtual BPicture::~BPicture()
:::

Destroys the Application Server's record of the {hclass}`BPicture` object
and deletes all its picture data.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} virtual status_t BPicture::Archive(BMessage* archive, bool deep = true) const
:::

Archives the {hclass}`BPicture` by recording its current settings in the
{cpp:class}`BMessage` {hparam}`archive`.

See also: {cpp:func}`BArchivable::Archive`, {cpp:func}`Instantiate()
<BPicture::Instantiate>` static function
::::

::::{abi-group}
:::{cpp:function} virtual status_t* BPicture::Play(void** callBackTable, int32 tableEntries, void* user)
:::

Plays back a picture using a user's rendering functions. The functions are
passed in {hparam}`callBackTable`, an array of function pointers.
{hparam}`tableEntries` contains the number of functions in the table. The
functions perform various tasks such as drawing lines and text.
{hparam}`user` is passed to each function, providing a hook for passing
additional data to the call back functions. The functions, along with their
positions in the call back table, are detailed below.

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Index

	- Function prototype

-
	- 0

	- no operation

-
	- 1

	- {hmethod}`MovePenBy`({htype}`void*` {hparam}`user`, {cpp:class}`BPoint`
delta)

-
	- 2

	- {hmethod}`StrokeLine`({htype}`void*` {hparam}`user`, {cpp:class}`BPoint`
{hparam}`start`, {cpp:class}`BPoint` {hparam}`end`)

-
	- 3

	- {hmethod}`StrokeRect`({htype}`void*` {hparam}`user`, BRect {hparam}`rect`)

-
	- 4

	- {hmethod}`FillRect`({htype}`void*` {hparam}`user`, BRect {hparam}`rect`)

-
	- 5

	- {hmethod}`StrokeRoundRect`({htype}`void*` {hparam}`user`, BRect
{hparam}`rect`, {cpp:class}`BPoint` {hparam}`radii`)

-
	- 6

	- {hmethod}`FillRoundRect`({htype}`void*` {hparam}`user`, BRect
{hparam}`rect`, {cpp:class}`BPoint` {hparam}`radii`)

-
	- 7

	- {hmethod}`StrokeBezier`({htype}`void*` {hparam}`user`,
{cpp:class}`BPoint`* {hparam}`control`)

-
	- 8

	- {hmethod}`FillBezier`({htype}`void*` {hparam}`user`, {cpp:class}`BPoint`*
{hparam}`control`)

-
	- 9

	- {hmethod}`StrokeArc`({htype}`void*` {hparam}`user`, {cpp:class}`BPoint`
{hparam}`center`, {cpp:class}`BPoint` {hparam}`radii`, {htype}`float`
{hparam}`startTheta`, {htype}`float` {hparam}`arcTheta`)

-
	- 10

	- {hmethod}`FillArc`({htype}`void*` {hparam}`user`, {cpp:class}`BPoint`
{hparam}`center`, {cpp:class}`BPoint` {hparam}`radii`, float
{hparam}`startTheta`, float {hparam}`arcTheta`)

-
	- 11

	- {hmethod}`StrokeEllipse`({htype}`void*` {hparam}`user`,
{cpp:class}`BPoint` {hparam}`center`, {cpp:class}`BPoint` {hparam}`radii`)

-
	- 12

	- {hmethod}`FillEllipse`({htype}`void*` {hparam}`user`, {cpp:class}`BPoint`
{hparam}`center`, {cpp:class}`BPoint` {hparam}`radii`)

-
	- 13

	- {hmethod}`StrokePolygon`({htype}`void*` {hparam}`user`, int32
{hparam}`numPoints`, {cpp:class}`BPoint`* {hparam}`points`, bool
{hparam}`isClosed`)

-
	- 14

	- {hmethod}`FillPolygon`({htype}`void*` {hparam}`user`, int32
{hparam}`numPoints`, {cpp:class}`BPoint`* {hparam}`points`, bool
{hparam}`isClosed`)

-
	- 15

	- Reserved

-
	- 16

	- Reserved

-
	- 17

	- {hmethod}`DrawString`({htype}`void*` {hparam}`user`, char*
{hparam}`string`, float {hparam}`deltax`, float {hparam}`deltay`)

-
	- 18

	- {hmethod}`DrawPixels`({htype}`void*` {hparam}`user`, BRect {hparam}`src`,
BRect {hparam}`dest`, int32 {hparam}`width`, int32 {hparam}`height`, int32
{hparam}`bytesPerRow`, int32 {hparam}`pixelFormat`, int32 {hparam}`flags`,
{htype}`void*` {hparam}`data`)

-
	- 19

	- Reserved

-
	- 20

	- {hmethod}`SetClippingRects`({htype}`void*` {hparam}`user`, BRect*
{hparam}`rects`, uint32 {hparam}`numRects`)

-
	- 21

	- Reserved

-
	- 22

	- {hmethod}`PushState`({htype}`void*` {hparam}`user`)

-
	- 23

	- {hmethod}`PopState`({htype}`void*` {hparam}`user`)

-
	- 24

	- {hmethod}`EnterStateChange`({htype}`void*` {hparam}`user`)

-
	- 25

	- {hmethod}`ExitStateChange`({htype}`void*` {hparam}`user`)

-
	- 26

	- {hmethod}`EnterFontState`({htype}`void*` {hparam}`user`)

-
	- 27

	- {hmethod}`ExitFontState`({htype}`void*` {hparam}`user`)

-
	- 28

	- {hmethod}`SetOrigin`({htype}`void*` {hparam}`user`, {cpp:class}`BPoint`
{hparam}`pt`)

-
	- 29

	- {hmethod}`SetPenLocation`({htype}`void*` {hparam}`user`,
{cpp:class}`BPoint` {hparam}`pt`)

-
	- 30

	- {hmethod}`SetDrawingMode`({htype}`void*` {hparam}`user`, drawing_mode
{hparam}`mode`)

-
	- 31

	- {hmethod}`SetLineMode`({htype}`void*` {hparam}`user`, cap_mode
{hparam}`capMode`, join_mode {hparam}`joinMode`, float
{hparam}`miterLimit`)

-
	- 32

	- {hmethod}`SetPenSize`({htype}`void*` {hparam}`user`, float {hparam}`size`)

-
	- 33

	- {hmethod}`SetForeColor`({htype}`void*` {hparam}`user`, rgb_color
{hparam}`color`)

-
	- 34

	- {hmethod}`SetBackColor`({htype}`void*` {hparam}`user`, rgb_color
{hparam}`color`)

-
	- 35

	- {hmethod}`SetStipplePattern`({htype}`void*` {hparam}`user`, pattern
{hparam}`p`)

-
	- 36

	- {hmethod}`SetScale`({htype}`void*` {hparam}`user`, float {hparam}`scale`)

-
	- 37

	- {hmethod}`SetFontFamily`({htype}`void*` {hparam}`user`, char*
{hparam}`family`)

-
	- 38

	- {hmethod}`SetFontStyle`({htype}`void*` {hparam}`user`, char*
{hparam}`style`)

-
	- 39

	- {hmethod}`SetFontSpacing`({htype}`void*` {hparam}`user`, int32
{hparam}`spacing`)

-
	- 40

	- {hmethod}`SetFontSize`({htype}`void*` {hparam}`user`, float
{hparam}`size`)

-
	- 41

	- {hmethod}`SetFontRotate`({htype}`void*` {hparam}`user`, float
{hparam}`rotation`)

-
	- 42

	- {hmethod}`SetFontEncoding`({htype}`void*` {hparam}`user`, int32
{hparam}`encoding`)

-
	- 43

	- {hmethod}`SetFontFlags`({htype}`void*` {hparam}`user`, int32
{hparam}`flags`)

-
	- 44

	- {hmethod}`SetFontShear`({htype}`void*` {hparam}`user`, float
{hparam}`shear`)

-
	- 45

	- Reserved

-
	- 46

	- {hmethod}`SetFontFace`({htype}`void*` {hparam}`user`, int32
{hparam}`flags`)


:::

While many of these functions are similar to those found in
{cpp:class}`BView`, there are some important differences:

-   The return value of the functions is ignored.

-   The {hmethod}`Fill…()` and {hmethod}`Stroke…()` functions do not
explicitly specify patterns. Instead, they should be drawn in the current
pattern, as set by the {hmethod}`SetStipplePattern()` (callback #35). Note
that there is no equivalent to {hmethod}`SetStipplePattern()` in
{cpp:class}`BView`.

-   The {hparam}`deltax` and {hparam}`deltay` arguments passed to
{hmethod}`DrawString()` are escapement delta values; the string should be
drawn at the current pen position.

-   {hmethod}`MovePenBy()` uses a {cpp:class}`BPoint` to specify the amount to
move the pen. The x component of the {cpp:class}`BPoint` gives the x offset
and the y component the y offset.

-   Similarly, {hmethod}`…RoundRect()` and {hmethod}`…Ellipse()` use a
{cpp:class}`BPoint` to specify the two separate radius components. The
{hparam}`x` component gives the x radius and the {hparam}`y` component the
y radius.

-   {hmethod}`DrawPixels()` is a {hclass}`BPicture`-specific primitive for
rendering bitmaps. It is a request to copy the {hparam}`src` rectangle from
the raw color information in {hparam}`data` to the {hparam}`dest` rectangle
of the current rendering area. {hparam}`width`, {hparam}`height`,
{hparam}`bytesPerRow`, and {hparam}`pixelFormat` provide all the
information necessary to interpret data. {hparam}`flags` is currently
always zero and should be ignored. {hparam}`src` and {hparam}`dest` need
not have the same dimensions; in these cases, the function should scale the
bitmap appropriately.

-   {hmethod}`SetClippingRects()` is a {hclass}`BPicture`-specific primitive
approximating {hmethod}`ConstrainClippingRegion()`. It instructs the
renderer to replace the current clipping region with the union of the
rectangles passed to SetClippingRects().

-   Changes in the graphics state are sandwiched between calls to
{hmethod}`EnterStateChange()` and {hmethod}`ExitStateChange()`. State
change functions will only be called between these functions. No other call
backs will be called between these functions. State change functions are
all {hmethod}`Set…()` functions in addition to {hmethod}`EnterFontState()`
and {hmethod}`ExitFontState()`.

-   Similarly, changes to the font state are sandwiched between calls to
{hmethod}`EnterFontState()` and {hmethod}`ExitFontState()`. Font state
change functions will only be called between these functions. No other call
backs will be called between these functions. Font state change functions
are all {hmethod}`SetFont…()` functions. Many of the font state functions
are found in BFont rather than {cpp:class}`BView`.

-   {hmethod}`SetFontRotate()` sets the rotation of the font. Unlike the
{cpp:func}`BFont::SetRotation` function, the angle here is specified in
radians, rather than in degrees. You can convert the value into degrees by
using the forumla:

  :::{code} cpp
degrees = (rotation*180.0) / 3.14159265369);
:::

    
::::

## Static Functions

::::{abi-group}
:::{cpp:function} static BArchivable* BPicture::Instantiate(BMessage* archive)
:::

Returns a new {hclass}`BPicture` object, allocated by new and created with
the version of the constructor that takes a {cpp:class}`BMessage` archive.
However, if the archive message doesn't contain data for a
{hclass}`BPicture` object, this function returns {cpp:expr}`NULL`.

See also: {cpp:func}`BArchivable::Instantiate`,
{cpp:func}`instantiate_object() <instantiate::object>`,
{cpp:func}`Archive() <BPicture::Archive>`
::::

## Archived Fields

The {cpp:func}`Archive() <BArchivable::Archive>` function adds the
following fields to its {cpp:class}`BMessage` argument:

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
	- {hparam}`_ver`

	- {cpp:enumerator}`B_INT32_TYPE`

	- Always 1.

-
	- {hparam}`_endian`

	- {cpp:enumerator}`B_INT8_TYPE`

	- Endianness of the data. Always {cpp:enumerator}`B_HOST_IS_BENDIAN`.

-
	- {hparam}`_data`

	- {cpp:enumerator}`B_RAW_TYPE`

	- The {hclass}`BPicture` data.


:::
