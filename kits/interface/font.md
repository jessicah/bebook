:::{cpp:class} BFont
:::

# BFont

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BFont::BFont(const BFont& font)
:::

:::{cpp:function} BFont::BFont(const BFont* font)
:::

:::{cpp:function} BFont::BFont()
:::

Initializes the new {hclass}`BFont` object as a copy of another font. If
no font is specified, {cpp:enumerator}`be_plain_font` is used.

The system {hclass}`BFont` objects, including
{cpp:enumerator}`be_plain_font`, are initialized only when you create a
{cpp:class}`BApplication` object for your application. Therefore, the
default settings of {hclass}`BFont` objects constructed before the
{cpp:class}`BApplication` object will be invalid.

See also: {cpp:func}`BView::SetFont`,
{cpp:func}`BTextView::SetFontAndColor`
::::

## Member Functions

::::{abi-group}
:::{cpp:function} unicode_block BFont::Blocks() const
:::

Returns a {htype}`unicode_block` object that identifies which Unicode
blocks the font supports. You can then use the
{hmethod}`unicode_block::Includes()` function to determine if specific
blocks are supported.
::::

::::{abi-group}
:::{cpp:function} BRect BFont::BoundingBox() const
:::

Returns a {cpp:class}`BRect` that can enclose the entire font in its
current style and size.
::::

::::{abi-group}
:::{cpp:function} font_direction BFont::Direction() const
:::

{hmethod}`Direction()` returns a {htype}`font_direction` constant that
describes the direction in which the object's text is meant to be read:

-   {cpp:enumerator}`B_FONT_LEFT_TO_RIGHT`

-   {cpp:enumerator}`B_FONT_RIGHT_TO_LEFT`

This is an inherent property of the font and cannot be set.

The direction of the font affects the direction in which
{cpp:func}`DrawString() <BView::DrawString>` draws the characters in a
string, but not the direction in which it moves the pen.

See also: {cpp:func}`BView::DrawString`
::::

::::{abi-group}
:::{cpp:function} font_file_format BFont::FileFormat() const
:::

Returns the {ref}`file format` of the font (ie, whether it's a PostScript™
or TrueType™ font).
::::

::::{abi-group}
:::{cpp:function} void BFont::GetBoundingBoxesAsGlyphs(const char charArray[], int32 numChars, font_metric_mode mode, BRect boundingBoxArray[]) const
:::

:::{cpp:function} void BFont::GetBoundingBoxesAsString(const char string[], int32 numChars, font_metric_mode mode, escapement_delta* delta, BRect boundingBoxArray[]) const
:::

:::{cpp:function} void BFont::GetBoundingBoxesForStrings(const char *stringArray[], int32 numStrings, font_metric_mode mode, escapement_delta* deltas[], BRect boundingBoxArray[]) const
:::

{hmethod}`GetBoundingBoxesAsGlyphs()` returns an array of
{cpp:class}`BRect` objects indicating the bounding rectangles of all the
characters in an array. Each {cpp:class}`BRect` returned corresponds to one
character's glyph.

{hmethod}`GetBoundingBoxesAsString()` returns an array of
{cpp:class}`BRect` objects indicating the bounding rectangles of each
character in a {hparam}`string`.

{hmethod}`GetBoundingBoxesForStrings()` returns an array of
{cpp:class}`BRect` objects indicating the bounding rectangles for an array
of strings, one {cpp:class}`BRect` per string. These rectangles enclose the
entire string they represent.

In all cases, the {hparam}`mode` indicates whether the rectangles should
be returned in the screen's metric ({cpp:enumerator}`B_SCREEN_METRIC`), or
in printing metrics ({cpp:enumerator}`B_PRINTING_METRIC`).

The {hparam}`delta` argument for {hmethod}`GetBoundingBoxesAsString()` and
the {hparam}`deltas` argument for {hmethod}`GetBoundingBoxesForStrings()`
indicate escapement deltas that should be applied when making the bounding
box calculations. This lets you indicate that the characters should be
closer together or further apart than normal, for example.
::::

::::{abi-group}
:::{cpp:function} void BFont::GetEscapements(const char charArray[], int32 numChars, float escapementArray[]) const
:::

:::{cpp:function} void BFont::GetEscapements(const char charArray[], int32 numChars, escapement_delta* delta, float escapementArray[]) const
:::

:::{cpp:function} void BFont::GetEscapements(const char charArray[], int32 numChars, escapement_delta* delta, BPoint escapementArray[]) const
:::

:::{cpp:function} void BFont::GetEscapements(const char charArray[], int32 numChars, escapement_delta* delta, BPoint escapementArray[], BPoint offsetArray[]) const
:::

:::{cpp:function} void BFont::GetEdges(const char charArray[], int32 numChars, edge_info edgeArray[]) const
:::

:::{code}
struct escapement_delta {
    float nonspace;
    float space;
}
:::

:::{code}
struct edge_info {
    float left;
    float right;
}
:::

These two functions provide the information required to precisely position
characters on the screen or printed page. For each character passed in the
{hparam}`charArray`, they write information about the horizontal dimension
of the character into the {hparam}`escapementArray` or the
{hparam}`edgeArray`. Both functions provide this information in "escapement
units" that yield standard coordinate units (72.0 per inch) when multiplied
by the font size.

{hmethod}`GetEscapements()` and {hmethod}`GetEdges()` expect the character
array they're passed to contain at least {hparam}`numChar` characters;
neither function checks the {hparam}`charArray` for a null terminator.
Because the array may hold multibyte characters (in
{cpp:enumerator}`B_UNICODE_UTF8` encoding), the number of bytes in the
array may be greater than the number of characters specified. The
{hparam}`escapementArray` and {hparam}`edgeArray` should be long enough to
hold an output value for every input character.

You can optionally request that escapement information be returned as an
array of {cpp:class}`BPoint` objects.

#### Escapements

A character's escapement measures the amount of horizontal space it
requires. It includes the space needed to display the character itself,
plus some extra room on the left and right edges to separate the character
from its neighbors. The illustration below shows the approximate
escapements for the letters 'l' and 'p'; the escapement for each character
is the distance between the vertical lines:

![Font Escapements](./images/TheInterfaceKit/font_escapement.png)

{hmethod}`GetEscapements()` measures the same space that functions such as
{cpp:func}`StringWidth() <BFont::StringWidth>` and {cpp:class}`BTextView`'s
{cpp:func}`LineWidth() <BTextView::LineWidth>` do, but it measures each
character individually and records its width in per-point-size escapement
units. To translate the escapement value to the width of the character, you
must multiply by the point size of the font:

:::{code} cpp
float width = escapementArray[i] * font.Size();
:::

Because of rounding errors, there may be some difference between the value
returned by {cpp:func}`StringWidth() <BFont::StringWidth>` and the width
calculated from the individual escapements of the characters in the string.

The versions of {hmethod}`GetEscapements()` that use {cpp:class}`BPoint`s
for the escapement value use the {cpp:class}`BPoint`
{hparam}`escapementArray` to indicate a vector by which the pen is moved
after drawing a character (this lets the escapement indicate both an X and
a Y adjustment; the Y might need to be adjusted if the font is rotated, for
example). The {hparam}`offsetArray` is applied by the dynamic spacing in
order to improve the relative position of the character's width with
relation to another character, without altering the width.

The escapement value is scalable if the spacing mode of the font is
{cpp:enumerator}`B_CHAR_SPACING`. In other words, given
{cpp:enumerator}`B_CHAR_SPACING` and the same set of font characteristics,
{hmethod}`GetEscapements()` will report the same measurement for a
character regardless of the font size. You can cache one value per
character and use it for all font sizes. For the other spacing modes, the
reported escapement depends on the font size and therefore can't be scaled.

For most spacing modes, a character has a constant escapement in all
contexts; it depends only on the font. However, for
{cpp:enumerator}`B_STRING_SPACING`, each character's escapement is also
contextually dependent on the string it's in. To find the escapement of a
character within a particular string, you must pass the entire string in
the input {hparam}`charArray`.

In the {cpp:enumerator}`B_BITMAP_SPACING` and
{cpp:enumerator}`B_FIXED_SPACING` modes, all characters have integral
widths (without a fractional part). For these modes, multiplying an
escapement by the font size should yield an integral value. In
{cpp:enumerator}`B_FIXED_SPACING` mode, all characters have the same
escapement.

If a {hparam}`delta` argument is provided, {hmethod}`GetEscapements()`
will adjust the escapements it reports so that, after multiplying by the
font size, the character widths will include the specified increments. An
{htype}`escapement_delta` structure contains two values:

:::{list-table}
---
header-rows: 0
align: left
widths: auto
---
-
	- floatnonspace
	- The amount to add to the width of each character with a visible glyph.
-
	- floatspace
	- The amount to add to each whitespace character (characters like
		{cpp:enumerator}`B_TAB` and {cpp:enumerator}`B_SPACE` with an escapement
		but no visible glyph).

:::

A similar argument can be passed to {hclass}`BView`'s
{cpp:func}`DrawString() <BView::DrawString>`  to adjust the spacing of the
characters as they're drawn.

#### Edges

Edge values measure how far a character outline is inset from its left and
right escapement boundaries. {hmethod}`GetEdges()` places the edge values
into an array of {htype}`edge_info` structures. Each structure has a
{hparam}`left` and a {hparam}`right` data member, as follows:

:::{code}
typedef struct {
    float left;
    float right;
} edge_info;
:::

Edge values, like escapements, are stated in per-point-size units that
need to be multiplied by the font size.

The illustration below shows typical character edges. As in the
illustration above, the solid vertical lines mark escapement boundaries.
The dotted lines mark off the part of each escapement that's an edge, the
distance between the character outline and the escapement boundary:

This is the normal case. The left edge is a positive value measured
rightward from the left escapement boundary. The right edge is a negative
value measured leftward from the right escapement boundary.

However, if the characters of a font overlap, the left edge can be a
negative value and the right edge can be positive. This is illustrated
below:

Note that the italic '__l__' extends beyond its escapement to the right,
and that the '__p__' begins before its escapement to the left. In this
case, instead of separating the adjacent characters, the edges determine
how much they overlap.

Edge values are specific to each character and depend on nothing but the
character and the font. They don't take into account any contextual
information; for example, the right edge for italic 'l' would be the same
no matter what letter followed. Edge values therefore aren't sufficient to
decide how character pairs can be kerned. Kerning is contextually dependent
on the combination of two particular characters.

See also: {cpp:func}`StringWidth() <BFont::StringWidth>`,
{cpp:func}`SetSpacing() <BFont::SetSpacing>`
::::

::::{abi-group}
:::{cpp:function} void BFont::GetGlyphShapes(const char charArray[], int32 numChars, BShape* glyphShapeArray[]) const
:::

Given an array of characters, {hparam}`charArray`, which contains
{hparam}`numChars` characters, and an array of {cpp:class}`BShape` objects,
{hparam}`glyphShapeArray`, this function makes each element in the
{hparam}`glyphShapeArray` describe the shape of the corresponding glyph in
the {hparam}`charArray`.

This lets you create {cpp:class}`BShape` objects in the shape of the
outline of a font. You can then manipulate these {cpp:class}`BShape`s to do
interesting text effects.

:::{admonition} Warning
:class: warning
The {hparam}`glyphShapeArray` must contain already-allocated
{cpp:class}`BShape` objects. They will be cleared by this function before
the glyphs' shapes are constructed into them, but the objects must already
exist.
:::

Fonts are drawn one pixel above the logical baseline; this affects
{cpp:class}`BShape` objects derived from fonts, too. The fonts are also one
pixel above the baseline in the {cpp:class}`BShape`s this function returns.
If you want to apply a transform to these shapes, be sure to remove the
offset before applying the transform, then add the offset back to the
points before drawing the shape, or you won't get the expected results.
::::

::::{abi-group}
:::{cpp:function} void BFont::GetHasGlyphs(const char charArray[], int32 numChars, bool hasArray[]) const
:::

Given an array of characters in {hparam}`charArray` (of which there are
{hparam}`numChars` members), this function fills out the array of booleans
specified by {hparam}`hasArray` such that each entry in {hparam}`hasArray`
is {cpp:expr}`true` if the corresponding character in {hparam}`charArray`
has a glyph in the font, and {cpp:expr}`false` if the character doesn't
have a glyph.

This way, you can determine if you can use one or more characters without
the user seeing "no glyph" symbols.
::::

::::{abi-group}
:::{cpp:function} void BFont::GetHeight(font_height* height) const
:::

:::{code}
struct font_height {
    float ascent;
    float descent;
    float leading;
}
:::

{hmethod}`GetHeight()` writes the three components that determine the
height of the font into the structure that the height argument refers to.
{htype}`A font_height` structure has the following fields:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Field

	- Description

-
	- floatascent
	- How far characters can ascend above the baseline.
-
	- floatdescent
	- How far characters can descend below the baseline.
-
	- floatleading
	- How much space separates lines (the distance between the descent of the
		line above and the ascent of the line below).

:::

If you need to round the font height, or any of its components, to an
integral value (to figure the spacing between lines of text on-screen, for
example), you should always round them up to reduce the amount of vertical
character overlap.

See also: {cpp:func}`BView::GetFontHeight`
::::

::::{abi-group}
:::{cpp:function} void BFont::GetTruncatedStrings(const char* inputStringArray[], int32 numChars, uint32 mode, float maxWidth, const char* truncatedStringArray[]) const
:::

:::{cpp:function} void BFont::GetTruncatedStrings(const char* inputStringArray[], int32 numChars, uint32 mode, float maxWidth, const BString truncatedStringArray[]) const
:::

:::{cpp:function} void BFont::TruncateString(BString* inOutString[], uint32 mode, float maxWidth) const
:::

{hmethod}`GetTruncatedStrings()` truncates a set of strings so that each
one (and an ellipsis to show where the string was cut) will fit into the
{hparam}`maxWidth` horizontal space. This function is useful for shortening
long strings that are displayed to the user—for showing path names in a
list, for example.

The {hparam}`numStrings` argument states how many strings in the
{hparam}`inputStringArray` should be shortened. The {hparam}`mode` argument
states where the string should be cut. It can be:

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
	- {cpp:enumerator}`B_TRUNCATE_BEGINNING`
	- Cut from the beginning of the string until it fits within the specified
		width.
-
	- {cpp:enumerator}`B_TRUNCATE_MIDDLE`
	- Cut from the middle of the string.
-
	- {cpp:enumerator}`B_TRUNCATE_END`
	- Cut from the end of the string.
-
	- {cpp:enumerator}`B_TRUNCATE_SMART`
	- Cut anywhere, but do so intelligently, so that all the strings remain
		different after being cut. For example, if a set of similar path names are
		passed in the {hparam}`inputStringArray`, this mode would attempt to cut
		from the identical parts of the path names and preserve the parts that are
		different. This mode also pays attention to word boundaries, separators,
		punctuation, and the like. However, it's not implemented for the current
		release.

:::

Each output string is written to the {hparam}`truncatedStringArray`—into
memory that the caller must provide—at an index that matches the index of
the full string in the {hparam}`inputStringArray`. The
{hparam}`truncatedStringArray` is a list of pointers to string buffers.
Each buffer should be allocated separately and should be at least 3 bytes
longer than the matching input string. The 3 bytes allow for the worst-case
scenario: {hmethod}`GetTruncatedStrings()` cuts a one-byte character from
the input string and replaces it with an ellipsis character, which takes
three bytes in UTF-8 encoding, for a net gain of 2 bytes. It then adds a
null terminator for the third byte.

{hmethod}`TruncateString()` truncates the {cpp:class}`BString`
{hparam}`inOutString` to be no longer than the width specified by
{hparam}`maxWidth`, using the given truncation mode.

The output strings are null-terminated. The input strings should likewise
be null-terminated.

See also: {cpp:func}`StringWidth() <BFont::StringWidth>`
::::

::::{abi-group}
:::{cpp:function} void BFont::GetTunedInfo(int32* index, tuned_font_info* info) const
:::

:::{cpp:function} int32 BFont::CountTuned() const
:::

:::{code}
struct tuned_font_info {
      float size;
      float shear;
      float rotation;
      uint32 flags;
      uint16 face;
}
:::

These functions are used to get information about fonts that have been
"tuned" to look good when displayed on-screen. A tuned font is a set of
character bitmaps, originally produced from the standard outline font and
then modified so that the characters are well proportioned and spaced when
displayed at the low resolution of the screen (1 pixel per point).

Because it's a bitmap font, a tuned font captures a specific configuration
of font attributes, including size, style, shear, and rotation. A tuned
font is a counterpart to an outline font with the same settings. If a
{cpp:class}`BView`'s current font has a tuned counterpart,
{cpp:func}`DrawString() <BView::DrawString>` automatically chooses it when
drawing on-screen. Tuned fonts are not used for printing.

{hmethod}`CountTuned()` returns how many tuned fonts there are for the
family and style represented by the {hclass}`BFont` object.
{hmethod}`GetTunedInfo()` writes information about the tuned font at
{hparam}`index` into the structure the {hparam}`info` argument refers to.
Indices begin at 0 and count only tuned fonts for the {hclass}`BFont`'s
family and style.

With this information, you can set the {hclass}`BFont` to values that
match those of a tuned font. When a {cpp:class}`BView` draws to the screen,
it picks a tuned font if there's one that corresponds to its current font
in all respects.

See also: {cpp:func}`get_font_family()`
::::

::::{abi-group}
:::{cpp:function} bool BFont::IsFixed() const
:::

Returns {cpp:expr}`true` if the font is fixed; {cpp:expr}`false`
otherwise.
::::

::::{abi-group}
:::{cpp:function} bool BFont::IsFullAndHalfFixed() const
:::

This function is not yet supported.
::::

::::{abi-group}
:::{cpp:function} void BFont::PrintToStream() const
:::

Writes the following information about the font to the standard output (on
a single line):

-   family

-   style

-   size (in points)

-   shear (in degrees)

-   rotation (in degrees)

-   ascent

-   descent

-   leading
::::

::::{abi-group}
:::{cpp:function} void BFont::SetEncoding(uint8 encoding)
:::

:::{cpp:function} uint8 BFont::Encoding() const
:::

These functions set and return the encoding that maps character values to
characters. The following encodings are supported:

-   {cpp:enumerator}`B_UNICODE_UTF8` (UTF-8)

-   {cpp:enumerator}`B_ISO_8859_1` (Latin 1)

-   {cpp:enumerator}`B_ISO_8859_2` (Latin 2)

-   {cpp:enumerator}`B_ISO_8859_3` (Latin 3)

-   {cpp:enumerator}`B_ISO_8859_4` (Latin 4)

-   {cpp:enumerator}`B_ISO_8859_5` (Latin/Cyrillic)

-   {cpp:enumerator}`B_ISO_8859_6` (Latin/Arabic)

-   {cpp:enumerator}`B_ISO_8859_7` (Latin/Greek)

-   {cpp:enumerator}`B_ISO_8859_8` (Latin/Hebrew)

-   {cpp:enumerator}`B_ISO_8859_9` (Latin 5)

-   {cpp:enumerator}`B_ISO_8859_10` (Latin 6)

-   {cpp:enumerator}`B_MACINTOSH_ROMAN`

UTF-8 is an 8-bit encoding for Unicode™ and is part of the Unicode™
standard. It matches ASCII values for all 7-bit character codes, but uses
multibyte characters for values over 127. The other encodings take only a
single byte to represent a character; they therefore necessarily encompass
a far smaller set of characters. Most of them represent standards in the
ISO/IEC 8859 family of character codes that extend the ASCII set.
{cpp:enumerator}`B_MACINTOSH_ROMAN` stands for the standard encoding used
by the Mac OS™.

The encoding affects both input and output functions of the
{cpp:class}`BView`. It determines how {cpp:func}`DrawString()
<BView::DrawString>` interprets the character values it's passed and also
how {cpp:func}`KeyDown() <BView::KeyDown>` encodes character values for the
keys the user pressed.

UTF-8 is the preferred encoding and the one that's most compatible with
objects defined in the software kits. For example, a {cpp:class}`BTextView`
expects all text it takes from the clipboard or from a dragged and dropped
message to be UTF-8 encoded. If it isn't, the results are not defined. The
more that applications stick with UTF-8 encoding, the more freely they'll
be able to exchange data.

See also: "{ref}`Character Encoding`" {ref}`convert_to_utf8()`,
{cpp:func}`BView::DrawString`, {cpp:func}`BView::KeyDown`()
::::

::::{abi-group}
:::{cpp:function} void BFont::SetFace(uint16 face)
:::

:::{cpp:function} uint16 BFont::Face() const
:::

These functions set and return a mask that record secondary
characteristics of the font, such as whether characters are underlined or
drawn in outline. The values that form the face mask are:

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
	- {cpp:enumerator}`B_ITALIC_FACE`
	- Characters are drawn italicized.
-
	- {cpp:enumerator}`B_UNDERSCORE_FACE`
	- Characters are drawn underlined.
-
	- {cpp:enumerator}`B_NEGATIVE_FACE`
	- Characters are drawn in the low color, while the background is drawn in
		the high color.
-
	- {cpp:enumerator}`B_OUTLINED_FACE`
	- Characters are drawn hollow, with a line around their border, but
		unfilled.
-
	- {cpp:enumerator}`B_STRIKEOUT_FACE`
	- Characters are drawn "struck-out," with a line drawn horizontally through
		the middle.
-
	- {cpp:enumerator}`B_BOLD_FACE`
	- Characters are drawn in boldface.
-
	- {cpp:enumerator}`B_REGULAR_FACE`
	- Characters are drawn normally.

:::
::::

::::{abi-group}
:::{cpp:function} void BFont::SetFamilyAndFace(const font_family family, uint16 face)
:::

Sets the family and face of the font. The {hparam}`family` passed to this
function must be one of the families enumerated by the
{cpp:func}`get_font_family()` global function and {hparam}`face` must be a
combination of the face values described under {cpp:func}`SetFace()
<BFont::SetFace>`. If the family is {cpp:expr}`NULL`,
{hmethod}`SetFamilyAndFace()` sets only the face.
::::

::::{abi-group}
:::{cpp:function} void BFont::SetFamilyAndStyle(const font_family family, const font_style style)
:::

:::{cpp:function} void BFont::SetFamilyAndStyle(uint32 code)
:::

:::{cpp:function} void BFont::GetFamilyAndStyle(font_family* family, font_style* style) const
:::

:::{cpp:function} uint32 BFont::FamilyAndStyle() const
:::

:::{code} c
typedef char font_family[B_FONT_FAMILY_LENGTH + 1]
:::

:::{code} c
typedef char font_style[B_FONT_STYLE_LENGTH + 1]
:::

{hmethod}`SetFamilyAndStyle()` sets the family and style of the font. The
{hparam}`family` passed to this function must be one of the families
enumerated by the {cpp:func}`get_font_family()` global function and
{hparam}`style` must be one of the styles associated with that family, as
reported by {ref}`get_font_style()`. If the {hparam}`family` is
{cpp:expr}`NULL`, {hmethod}`SetFamilyAndStyle()` sets only the style; if
{hparam}`style` is {cpp:expr}`NULL`, it sets only the family.

{hmethod}`GetFamilyAndStyle()` writes the names of the current family and
style into the {hparam}`font_value` and {hparam}`font_style` variables
provided.

Internally, the {hclass}`BFont` class encodes each family and style
combination as a unique integer. {hmethod}`FamilyAndStyle()` returns that
code, which can then be passed to {hmethod}`SetFamilyAndStyle()` to set
another {hclass}`BFont` object. The integer code is not persistent; its
meaning may change when the list of installed fonts changes and when the
machine is rebooted.
::::

::::{abi-group}
:::{cpp:function} void BFont::SetFlags(uint32 flags)
:::

:::{cpp:function} uint32 BFont::Flags() const
:::

These functions set and return a mask that records various behaviors of
the font. There are two flags: {cpp:enumerator}`B_DISABLE_ANTIALIASING`,
which turns off all antialiasing for characters displayed in the font, and
{cpp:enumerator}`B_FORCE_ANTIALIASING`, which forces all font rendering to
be anti-aliased. The default mask has antialiasing turned on.
::::

::::{abi-group}
:::{cpp:function} void BFont::SetRotation(float rotation)
:::

:::{cpp:function} float BFont::Rotation() const
:::

These functions set and return the rotation of the baseline for characters
displayed in the font. The baseline rotates counterclockwise from an axis
on the left side of the character. The default (horizontal) baseline is at
0°. For example, this code

:::{code} cpp
BFont font;
font.SetRotation(45.0);
myView->SetFont(&font, B_FONT_ROTATION);
myView->DrawString("to the northeast");
:::

would draw a string that extended upwards and to the right.

Rotation is not supported by some Interface Kit classes, including
{cpp:class}`BTextView`.
::::

::::{abi-group}
:::{cpp:function} void BFont::SetShear(float shear)
:::

:::{cpp:function} float BFont::Shear() const
:::

These functions set and return the angle at which characters are drawn
relative to the baseline. The default (perpendicular) shear for all font
styles, including oblique and italic ones, is 90.0°. The shear is measured
counterclockwise and can be adjusted within the range 45.0° (slanted to the
right) through 135.0° (slanted to the left). If the shear passed falls
outside this range, it will be adjusted to the closest value within range.
::::

::::{abi-group}
:::{cpp:function} void BFont::SetSize(float size)
:::

:::{cpp:function} float BFont::Size() const
:::

These functions set and return the size of the font in points. Valid sizes
range from less than 1.0 point through 10,000 points.

See also: {cpp:func}`BView::SetFontSize`
::::

::::{abi-group}
:::{cpp:function} void BFont::SetSpacing(uint8 spacing)
:::

:::{cpp:function} uint8 BFont::Spacing() const
:::

These functions set and return the mode that determines how characters are
horizontally spaced relative to each other when they're drawn. The mode
also affects the width or "escapement" of each character as reported by
{cpp:func}`GetEscapements() <BFont::GetEscapements>`.

There are four spacing modes:

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
	- {cpp:enumerator}`B_CHAR_SPACING`
	- Positions each character according to its own inherent width, without
		adjustment. This produces good results on high-resolution devices like
		printers, and is the best mode to use for printing. However, when character
		widths are rounded for the screen, the results are generally poor.
		Characters are not well-separated and can collide or overlap at small font
		sizes.
-
	- {cpp:enumerator}`B_STRING_SPACING`
	- Keeps the string at the same width as it would have for
		{cpp:enumerator}`B_CHAR_SPACING`, but optimizes the position of each
		character within that space. The position of a character depends on the
		surrounding characters and the overall width of the string. Collisions are
		unlikely in this mode, but because the width of the string constrains what
		can be done, characters may touch each other.

		This mode is preferred when it's important to have the screen match the
		printed page—for example, to have lines break on-screen where they will
		break when the display is printed. As the user types new characters into a
		line of text, the application must redraw the entire line to add each
		character. The characters in the line may therefore appear to "jiggle" or
		jump around as new ones are added. New optimal positions are calculated for
		each character as the width and composition of the string changes.
-
	- {cpp:enumerator}`B_BITMAP_SPACING`
	- Calculates the width of each character according to its bitmap appearance
		on-screen. The widths are chosen for optimal spacing, so that characters
		never collide and rarely touch. This mode increases the
		{cpp:enumerator}`B_CHAR_SPACING` width of a string if necessary to keep
		characters separated. (For a small-sized bold font, it may increase the
		string width substantially.)

		In this mode, the spacing between characters is regular and not
		contextually dependent. Character widths are integral values. This is the
		best mode for drawing small amounts of text in the user interface; it's the
		mode that {cpp:class}`BTextView` objects use and it works for both
		proportional and fixed-width fonts. However, the spacing of text shown
		on-screen won't correspond to the spacing when the text is printed in
		{cpp:enumerator}`B_CHAR_SPACING` mode.
-
	- {cpp:enumerator}`B_FIXED_SPACING`
	- Positions characters according to a constant, integral width. This mode
		can only be used with fixed-width fonts (fonts with the
		{cpp:enumerator}`B_IS_FIXED` flag set); trying to use
		{cpp:enumerator}`B_FIXED_SPACING` on other fonts will result in
		{cpp:enumerator}`B_CHAR_SPACING` being used by default. All characters have
		the same escapement.

:::

The {cpp:enumerator}`B_CHAR_SPACING` mode is the preferred mode for
printing. It's also somewhat faster than {cpp:enumerator}`B_STRING_SPACING`
or {cpp:enumerator}`B_BITMAP_SPACING`. In all modes other than
{cpp:enumerator}`B_STRING_SPACING`, it's possible to change the character
displayed at the end of a string by erasing it and drawing a new character.
However, in {cpp:enumerator}`B_STRING_SPACING` mode, it's necessary to
erase the entire string and redraw it. The longer the string, the better
the results.

The {cpp:enumerator}`B_STRING_SPACING` and
{cpp:enumerator}`B_BITMAP_SPACING` modes are relevant only for font sizes
in a range of about 7.0 points to 18.0 points. Above that range,
{cpp:enumerator}`B_CHAR_SPACING` achieves reasonable results on-screen and
may be used even where one of the other two modes is specified. Below that
range, the screen resolution isn't great enough for the different modes to
produce significantly different results, so again
{cpp:enumerator}`B_CHAR_SPACING` is used.

In addition, {cpp:enumerator}`B_CHAR_SPACING` is always used for rotated
or sheared text and when antialiasing is disabled.

See also: {cpp:func}`BView::DrawString`, {cpp:func}`GetEscapements()
<BFont::GetEscapements>`
::::

::::{abi-group}
:::{cpp:function} float BFont::StringWidth(const char* string) const
:::

:::{cpp:function} float BFont::StringWidth(const char* string, int32 length) const
:::

:::{cpp:function} void BFont::GetStringWidths(const char* stringArray[], const int32 lengthArray[], int32 numStrings, float widthArray[]) const
:::

{hmethod}`StringWidth()` returns how much room is required to draw a
string in the font. It measures the characters encoded in {hparam}`length`
bytes of the {hparam}`string`—or, if no length is specified, the entire
string up to the null character, '0', which terminates it. The return value
totals the width of all the characters in coordinate units; it's the length
of the baseline required to draw the string.

{hmethod}`GetStringWidth()` provides the same information for a group of
strings. It works its way through the {hparam}`stringArray` looking at a
total of {hparam}`numStrings`. For each string, it gets the length at the
corresponding index from the {hparam}`lengthArray` and places the width of
the string in the {hparam}`widthArray` at the same index.

These functions take all the attributes of the font—including family,
style, size, and spacing—into account.

See also: {cpp:func}`BView::StringWidth`
::::

## Operators

::::{abi-group}
:::{cpp:function} BFont& BFont::operator=(const BFont& font)
:::

Assigns one {hclass}`BFont` object to another. After the assignment, the
two objects are identical to each other and do not share any data.
::::

::::{abi-group}
:::{cpp:function} bool BFont::operator==(const BFont& font) const
:::

:::{cpp:function} bool BFont::operator!=(const BFont& font) const
:::

These operators test whether two {hclass}`BFont` objects are identical in
all respects. If all settable font attributes are the same in both objects,
they're equal. If not, they're unequal.
::::

## Global Variables

### System Fonts

Declared in: interface/Font.h

:::{code} cpp
const BFont* be_plain_font
const BFont* be_bold_font
const BFont* be_fixed_font
:::

These global {cpp:class}`BFont` objects are created when the
{cpp:class}`BApplication` object is constructed. They encapsulate the three
system fonts—the plain font which is used for labels and small stretches of
text in the user interface, the bold font which is used for window and
group titles, and the fixed font which is used in Terminal windows and
other places where a fixed-width font is required.

These objects cannot be modified directly, nor are they modified when the
user redefines a system font. The user's changed preferences don't affect
running applications.

## Constants

### Font Encodings

Declared in: interface/Font.h

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Constant

-
	- {cpp:enumerator}`B_UNICODE_UTF8`

-
	- {cpp:enumerator}`B_ISO_8859_1`

-
	- {cpp:enumerator}`B_ISO_8859_2`

-
	- {cpp:enumerator}`B_ISO_8859_3`

-
	- {cpp:enumerator}`B_ISO_8859_4`

-
	- {cpp:enumerator}`B_ISO_8859_5`

-
	- {cpp:enumerator}`B_ISO_8859_6`

-
	- {cpp:enumerator}`B_ISO_8859_7`

-
	- {cpp:enumerator}`B_ISO_8859_8`

-
	- {cpp:enumerator}`B_ISO_8859_9`

-
	- {cpp:enumerator}`B_ISO_8859_10`

-
	- {cpp:enumerator}`B_MACINTOSH_ROMAN`


:::

The constants name the various character encodings that the BeOS supports.
{cpp:enumerator}`B_UNICODE_UTF8` is the default encoding. It matches ASCII
values for 7-bit character codes but uses multiple bytes to encode other
values in the {ref}`Unicode standard.`

See also: {cpp:func}`BFont::SetEncoding`, the "{ref}`Character Encoding`"
section of this chapter

### Font Flags

Declared in: interface/Font.h

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Constant

-
	- {cpp:enumerator}`B_DISABLE_ANTIALIASING`

-
	- {cpp:enumerator}`B_IS_FIXED`

-
	- {cpp:enumerator}`B_HAS_TUNED_FONT`


:::

The first flag, {cpp:enumerator}`B_DISABLE_ANTIALIASING`, is passed to a
{cpp:class}`BFont` object to turn antialiasing off. Antialiasing should be
turned off when printing, but should generally be left on when drawing to
the screen.

The other two flags enable {ref}`get_font_family()` and
{ref}`get_font_style()` to give information about a font.
{cpp:enumerator}`B_IS_FIXED` indicates that the font is nonproportional.
{cpp:enumerator}`B_HAS_TUNED_FONT` indicates that the family or style has
one or more tuned fonts—bitmap fonts that have been adjusted to look good
on the screen—for some set of font properties (such as size and shear).

See also: {cpp:func}`BFont::SetFlags`

### Font Name Lengths

Declared in: interface/Font.h

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Constant

	- Value

-
	- {cpp:enumerator}`B_FONT_FAMILY_NAME_LENGTH`

	- 63

-
	- {cpp:enumerator}`B_FONT_STYLE_NAME_LENGTH`

	- 63


:::

These constants define the maximum length of names for font families and
styles, exclusive of a null terminator. They're used in the definition of
the {htype}`font_family` and {htype}`font_style` types.

See also: {cpp:func}`font_family <font::family>` under "{ref}`Defined
Types`" below

### Font Properties

Declared in: interface/View.h

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Constant

-
	- {cpp:enumerator}`B_FONT_FAMILY_AND_STYLE`

-
	- {cpp:enumerator}`B_FONT_SIZE`

-
	- {cpp:enumerator}`B_FONT_SHEAR`

-
	- {cpp:enumerator}`B_FONT_ROTATION`

-
	- {cpp:enumerator}`B_FONT_SPACING`

-
	- {cpp:enumerator}`B_FONT_ENCODING`

-
	- {cpp:enumerator}`B_FONT_FACE`

-
	- {cpp:enumerator}`B_FONT_FLAGS`

-
	- {cpp:enumerator}`B_FONT_ALL`


:::

These constants list the font properites that can be set for a
{cpp:class}`BView` individually or in combination. The constants form a
mask that's passed, along with a {cpp:class}`BFont` object, to
{cpp:class}`BView`'s {cpp:func}`BView <BView::SetFont>` and
{cpp:class}`BTextView`'s {cpp:func}`SetFontAndColor()
<BTextView::SetFontAndColor>` functions. For example:

:::{code} cpp
myView->SetFont(theFont, B_FONT_SIZE | B_FONT_ENCODING);
:::

{cpp:enumerator}`B_FONT_ALL` stands for all properties of the
{cpp:class}`BFont`.

### Font Spacing Modes

Declared in: interface/Font.h

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Constant

-
	- {cpp:enumerator}`B_CHAR_SPACING`

-
	- {cpp:enumerator}`B_STRING_SPACING`

-
	- {cpp:enumerator}`B_BITMAP_SPACING`

-
	- {cpp:enumerator}`B_FIXED_SPACING`


:::

These constants enumerate the four modes for positioning characters in a
line of text.

See also: {cpp:func}`BFont::SetSpacing`

### font_metric_mode

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
	- {cpp:enumerator}`B_SCREEN_METRIC`
	- The screen metric.
-
	- {cpp:enumerator}`B_PRINTING_METRIC`
	- The printing metric.

:::

Declared In: interface/Font.h

The {htype}`font_metric_mode` constants above indicate whether a font
calculation should be done with the screen or the printer in mind.

### font_file_format

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
	- {cpp:enumerator}`B_TRUETYPE_WINDOWS`
	- Microsoft Windows format TrueType font.
-
	- {cpp:enumerator}`B_POSTSCRIPT_TYPE1_WINDOWS`
	- Microsoft Windows format PostScript Type 1 font.

:::

Declared In: interface/Font.h

The {htype}`font_file_format` constants are used to specify what type of
file a font was loaded from. Currently, only Microsoft Windows™-format
TrueType and PostScript Type 1 fonts are supported.

## Defined Types

### font_direction Constants

Declared in: interface/Font.h

:::{code} c
enum font_direction {
    B_FONT_LEFT_TO_RIGHT,
    B_FONT_RIGHT_TO_LEFT
}
:::

These constants tell whether a font is used for text that's read
left-to-right or right-to-left. Thus is an inherent property of the font.

See also: {cpp:func}`BFont::Direction`

### unicode_block

interface/Font.h

:::{code} c
class unicode_block {
public:
   inline unicode_block();
   inline unicode_block(uint64 block2, uint64 block1);

   inline bool Includes(const unicode_block &block) const;
   inline unicode_block operator&(const unicode_block& block) const;
   inline unicode_block operator|(const unicode_block& block) const;
   inline unicode_block& operator=(const unicode_block &block);
   inline unicode_block operator==(const unicode_block &block) const;
   inline unicode_block operator!=(const unicode_block &block) const;

private:
   fData[2];
};
:::

The {htype}`unicode_block` class describes the ranges of Unicode™
characters a font supports. You can get a {htype}`unicode_block` object for
a font by calling the {cpp:func}`Blocks() <BFont::Blocks>` function. Once
you have this, you can check to see if a particular block is supported, or
compare it to another block to see if it's inclusive, equal, unequal, and
so forth.

In general, you won't instantiate a {htype}`unicode_block` object on your
own.

The {hmethod}`unicode_block::Includes()` function lets you determine if
another block is a subset of the {htype}`unicode_block` object.

There are a number of predefined Unicode™ blocks, as follows:

:::{code} sh
B_BASIC_LATIN_BLOCK
B_LATIN1_SUPPLEMENT_BLOCK
B_LATIN_EXTENDED_A_BLOCK
B_LATIN_EXTENDED_B_BLOCK
B_IPA_EXTENSIONS_BLOCK
B_SPACING_MODIFIER_LETTERS_BLOCK
B_COMBINING_DIACRITICAL_MARKS_BLOCK
B_BASIC_GREEK_BLOCK
B_GREEK_SYMBOLS_AND_COPTIC_BLOCK
B_CYRILLIC_BLOCK
B_ARMENIAN_BLOCK
B_BASIC_HEBREW_BLOCK
B_HEBREW_EXTENDED_BLOCK
B_BASIC_ARABIC_BLOCK
B_ARABIC_EXTENDED_BLOCK
B_DEVANAGARI_BLOCK
B_BENGALI_BLOCK
B_GURMUKHI_BLOCK
B_GUJARATI_BLOCK
B_ORIYA_BLOCK
B_TAMIL_BLOCK
B_TELUGU_BLOCK
B_KANNADA_BLOCK
B_MALAYALAM_BLOCK
B_THAI_BLOCK
B_LAO_BLOCK
B_BASIC_GEORGIAN_BLOCK
B_GEORGIAN_EXTENDED_BLOCK
B_HANGUL_JAMO_BLOCK
B_LATIN_EXTENDED_ADDITIONAL_BLOCK
B_GREEK_EXTENDED_BLOCK
B_GENERAL_PUNCTUATION_BLOCK
B_SUPERSCRIPTS_AND_SUBSCRIPTS_BLOCK
B_CURRENCY_SYMBOLS_BLOCK
B_COMBINING_MARKS_FOR_SYMBOLS_BLOCK
B_LETTERLIKE_SYMBOLS_BLOCK
B_NUMBER_FORMS_BLOCK
B_ARROWS_BLOCK
B_MATHEMATICAL_OPERATORS_BLOCK
B_MISCELLANEOUS_TECHNICAL_BLOCK
B_CONTROL_PICTURES_BLOCK
B_OPTICAL_CHARACTER_RECOGNITION_BLOCK
B_ENCLOSED_ALPHANUMERICS_BLOCK
B_BOX_DRAWING_BLOCK
B_BLOCK_ELEMENTS_BLOCK
B_GEOMETRIC_SHAPES_BLOCK
B_MISCELLANEOUS_SYMBOLS_BLOCK
B_DINGBATS_BLOCK
B_CJK_SYMBOLS_AND_PUNCTUATION_BLOCK
B_HIRAGANA_BLOCK
B_KATAKANA_BLOCK
B_BOPOMOFO_BLOCK
B_HANGUL_COMPATIBILITY_JAMO_BLOCK
B_CJK_MISCELLANEOUS_BLOCK
B_ENCLOSED_CJK_LETTERS_AND_MONTHS_BLOCK
B_CJK_COMPATIBILITY_BLOCK
B_HANGUL_BLOCK
B_HIGH_SURROGATES_BLOCK
B_LOW_SURROGATES_BLOCK
B_CJK_UNIFIED_IDEOGRAPHS_BLOCK
B_PRIVATE_USE_AREA_BLOCK
B_CJK_COMPATIBILITY_IDEOGRAPHS_BLOCK
B_ALPHABETIC_PRESENTATION_FORMS_BLOCK
B_ARABIC_PRESENTATION_FORMS_A_BLOCK
B_COMBINING_HALF_MARKS_BLOCK
B_CJK_COMPATIBILITY_FORMS_BLOCK
B_SMALL_FORM_VARIANTS_BLOCK
B_ARABIC_PRESENTATION_FORMS_B_BLOCK
B_HALFWIDTH_AND_FULLWIDTH_FORMS_BLOCK
B_SPECIALS_BLOCK
B_TIBETAN_BLOCK
:::
