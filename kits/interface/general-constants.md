# General Constants

## alignment Constants

Declared in: interface/InterfaceDefs.h

:::{code} c
enum alignment {
    B_ALIGN_LEFT,
    B_ALIGN_RIGHT,
    B_ALIGN_CENTER
:::

These constants define the {htype}`alignment` data type. They determine
how lines of text and labels are aligned by {cpp:class}`BTextView`,
{cpp:class}`BStringView`, and {cpp:class}`BMenuField` objects.

See also: {cpp:func}`BTextView::SetAlignment`

## border_style Constants

Declared in: interface/InterfaceDefs.h

:::{code} c
enum border_style {
    B_PLAIN_BORDER,
    B_FANCY_BORDER,
    B_NO_BORDER
:::

These constants define how {cpp:class}`BBox` objects and
{cpp:class}`BScrollView`s are bordered.

## Character Constants

Declared in: interface/InterfaceDefs.h

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Constant

	- Character value

-
	- {cpp:enumerator}`B_BACKSPACE`

	- 0x08 (same as 'b')

-
	- {cpp:enumerator}`B_ENTER`

	- 0x0a (same as 'n')

-
	- {cpp:enumerator}`B_RETURN`

	- 0x0a (synonym for {cpp:enumerator}`B_ENTER`)

-
	- {cpp:enumerator}`B_SPACE`

	- 0x20 (same as ' ')

-
	- {cpp:enumerator}`B_TAB`

	- 0x09 (same as 't')

-
	- {cpp:enumerator}`B_ESCAPE`

	- 0x1b

-
	- {cpp:enumerator}`B_LEFT_ARROW`

	- 0x1c

-
	- {cpp:enumerator}`B_RIGHT_ARROW`

	- 0x1d

-
	- {cpp:enumerator}`B_UP_ARROW`

	- 0x1e

-
	- {cpp:enumerator}`B_DOWN_ARROW`

	- 0x1f

-
	- {cpp:enumerator}`B_INSERT`

	- 0x05

-
	- {cpp:enumerator}`B_DELETE`

	- 0x7f

-
	- {cpp:enumerator}`B_HOME`

	- 0x01

-
	- {cpp:enumerator}`B_END`

	- 0x04

-
	- {cpp:enumerator}`B_PAGE_UP`

	- 0x0b

-
	- {cpp:enumerator}`B_PAGE_DOWN`

	- 0x0c

-
	- {cpp:enumerator}`B_FUNCTION_KEY`

	- 0x10

-
	- {cpp:enumerator}`B_UTF8_ELLIPSIS`

	- "xE2x80xA6"

-
	- {cpp:enumerator}`B_UTF8_OPEN_QUOTE`

	- "xE2x80x9C"

-
	- {cpp:enumerator}`B_UTF8_CLOSE_QUOTE`

	- "xE2x80x9D"

-
	- {cpp:enumerator}`B_UTF8_COPYRIGHT`

	- "xC2xA9"

-
	- {cpp:enumerator}`B_UTF8_REGISTERED`

	- "xC2xAE"

-
	- {cpp:enumerator}`B_UTF8_TRADEMARK`

	- "xE2x84xA2"

-
	- {cpp:enumerator}`B_UTF8_SMILING_FACE`

	- "xE2x98xBB"

-
	- {cpp:enumerator}`B_UTF8_HIROSHI`

	- "xE5xBCx98"


:::

Constants in the first group stand for the ASCII characters they name.
They're defined only for characters that normally don't have visible
symbols.

Constants in the second group are Unicode UTF-8 encodings of common
characters that have multibyte representations. These constants are strings
that can be concatenated with other strings—for example, to set a button
label that ends in an ellipsis:

:::{code} cpp
myButton->SetLabel("Options"B_UTF_ELLIPSIS);
:::

See also: "{ref}`Function Key Constants`" below

## color_space

Declared in: interface/GraphicsDefs.h

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
	- {cpp:enumerator}`B_NO_COLOR_SPACE`

	- Undefined color space

-
	- {cpp:enumerator}`B_RGB32`

	- xRGB 8:8:8:8, stored as little endian uint32

-
	- {cpp:enumerator}`B_RGBA32`

	- ARGB 8:8:8:8, stored as little endian uint32

-
	- {cpp:enumerator}`B_RGB24`

	- Currently unused

-
	- {cpp:enumerator}`B_RGB16`

	- xRGB 5:6:5, stored as little endian uint16

-
	- {cpp:enumerator}`B_RGB15`

	- RGB 1:5:5:5, stored as little endian uint16

-
	- {cpp:enumerator}`B_RGBA15`

	- ARGB 1:5:5:5, stored as little endian uint16

-
	- {cpp:enumerator}`B_CMAP8`

	- 256-color index into the color table.

-
	- {cpp:enumerator}`B_GRAY8`

	- 256-color greyscale value.

-
	- {cpp:enumerator}`B_GRAY1`

	- Each bit represents a single pixel, where 0 is the view's low color and 1
is the high color.

-
	- {cpp:enumerator}`B_RGB32_BIG`

	- xRGB 8:8:8:8, stored as big endian uint32

-
	- {cpp:enumerator}`B_RGBA32_BIG`

	- ARGB 8:8:8:8, stored as big endian uint32

-
	- {cpp:enumerator}`B_RGB24_BIG`

	- Currently unused

-
	- {cpp:enumerator}`B_RGB16_BIG`

	- RGB 5:6:5, stored as big endian uint16

-
	- {cpp:enumerator}`B_RGB15_BIG`

	- xRGB 1:5:5:5, stored as big endian uint16

-
	- {cpp:enumerator}`B_RGBA15_BIG`

	- ARGB 1:5:5:5, stored as big endian uint16

-
	- {cpp:enumerator}`B_YCbCr422`

	- Currently unused.

-
	- {cpp:enumerator}`B_YCbCr411`

	- Currently unused.

-
	- {cpp:enumerator}`B_YCbCr444`

	- Currently unused.

-
	- {cpp:enumerator}`B_YCbCr420`

	- Currently unused.

-
	- {cpp:enumerator}`B_YUV422`

	- Currently unused.

-
	- {cpp:enumerator}`B_YUV411`

	- Currently unused.

-
	- {cpp:enumerator}`B_YUV420`

	- Currently unused.

-
	- {cpp:enumerator}`B_YUV444`

	- Currently unused.

-
	- {cpp:enumerator}`B_YUV9`

	- Currently unused.

-
	- {cpp:enumerator}`B_YUV12`

	- Currently unused.

-
	- {cpp:enumerator}`B_UVL24`

	- Currently unused.

-
	- {cpp:enumerator}`B_UVL32`

	- Currently unused.

-
	- {cpp:enumerator}`B_UVLA32`

	- Currently unused.

-
	- {cpp:enumerator}`B_LAB24`

	- Currently unused.

-
	- {cpp:enumerator}`B_LAB32`

	- Currently unused.

-
	- {cpp:enumerator}`B_LABA32`

	- Currently unused.

-
	- {cpp:enumerator}`B_HSI24`

	- Hue, saturation, and intensity: x:8:8:8 format

-
	- {cpp:enumerator}`B_HSI32`

	- Hue, saturation, and intensity: 8:8:8 format

-
	- {cpp:enumerator}`B_HSIA32`

	- Hue, saturation, intensity, and alpha: 8:8:8:8 format

-
	- {cpp:enumerator}`B_HSV24`

	- Hue, saturation, and value: x:8:8:8 format

-
	- {cpp:enumerator}`B_HSV32`

	- Hue, saturation, and value: 8:8:8 format

-
	- {cpp:enumerator}`B_HSVA32`

	- Hue, saturation, value, and alpha: 8:8:8:8 format

-
	- {cpp:enumerator}`B_HLS24`

	- Hue, lightness, and saturation: x:8:8:8 format

-
	- {cpp:enumerator}`B_HLS32`

	- Hue, lightness, and saturation: 8:8:8 format

-
	- {cpp:enumerator}`B_HLSA32`

	- Hue, lightness, saturation, and alpha: 8:8:8:8 format

-
	- {cpp:enumerator}`B_CMY24`

	- Cyan, magenta, and yellow: x:8:8:8 format

-
	- {cpp:enumerator}`B_CMY32`

	- Cyan, magenta, and yellow: 8:8:8 format

-
	- {cpp:enumerator}`B_CMYA32`

	- Cyan, magenta, yellow, and alpha: 8:8:8:8 format

-
	- {cpp:enumerator}`B_CMYK32`

	- Cyan, magenta, yellow, and black: 8:8:8:8 format

-
	- {cpp:enumerator}`B_MONOCHROME_1_BIT`

	- For compatibility only: use B_GRAY1

-
	- {cpp:enumerator}`B_GRAYSCALE_8_BIT`

	- For compatibility only; use B_GRAY8

-
	- {cpp:enumerator}`B_COLOR_8_BIT`

	- For compatibility only; use B_CMAP8

-
	- {cpp:enumerator}`B_RGB_32_BIT`

	- For compatibility only; use B_RGB32

-
	- {cpp:enumerator}`B_RGB_16_BIT`

	- For compatibility only; use B_RGB15

-
	- {cpp:enumerator}`B_BIG_RGB_32_BIT`

	- For compatibility only; use B_RGB32_BIG

-
	- {cpp:enumerator}`B_BIG_RGB_16_BIT`

	- For compatibility only; use B_RGB15_BIG


:::

These constants define the {htype}`color_space` data type. A color space
describes three properties of screens and bitmap images:

-   How many bits of information there are per pixel (the depth of the image)

-   How those bits are to be interpreted (whether as colors or on a grayscale,
what the color components are, and so on).

-   How are components are arranged

A number of these aren't actually usable as screen display color spaces,
but are intended for use in identifying the color format for video media
buffers and other offscreen graphics data.

See the "{ref}`Color Spaces`" section in the "{ref}`Drawing`" section of
this chapter for a fuller explanation of these color spaces.

See also: the {cpp:class}`BBitmap` and {cpp:class}`BScreen` classes

## Control Values

Declared in: interface/Control.h

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
	- {cpp:enumerator}`B_CONTROL_ON`

	- 1

-
	- {cpp:enumerator}`B_CONTROL_OFF`

	- 0


:::

These constants define the bipolar states of a typical control device.

See also: {cpp:func}`BControl::SetValue`

## Cursor Transit Constants

Declared in: interface/View.h

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
	- {cpp:enumerator}`B_ENTERED_VIEW`

	- The cursor has just entered a view.

-
	- {cpp:enumerator}`B_INSIDE_VIEW`

	- The cursor has moved within the view.

-
	- {cpp:enumerator}`B_EXITED_VIEW`

	- The cursor has left the view


:::

These constants describe the cursor's transit through a view. Each
{cpp:func}`MouseMoved() <BView::MouseMoved>` notification includes one of
these constants as an argument, to inform the {cpp:class}`BView` whether
the cursor has entered the view, moved while inside the view, or exited the
view.

## Dead-Key Mapping

Declared in: interface/InterfaceDefs.h

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Constant

-
	- {cpp:enumerator}`B_CONTROL_TABLE`

-
	- {cpp:enumerator}`B_OPTION_CAPS_SHIFT_TABLE`

-
	- {cpp:enumerator}`B_OPTION_CAPS_TABLE`

-
	- {cpp:enumerator}`B_OPTION_SHIFT_TABLE`

-
	- {cpp:enumerator}`B_OPTION_TABLE`

-
	- {cpp:enumerator}`B_CAPS_SHIFT_TABLE`

-
	- {cpp:enumerator}`B_CAPS_TABLE`

-
	- {cpp:enumerator}`B_SHIFT_TABLE`

-
	- {cpp:enumerator}`B_NORMAL_TABLE`


:::

These constants determine which combinations of modifiers can cause a key
to be the "dead" member of a two-key combination.

See also: {ref}`get_key_map()`

## drawing_mode Constants

Declared in: interface/GraphicsDefs.h

:::{code} c
enum drawing_mode {
    B_OP_COPY,
    B_OP_OVER,
    B_OP_ERASE,
    B_OP_INVERT,
    B_OP_SELECT,
    B_OP_ALPHA,
    B_OP_ADD,
    B_OP_SUBTRACT,
    B_OP_BLEND,
    B_OP_MIN,
    B_OP_MAX
:::

These constants define the {htype}`drawing_mode` data type. The drawing
mode is a {cpp:class}`BView` graphics parameter that determines how the
image being drawn interacts with the image already in place in the area
where it's drawn. The various modes are explained under "{ref}`Drawing
Modes`" in the "{ref}`Drawing`" section of this chapter.

See also: {cpp:func}`BView::SetDrawingMode`

## Function Key Constants

Declared in: interface/InterfaceDefs.h

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Constant

-
	- {cpp:enumerator}`B_F1_KEY`

-
	- {cpp:enumerator}`B_F2_KEY`

-
	- {cpp:enumerator}`B_F3_KEY`

-
	- {cpp:enumerator}`B_F4_KEY`

-
	- {cpp:enumerator}`B_F5_KEY`

-
	- {cpp:enumerator}`B_F6_KEY`

-
	- {cpp:enumerator}`B_F7_KEY`

-
	- {cpp:enumerator}`B_F8_KEY`

-
	- {cpp:enumerator}`B_F9_KEY`

-
	- {cpp:enumerator}`B_F10_KEY`

-
	- {cpp:enumerator}`B_F11_KEY`

-
	- {cpp:enumerator}`B_F12_KEY`

-
	- {cpp:enumerator}`B_PRINT_KEY` (the "Print Screen" key)

-
	- {cpp:enumerator}`B_SCROLL_KEY` (the "Scroll Lock" key)

-
	- {cpp:enumerator}`B_PAUSE_KEY`


:::

These constants stand for the various keys that are mapped to the
{cpp:enumerator}`B_FUNCTION_KEY` character. When the
{cpp:enumerator}`B_FUNCTION_KEY` character is reported in a key-down event,
the application can determine which key produced the character by testing
the key code against these constants. ( {hkey}`Control`+{hkey}`p` also
produces the {cpp:enumerator}`B_FUNCTION_KEY` character.)

See also: "Character Mapping" in the {ref}`Keyboard Information` appendix

## Interface Messages

Declared in: app/AppDefs.h

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Constant

-
	- {cpp:enumerator}`B_ZOOM`

-
	- {cpp:enumerator}`B_MINIMIZE`

-
	- {cpp:enumerator}`B_WINDOW_RESIZED`

-
	- {cpp:enumerator}`B_WINDOW_MOVED`

-
	- {cpp:enumerator}`B_WINDOW_ACTIVATED`

-
	- {cpp:enumerator}`B_QUIT_REQUESTED`

-
	- {cpp:enumerator}`B_SCREEN_CHANGED`

-
	- {cpp:enumerator}`B_WORKSPACE_ACTIVATED`

-
	- {cpp:enumerator}`B_WORKSPACES_CHANGED`

-
	- {cpp:enumerator}`B_KEY_DOWN`

-
	- {cpp:enumerator}`B_KEY_UP`

-
	- {cpp:enumerator}`B_MOUSE_DOWN`

-
	- {cpp:enumerator}`B_MOUSE_UP`

-
	- {cpp:enumerator}`B_MOUSE_MOVED`

-
	- {cpp:enumerator}`B_VIEW_RESIZED`

-
	- {cpp:enumerator}`B_VIEW_MOVED`

-
	- {cpp:enumerator}`B_VALUE_CHANGED`

-
	- {cpp:enumerator}`B_PULSE`


:::

These constants identify interface messages—system messages that are
delivered to {cpp:class}`BWindow` objects. Each constant conveys an
instruction to do something in particular ({cpp:enumerator}`B_ZOOM`) or
names a type of event ({cpp:enumerator}`B_KEY_DOWN`).

See also: "{ref}`Interface Messages`" in the "{ref}`Responding to the
User`" section of this chapter

## list_view_type Constants

Declared in: interface/ListView.h

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Constant

-
	- {cpp:enumerator}`B_SINGLE_SELECTION_LIST`

-
	- {cpp:enumerator}`B_MULTIPLE_SELECTION_LIST`


:::

These constants distinguish between lists that permit the user to select
only one item at a time and those that allow multiple items to be selected.

See also: The {cpp:class}`BListView` class

## Main Screen

Declared in: interface/Screen.h

const screen_id {cpp:enumerator}`B_MAIN_SCREEN_ID`

This constant stands for the main screen, the screen that has the origin
of the screen coordinate system at its left top corner. (Currently only one
screen can be attached to the computer and it is the main screen.)

See also: {cpp:func}`screen_id <screen::id>`

## menu_bar_border Constants

Declared in: interface/MenuBar.h

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
	- {cpp:enumerator}`B_BORDER_FRAME`

	- Put a border inside the entire frame rectangle.

-
	- {cpp:enumerator}`B_BORDER_CONTENTS`

	- Put a border around the group of items only.

-
	- {cpp:enumerator}`B_BORDER_EACH_ITEM`

	- Put a border around each item.


:::

These constants can be passed as an argument to {cpp:class}`BMenuBar`'s
{cpp:func}`SetBorder() <BMenuBar::SetBorder>` function.

## menu_layout Constants

Declared in: interface/Menu.h

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
	- {cpp:enumerator}`B_ITEMS_IN_ROW`

	- Menu items are arranged horizontally, in a row.

-
	- {cpp:enumerator}`B_ITEMS_IN_COLUMN`

	- Menu items are arranged vertically, in a column.

-
	- {cpp:enumerator}`B_ITEMS_IN_MATRIX`

	- Menu items are arranged in a custom fashion.


:::

These constants define the {htype}`menu_layout` data type. They
distinguish the ways that items can be arranged in a menu or menu bar—they
can be laid out from end to end in a row like a typical menu bar, stacked
from top to bottom in a column like a typical menu, or arranged in some
custom fashion like a matrix.

See also: The {cpp:class}`BMenu` and {cpp:class}`BMenuBar` constructors

## Modifier States

Declared in: interface/InterfaceDef.h

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Constant

-
	- {cpp:enumerator}`B_SHIFT_KEY`

-
	- {cpp:enumerator}`B_LEFT_SHIFT_KEY`

-
	- {cpp:enumerator}`B_RIGHT_SHIFT_KEY`

-
	- {cpp:enumerator}`B_CONTROL_KEY`

-
	- {cpp:enumerator}`B_LEFT_CONTROL_KEY`

-
	- {cpp:enumerator}`B_RIGHT_CONTROL_KEY`

-
	- {cpp:enumerator}`B_CAPS_LOCK`

-
	- {cpp:enumerator}`B_SCROLL_LOCK`

-
	- {cpp:enumerator}`B_NUM_LOCK`

-
	- {cpp:enumerator}`B_OPTION_KEY`

-
	- {cpp:enumerator}`B_LEFT_OPTION_KEY`

-
	- {cpp:enumerator}`B_RIGHT_OPTION_KEY`

-
	- {cpp:enumerator}`B_COMMAND_KEY`

-
	- {cpp:enumerator}`B_LEFT_COMMAND_KEY`

-
	- {cpp:enumerator}`B_RIGHT_COMMAND_KEY`

-
	- {cpp:enumerator}`B_MENU_KEYB_PULSE`


:::

These constants designate the {hkey}`Shift`, {hkey}`Option`,
{hkey}`Control`, {hkey}`Command`, and {hkey}`Menu` modifier keys and the
lock states set by the {hkey}`Caps Lock`, {hkey}`Scroll Lock`, and
{hkey}`Num Lock` keys. They're typically used to form a mask that describes
the current, or required, modifier states.

For each variety of modifier key, there are constants that distinguish
between the keys that appear at the left and right of the keyboard, as well
as one that lumps both together. For example, if the user is holding the
left {hkey}`Control` key down, both {cpp:enumerator}`B_CONTROL_KEY` and
{cpp:enumerator}`B_LEFT_CONTROL_KEY` will be set in the mask.

See also: {ref}`modifiers()`, {cpp:func}`BWindow::AddShortcut`, the
{cpp:class}`BMenu` constructor

## Mouse Buttons

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
	- {cpp:enumerator}`B_PRIMARY_MOUSE_BUTTON`

-
	- {cpp:enumerator}`B_SECONDARY_MOUSE_BUTTON`

-
	- {cpp:enumerator}`B_TERTIARY_MOUSE_BUTTON`


:::

These constants name the mouse buttons. Buttons are identified, not by
their physical positions on the mouse, but by their roles in the user
interface.

See also: {cpp:func}`BView::GetMouse`, {ref}`set_mouse_map()`

## Orientation Constants

Declared in: interface/InterfaceDef.h

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Constant

-
	- {cpp:enumerator}`B_HORIZONTAL`

-
	- {cpp:enumerator}`B_VERTICAL`


:::

These constants define the orientation data type that distinguishes
between the vertical and horizontal orientation of graphic objects. It's
currently used only to differentiate scroll bars.

See also: The {cpp:class}`BScrollBar` and {cpp:class}`BScrollView` classes

## Pattern Constants

Declared in: interface/GraphicsDef.h

:::{code} cpp
const pattern B_SOLID_HIGH =
    { 0xff, 0xff, 0xff, 0xff, 0xff,0xff, 0xff, 0xff }

const pattern B_SOLID_LOW =
    { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 }

const pattern B_MIXED_COLORS =
    { 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55 }
:::

These constants name the three standard patterns defined in the Interface
Kit.

{cpp:enumerator}`B_SOLID_HIGH` is a pattern that consists of the high
color only. It's the default pattern for all BView drawing functions that
stroke lines and fill shapes.

{cpp:enumerator}`B_SOLID_LOW` is a pattern with only the low color. It's
used mainly to erase images (to replace them with the background color).

{cpp:enumerator}`B_MIXED_COLORS` alternates pixels between the high and
low colors in a checkerboard pattern. The result is a halftone midway
between the two colors. This pattern can produce fine gradations of color,
especially when the high and low colors are set to two colors that are
already quite similar.

See also: "{ref}`Patterns`" in the "{ref}`Drawing`" section of this
chapter

## Resizing Modes

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
	- {cpp:enumerator}`B_FOLLOW_LEFT`

-
	- {cpp:enumerator}`B_FOLLOW_RIGHT`

-
	- {cpp:enumerator}`B_FOLLOW_LEFT_RIGHT`

-
	- {cpp:enumerator}`B_FOLLOW_H_CENTER`

-
	- {cpp:enumerator}`B_FOLLOW_TOP`

-
	- {cpp:enumerator}`B_FOLLOW_BOTTOM`

-
	- {cpp:enumerator}`B_FOLLOW_TOP_BOTTOM`

-
	- {cpp:enumerator}`B_FOLLOW_V_CENTER`

-
	- {cpp:enumerator}`B_FOLLOW_ALL`

-
	- {cpp:enumerator}`B_FOLLOW_NONE`


:::

These constants are used to set the behavior of a view when its parent is
resized. They're explained under the {hclass}`BView` {cpp:func}`constructor
<BView::BView()>`.

See also: {cpp:func}`BView::SetResizingMode`

## Screen Spaces

Declared in: interface/GraphicsDef.h

:::{code}
B_8_BIT_640x400
B_8_BIT_640x480    B_15_BIT_640x480
B_16_BIT_640x480   B_32_BIT_640x480

B_8_BIT_800x600    B_15_BIT_800x600
B_16_BIT_800x600   B_32_BIT_800x600

B_8_BIT_1024x768   B_15_BIT_1024x768
B_16_BIT_1024x768  B_32_BIT_1024x768

B_8_BIT_1152x900   B_15_BIT_1152x900
B_16_BIT_1152x900  B_32_BIT_1152x900

B_8_BIT_1280x1024  B_15_BIT_1280x1024
B_16_BIT_1280x1024 B_32_BIT_1280x1024

B_8_BIT_1600x1200  B_15_BIT_1600x1200
B_16_BIT_1600x1200 B_32_BIT_1600x1200
:::

These constants are currently used to configure the screen—to set its
depth and the size of the pixel grid it displays—as well as to report which
configurations are possible. However, they may not be supported in the
future. 15-bit depths are not currently supported

See also: {ref}`set_screen_space()`, get_screen_info().

## ScrollBar Constants

Declared in: interface/ScrollBar.h

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Constant

-
	- {cpp:enumerator}`B_H_SCROLL_BAR_HEIGHT`

-
	- {cpp:enumerator}`B_V_SCROLL_BAR_WIDTH`


:::

These constants record the recommended thickness of scroll bars. They
should be used to help define the frame rectangles passed to the
{hclass}`BScrollBar` {cpp:func}`constructor <BScrollBar::BScrollBar()>`.

## String Truncation Constants

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
	- {cpp:enumerator}`B_TRUNCATE_END`

-
	- {cpp:enumerator}`B_TRUNCATE_BEGINNING`

-
	- {cpp:enumerator}`B_TRUNCATE_MIDDLE`

-
	- {cpp:enumerator}`B_TRUNCATE_SMART`


:::

These constants instruct a {cpp:class}`BFont` where it should remove
characters from a set of strings to shorten them.

See also: {cpp:func}`BFont::GetTruncatedStrings`

## tint_color() Constants

Declared in: interface/InterfaceDefs.h

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
	- {cpp:enumerator}`B_LIGHTEN_MAX_TINT`

	- The maximum amount of tinting lighter. A color component value of 216 will
become 255.

-
	- {cpp:enumerator}`B_LIGHTEN_2_TINT`

	- The second largest amount of lightening. A color component value of 216
will become 240.

-
	- {cpp:enumerator}`B_LIGHTEN_1_TINT`

	- A small amount of lightening. A color component value of 216 will become
232.

-
	- {cpp:enumerator}`B_NO_TINT`

	- Has no effect on the color.

-
	- {cpp:enumerator}`B_DARKEN_1_TINT`

	- The least amount of darkening. A color component value of 184 will become
zero.

-
	- {cpp:enumerator}`B_DARKEN_2_TINT`

	- Darker. A color component value of 216 will become 152.

-
	- {cpp:enumerator}`B_DARKEN_3_TINT`

	- Even darker. A color component value of 216 will become 128.

-
	- {cpp:enumerator}`B_DARKEN_4_TINT`

	- Darker still A color component value of 216 will become 96.

-
	- {cpp:enumerator}`B_DARKEN_MAX_TINT`

	- Wow, that's really dark. A color component value of 216 will become zero.

-
	- {cpp:enumerator}`B_DISABLED_LABEL_TINT`

	- Use this constant when generating colors with which to disable text
labels.

-
	- {cpp:enumerator}`B_HIGHLIGHT_BACKGROUND_TINT`

	- Use this constant to create a dark color for use as a background color on
selected data.

-
	- {cpp:enumerator}`B_DISABLED_MARK_TINT`

	- Use this to create a color for a disabled checkmark or radio button mark
(or other tick-mark type items).


:::

These constants are used when calling {cpp:func}`tint_color()
<tint::color>` to alter an existing color, especially for creating disabled
objects or highlighting backgrounds.

## Transparency Constants

Declared in: interface/GraphicsDefs.h

:::{code}
const uint8 B_TRANSPARENT_8_BIT
const rgb_color B_TRANSPARENT_32_BIT
:::

These constants set transparent pixel values in a bitmap image.
{cpp:enumerator}`B_TRANSPARENT_8_BIT` designates a transparent pixel in the
{cpp:enumerator}`B_CMAP8` color space, and
{cpp:enumerator}`B_TRANSPARENT_32_BIT` designates a transparent pixel in
the {cpp:enumerator}`B_RGB32` color space.

Transparency is explained in the "Drawing Modes" part of the "Drawing"
section of this chapter. Drawing modes other than B_OP_COPY preserve the
destination image where a source bitmap is transparent.

See also: "{ref}`Drawing Modes`" in the "{ref}`Drawing`" section of this
chapter, the {cpp:class}`BBitmap` class, {cpp:func}`BView::SetViewColor`

## color_which Constants

Declared in: interface/InterfaceDefs.h

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
	- {cpp:enumerator}`B_PANEL_BACKGROUND_COLOR`

	- The background color used for view panels.

-
	- {cpp:enumerator}`B_MENU_BACKGROUND_COLOR`

	- The background color used for menus.

-
	- {cpp:enumerator}`B_MENU_SELECTION_BACKGROUND_COLOR`

	- The color used for highlighting menu items when selected.

-
	- {cpp:enumerator}`B_MENU_ITEM_TEXT_COLOR`

	- The color used for drawing menu item labels when not selected.

-
	- {cpp:enumerator}`B_MENU_SELECTED_ITEM_TEXT_COLOR`

	- The color used for drawing menu item labels when selected.

-
	- {cpp:enumerator}`B_WINDOW_TAB_COLOR`

	- The color used to draw the window's title tab.

-
	- {cpp:enumerator}`B_KEYBOARD_NAVIGATION_COLOR`

	- The color used to draw the mark indicating which control is focused for
keyboard navigation.

-
	- {cpp:enumerator}`B_DESKTOP_COLOR`

	- The current desktop color.


:::

When calling {cpp:func}`ui_color() <ui::color>` to obtain the color for a
user interface element, these constants are used to select the desired
element.

## View Flags

Declared in: interface/View.h

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
	- {cpp:enumerator}`B_FULL_UPDATE_ON_RESIZE`

	- Include the entire view in the clipping region.

-
	- {cpp:enumerator}`B_WILL_DRAW`

	- Allow the {hclass}`BView` to draw.

-
	- {cpp:enumerator}`B_PULSE_NEEDED`

	- Report pulse events to the {hclass}`BView`.

-
	- {cpp:enumerator}`B_FRAME_EVENTS`

	- Report view-resized and view-moved events.

-
	- {cpp:enumerator}`B_NAVIGABLE`

	- Let users navigate to the view with the {hkey}`Tab` key.

-
	- {cpp:enumerator}`B_NAVIGABLE_JUMP`

	- Mark the view for {hkey}`Control`+{hkey}`Tab` navigation.


:::

These constants can be combined to form a mask that sets the behavior of a
{cpp:class}`BView` object. They're explained in more detail under the class
constructor. The mask is passed to the {cpp:func}`constructor
<BView::BView()>`, or to the {cpp:func}`SetFlags() <BView::SetFlags>`
function.

## Window Flags

Declared in: interface/Window.h

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Constant

-
	- {cpp:enumerator}`B_NOT_MOVABLE B_NOT_CLOSABLE`

-
	- {cpp:enumerator}`B_NOT_H_RESIZABLE`

-
	- {cpp:enumerator}`B_NOT_ZOOMABLE`

-
	- {cpp:enumerator}`B_NOT_V_RESIZABLE`

-
	- {cpp:enumerator}`B_NOT_MINIMIZABLE`

-
	- {cpp:enumerator}`B_NOT_RESIZABLE`

-
	- {cpp:enumerator}`B_WILL_FLOAT`

-
	- {cpp:enumerator}`B_WILL_ACCEPT_FIRST_CLICK`


:::

These constants set the behavior of a window. They can be combined to form
a mask that's passed to the {hclass}`BWindow` {cpp:func}`constructor
<BWindow::BWindow()>`.

## window_type Constants

Declared in: interface/Window.h

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
	- {cpp:enumerator}`B_MODAL_WINDOW`

	- The window is a modal window.

-
	- {cpp:enumerator}`B_BORDERED_WINDOW`

	- The window has a border but no title tab.

-
	- {cpp:enumerator}`B_TITLED_WINDOW`

	- The window has a border and a title tab.

-
	- {cpp:enumerator}`B_DOCUMENT_WINDOW`

	- The window has a border, tab and resize knob.


:::

These constants describe the various kinds of windows that can be
requested from the Application Server.

See also: The {hclass}`BWindow` {cpp:func}`constructor
<BWindow::BWindow()>`

## Workspace Constants

Declared in: interface/Window.h

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Constant

-
	- {cpp:enumerator}`B_CURRENT_WORKSPACE`

-
	- {cpp:enumerator}`B_ALL_WORKSPACES`


:::

These constants are used—along with designations of specific workspaces—to
associate a set of one or more workspaces with a {cpp:class}`BWindow`.

See also: The {hclass}`BWindow` {cpp:func}`constructor
<BWindow::BWindow()>`, {cpp:func}`BWindow::SetWorkspaces`
