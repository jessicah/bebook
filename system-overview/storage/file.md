# BFile

A {hclass}`BFile` lets you read and write the data portion of a file. It
does this by implementing the {cpp:func}`Read() <BFile::Read>` /
{cpp:func}`Write() <BFile::Write>` and {cpp:func}`ReadAt() <BFile::ReadAt>`
/ {cpp:func}`WriteAt() <BFile::WriteAt>` functions that are declared by the
{cpp:class}`BPositionIO` class.

## Initializing and Opening

When you construct (or otherwise initialize) a {hclass}`BFile`, the file
is automatically opened. The file is closed when you re-initialize or
destroy the object.

At each initialization, you're asked to supply an "open mode" value. this
is a combination of flags that tells the object whether you want to read
and/or write the file, create it if it doesn't exist, truncate it, and so
on.

You can also initialize a BFile, and create a new file at the same time,
through {cpp:class}`BDirectory`'s {cpp:func}`CreateFile()
<BDirectory::CreateFile>` function. In this case, you don't have to supply
an open mode—the {hclass}`BFile` that's returned to you will automatically
be open for reading and writing. (You are asked if you want the creation to
fail if the named file already exists.)

## Access to Directories and Symbolic Links

Although {hclass}`BFile`s are meant to be used to access regular files,
you aren't prevented from opening and reading a directory (you won't be
able to write the directory, however). This isn't exactly a feature—there's
not much reason to access a directory this way—you should simply be aware
that it's not an error.

Symbolic links, however, can't be opened by a {hclass}`BFile`—not because
it's illegal, but because if you ask to open a symbolic link, the link is
automatically traversed. The node that the {hclass}`BFile` ends up opening
will be the file or directory that the link points to.

This is a feature; very few applications should ever need to look at a
symbolic link. (If yours is one of the few that does want to, you should go
visit the {cpp:class}`BSymLink` class.)
