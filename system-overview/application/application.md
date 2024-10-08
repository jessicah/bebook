# BApplication

The {cpp:class}`BApplication` class defines an object that represents your
application, creates a connection to the App Server, and runs your app's
main message loop. An app can only create one {cpp:class}`BApplication`
object; the system automatically sets the global {cpp:var}`be_app` object
to point to the {cpp:class}`BApplication` object you create.

A {cpp:class}`BApplication` object's most pervasive task is to handle
messages that are sent to your app, a subject that's described in detail
below. But message handling aside, you can also use your
{cpp:class}`BApplication` object to…

Control the cursor.

: {cpp:class}`BApplication` defines functions that hide and show the cursor,
and set the cursor's image. See {cpp:func}`~BApplication::SetCursor()`.

Access the window list.

: You can iterate through the windows that your application has created with
{cpp:func}`~BApplication::WindowAt()`.

Get information about your application.

: Your app's signature, executable location, and launch flags can be
retrieved through {cpp:func}`~BApplication::GetAppInfo()`. Additional
information icons, version strings, recognized file types can be retrieved
by creating an {cpp:class}`BAppFileInfo` object based on your app's
executable file. {cpp:class}`BAppFileInfo` is defined in the {ref}`The
Storage Kit`.

## be_app and Subclassing BApplication

Because of its importance, the {cpp:class}`BApplication` object that you
create is automatically assigned to the global {cpp:var}`be_app` variable.
Anytime you need to refer to your {cpp:class}`BApplication` object from
anywhere in your code you can use {cpp:var}`be_app` instead.

Unless you're creating a very simple application, you should subclass
{cpp:class}`BApplication`. But be aware that the {cpp:var}`be_app` variable
is typed as ({cpp:class}`BApplication` *). You'll have to cast
{cpp:var}`be_app` when you call a function that's declared by your
subclass:

:::{code} cpp
((MyApp *)be_app)->MyAppFunction();
:::

## Constructing the Object and Running the Message Loop

As with all {cpp:class}`BLooper`s, to use a {cpp:class}`BApplication` you
construct the object and then tell it to start its message loop by calling
the {cpp:func}`~BApplication::Run()` function. However, unlike other
loopers, {cpp:class}`BApplication`'s {cpp:func}`~BApplication::Run()`
doesn't return until the application is told to quit. And after
{cpp:func}`~BApplication::Run()` returns, you delete the object it isn't
deleted for you.

Typically, you create your {cpp:class}`BApplication` object in your
{hmethod}`main()` function—it's usually the first object you create. The
barest outline of a typical {hmethod}`main()` function looks something like
this:

:::{code} cpp
#include Application.h

main()
{
   new BApplication("application/x-vnd.your-app-sig");
   /* Further initialization goes here -- read settings,
      set globals, etc. */
   be_app->Run();
   /* Clean up -- write settings, etc. */
   delete be_app;
}
:::

:::{list-table}
---
header-rows: 0
align: left
widths: auto
---
-
	- {ref}``

	- The {hmethod}`main()` function doesn't declare {hparam}`argc` and
		{hparam}`argv` parameters (used for passing along command line arguments).
		If the user passes command line arguments to your app, they'll show up in
		the {cpp:func}`~BApplication::ArgvReceived()` hook function.
-
	- {ref}``

	- Why no pointer assignment? The constructor automatically assigns the object
		to {cpp:var}`be_app`, so you don't have to assign it yourself.
-
	- {ref}``

	- The string passed to the constructor sets the application's signature. This
		is a precautionary measure it's better to add the signature as a resource
		than to define it here (a resource signature overrides the constructor
		signature). Use the FileTypes app to set the signature as a resource.
-
	- {ref}``

	- As explained in the {cpp:class}`BLooper` class,
		{cpp:func}`~BApplication::Run()` is almost always called from the same
		thread in which you construct the {cpp:class}`BApplication` object. (More
		accurately, the constructor locks the object, and
		{cpp:func}`~BApplication::Run()` unlocks it. Since locks are scoped to
		threads, the easiest thing to do is to construct and
		{cpp:func}`~BApplication::Run()` in the same thread.)

:::

## Application Messages

After you tell your {cpp:class}`BApplication` to run, its message loop
begins to receive messages. In general, the messages are handled in the
expected fashion: They show up in {cpp:class}`BApplication`'s
{cpp:func}`~BApplication::MessageReceived()` function (or that of a
designated {cpp:class}`BHandler`; for more on how messages are dispatched
to handlers, see ("{ref}`From Looper to Handler`").

But {cpp:class}`BApplication` also recognizes a set of application messages
that it handles by invoking corresponding hook functions. The hook
functions are invoked by {cpp:func}`~BApplication::DispatchMessage()` so
the application messages never show up in
{cpp:func}`~BApplication::MessageReceived()`.

Overriding the hook functions that correspond to the application messages
is an important part of the implementation of a {cpp:class}`BApplication`
subclass.

In the table below, the application messages (identified by their command
constants) are listed in roughly the order your {cpp:class}`BApplication`
can expect to receive them.

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Command Constant

	- Hook function

	- Description

-
	- {cpp:enumerator}`B_ARGV_RECEIVED`

	- {cpp:func}`~BApplication::ArgvReceived()`

	- Command line arguments are delivered through this message.

-
	- {cpp:enumerator}`B_REFS_RECEIVED`

	- {cpp:func}`~BApplication::RefsReceived()`

	- Files ({htype}`entry_ref`s) that are dropped on your app's icon, or that
are double-clicked to launch your app are delivered through this message.

-
	- {cpp:enumerator}`B_READY_TO_RUN`

	- {cpp:func}`~BApplication::ReadyToRun()`

	- Invoked from within {cpp:func}`~BApplication::Run()`, the application has
finished configuring itself and is ready to go. If you haven't already
created and displayed an initial window, you should do so here.

-
	- {cpp:enumerator}`B_APP_ACTIVATED`

	- {cpp:func}`~BApplication::AppActivated()`

	- The application has just become the active application, or has relinquished
that status.

-
	- {cpp:enumerator}`B_PULSE`

	- {cpp:func}`~BApplication::Pulse()`

	- If requested, pulse messages are sent at regular intervals by the system.

-
	- {cpp:enumerator}`B_ABOUT_REQUESTED`

	- {cpp:func}`~BApplication::AboutRequested()`

	- The user wants to see the app's About… box.


:::

The protocols for the application messages are described in the
"{ref}`Message Constants`" section of this chapter.

For more information on the details of when and why the hook functions are
invoked, see the individual function descriptions.

A {cpp:class}`BApplication` can also receive the
{cpp:enumerator}`B_QUIT_REQUESTED` looper message. As explained in
{cpp:class}`BLooper`, {cpp:enumerator}`B_QUIT_REQUESTED` causes
{hmethod}`Quit()` to be called, contingent on the value returned by the
{hmethod}`QuitRequested`() hook function. However,
{cpp:class}`BApplication`'s implementation of
{cpp:func}`~BApplication::Quit()` is different from {cpp:class}`BLooper`'s
version. Don't miss it.

## Other Topics

Locking.

: Like a {cpp:class}`BLooper`, a {cpp:class}`BApplication` must be locked
before calling certain protected functions. The {cpp:class}`BApplication`
locking mechanism is inherited without modification from
{cpp:class}`BLooper`.

FileTypes settings.

: The {cpp:class}`BApplication` object represents your application at
run-time. However, some of the characteristics of your application, whether
it can be launched more than once, the file types it can open, its icon are
not run-time decisions.
