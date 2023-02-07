# BPicture
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BPicture::BPicture()
:::
:::{cpp:function} BPicture::BPicture(const BPicture& picture)
:::
:::{cpp:function} BPicture::BPicture(BMessage* archive)
:::

Initializes the {hclass}`BPicture` object by ensuring that it's empty, or by
copying data from another picture or archive of a {hclass}`BPicture` object.

::::

::::{abi-group}

:::{cpp:function} virtual BPicture::~BPicture()
:::

Destroys the Application Server's record of the
{hclass}`BPicture` object and deletes all its picture data.

::::

## Member Functions
::::{abi-group}

:::{cpp:function} virtual status_t BPicture::Archive(BMessage* archive, bool deep = true) const
:::

Archives the {hclass}`BPicture` by
recording its current settings in the
{cpp:class}`BMessage`
{hparam}`archive`.

See also:
{cpp:func}`BArchivable::Archive`,
{cpp:func}`~BPicture::Instantiate`
static function

::::

::::{abi-group}

:::{cpp:function} virtual status_t* BPicture::Play(void** callBackTable, int32 tableEntries, void* user)
:::

Plays back a picture using a user's rendering functions. The functions
are passed in {hparam}`callBackTable`, an array of function pointers.
{hparam}`tableEntries`
contains the number of functions in the table. The functions perform
various tasks such as drawing lines and text. {hparam}`user` is passed to each
function, providing a hook for passing additional data to the call back
functions. The functions, along with their positions in the call back
table, are detailed below.

IndexFunction prototype0no operation1MovePenBy(void* user, BPoint delta)2StrokeLine(void* user, BPoint start, BPoint end)3StrokeRect(void* user, BRect rect)4FillRect(void* user, BRect rect)5StrokeRoundRect(void* user, BRect rect, BPoint radii)6FillRoundRect(void* user, BRect rect, BPoint radii)7StrokeBezier(void* user, BPoint* control)8FillBezier(void* user, BPoint* control)9StrokeArc(void* user, BPoint center, BPoint radii, float startTheta, float arcTheta)10FillArc(void* user, BPoint center, BPoint radii, float startTheta, float arcTheta)11StrokeEllipse(void* user, BPoint center, BPoint radii)12FillEllipse(void* user, BPoint center, BPoint radii)13StrokePolygon(void* user, int32 numPoints, BPoint* points, bool isClosed)14FillPolygon(void* user, int32 numPoints, BPoint* points, bool isClosed)15Reserved16Reserved17DrawString(void* user, char* string, float deltax, float deltay)18DrawPixels(void* user, BRect src, BRect dest, int32 width, int32 height, int32 bytesPerRow, int32 pixelFormat, int32 flags, void* data)19Reserved20SetClippingRects(void* user, BRect* rects, uint32 numRects)21Reserved22PushState(void* user)23PopState(void* user)24EnterStateChange(void* user)25ExitStateChange(void* user)26EnterFontState(void* user)27ExitFontState(void* user)28SetOrigin(void* user, BPoint pt)29SetPenLocation(void* user, BPoint pt)30SetDrawingMode(void* user, drawing_mode mode)31SetLineMode(void* user, cap_mode capMode, join_mode joinMode, float miterLimit)32SetPenSize(void* user, float size)33SetForeColor(void* user, rgb_color color)34SetBackColor(void* user, rgb_color color)35SetStipplePattern(void* user, pattern p)36SetScale(void* user, float scale)37SetFontFamily(void* user, char* family)38SetFontStyle(void* user, char* style)39SetFontSpacing(void* user, int32 spacing)40SetFontSize(void* user, float size)41SetFontRotate(void* user, float rotation)42SetFontEncoding(void* user, int32 encoding)43SetFontFlags(void* user, int32 flags)44SetFontShear(void* user, float shear)45Reserved46SetFontFace(void* user, int32 flags)

While many of these functions are similar to those found in {cpp:class}`BView`, there
are some important differences:

- The return value of the functions is ignored.
- The {hmethod}`Fill…()` and {hmethod}`Stroke…()` functions do not explicitly specify patterns. Instead, they should be drawn in the current pattern, as set by the {hmethod}`SetStipplePattern()` (callback #35). Note that there is no equivalent to {hmethod}`SetStipplePattern()` in {cpp:class}`BView`.
- The {hparam}`deltax` and {hparam}`deltay` arguments passed to {hmethod}`DrawString()` are escapement delta values; the string should be drawn at the current pen position.
- {hmethod}`MovePenBy()` uses a {cpp:class}`BPoint` to specify the amount to move the pen. The x component of the {cpp:class}`BPoint` gives the x offset and the y component the y offset.
- Similarly, {hmethod}`…RoundRect()` and {hmethod}`…Ellipse()` use a {cpp:class}`BPoint` to specify the two separate radius components. The x component gives the x radius and the y component the y radius.
- {hmethod}`DrawPixels()` is a {hclass}`BPicture`-specific primitive for rendering bitmaps. It is a request to copy the {hparam}`src` rectangle from the raw color information in {hparam}`data` to the {hparam}`dest` rectangle of the current rendering area. {hparam}`width`, {hparam}`height`, {hparam}`bytesPerRow`, and {hparam}`pixelFormat` provide all the information necessary to interpret data. {hparam}`flags` is currently always zero and should be ignored. {hparam}`src` and {hparam}`dest` need not have the same dimensions; in these cases, the function should scale the bitmap appropriately.
- {hmethod}`SetClippingRects()` is a {hclass}`BPicture`-specific primitive approximating {hmethod}`ConstrainClippingRegion()`. It instructs the renderer to replace the current clipping region with the union of the rectangles passed to SetClippingRects().
- Changes in the graphics state are sandwiched between calls to {hmethod}`EnterStateChange()` and {hmethod}`ExitStateChange()`. State change functions will only be called between these functions. No other call backs will be called between these functions. State change functions are all {hmethod}`Set…()` functions in addition to {hmethod}`EnterFontState()` and {hmethod}`ExitFontState()`.
- Similarly, changes to the font state are sandwiched between calls to {hmethod}`EnterFontState()` and {hmethod}`ExitFontState()`. Font state change functions will only be called between these functions. No other call backs will be called between these functions. Font state change functions are all {hmethod}`SetFont…()` functions. Many of the font state functions are found in BFont rather than {cpp:class}`BView`.
- {hmethod}`SetFontRotate()` sets the rotation of the font. Unlike the {cpp:func}`BFont::SetRotation` function, the angle here is specified in radians, rather than in degrees. You can convert the value into degrees by using the forumla:degrees = (rotation*180.0) / 3.14159265369);

::::

## Static Functions
::::{abi-group}

:::{cpp:function} static BArchivable* BPicture::Instantiate(BMessage* archive)
:::

Returns a new {hclass}`BPicture` object, allocated by new and created with the
version of the constructor that takes a {cpp:class}`BMessage`
archive. However, if the
archive message doesn't contain data for a {hclass}`BPicture` object, this
function returns {cpp:enum}`NULL`.

See also:
{cpp:func}`BArchivable::Instantiate`,
{cpp:func}`~instantiate::object`,
{cpp:func}`~BPicture::Archive`

::::

## Archived Fields