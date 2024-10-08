# BRoster

The {cpp:class}`BRoster` object represents a service that keeps a roster of
all applications currently running. It can provide information about any of
those applications, activate one of them, add another application to the
roster by launching it, or get information about an application to help you
decide whether to launch it.

There's just one roster and it's shared by all applications. When an
application starts up, a {cpp:class}`BRoster` object is constructed and
assigned to a global variable, {cpp:var}`be_roster`. You always access the
roster through this variable; you never have to instantiate a
{cpp:class}`BRoster` in application code.

The {cpp:class}`BRoster` identifies applications in three ways:

1. By {htype}`entry_ref` references to the executable files where they
  reside.

2. By their signatures. The signature is a unique identifier for the
  application assigned as a file-system attribute or resource at compile
  time or by the {cpp:class}`BApplication` constructor at run time.

3. At run time, by their {htype}`team_id`s. A team is a group of threads
  sharing an address space; every application is a team.

If an application is launched more than once, the roster will include one
entry for each instance of the application that's running. These instances
will have the same signature, but different team identifiers.
