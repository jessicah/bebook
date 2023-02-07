# BPrintJob
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BPrintJob::BPrintJob(const char* name)
:::

Initializes the {hclass}`BPrintJob` object and assigns the job a {hparam}`name`.
The Print Server isn't contacted until
{cpp:func}`~BPrintJob::ConfigPage` or
{cpp:func}`~BPrintJob::ConfigJob` is called. The
spool file isn't created until
{cpp:func}`~BPrintJob::BeginJob`
prepares for the production of pages.

::::

::::{abi-group}

:::{cpp:function} virtual BPrintJob::~BPrintJob()
:::

Frees all memory allocated by the object.

::::

## Member Functions
::::{abi-group}

:::{cpp:function} void BPrintJob::BeginJob()
:::

Opens a spool file for the job and prepares for the production of a
series of pages. Call this function only once per printing
session—just after initializing the job and just before drawing the
first page.

See also:
{cpp:func}`~BPrintJob::CommitJob`,
"{cpp:func}`~BPrintJob::Overview`" in the class overview

::::

::::{abi-group}

:::{cpp:function} void BPrintJob::CancelJob()
:::

Cancels the print job programmatically and gets rid of the spool file.
The job cannot be restarted; you must destroy the {hclass}`BPrintJob` object.
Create a new object to renew printing.

::::

::::{abi-group}

:::{cpp:function} bool BPrintJob::CanContinue()
:::

Returns {cpp:enum}`true` if there's no impediment to continuing with the print job,
and {cpp:enum}`false` if the user has canceled the job, the spool file has grown too
big, or something else has happened to terminate printing. It's a good
idea to liberally sprinkle {hmethod}`CanContinue()` queries throughout your printing
code to make sure that the work you're about to do won't be wasted.

See also:
"{cpp:func}`~BPrintJob::Overview`"
in the class overview

::::

::::{abi-group}

:::{cpp:function} void BPrintJob::CommitJob()
:::

Commits all spooled pages to the printer. This ends the print job; when
{hmethod}`CommitJob()` returns, the {hclass}`BPrintJob`
object can be deleted. {hmethod}`CommitJob()` can
be called only once per job.

See also:
{cpp:func}`~BPrintJob::BeginJob`,
"{cpp:func}`~BPrintJob::Overview`"
in the class overview

::::

::::{abi-group}

:::{cpp:function} status_t BPrintJob::ConfigPage()
:::
:::{cpp:function} status_t BPrintJob::ConfigJob()
:::

These functions contact the Print Server and have the server interact
with the user to lay out the document on a page (in the case of
{hmethod}`ConfigPage()`) or to define a print job
(in the case of {hmethod}`ConfigJob()`). The
page layout includes such things as the orientation of the image
(portrait or landscape), the dimensions of the paper on which the
document will be printed, and the size of the margins. The job definition
includes such things as which pages are to be printed and the number of
copies.

Both functions record the user's choices in a
{cpp:class}`BMessage` object that
{cpp:func}`~BPrintJob::Settings` returns.

If {cpp:func}`~BPrintJob::SetSettings`
has been called to establish a default configuration for
the page layout or the job, these functions will pass it to the Print Server so the server can present it to the user. Otherwise, the server
will choose a default configuration to show the user.

These two functions return status_t error codes, despite having return
values that are declared int32. They return {cpp:enum}`B_ERROR` if they have trouble
communicating with the server or if the job can't be established for any
reason. They return {cpp:enum}`B_OK` if all goes well.

See also:
{cpp:func}`~BPrintJob::SetSettings`,
"{cpp:func}`~BPrintJob::Overview`" and
"{cpp:func}`~BPrintJob::Overview`"
in the class overview

::::

::::{abi-group}

:::{cpp:function} virtual void BPrintJob::DrawView(BView* view, BRect rect, BPoint point)
:::
:::{cpp:function} void BPrintJob::SpoolPage()
:::

{hmethod}`DrawView()` calls upon a {hparam}`view` to draw the
{hparam}`rect` portion of its display at
the location specified by {hparam}`point` on the page. As a result, the {hparam}`view`'s
{cpp:func}`~BView::Draw`
function will be called with {hparam}`rect` passed as the update rectangle.
The rectangle should be stated in the
{cpp:class}`BView`'s coordinate system. The
{hparam}`point` should be stated in a coordinate system that has the origin at the
top left corner of the printable rectangle. Together the
{hparam}`rect` and {hparam}`point`
should be fashioned so that the entire rectangle lies within the
boundaries of the page's printable area.

The {hparam}`view` must be attached to a window; that is, it must be known to the
Application Server. However, when printing, a
{cpp:class}`BView` can be asked to draw
portions of its display that are not visible on-screen. Its drawing is
not limited by the clipping region, its bounds rectangle, or the frame
rectangles of ancestor views.

Any number of {cpp:class}`BView`s
can draw on a page if they are subjects of separate
{hmethod}`DrawView()` calls.

{hmethod}`DrawView()` renders the entire hierarchy of
{cpp:class}`BView`s attached to the
specified {cpp:class}`BView`.

Note the following bugs (which will be fixed in subsequent releases):

- BeOS 5 (and earlier) renders only the first two hierarchy levels correctly.
- Hidden {cpp:class}`BView`s (and views without {cpp:enum}`B_WILL_DRAW` specified) are rendered.
- {cpp:class}`BScrollBar` and derived {cpp:class}`BView`s aren't rendered.
- View background and overlay bitmaps are ignored; instead, the view color is printed.

After all views have drawn and the page is complete,
{hmethod}`SpoolPage()` adds it
to the spool file. {hmethod}`SpoolPage()`
must be called once to terminate each page.

See also:
{cpp:func}`~BPrintJob::PrintableRect`,
{cpp:func}`BView::Draw`,
"{cpp:func}`~BPrintJob::Overview`" in the
class overview

::::

::::{abi-group}

:::{cpp:function} int32 BPrintJob::FirstPage()
:::
:::{cpp:function} int32 BPrintJob::LastPage()
:::

These functions return the first and last pages that should be printed as
part of the current job. If the pages are not set (for example, if the
current job has been canceled), {hmethod}`FirstPage()`
returns 0 and {hmethod}`LastPage()`
returns a very large number ({cpp:enum}`LONG_MAX`).

::::

::::{abi-group}

:::{cpp:function} void BPrintJob::GetResolution(int32* xdpi, int32* ydpi)
:::

Fills the {hparam}`xdpi` and {hparam}`ydpi`
variables with the X and Y resolution of the
printer, in dots per inch.

::::

::::{abi-group}

:::{cpp:function} BRect BPrintJob::PaperRect()
:::
:::{cpp:function} BRect BPrintJob::PrintableRect()
:::

{hmethod}`PaperRect()` returns a rectangle that records the presumed size of the
paper that the printer will use. Its left and top sides are at 0.0, so
its right and bottom coordinates reflect the size of a sheet of paper.
The size depends on choices made by the user when setting up the page
layout.

{hmethod}`PrintableRect()` returns a rectangle that encloses the portion of a page
where printing can appear. It's stated in the same coordinate system as
the rectangle returned by {hmethod}`PaperRect()`, but excludes the margins around
the edge of the paper. When drawing on the printed page, the left top
corner of this rectangle is taken to be the coordinate origin, (0.0, 0.0).

The "{cpp:func}`~BPrintJob::Overview`"
section in the class overview illustrates these
rectangles and their coordinate systems.

See also:
{cpp:func}`~BPrintJob::DrawView`

::::

::::{abi-group}

:::{cpp:function} int32 BPrintJob::PrinterType(void* type = NULL)
:::

Returns a code identifying whether the printer is color or black and
white. The argument is currently not used.

The return value will be either {cpp:enum}`B_BW_PRINTER`
or {cpp:enum}`B_COLOR_PRINTER`.

:::{admonition} Note
:class: note
In the current release of BeOS, this function always returns
{cpp:enum}`B_COLOR_PRINTER`, since there's no printer driver API for determining the
printer type yet.
:::

If an error occurs, this function will return an appropriate error code
(for example, if the Print Server isn't running).

::::

::::{abi-group}

:::{cpp:function} void BPrintJob::SetSettings(BMessage* configuration)
:::
:::{cpp:function} BMessage* BPrintJob::Settings()
:::
:::{cpp:function} void BPrintJob::IsSettingsMessageValid(BMessage* configuration) const
:::

These functions set and return the group of parameters that define how a
document should be printed. The parameters include some that capture the
page layout of the document and some that define the current job. They're
recorded in a {cpp:class}`BMessage`
object that can be regarded as a black box; the
data in the message are interpreted by the Print Server and will be
documented where the print driver API is documented.

Instead of looking in the {hmethod}`Settings()`
{cpp:class}`BMessage`, rely on {hclass}`BPrintJob`
functions to provide specific information about the layout and the print
job. Currently, there are only two functions –
{cpp:func}`~BPrintJob::FirstPage` and
{cpp:func}`~BPrintJob::LastPage`,
which return the first and last pages that need to be printed.

{hmethod}`Settings()` can be called to get the current configuration message, which
can then be flattened and stored with the document. You can retrieve it
later and pass it to {hmethod}`SetSettings()` to set initial configuration values
the next time the document is printed, as discussed in the
"{cpp:func}`~BPrintJob::Overview`" and
"{cpp:func}`~BPrintJob::Overview`"
sections of the class overview.

If the message passed to settings doesn't contain all the information
needed to properly configure the print job, the printer add-on being used
will either determine appropriate default values or present a
configuration dialog box.

{hmethod}`SetSettings()` assumes ownership of the object it's passed. If your
application needs to retain the object, pass a copy to
{hmethod}`SetSettings()`:

:::{code}
print_job_object.SetSettings(new BMessage(settings_message));
:::

On the other hand, {hmethod}`Settings()` transfers ownership of the object it
returns to the caller; you don't need to make a copy.

{hmethod}`IsMessageSettingsValid()` returns
{cpp:enum}`true` if the specified message is a valid
settings message; otherwise it returns {cpp:enum}`false`.

See also:
{cpp:func}`~BPrintJob::ConfigPage`

::::
