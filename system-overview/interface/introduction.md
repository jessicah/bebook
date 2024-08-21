---
title: The Interface Kit
---

# Introduction

Most applications have an interactive graphic user interface. When an app
starts, it displays a set of windows in which the user can click and type. The
application responds to the user's actions, and updates its window to show the
user that it's listening.

To run this kind of user interface, an application has to:

* Manage a set of windows

* Draw within the windows

* Respond to the users's actions (reported as interface messages)

The Interface Kit defines a set of C++ classes that provide a structure for
these operations. This chapter first introduces the conceptual framework for the
user interface. A [second chapter](./index.rst) then describes all the classes, functions,
types, and constants the kit defines.

# Framework for the User Interface

A graphical user interface is organized around windows. In a multitasking
environment, any number of applications might be running at the same time, each
with its own set of windows on-screen. The windows of all running applications
must cooperate in a common interface. The Application Server manages this mess.
It's the conduit for an application's message input and drawing output:

- It monitors the keyboard and mouse and sends messages reporting each user keystroke and mouse action to the application.

- It receives drawing instructions from the application and interprets them to render images within windows.

# BWindow Objects

Every window in an application is represented by a separate {cpp:class}`BWindow` object.
Constructing the {cpp:class}`BWindow` establishes a connection to the Application Server.
When you call {cpp:class}`BWindow`'s window-manipulating functions ({cpp:func}`~BWindow::Show()`, {cpp:func}`~BWindow::MoveTo()`,
{cpp:func}`~BWindow::SetTitle()` and so on), the object sends a message to the server, which performs
the actual manipulation.

The {cpp:class}`BWindow` class inherits from {cpp:class}`BLooper`. Every {cpp:class}`BWindow` object spawns a thread
(in the application's address space) where it receives and responds to interface
messages from the server.

All other Interface Kit objects play roles that depend on a {cpp:class}`BWindow`. They
draw in a window, respond to interface messages received by a window, or act in
support of other objects that draw and respond to messages.

# BView Objects

A window is divided into smaller rectangular areas called views. Each view
corresponds to one part of what the window displays—a scroll bar, a document, a
list, and so on.

An application sets up a view by constructing a {cpp:class}`BView` object and associating
it with a particular {cpp:class}`BWindow`. The {cpp:class}`BView` object is responsible for drawing
within the view rectangle and for handling interface messages directed at that
area.

## Drawing in a View

A window can retain and display rendered images, but it can't draw them; for
that it needs a set of {cpp:class}`BView`s. A {cpp:class}`BView` is an agent for drawing, but it can't
render the images it creates; for that it needs a {cpp:class}`BWindow`. The two objects work
hand in hand.

Each {cpp:class}`BView` object is an autonomous graphics environment for drawing: It has its
own coordinate system, current colors, drawing mode, clipping region, font, pen
position, and so on. The {cpp:class}`BView` class also defines functions that represent
elemental drawing operations such as line stroking, character drawing, and image
blitting.

## Handling Messages in a View

When the user acts, system messages that report the resulting events are sent to
the {cpp:class}`BWindow` object, which determines which {cpp:class}`BView` elicited the user action and
should respond to it. For example, a {cpp:class}`BView` that draws typed text can expect to
respond to messages reporting the user's keystrokes. A {cpp:class}`BView` that draws a button
gets to handle the messages that are generated when the button is clicked. The
{cpp:class}`BView` class derives from {cpp:class}`BHandler`, so {cpp:class}`BView` objects are eligible to handle
messages dispatched by the {cpp:class}`BWindow`.

# The View Hierarchy

A window typically contains a number of different views—all arranged in a
hierarchy beneath the top view, a view that's exactly the same size as the
content area of the window. The top view is a companion of the window; it's
created by the {cpp:class}`BWindow` object when the {cpp:class}`BWindow` is constructed. When the window
is resized, the top view is resized to match. Unlike other views, the top view
doesn't draw or respond to messages; it serves merely to connect the window to
the views that the application creates and places in the hierarchy.

The view hierarchy can be represented as a branching tree structure with the top
view at its root. All views in the hierarchy (except the top view) have one, and
only one, parent view. Each view (including the top view) can have any number of
child views.

When a new {cpp:class}`BView` object is created, it isn't attached to a window and it has no
parent. It's added to a window by making it a child of a view already in the
view hierarchy. This is done with the {cpp:func}`~BView::AddChild()` function. A view can be made a
child of the window's top view by calling {cpp:class}`BWindow`'s version of {cpp:func}`~BWindow::AddChild()`.

Until it's assigned to a window, a {cpp:class}`BView` can't draw and won't receive reports of
events. {cpp:class}`BView`s know how to produce images, but it takes a window to display and
retain the images they create.

## Drawing and Message Handling in the View Hierarchy

The view hierarchy determines what's displayed where on-screen, and also how
user actions are associated with the responsible {cpp:class}`BView` object:

- When the views in a window are called on to draw, parents draw before their children; children draw in front of their ancestors.

- Mouse events are associated with the view where the cursor is located.

## Overlapping Siblings

Siblings don't draw in a predefined order. If they overlap, it's indeterminate
which view will draw last—that is, which one will draw in front of the others.
Similarly, it's indeterminate which view will receive the mouse events that
occur in the area the siblings share.

Therefore, it's strongly recommended that you arrange your sibling views so they
don't overlap.
