# BFileGameSound

If you want to play back audio from a disk file, such as background music,
or low-priority sound effects, {cpp:class}`BFileGameSound` is for you.

Keep in mind that if the sound needs to play at precise moments, or
latency is an issue, that {cpp:class}`BFileGameSound` may not be
appropriate for your needs.

Using {cpp:class}`BFileGameSound` is easy, and it supports automatically
looping sounds. The following code snippet starts up the theme music for
the hot new game "Mystery Warriors From the Doomed Planet Z":

:::{code} cpp
BFileGameSound themeSong("music/theme.aif", true);
themeSong.StartPlaying();
:::

This starts up a looped sound from the file music/theme.aif. If you want
the theme to only play through once, just specify {cpp:expr}`false` instead
of {cpp:expr}`true` for the looping argument to the
{cpp:class}`BFileGameSound` constructor.

You can pause the {cpp:class}`BFileGameSound` by calling
{cpp:func}`SetPaused() <BFileGameSound::SetPaused>`:

:::{code} cpp
themeSong.SetPaused(true, 0);
:::

This pauses the sound, effective immediately. The pause can optionally be
ramped, so that the sound slows down or speeds up to reach the new setting.
For example:

:::{code} cpp
themeSong.SetPaused(true, 2);
:::

This causes the sound to slow down over the course of two seconds, until
it's stopped.

The inverse is also possible:

:::{code} cpp
themeSong.SetPaused(false, 0);
:::

This resumes playback immediately. You can ramp the resume by specifying a
non-zero value for the ramp time.

{cpp:class}`BFileGameSound` uses the {cpp:class}`BMediaFile` class to
access the sound file. If {cpp:class}`BMediaFile` can't identify the sound,
the file is assumed to contain raw 44.1kHz, 16-bit stereo.
