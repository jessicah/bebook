# BPrintJob

A {cpp:class}`BPrintJob` object runs a printing session. It negotiates
everything after the user's initial request to print—from engaging the
Print Server to calling upon {cpp:class}`BView`s to draw and spooling the
results to the printer. It also handles a secondary and somewhat separate
matter related to printing—configuring the page layout.

## Setting Up the Page Layout

Users typically don't decide how a document fits on a page—the size of the
paper, the width of the margins, the orientation of the image, and so
on—each time they print. These decisions are usually made when setting up
the document, perhaps from a Page Layout menu item, rather than Print.

To set up the page parameters for a document, an application should create
a {cpp:class}`BPrintJob` object, assign it a name, and call
{cpp:func}`ConfigPage() <BPrintJob::ConfigPage>`:

:::{code} cpp
status_t MyDocumentManager::SetUpPage()
{
   BPrintJob job("document");
   return job.ConfigPage();
}
:::

{cpp:func}`ConfigPage() <BPrintJob::ConfigPage>` has the Print Server
interact with the user to set up the page configuration. Configuration
settings are stored in a {cpp:class}`BMessage` object that will be handed
to the server when the document is printed. The {cpp:class}`BMessage` is
important to the server, but the application doesn't need to look at it
directly; functions are provided to access the useful data it contains.
However, you may want to get the object and store it with the document so
that the configuration can be reused whenever the document is printed—and
so that the user's previous choices can be the default settings when
{cpp:func}`ConfigPage() <BPrintJob::ConfigPage>` is called again. This is
good behavior for an application to follow, and is highly recommended.

{cpp:func}`Settings() <BPrintJob::Settings>` returns the page
configuration the user set up; {cpp:func}`SetSettings()
<BPrintJob::SetSettings>` initializes the configuration that's presented to
the user. For example:

:::{code} cpp
BMessage *setup;
. . .
status_t MyDocumentManager::SetUpPage() {
   status_t result;
   BPrintJob job("document's name");

   if (setup) {
      job.SetSettings(new BMessage(*setup));
   }

   result = job.ConfigPage();

   if (result == B_OK) {
      setup = job.Settings();

      /* record the settings for your own use */
      paper_rect = job.PaperRect();
      printable_rect = job.PrintableRect();
   }

   return result;
}
:::

In this example, the setup {cpp:class}`BMessage` presumably is flattened
and saved with the document whenever the document is saved, and unflattened
whenever the document is open and the page settings are needed.

## Printing

To print a document, an application must go through several ordered steps:

-   Engaging the Print Server and setting parameters for the job.

-   Setting up a spool file to hold image data.

-   Asking {cpp:class}`BView`s to draw each page.

-   After each page is drawn, putting the data for the page in the spool file.

-   Committing the spool file to the Print Server.

A {cpp:class}`BPrintJob` object has member functions that assist with each
step.

### Setting Up a Print Job

A print job begins when the user requests the application to print
something. In response, the application should create a
{cpp:class}`BPrintJob` object, assign the job a name, and call
{cpp:func}`ConfigJob() <BPrintJob::ConfigJob>` to initialize the printing
environment. For example:

:::{code} cpp
BMessage *setup;
. . .
status_t MyDocumentManager::Print()
{
   BPrintJob job("document");
   status_t err;

   if ( setup )
      job.SetSettings(new BMessage(*setup));
   if ( (err = job.ConfigJob()) == B_OK ) {
      delete setup;
      setup = job.Settings();
   }
   . . .
}
:::

So far, this looks much like the code for configuring the page presented
in the previous "{ref}`Setting Up the Page Layout`" section. The idea is
the same. {cpp:func}`ConfigJob() <BPrintJob::ConfigJob>` gets the Print
Server ready for a new printing session and has it interact with the user
to set up the parameters for the job—which pages, how many copies, and so
on. It uses the same settings {cpp:class}`BMessage` to record the user's
choices as {cpp:func}`ConfigPage() <BPrintJob::ConfigPage>` did, though it
records information that's more immediate to the particular printing
session.

Again, you may want to store the user's choices with the document so that
they can be used to set the initial configuration for the job when the
document is next printed. By calling {cpp:func}`Settings()
<BPrintJob::Settings>`, you can get the job configuration the user set up;
{cpp:func}`SetSettings() <BPrintJob::SetSettings>` initializes the
configuration that's presented to the user.

Information about the page layout will be required while printing. If that
information isn't available in the {cpp:func}`Settings()
<BPrintJob::Settings>` {cpp:class}`BMessage`, {cpp:func}`ConfigJob()
<BPrintJob::ConfigJob>` will begin, in essence, by calling
{cpp:func}`ConfigPage() <BPrintJob::ConfigPage>` so that the server can ask
the user to supply it.

To discover which pages the user wants to print, you can call the
{cpp:func}`FirstPage() <BPrintJob::FirstPage>` and {cpp:func}`LastPage()
<BPrintJob::LastPage>` functions after {cpp:func}`ConfigJob()
<BPrintJob::ConfigJob>` returns:

:::{code} cpp
int32 pageCount = job.LastPage() - job.FirstPage() + 1;
:::

### The Spool File

The next step after configuring the job is to call {cpp:func}`BeginJob()
<BPrintJob::BeginJob>` to set up a spool file and begin the production of
pages. After all the pages are produced, {cpp:func}`CommitJob()
<BPrintJob::CommitJob>` is called to commit them to the printer.

:::{code} cpp
job.BeginJob();
/* draw pages here*/
job.CommitJob();
:::

{cpp:func}`BeginJob() <BPrintJob::BeginJob>` and {cpp:func}`CommitJob()
<BPrintJob::CommitJob>` bracket all the drawing that's done during the job.

### Cancellation

A number of things can happen to derail a print job after it has
started—most significantly, the user can cancel it at any time. To be sure
that the job hasn't been canceled or something else hasn't happened to
defeat it, you can call {cpp:func}`CanContinue() <BPrintJob::CanContinue>`
at critical junctures in your code. This function will tell you whether
it's sensible to continue with the job. In the following example, a while
loop is used to loop through all the pages in the document, or until
{cpp:func}`CanContinue() <BPrintJob::CanContinue>` returns false,
indicating that the job has been canceled:

:::{code} cpp
job.BeginJob();
while (job.CanContinue() && page <= pageCount) {
   /* draw each page here*/
   page++;
}
job.CommitJob();
:::

### Drawing on the Page

A page is produced by asking one or more {cpp:class}`BView`s to draw
within a rectangle that can be mapped to a sheet of paper (excluding the
margins at the edge of the paper). {cpp:func}`DrawView()
<BPrintJob::DrawView>` requests one {cpp:class}`BView` to draw some portion
of its data and specifies where the data should appear on the page. You can
call {cpp:func}`DrawView() <BPrintJob::DrawView>` any number of times for a
single page to ask any number of {cpp:class}`BView`s to contribute to the
page. After all views have drawn, {cpp:func}`SpoolPage()
<BPrintJob::SpoolPage>` spools the data to the file that will eventually be
committed to the printer. {cpp:func}`SpoolPage() <BPrintJob::SpoolPage>` is
called just once for each page. For example:

:::{code} cpp
for (int i = job.FirstPage();
job.CanContinue() && i <= job.LastPage();
i++) {
   . . .
   job.DrawView(someView, viewRect, pointOnPage);
   job.DrawView(anotherView, anotherRect, differentPoint);
   . . .
   job.SpoolPage();
}
:::

{cpp:func}`DrawView() <BPrintJob::DrawView>` calls the
{cpp:class}`BView`'s {cpp:func}`Draw() <BView::Draw>` function. That
function must be prepared to draw either for the screen or on the printed
page. It can test the destination of its output by calling the
{cpp:func}`Draw() <BView::Draw>` {cpp:func}`IsPrinting()
<BView::IsPrinting>` function.

:::{admonition} Note
:class: note
Don't use the {cpp:func}`BView::Bounds` function to determine the area to
render. Instead, use the update rectangle passed to the
{cpp:func}`BView::Draw` function.
:::

### A Complete Printing Function

This function puts together all the above code snippets and handles the
printing of a document (minus the actual drawing and visual status
information presented to the user as printing goes on).

:::{code} cpp
status_t MyDocumentManager::Print() {
   status_t result = B_OK;
   BPrintJob job("document's name");

   // If we have no setup message, we should call ConfigPage()
   // You must use the same instance of the BPrintJob object
   // (you can't call the previous "PageSetup()" function, since it
   // creates its own BPrintJob object).

   if (!setup) {
      result = job.ConfigPage();
      if (result == B_OK) {
         // Get the user Settings
         setup = job.Settings();

         // Use the new settings for your internal use
         paper_rect = job.PaperRect();
         printable_rect = job.PrintableRect();
      }
   }

   if (result == B_OK) {
      // Setup the driver with user settings
      job.SetSettings(setup);

      result = job.ConfigJob();
      if (result == B_OK) {
         // WARNING: here, setup CANNOT be NULL.
         if (setup == NULL) {
            // something's wrong, handle the error and bail out
         }
         delete setup;

         // Get the user Settings
         setup = job.Settings();

         // Use the new settings for your internal use
         // They may have changed since the last time you read it
         paper_rect = job.PaperRect();
         printable_rect = job.PrintableRect();

         // Now you have to calculate the number of pages
         // (note: page are zero-based)
         int32 firstPage = job.FirstPage();
         int32 lastPage = job.LastPage();

         // Verify the range is correct
         // 0 ... LONG_MAX -> Print all the document
         // n ... LONG_MAX -> Print from page n to the end
         // n ... m -> Print from page n to page m

         if (lastPage > your_document_last_page)
            last_page = your_document_last_page;

         int32 nbPages = lastPage - firstPage + 1;

         // Verify the range is correct
         if (nbPages <= 0)
            return B_ERROR;

         // Now you can print the page
         job.BeginJob();

         // Print all pages
         bool can_continue = job.CanContinue();

         for (int i=firstPage ; can_continue && i<=lastPage ; i++) {
            // Draw all the needed views
            job.DrawView(someView, viewRect, pointOnPage);
            job.DrawView(anotherView, anotherRect, differentPoint);

            // If the document have a lot of pages, you can update
               a BStatusBar, here
            // or else what you want...
            update_status_bar(i-firstPage, nbPages);

            // Spool the page
            job.SpoolPage();

            // Cancel the job if needed.
            // You can for exemple verify if the user pressed the
            // ESC key or (SHIFT + '.')...
            if (user_has_canceled)
            {
               // tell the print_server to cancel the printjob
               job.CancelJob();
               can_continue = false;
               break;
            }

            // Verify that there was no error (disk full for example)
            can_continue = job.CanContinue();
         }

         // Now, you just have to commit the job!
         if (can_continue)
            job.CommitJob();
         else
            result = B_ERROR;
      }
   }

   return result;
}
:::

### Drawing Coordinates

When a {cpp:class}`BView` draws for the printer, it draws within the
printable rectangle of a page—a rectangle that matches the size of a sheet
of paper minus the unprinted margin around the paper's edge. The
{cpp:func}`PaperRect() <BPrintJob::PaperRect>` function returns a rectangle
that measures a sheet of paper and {cpp:func}`PrintableRect()
<BPrintJob::PrintableRect>` returns the printable rectangle, as illustrated
in this diagram.

![Paper And Print Rectangles](./images/TheInterfaceKit/printjob1.png)

Both rectangles are stated in a coordinate system that has its origin at
the left top corner of the page. Thus, the left and top sides of the
rectangle returned by {cpp:func}`PaperRect() <BPrintJob::PaperRect>` are
always 0.0. {cpp:func}`PrintableRect() <BPrintJob::PrintableRect>` locates
the printable rectangle on the paper rectangle. However,
{cpp:func}`DrawView() <BPrintJob::DrawView>` assumes coordinates that are
local to the printable rectangle—that is, an origin at the left top corner
of the printable rectangle rather than the paper rectangle.

The diagram below shows the left top coordinates of the printable
rectangle as {cpp:func}`PrintableRect() <BPrintJob::PrintableRect>` would
report them and as {cpp:func}`DrawView() <BPrintJob::DrawView>` would
assume them, given a half-inch margin.

![Views In Page Layout With Margin](./images/TheInterfaceKit/printjob2.png)

{cpp:func}`Draw() <BView::Draw>` always draws in the {cpp:class}`BView`'s
own coordinate system. Those coordinates are mapped to locations in the
printable rectangle as specified by the arguments passed to
{cpp:func}`DrawView() <BPrintJob::DrawView>`.

See also: {cpp:func}`BView::IsPrinting`
