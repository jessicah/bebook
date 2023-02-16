# BStreamingGameSound

The {cpp:class}`BStreamingGameSound` class provides the ability to stream
audio data. A hook function is called whenever a buffer needs to be filled
with audio data. This hook function is set by calling
{cpp:func}`SetStreamHook() <BStreamingGameSound::SetStreamHook>`.

Using this class requires special magic powers; unless you're directly in
contact with Be about it, don't use it. You'll regret it later.
