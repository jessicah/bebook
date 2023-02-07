# BApplication
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BApplication::BApplication(const char* signature)
:::
:::{cpp:function} BApplication::BApplication(const char* signature, status_t* error)
:::
:::{cpp:function} BApplication::BApplication(BMessage* archive)
:::
The constructor creates a new object, locks it, sets the global variable
{cpp:func}`~BApplication::be` to point to it,
and establishes a connection to the Application Server. From this point on,
your application can receive messages, although it won't start processing them until you call
{cpp:func}`~BApplication::Run`.
You can also begin creating and displaying
{cpp:class}`BWindow` objects even
before you call
{cpp:func}`~BApplication::Run`.
The {hparam}`signature` constructors assign the argument as the app's
application signature. The argument is ignored if a signature is already specified
in a resource or attribute of the application's executable (serious apps should
always set the signature as both an attribute and a resource). The signature is
a MIME type string
that must have the supertype "application". For more information on
application signatures and how to set them, see
TODO.
If you specify {hparam}`error`, a pointer to a status_t, any error that occurs
while constructing the {hclass}`BApplication` will be returned in
that variable. Alternately, you can call
{cpp:func}`~BApplication::InitCheck`
to check the results. If an error is returned by the constructor, you shouldn't call
{cpp:func}`~BApplication::Run`.
The {hparam}`archive` constructor is an implementation detail; see the
{ref}`BArchivable` class.
::::

::::{abi-group}

:::{cpp:function} virtual BApplication::~BApplication()
:::
Closes and deletes the application's
{cpp:class}`BWindow`s (and the
{cpp:class}`BView`s they contain),
and severs the application's connection to the
Application Server.
Never delete a {hclass}`BApplication` object while it's
running; wait until
{cpp:func}`~BApplication::Run`
returns. To stop a {hclass}`BApplication` (and so cause
{cpp:func}`~BApplication::Run`
to return), send it a
{cpp:func}`~B::QUIT`
message:
:::{code}
be_app->PostMessage(B_QUIT_REQUESTED);
:::
::::

## Hook Functions
::::{abi-group}

:::{cpp:function} virtual void BApplication::AboutRequested()
:::
Hook function that's invoked when the {hclass}`BApplication`
receives a
{cpp:func}`~B::ABOUT` message, undoubtedly
because the user clicked an "About…"
menu item. You should implement the function to put a window on-screen that
provides the user with information about the application (version number,
license restrictions, authors' names, etc).
::::

::::{abi-group}

:::{cpp:function} virtual void BApplication::AppActivated(bool active)
:::
Hook function that's invoked when the application receives a
{cpp:func}`~B::APP`
message. The message is sent when the
application gains or loses active application status. The {hparam}`active`
flag tells you which way the wind blows: {cpp:enum}`true` means
your application is now active; {cpp:enum}`false` means it isn't.
The user can activate an application by clicking on or unhiding one of its windows;
you can activate an application programmatically by calling {cpp:func}`BWindow::Activate` or
{cpp:func}`BRoster::ActivateApp`. (With regard to the latter: This function is called only if the
application has an "activatable" window i.e. a non-modal, non-floating
window).
During launch, this function is called after
{cpp:func}`~BApplication::ReadyToRun`
(provided the application is displaying an activatable window).
::::

::::{abi-group}

:::{cpp:function} virtual void BApplication::ArgvReceived(int32 argc, char** argv)
:::
Hook function that's invoked when the application receives a
{cpp:func}`~B::ARGV`
message. The message is sent if command
line arguments are used in launching the application from the shell, or if
{hparam}`argv`/{hparam}`argc` values are passed to
{cpp:func}`BRoster::Launch`.
:::{admonition} Warning
:class: warning
This function isn't called if there were no command line arguments, or if
{cpp:func}`BRoster::Launch`
was called without {hparam}`argv`/{hparam}`argc` values.
:::
When the application is launched from the shell, {hmethod}`ArgvReceived()`'s
arguments are identical to the traditional main()
arguments: The number of command line arguments is passed as
{hparam}`argc`; the arguments themselves are passed as an array of
strings in {hparam}`argv`. The first {hparam}`argv`
string identifes the executable file; the other strings are the command line
arguments proper. For example, this…
:::{code}
$ MyApp file1 file2
:::
…produces the {hparam}`argv` array
{ "./MyApp", "file1", "file2" }.

{cpp:func}`BRoster::Launch`
forwards its {hparam}`argv` and {hparam}`argc`
arguments, but adds the executable name to the front of the
{hparam}`argv` array and increments the
{hparam}`argc` value.
Normally, the {cpp:func}`~B::ARGV`
message (if sent at all) is sent once, just before
{cpp:func}`~B::READY`
is sent. However, if the user tries to re-launch (from the command line and with
arguments) an already-running application that's set to
{cpp:func}`~B::EXCLUSIVE` or
{cpp:func}`~B::SINGLE`,
the re-launch will generate a
{cpp:func}`~B::ARGV`
message that's sent to the already-running image. Thus, for such apps, the
{cpp:func}`~B::ARGV`
message can show up at any time.
::::

::::{abi-group}

:::{cpp:function} virtual void BApplication::Pulse()
:::
{hmethod}`Pulse()` is a hook function that's called when
the application receives a {cpp:func}`~B::PULSE`
message. The message is sent at the rate set in
{cpp:func}`~BApplication::SetPulseRate`.
The first {hmethod}`Pulse()` message is sent after
{cpp:func}`~BApplication::ReadyToRun` returns.
You can implement {hmethod}`Pulse()` to do whatever you want (the
default version does nothing), but don't try to use it for precision timing: The
pulse granularity is no better than 100,000 microseconds.
Keep in mind that {hmethod}`Pulse()` executes in the app's message loop
thread along with all other message handling functions. Your application won't receive any
{hmethod}`Pulse()` invocations while it's waiting for some other handler
function (including
{cpp:func}`~BApplication::MessageReceived`)
to finish. In the meantime,
{cpp:func}`~B::PULSE`
messages will be stacking up
in the message queue; when the loop becomes "unblocked", you'll see a burst
of {hmethod}`Pulse()` invocations.
::::

::::{abi-group}

:::{cpp:function} virtual bool BApplication::QuitRequested()
:::
Hook function that's invoked when the application receives a
{cpp:func}`~B::QUIT`
message. As described in the
{cpp:class}`BLooper` class (which declares
this function), the request to quit is confirmed if
{hmethod}`QuitRequested()` returns {cpp:enum}`true`, and
denied if it returns {cpp:enum}`false`.
In its implementation, {hclass}`BApplication` sends
{cpp:func}`BLooper::QuitRequested`
to each of its {cpp:class}`BWindow`
objects. If they all agree to quit, the windows are all destroyed (through
{cpp:func}`BWindow::Quit`)
and this {hmethod}`QuitRequested()` returns
{cpp:enum}`true`. But if any
{cpp:class}`BWindow` refuses to quit,
that window and all surviving windows are saved, and this
{hmethod}`QuitRequested()` returns {cpp:enum}`false`.
Augment this function as you will, but be sure to call the
{hclass}`BApplication` version in your implementation.
::::

::::{abi-group}

:::{cpp:function} virtual void BApplication::ReadyToRun()
:::
Hook function that's called when the application receives a
{cpp:func}`~B::READY`
message. The message is sent automatically during the
{cpp:func}`~BApplication::Run`
function, and is sent after the initial
{cpp:func}`~B::REFS` and
{cpp:func}`~B::ARGV`
messages (if any) have been handled. This is the only application message
that every running application is guaranteed to receive.
What you do with {hmethod}`ReadyToRun()` is up to you,
if your application hasn't put up a window by the time this function is
called, you'll probably want to do it here. The default version of
{hmethod}`ReadyToRun()` is empty.
::::

::::{abi-group}

:::{cpp:function} virtual void BApplication::RefsReceived(BMessage* message)
:::
Hook function that's called when the application receives a
{cpp:func}`~B::REFS`
message. The message is sent when the user drops a file (or files) on your
app's icon, or double clicks a file that's handled by your app. The message
can arrive either at launch time, or while your application is already
running use
{cpp:func}`~BApplication::IsLaunching`
to tell which.
{hparam}`message` contains a single field named
be:refs that contains one or more entry_ref
({cpp:enum}`B_REF_TYPE`) items one for each file that was dropped
or double-clicked. Do with them what you will; the default implementation
is empty. Typically, you would use the refs to create
{cpp:class}`BEntry` or
{cpp:class}`BFile` objects.
::::

## Member Functions
::::{abi-group}

????
::::

::::{abi-group}

See {cpp:func}`BArchivable::Archive`
::::

::::{abi-group}

See {cpp:func}`BLooper::DispatchMessage`

::::

::::{abi-group}

:::{cpp:function} status_t BApplication::GetAppInfo(app_info* theInfo) const
:::
Returns information about the application. This is a cover for
:::{code}
be_roster->GetRunningAppInfo(be_app->Team(), theInfo);
:::
See {cpp:func}`BRoster::GetAppInfo`
for more information.
::::

::::{abi-group}

:::{cpp:function} virtual status_t BApplication::GetSupportedSuites(BMessage* message)
:::
Adds the scripting suite "suite/vnd.Be-application" to message. See
"{cpp:func}`~BApplication::ScriptingSuites`"
for the suite's properties. Also see
{cpp:func}`BHandler::GetSupportedSuites`
for more information on how this function works.
::::

::::{abi-group}

:::{cpp:function} bool BApplication::IsLaunching() const
:::
Returns {cpp:enum}`true` if the application is still
launching. An application is considered to be in its launching phase until
{cpp:func}`~BApplication::ReadyToRun`
returns. Invoked from within
{cpp:func}`~BApplication::ReadyToRun`,
{hmethod}`IsLaunching()` returns
{cpp:enum}`true`.
::::

::::{abi-group}

See
{cpp:func}`BHandler::MessageReceived`
::::

::::{abi-group}

See
{cpp:func}`BHandler::ResolveSpecifier`
::::

::::{abi-group}

:::{cpp:function} virtual thread_id BApplication::Run()
:::
:::{cpp:function} virtual void BApplication::Quit()
:::
These functions, inherited from
{cpp:class}`BLooper`, are different
enough from their parent versions to warrant description.
{hmethod}`Run()` doesn't spawn a new thread—it runs
the message loop in the thread that it's called from, and doesn't return
until the message loop stops.
{hmethod}`Quit()` doesn't kill the looper thread it tells the
thread to finish processing the message queue (disallowing new messages) at
which point {hmethod}`Run()` will be able to return. After so
instructing the thread, {hmethod}`Quit()` returns, it doesn't
wait for the message queue to empty.
Also, {hmethod}`Quit()` doesn't delete the
{hclass}`BApplication` object. It's up to you to delete it
after {hmethod}`Run()` returns. (However,
{hmethod}`Quit()` does delete the object
if it's called before the message loop starts i.e. before
{hmethod}`Run()` is called.)
::::

::::{abi-group}

:::{cpp:function} void BApplication::SetCursor(const void* cursor)
:::
:::{cpp:function} void BApplication::SetCursor(const BCursor* cursor, bool sync = true)
:::
:::{cpp:function} void BApplication::HideCursor()
:::
:::{cpp:function} void BApplication::ShowCursor()
:::
:::{cpp:function} void BApplication::ObscureCursor()
:::
:::{cpp:function} bool BApplication::IsCursorHidden() const
:::
{hmethod}`SetCursor()` sets the cursor image that's used when
this is the active application.
You can pass one of the Be-defined cursor
constants ({cpp:func}`~B::HAND` and
{cpp:func}`~B::I`)
or create your own cursor image. The cursor data format is described
in the {cpp:class}`BCursor`
{ref}`class overview`.
You can also call {hmethod}`SetCursor()` passing a
{cpp:class}`BCursor` object;
specifying {hparam}`sync` as {cpp:enum}`true`
forces the Application Server to immediately
resynchronize, thereby ensuring that the cursor change takes place
immediately. The default {cpp:class}`BCursor`s are
{cpp:func}`~B::CURSOR`
for the hand cursor and
{cpp:func}`~B::CURSOR`
for the I-beam text editing cursor.
{hmethod}`HideCursor()` removes the cursor from the screen.
{hmethod}`ShowCursor()` restores it.
{hmethod}`ObscureCursor()` hides the cursor until the user moves the mouse.
{hmethod}`IsCursorHidden()` returns {cpp:enum}`true`
if the cursor is hidden (but not obscured), and {cpp:enum}`false`
if not.
The cursor data format is described in the
"{cpp:func}`~BCursor::Overview`" section
in the {cpp:class}`BCursor overview`.
::::

::::{abi-group}

:::{cpp:function} void BApplication::SetPulseRate(bigtime_t rate)
:::
Sets the period between
{cpp:func}`~B::PULSE`
messages being sent and the
{cpp:func}`~BApplication::Pulse`
method being called. If the pulse rate is 0 (the default), the
{cpp:func}`~B::PULSE`
messages aren't sent.
::::

::::{abi-group}

:::{cpp:function} BWindow* BApplication::WindowAt(int32 index) const
:::
:::{cpp:function} int32 BApplication::CountWindows() const
:::
{hmethod}`WindowAt()` returns the {hparam}`index`'th
{cpp:class}`BWindow` object in the
application's window list. If {hparam}`index` is out of range, the
function returns {cpp:enum}`NULL`.
{hmethod}`CountWindows()` returns the number of windows in the
window list.
The windows list includes all windows explicitly created by the app—whether
they're normal, floating, or modal, and whether or not they're actually
displayed—but excludes private windows created by Be classes.
The order of windows in the list has no signficance.
Locking the {hclass}`BApplication` object doesn't lock the window
list. If you need coordinated access to the list, you'll have to provide your
own locking mechanism that protects these functions and all
{cpp:class}`BWindow` construction
and deletion.
::::

## Static Functions
::::{abi-group}

:::{cpp:function} static BResources* BApplication::AppResources()
:::
Returns a {cpp:class}`BResources` object that's
configured from your application's executable file. You may read the data
in the {cpp:class}`BResources`
object, but you're not allowed to write it; see the {cpp:class}`BResources` class for
details. The {cpp:class}`BResources` object
belongs to the {hclass}`BApplication` class and mustn't be
freed.
You needn't have a be_app object to
invoke this function.
::::

::::{abi-group}

See {cpp:func}`BArchivable::Instantiate`
::::

## Global Variables
::::{abi-group}

:::{code}
BApplication* be_app;
:::
be_app is the global variable that
represents your {hclass}`BApplication` object. You can refer
to be_app anywhere you need a reference to the {hclass}`BApplication` object that you created. If you want to call a function that's declared by your {hclass}`BApplication` subclass, you have to cast be_app to your subclass:
:::{code}
((MyApp *)be_app)->MyAppFunction();
:::
::::

::::{abi-group}

:::{code}
BMessenger* be_app_messenger;
:::
be_app_messenger is a global
{cpp:class}`BMessenger` that
targets your be_app object. It's created in the
{hclass}`BApplication` {cpp:func}`~BApplication::Constructor`.
::::

## Archived Fields
## Scripting Suites and Properties
::::{abi-group}

"Name"CommandSpecifierDescriptionB_GET_PROPERTYB_DIRECT_SPECIFIERGets the name of the application's main thread.
"Window"CommandSpecifierDescriptionB_COUNT_PROPERTIESB_DIRECT_SPECIFIERReturns CountWindows().Not applicable.B_NAME_SPECIFIER, B_INDEX_SPECIFIER, B_REVERSE_INDEX_SPECIFIERThe message is forwarded to the specified BWindow.
::::
