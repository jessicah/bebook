# BSimpleGameSound

The {cpp:class}`BSimpleGameSound` class represents simple sound effects
that don't change, and remain in memory.

Using {cpp:class}`BSimpleGameSound` is, well, simple:

:::{code} cpp
BSimpleGameSound* mysound = new BSimpleGameSound("soundfile.wav");
...
mysound.StartPlaying();
:::

This snippet uses {cpp:class}`BSimpleGameSound` to create an object that
can be used to play the sound effect in the file "soundfile.wav". Playing
the sound is as simple as calling {cpp:func}`StartPlaying()
<BGameSound::StartPlaying>`.

:::{admonition} Note
:class: note
In the current version of the BeOS, when you clone a
{cpp:class}`BSimpleGameSound`, the sound data buffer is also cloned, so
you'll have multiple copies of the sound effect in memory. Keep this in
mind as you write your code, as you can rapidly use a lot of memory this
way.
:::
