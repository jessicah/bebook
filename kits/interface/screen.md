# BScreen
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BScreen::BScreen(BWindow* window)
:::
:::{cpp:function} BScreen::BScreen(screen_id id = B_MAIN_SCREEN_ID)
:::

Initializes the {hclass}`BScreen` object so that it represents the screen where
{hparam}`window` is displayed or the screen identified by
{hparam}`id`. If {hparam}`window` is {cpp:enum}`NULL` or
hidden, or if the {hparam}`id` is invalid, the
{hclass}`BScreen` will represent the main
screen.

:::{admonition} Note
:class: note
Since multiple monitors aren't currently supported, there's no API for
screen identifiers other than for the main screen.
:::

To be sure the new object was correctly constructed, call
{cpp:func}`~BScreen::IsValid`.

::::

::::{abi-group}

:::{cpp:function} BScreen::~BScreen()
:::

Unlocks the screen and invalidates the {hclass}`BScreen` object.

::::

## Member Functions
::::{abi-group}

:::{cpp:function} const color_map* BScreen::ColorMap()
:::
:::{cpp:function} inline uint8 BScreen::IndexForColor(rgb_color color)
:::
:::{cpp:function} uint8 BScreen::IndexForColor(uint8 red, uint8 green, uint8 blue, uint8 alpha = 255)
:::
:::{cpp:function} rgb_color BScreen::ColorForIndex(const uint8 index)
:::
:::{cpp:function} uint8 BScreen::InvertIndex(uint8 index)
:::

These functions return information from the color_map structure for this
screen. The {cpp:func}`~color::map`
structure defines the set of 256 colors that can be
displayed in an {cpp:enum}`B_CMAP8` color space. A single
color_map is shared by all
applications that display on the same screen. See the color_map structure
for more information about the structure.

{hmethod}`ColorMap()` returns a pointer to the color_map itself. The structure
belongs to the {hclass}`BScreen` object; you can't modify or free it. (Note that
the the {hmethod}`system_colors()` function retrieves the color_map structure for
the main screen without reference to a {hclass}`BScreen` object.)

{hmethod}`IndexForColor()` returns the "index" of the 8-bit color that, in this
screen's color map, most closely matches the given 32-bit color. You can
pass the {hparam}`index` to functions such
{cpp:func}`BBitmap::SetBits` to set an 8-bit
color. Note that {hmethod}`IndexForColor()` knows how to convert
{cpp:enum}`B_TRANSPARENT_32_BIT` into {cpp:enum}`B_TRANSPARENT_8_BIT`.

{hmethod}`ColorForIndex()` returns the 32-bit color representation of a given 8-bit
color {hparam}`index`. This function doesn't convert
{cpp:enum}`B_TRANSPARENT_8_BIT` into
{cpp:enum}`B_TRANSPARENT_32_BIT`.

{hmethod}`InvertIndex()` takes an 8-bit {hparam}`index`
and returns an index that represents
the color's "inversion." Inverted colors are typically used for
highlighting.

:::{admonition} Important
:class: important
The information gained through {hmethod}`IndexForColor()`,
{hmethod}`ColorForIndex()`, and
{hmethod}`InvertIndex()` can be retrieved more efficiently
from the color_map
structure. If you're repeatedly calling these functions, you should
consider accessing the color_map structure, instead. Note, however, that
the intelligent {cpp:enum}`B_TRANSPARENT_32_BIT` to
{cpp:enum}`B_TRANSPARENT_8_BIT` conversion is
not supported by the structure.
:::
::::

::::{abi-group}

:::{cpp:function} color_space BScreen::ColorSpace()
:::

Returns the color space of the screen display—typically {cpp:enum}`B_CMAP8`,
{cpp:enum}`B_RGB15`, or {cpp:enum}`B_RGB32`—or
{cpp:enum}`B_NO_COLOR_SPACE` if the {hclass}`BScreen` object is
invalid.

The color space is set by the user through the Screen preferences
application. You can set it programatically through the
{cpp:func}`~BScreen::SetMode`
function.

::::

::::{abi-group}

:::{cpp:function} BRect BScreen::Frame()
:::

Returns the rectangle that locates the screen in the screen coordinate
system. For example, the frame for a 1,024 * 768 main screen looks like
this:

:::{code}
BRect(0.0, 0.0, 1023.0, 767.0)
:::

If the {hclass}`BScreen` object is invalid, all sides of the rectangle are set to
0.0.

The screen's frame rectangle is set by the user through the Screen
preferences application. You can set it programatically through the
{cpp:func}`~BScreen::SetMode` function.

::::

::::{abi-group}

:::{cpp:function} status_t BScreen::GetDeviceInfo(accelerant_device_info* info)
:::

Returns information about the graphics card.

::::

::::{abi-group}

:::{cpp:function} status_t BScreen::GetModeList(display_mode** mode_list, uint32* count)
:::
:::{cpp:function} status_t BScreen::SetMode(display_mode* mode, bool makeDefault = false)
:::
:::{cpp:function} status_t BScreen::GetMode(display_mode* mode)
:::

These functions set and get the screen's display mode. Each display_mode
structure (defined in add-ons/graphics/Accelerant.h) is a distinct
combination of screen size, pixel depth, and display timing.

{hmethod}`GetModeList()` allocates and returns, in {hparam}`mode_list`, a list of the
display_mode structures that the graphics card is guaranteed to support;
{hparam}`count` is set to the number of display_mode elements in the list. The
caller is responsible for freeing {hparam}`mode_list`.

:::{admonition} Warning
:class: warning
There's no guarantee that the monitor can support all of the modes that
{hmethod}`GetModeList()` retrieves.
:::

{hmethod}`SetMode()` resets the screen to the given {hparam}`mode`.
If {hparam}`makeDefault` is {cpp:enum}`true`,
the mode becomes the default for the current workspace.

{hmethod}`GetMode()` copies the current display_mode
into {hparam}`mode`.

The display_mode structure is:

:::{code}
typedef struct {
      display_timing timing;
      uint32 space;
      uint16 virtual_width;
      uint16 virtual_height;
      uint16 h_display_start;
      uint16 v_display_start;
      uint32 flags;
} display_mode;
:::
:::{list-table}
---
header-rows: 1
---
-
	- Field
	- Description
-
	- timing
	- Provides CTRC timing information.
-
	- space
	- Is the color space of the display.
-
	- virtual_width
	- Is the screen's virtual width in pixels
-
	- virtual_height
	- Is the screen's virtual height in lines.
-
	- h_display_start
	- Is the first displayed pixel in a line
-
	- v_display_start
	- Is the first displayed line.
-
	- flags
	- Are mode flags:B_SCROLLScrolling display; a large display is being simulated by scrolling around on a smaller screen.B_8_BIT_DACThe DAC is in 8-bit mode.B_HARDWARE_CURSORThe mode supports a hardware cursor.B_PARALLEL_ACCESSThe mode supports parallel access.B_DPMSThe mode supports power management.B_IO_FB_NAThe graphics card's frame buffer shouldn't be touched by the Application Server while the card's acceleration engine might be doing so.
:::

The display_timing structure is:

:::{code}
typedef struct {
      uint32 pixel_clock;
      uint16 h_display;
      uint16 h_sync_start;
      uint16 h_sync_end;
      uint16 h_total;
      uint16 v_display;
      uint16 h_display;
      uint16 v_sync_start;
      uint16 v_sync_end;
      uint16 v_total;
      uint32 flags;
} display_timing;
:::
:::{list-table}
---
header-rows: 1
---
-
	- Field
	- Description
-
	- pixel_clock
	- Is in kHz.
-
	- h_display
	- Is in pixels, not in character clocks.
-
	- v_display
	- is in lines.
-
	- flags
	- are:B_BLANK_PEDESTALUse a 7.5 IRE blanking pedestal instead of a 0.0 IRE blanking pedestal. Usually 0.0 IRE.B_TIMING_INTERLACEDThe mode is interlaced instead of progressively scanned. Rarely set; most modern displays don't need this.B_POSITIVE_HSYNCIf set, the mode uses a positive (high) sync polarity.B_POSITIVE_VSYNCIf set, the mode uses a negative (low) sync polarity.B_SYNC_ON_GREENThe mode generates sync information on the green color signal.
:::

See also:
{cpp:func}`~BScreen::ProposeMode`

::::

::::{abi-group}

:::{cpp:function} status_t BScreen::GetPixelClockLimits(display_mode* mode, uint32* low, uint32* high)
:::

This function returns, in {hparam}`low` and {hparam}`high`,
the minimum and maximum "pixel
clock" rates (in thousands-of-pixels per second) that are possible for
the given {hparam}`mode`. Given the pixel clock and a display mode, you can
determine the refresh rate range by dividing the pixel clock by the
"real" size of the screen, thus:

:::{code}
uint32 hi_clock, lo_clock;
float hi_refresh, lo_refresh;
float real_size;
display_mode mode;
GetMode(&mode);
GetPixelClockLimits(&mode, &lo_clock, &hi_clock);
/* The real screen dimensions (i.e. the dimensions for the purposes
* of the gun) are given by the 'timing.h_total' and
* 'timing.v_total' fields.
*/
total_size = mode.timing.h_total * mode.timing.v_total
/* Get the refresh rate by dividing the pixel clock by the total
* screen size. Remember -- the pixel clock values are given in
* kHz; we multiply by 1000.0 to retrieve refresh rates in Hz.
*/
hi_refresh = ((float) hi_clock*1000.0)/(float) total_size;
lo_refresh = ((float) lo_clock*1000.0)/(float) total_size;
:::
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- Pixel clock limits returned successfully.
-
	- {cpp:enum}`B_ERROR`.
	- No clock limits known.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BScreen::GetTimingConstraints(display_timing_constraints* dtc)
:::

This function fills out the {hparam}`dtc` structure with the timing constraints of
the current display mode.

:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- Constraints returned successfully.
-
	- {cpp:enum}`B_ERROR`.
	- No constraints known.
:::
::::

::::{abi-group}

:::{cpp:function} screen_id BScreen::ID()
:::

Returns the identifier for the screen. The main screen is identified as
{cpp:enum}`B_MAIN_SCREEN_ID`.

The ID isn't presistent across boots, and may change if the monitor is
diconnected and then reconnected.

:::{admonition} Warning
:class: warning
Currently, this function always returns {cpp:enum}`B_MAIN_SCREEN_ID`, even if the
{hclass}`BScreen` object is invalid.
:::
::::

::::{abi-group}

:::{cpp:function} bool BScreen::IsValid()
:::

Returns {cpp:enum}`true` if the {hclass}`BScreen`
object is valid (if it represents a real
screen connected to the computer), and {cpp:enum}`false` if not.

::::

::::{abi-group}

:::{cpp:function} status_t BScreen::ProposeMode(display_mode* candidate, const display_mode* low, const display_mode* high)
:::

{hmethod}`ProposeMode()` is a convenience function
that attempts to adjust {hparam}`candidate`
so that it's a supported mode (as listed by the
{cpp:func}`~BScreen::GetModeList` function).
It then compares the possibly-adjusted {hparam}`candidate` to the limits declared
in {hparam}`low` and {hparam}`high`
and expresses this comparison in the return value. Note
that the function doesn't adjust {hparam}`candidate` so that it is, of necessity,
between {hparam}`low` and {hparam}`high`.

Exactly how {hmethod}`ProposeMode()` works is up to the individual graphics driver.
It's expected that the function will adjust {hparam}`candidate`'s screen size
fields while holding the color space constant.

:::{admonition} Note
:class: note
This function was formerly called {hmethod}`ProposeDisplayMode()`.
:::
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- Candidate (as returned) is supported and falls within the limits.
-
	- {cpp:enum}`B_BAD_VALUE`.
	- Candidate (as returned) is supported, but doesn't fall within the limits.
-
	- {cpp:enum}`B_ERROR`.
	- candidate isn't supported.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BScreen::ReadBitmap(BBitmap* buffer, bool draw_cursor = true, BRect* bounds = NULL)
:::
:::{cpp:function} status_t BScreen::GetBitmap(BBitmap** buffer, bool draw_cursor = true, BRect* bounds = NULL)
:::

These functions provide read-only access to the screen by copying the
screen's contents into the first argument
{cpp:class}`BBitmap`. The difference between
them is that {hmethod}`ReadBitmap()` expects you to allocate the
{cpp:class}`BBitmap` before
passing it in, while {hmethod}`GetBitmap()` allocates a new
{cpp:class}`BBitmap` for you. The
caller is responsible for freeing the
{cpp:class}`BBitmap` allocated by
{hmethod}`GetBitmap()`.

The {hparam}`draw_cursor` argument determines whether the cursor is drawn in the
screen shot; {hparam}`bounds` let you specify the region, in screen coordinates,
that you want copied. If {hparam}`bounds` is {cpp:enum}`NULL`,
the entire screen is copied. The
functions fail if the {hparam}`bounds` rectangle doesn't fall wholly within the
screen's frame.

The functions return {cpp:enum}`B_OK` on success or
{cpp:enum}`B_ERROR` on failure.

::::

::::{abi-group}

:::{cpp:function} void BScreen::SetDesktopColor(rgb_color color, bool makeDefault = true)
:::
:::{cpp:function} rgb_color BScreen::DesktopColor()
:::

These functions set and return the color of the desktop—the
backdrop against which windows are displayed on the screen.
{hmethod}`SetDesktopColor()` makes an immediate change in the desktop color
displayed on-screen;
{hmethod}`DesktopColor()` returns the color currently displayed.

If the {hparam}`makeDefault` flag is {cpp:enum}`true`,
the color that's set becomes the default
color for the screen; it's the color that will be shown the next time the
machine is booted. If the flag is {cpp:enum}`false`, the color is set only for the
current session.

:::{admonition} Note
:class: note
The "Background Images" section tells you how to convince the desktop
to display a bitmap image.
:::

Typically, users choose the desktop color with the Screen preferences
application.

::::

::::{abi-group}

:::{cpp:function} status_t BScreen::SetDPMS(uint32 dpmsState)
:::
:::{cpp:function} uint32 BScreen::DPMSState()
:::
:::{cpp:function} uint32 BScreen::DPMSCapabilities()
:::

{hmethod}`SetDPMS()` lets you set the VESA Display Power Management Signaling state
for the screen. The state can be one of the following values:

:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_DPMS_ON`
	- Image is visible, normal screen operation.
-
	- {cpp:enum}`B_DPMS_STAND_BY`
	- Image is not visible, but can be restored "instantly." Saves around 30% of the power used by the monitor in {cpp:enum}`B_DPMS_ON` mode.
-
	- {cpp:enum}`B_DPMS_SUSPEND`
	- Image is not visible, but can be restored in less than five seconds. Saves more power by turning off the CRT's heater. The amount of savings (or if there's any) depends on the display.
-
	- {cpp:enum}`B_DPMS_OFF`
	- Image is not visible and will take some time to restore. Typically turns off all monitor power except the processor watching the sync signals for a higher power state (typically {cpp:enum}`B_DPMS_ON`).
:::

{hmethod}`DPMSState()` returns the current display state, indicating whether the
monitor is on or off or in one of the two sleep modes.

{hmethod}`DPMSCapabilities()` indicates which of the above modes the monitor
supports.

::::

::::{abi-group}

:::{cpp:function} status_t BScreen::SetToNext()
:::

In the current BeOS release, this function always returns {cpp:enum}`B_ERROR`.

::::

::::{abi-group}

:::{cpp:function} status_t BScreen::WaitForRetrace()
:::
:::{cpp:function} status_t BScreen::WaitForRetrace(bigtime_t timeout)
:::

Blocks until the monitor has finished the current vertical retrace, then
returns {cpp:enum}`B_OK`. There are a few milliseconds available before it begins
another retrace. Drawing changes made to the frame buffer in this period
won't cause any "flicker" on-screen.

For some graphics card drivers, this function will wait for vertical
sync; for others it will wait until vertical blank, providing a few extra
milliseconds.

The {hparam}`timeout` argument lets you provide a timeout in microseconds—if
the screen hasn't retraced within the limit, the function returns
{cpp:enum}`B_ERROR`.

::::
