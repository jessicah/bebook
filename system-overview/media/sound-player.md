# BSoundPlayer

The {cpp:class}`BSoundPlayer` class plays sound by directly filling audio
buffers with data provided by a hook function you specify. A single
{cpp:class}`BSoundPlayer` can play multiple sounds at a time.

{cpp:class}`BSoundPlayer` takes care of all the nitty-gritty details of
instantiating the necessary sound player node and managing the time source.
All you have to do is start up a {cpp:class}`BSoundPlayer` and feed it
sounds to play.

You need to implement a hook function that will be called for each audio
buffer passed through the {cpp:class}`BSoundPlayer`'s playback node.

## Using BSoundPlayer

Once you've instantiated a {cpp:class}`BSoundPlayer` object, you need to
start it up before you can actually play sounds with it. This instantiates
the sound player node, attaches it to an appropriate time source, and makes
sure the time source is running. This is done by calling the
{cpp:func}`Start() <BSoundPlayer::Start>` function.

When you're done using the {cpp:class}`BSoundPlayer`, you can delete it if
you don't plan to use it again, or, if you want to keep it around for
reuse, you can just {cpp:func}`Stop() <BSoundPlayer::Stop>` it. This
deletes the sound node and cleans up the sounds.

You can find out the current time of the time source to which sounds are
being synchronized by calling the {cpp:func}`CurrentTime()
<BSoundPlayer::CurrentTime>` function.

By default, the audio format used by a {cpp:class}`BSoundPlayer` is
{hclass}`BSoundPlayer`::{cpp:enumerator}`B_AUDIO_FLOAT`, which is to say
that the audio is in floating-point format, where each sample ranges from
-1.0 to 1.0. The Media Kit uses floating-point audio internally, so using
floating-point audio whenever you can will improve your application's
performance by cutting down on format conversions. However, if you want to
use another format, you may do so by specifying a
{ref}`media_raw_audio_format` when you instantiate the
{cpp:class}`BSoundPlayer` object.

Sound streams may only contain 1 or 2 channels (either mono or stereo, in
other words). There's no support yet for multichannel sound.

:::{admonition} Note
:class: note
{cpp:class}`BSoundPlayer` can only play sounds in the native byte order.
:::

The audio mixer performs best if you don't specify a particular buffer
size.

### Playing Sound

When you specify a play buffer handler function, either when instantiating
the {cpp:class}`BSoundPlayer` object or by calling
{cpp:func}`SetCallbacks() <BSoundPlayer::SetCallbacks>` or
{cpp:func}`SetBufferPlayer() <BSoundPlayer::SetBufferPlayer>`, that
function will be called once for each buffer that passes through the
{cpp:class}`BSoundPlayer`'s sound playing node. Your play buffer handler
can then fill the buffer with whatever data you wish.

The following code sets up a {cpp:class}`BSoundPlayer` that will play a
triangle wave.

:::{code}
typedef struct cookie_record {
   float value;
   float direction;
} cookie_record;

...
cookie_record cookie;

cookie.value = 0.0;
cookie.direction = 1.0;

BSoundPlayer player("wave_player", BufferProc, NULL, &cookie);
player.Start();
player.SetHasData(true);
...
player.Stop();
:::

This code establishes a record, cookie, that contains information the play
buffer function will need to track, and creates a {cpp:class}`BSoundPlayer`
named "wave_player" that will use a function called BufferProc() to play
sound, and uses the cookie we've created.

Then the player is started, and {cpp:func}`SetHasData()
<BSoundPlayer::SetHasData>` is called to let the sound player node know
that there's data to be played. This will cause the play buffer function to
start being called.

Once playback is over, the {cpp:func}`Stop() <BSoundPlayer::Stop>`
function is called to stop playback.

The BufferProc() function looks like this:

:::{code} cpp
void BufferProc(void *theCookie, void *buffer, size_t size,
            const media_raw_audio_format &format) {
   size_t i, j;
   float *buf = (float *) buffer;
   size_t float_size = size/4;
   uint32 channel_count = format.channel_count;
   cookie_record *cookie = (cookie_record *) theCookie;

   // We're going to be cheap and only work for floating-point audio

   if (format.format != media_raw_audio_format::B_AUDIO_FLOAT) {
      return;
   }

   // Now fill the buffer with sound!

   for (i=0; i<float_size; i+=channel_count) {
      for (j=0; j<channel_count; j++) {
         buf[i+j] = cookie->value;
      }
      if ((cookie->direction == 1.0) && (cookie->value >= 1.0)) {
         cookie->direction = -1.0;
      }
      else if ((cookie->direction == -1.0) && (cookie->value <= -1.0)) {
         cookie->direction = 1.0;
      }
      cookie->value += cookie->direction*(1.0/64.0);
   }
}
:::

This example play buffer function generates a triangle wave, ramping the
wave up and down from 1.0 to -1.0 and back, over and over again, 1/64th at
a time. The next value to store in the buffer and the direction in which
the value is changing are kept in the cookie's fields.

:::{admonition} Note
:class: note
The buffers your play buffer function receives are empty. Do with them as
you please (or do nothing at all).
:::
