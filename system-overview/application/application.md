# BApplication

The {cpp:class}`BApplication` class defines an object that represents your
application, creates a connection to the App Server, and runs your app's
main message loop. An app can only create one {cpp:class}`BApplication`
object; the system automatically sets the global
{cpp:func}`~BApplication::be` object to point to the
{cpp:class}`BApplication` object you create.

A {cpp:class}`BApplication` object's most pervasive task is to handle
messages that are sent to your app, a subject that's described in detail
below. But message handling aside, you can also use your
{cpp:class}`BApplication` object to…



## be_app and Subclassing BApplication

Because of its importance, the {cpp:class}`BApplication` object that you
create is automatically assigned to the global
{cpp:func}`~BApplication::be` variable. Anytime you need to refer to your
{cpp:class}`BApplication` object from anywhere in your code you can use
{cpp:func}`~BApplication::be` instead.

Unless you're creating a very simple application, you should subclass
{cpp:class}`BApplication`. But be aware that the
{cpp:func}`~BApplication::be` variable is typed as
({cpp:class}`BApplication` *). You'll have to cast
{cpp:func}`~BApplication::be` when you call a function that's declared by
your subclass:

:::{code}
((MyApp *)be_app)->MyAppFunction();
:::

## Constructing the Object and Running the Message Loop

As with all {cpp:class}`BLooper`s, to use a {cpp:class}`BApplication` you
construct the object and then tell it to start its message loop by calling
the {cpp:func}`~BApplication::Run` function. However, unlike other loopers,
{cpp:class}`BApplication`'s {cpp:func}`~BApplication::Run` doesn't return
until the application is told to quit. And after
{cpp:func}`~BApplication::Run` returns, you delete the object it isn't
deleted for you.

Typically, you create your {cpp:class}`BApplication` object in your
{hmethod}`main()` function—it's usually the first object you create. The
barest outline of a typical {hmethod}`main()` function looks something like
this:

:::{code}
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



## Application Messages

After you tell your {cpp:class}`BApplication` to run, its message loop
begins to receive messages. In general, the messages are handled in the
expected fashion: They show up in {cpp:class}`BApplication`'s
{cpp:func}`~BApplication::MessageReceived` function (or that of a
designated {cpp:class}`BHandler`; for more on how messages are dispatched
to handlers, see ("{cpp:func}`~TheApplicationKit::Messaging`").

But {cpp:class}`BApplication` also recognizes a set of application
messages that it handles by invoking corresponding hook functions. The hook
functions are invoked by {cpp:func}`~BApplication::DispatchMessage` so the
application messages never show up in
{cpp:func}`~BApplication::MessageReceived`.

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

	- {cpp:func}`~B::ARGV`

	- {cpp:func}`~BApplication::ArgvReceived`

	- Command line arguments are delivered through this message.

-

	- {cpp:func}`~B::REFS`

	- {cpp:func}`~BApplication::RefsReceived`

	- Files ({htype}`entry_ref`s) that are dropped on your app's icon, or that
are double-clicked to launch your app are delivered through this message.

-

	- {cpp:func}`~B::READY`

	- {cpp:func}`~BApplication::ReadyToRun`

	- Invoked from within {cpp:func}`~BApplication::Run`, the application has
finished configuring itself and is ready to go. If you haven't already
created and displayed an initial window, you should do so here.

-

	- {cpp:func}`~B::APP`

	- {cpp:func}`~BApplication::AppActivated`

	- The application has just become the active application, or has
relinquished that status.

-

	- {cpp:func}`~B::PULSE`

	- {cpp:func}`~BApplication::Pulse`

	- If requested, pulse messages are sent at regular intervals by the system.

-

	- {cpp:func}`~B::ABOUT`

	- {cpp:func}`~BApplication::AboutRequested`

	- The user wants to see the app's About… box.
:::

The protocols for the application messages are described in the
"{ref}`Message Constants`" section of this chapter.

For more information on the details of when and why the hook functions are
invoked, see the individual function descriptions.

A {cpp:class}`BApplication` can also receive the {cpp:func}`~B::QUIT`
looper message. As explained in {cpp:class}`BLooper`, {cpp:func}`~B::QUIT`
causes {hmethod}`Quit()` to be called, contingent on the value returned by
the {hmethod}`QuitRequested`() hook function. However,
{cpp:class}`BApplication`'s implementation of
{cpp:func}`~BApplication::Quit` is different from {cpp:class}`BLooper`'s
version. Don't miss it.

## Other Topics


