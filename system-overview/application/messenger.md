# BMessenger

A {cpp:class}`BMessenger` represents and sends messages to a message
target, where the target is a {cpp:class}`BLooper` and, optionally, a
specific {cpp:class}`BHandler` within that looper. The target can live in
the same application as the {cpp:class}`BMessenger` (a local target), or it
can live in some other application (a remote target).

{cpp:class}`BMessenger`'s most significant function is
{cpp:func}`SendMessage() <BMessenger::SendMessage>`, which sends its
argument {cpp:class}`BMessage` to the target.

:::{admonition} Note
:class: note
For a local target, {cpp:func}`SendMessage() <BMessenger::SendMessage>` is
roughly equivalent, in terms of efficiency, to posting a message directly
to the {cpp:class}`BMessenger`'s target (i.e
{cpp:func}`BLooper::PostMessage`).
:::

The global {cpp:var}`be_app_messenger` {cpp:class}`BMessenger` pointer,
which targets {cpp:var}`be_app`'s main message loop, is automatically
initialized for you when you create your {cpp:class}`BApplication` object.
You can use it wherever {cpp:class}`BMessenger`s are called for.
