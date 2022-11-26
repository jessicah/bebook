# BApplication Overview

## BApplication

The BApplication class defines an object that represents your application,
creates a connection to the App Server, and runs your app's main message loop.
An app can only create one BApplication object; the system automatically sets
the global `be_app` object to point to the `BApplication` object you create.

A `BApplication` object's most pervasive task is to handle messages that are
sent to your app, a subject that's described in detail below. But message
handling aside, you can also use your `BApplication` object to...

Control the cursor.

: `BApplication` defines functions that hide and show the cursor, and set
  the cursor's image. See `SetCursor()`.

Access the window list.

: You can iterate through the windows that your application has created with
  `WindowAt()`.

Get information about your application.

: Your app's signature, executable location, and launch flags can be retrieved
  through `GetAppInfo()`. Additional information icons, version strings,
  recognized file types can be retrieved by creating an `BAppFileInfo`
  object based on your app's executable file. `BAppFileInfo` is defined in
  `The Storage Kit`.

## `be_app` and Subclassing BApplication

Because of its importance, the `BApplication` object that you create is
automatically assigned to the global `be_app` variable. Anytime you need to
refer to your `BApplication` object from anywhere in your code you can use
`be_app` instead.

Unless you're creating a very simple application, you should subclass
`BApplication`. But be aware that the `be_app` variable is typed as
`BApplication *`. You'll have to cast `be_app` when you call a function
that's declared by your subclass:

```
((MyApp *)be_app)->MyAppFunction();
```

## Constructing the Object and Running the Message Loop

As with all `BLooper`s, to use a `BApplication` you construct the object and
then tell it to start its message loop by calling the `Run()` function.
However, unlike other loopers, `BApplication`s `Run()` doesn't return until
the application is told to quit. And after `Run()` returns, you delete the
object, it isn't deleted for you.

Typically, you create your `BApplication` object in your `main()`
function--it's usually the first object you create. The barest outline of a
typical `main()` function looks something like this:

```beapi
#include <Application.h>

main()
{
        new BApplication("application/x-vnd.your-app-sig");
        /* Further initialization goes here -- read settings,
           set globals, etc. */
        be_app->Run();
        /* Clean up -- write settings, etc. */
        delete be_app;
}
```

1. The `main()` function doesn't declare `argc` and `argv` parameters
   : (used for passing along command line arguments). If the user passes command line
     arguments to your app, they'll show up in the `ArgsReceived()` hook function.
2. Why no pointer assignment? The constructor automatically assigns the object
   : to `be_app`, so you don't have to assign it yourself.
3. The string passed to the constructor sets the application's signature. This
   : is a precautionary measure; it's better to add the signature as a resource
     than to define it here (a resource signature overrides the constructor
     signature). Use the FileTypes app to set the signature as a resource.

## Application Messages

After you tell your BApplication to run, its message loop begins to receive messages. In general,
the messages are handled in the expected fashion: They show up in BApplication's MessageReceived()
function (or that of a designated BHandler; for more on how messages are dispatched to handlers, see
"From Looper to Handler").

But BApplication also recognizes a set of application messages that it handles by invoking
corresponding hook functions. The hook functions are invoked by DispatchMessage() so the application
messages never show up in MessageRecieved().

Overriding the hook functions that correspond to the application messages is an important part of
the implementation of a BApplication subclass.

In the table below, the application messages (identified by their command constants) are listed in
roughly the order your BApplication can expect to receive them.

:::{list-table}
---
header-rows: 1
---
-
  - Command Constant
  - Hook Function
  - Description
-
  - `B_ARGV_RECEIVED`
  - `ArgvReceived()`
  - Command line arguments are delivered through this message.
-
  - `B_REFS_RECEIVED`
  - `RefsReceived()`
  - Files (`entry_refs`) that are dropped on your app's icon, or that are double-clicked to launch
    your app, are delivered through this message.
-
  - `B_READY_TO_RUN`
  - `ReadyToRun()`
  - Invoked from within `Run()`, the application has finished configuring itself and is ready to go.
   you haven't already created and displayed an initial window, you should do so here.
-
  - `B_APP_ACTIVATED`
  - `AppActivated()`
  - The application has just become the active application, or has relinquished that status.
-
  - `B_PULSE`
  - `Pulse()`
  - If requested, pulse messages are sent at regular intervals by the system.
-
  - `B_ABOUT_REQUESTED`
  - `AboutRequested()`
  - The user wants to see the app's About... box.
:::

The protocols for the application messages are described in the "Message Constants" section of this
chapter.

For more information on the details of when and why the hook functions are invoked, see the
individual function descriptions.

A BApplication can also receive the B_QUIT_REQUESTED looper message. As explained in BLooper,
B_QUIT_REQUESTED causes Quit() to be called, contigent on the value returned by the QuitRequested()
hook function. However, BApplication's implementation of Quit() is different from BLooper's version.
Don't miss it.

## Other Topics

Locking

: Like a `BLooper`, a `BApplication` must be locked before calling certain
  protected functions. The `BApplication` locking mechanism is inherited
  without modification from `BLooper`.

FileTypes settings

: The `BApplication` object represents your application at runt-time.
  However, some of the characteristics of your application, whether it can be
  launched more than once, the file types it can open, its icon are not
  run-time decisions.
