# BMediaRoster

The {cpp:class}`BMediaRoster` class comprises the functionality that
applications that use the Media Kit can access.

An application can only have a single instance of the
{cpp:class}`BMediaRoster` class, which is accessed by calling the static
member function {cpp:func}`BMediaRoster::Roster`, which creates the media
roster, establishes the connection to the Media Server, then returns a
pointer to the roster.

The creation of the roster object is thread protected, so you can safely
call {cpp:func}`BMediaRoster::Roster` from multiple threads without
synchronization, and both threads will safely get the same instance. The
cost of this synchronization is low enough that there's no need to cache
the returned pointer, but it's perfectly safe to do so if you wish:

:::{code} cpp
BMediaRoster *gMediaRoster;

int main(void) {
   status_t err;

   BApplication app("application/x-vnd.me-myself");
   gMediaRoster = BMediaRoster::Roster(&err);

   if (!gMediaRoster || (err != B_OK)) {
      /* the Media Server appears to be dead -- handle that here */
   }

   /* The Media Server connection is in place -- enjoy! */

   return 0;
}
:::

Because {cpp:class}`BMediaRoster` is derived from {cpp:class}`BLooper`,
you should create your {cpp:class}`BApplication` before calling
{cpp:func}`BMediaRoster::Roster`, although the {cpp:class}`BApplication`
doesn't have to be running yet.

You should never delete the {cpp:class}`BMediaRoster` returned to you by
{cpp:class}`BMediaRoster`. Also, you can't derive a class from
{cpp:class}`BMediaRoster`.

If you want to receive notifications from the Media Server when specific
changes occur, such as nodes coming online or going offline, for example,
you can register to receive such notifications by calling
{cpp:func}`StartWatching() <BMediaRoster::StartWatching>`.

## Playing Media from Disk

To play a media file from disk, you would follow the following steps:

-   Create an {cpp:func}`entry_ref <entry::ref>` that refers to the file to be
played.

-   Call {cpp:func}`SniffRef() <BMediaRoster::SniffRef>` to obtain a
{ref}`dormant_node_info` reference to the node that is best capable of
playing back the media file.

-   Call {cpp:func}`InstantiateDormantNode()
<BMediaRoster::InstantiateDormantNode>` to instantiate the node; this
returns a {cpp:func}`media_node <media::node>` that you can use for other
{cpp:class}`BMediaRoster` calls.

-   Use {cpp:func}`SetRefFor() <BMediaRoster::SetRefFor>` to pass the
{cpp:func}`entry_ref <entry::ref>` of the file to be played to the node.

-   Call {cpp:func}`GetFreeOutputsFor() <BMediaRoster::GetFreeOutputsFor>` to
obtain a {cpp:func}`media_output <media::output>` structure describing an
available output on the producer node. This structure contains a
{cpp:func}`media_source <media::source>` you can pass to
{cpp:func}`Connect() <BMediaRoster::Connect>` as the source of the media
data.

-   The {cpp:func}`media_output <media::output>` structure returned by
{cpp:func}`GetFreeOutputsFor() <BMediaRoster::GetFreeOutputsFor>` contains
a {cpp:func}`media_format <media::format>` field that indicates the general
type of media data contained by the media file; if you don't already know
what type of data you're playing back (audio or video or whatever), this
will let you determine what you'll be playing.

-   You can use this value to determine what type of destination is needed to
output the data (for example, {cpp:enumerator}`B_MEDIA_RAW_AUDIO` would go
to an audio output, and {cpp:enumerator}`B_MEDIA_RAW_VIDEO` would go to a
video output).

-   Call {cpp:func}`GetAudioMixer() <BMediaRoster::StartWatching>` to get a
{cpp:func}`media_node <media::node>` for the default audio mixer (if the
media data is audio), or {cpp:func}`GetVideoOutput()
<BMediaRoster::GetVideoOutput>` to get a {cpp:func}`media_node
<media::node>` for the default video output (if the media data is video).

-   Use {cpp:func}`GetFreeInputsFor() <BMediaRoster::GetFreeInputsFor>` to
obtain a {cpp:func}`media_input <media::input>` structure describing an
available input on the consumer node (the audio mixer or video output);
this structure contains a {cpp:func}`media_destination
<media::destination>` you can pass to {cpp:func}`Connect()
<BMediaRoster::Connect>`.

-   Call {cpp:func}`Connect() <BMediaRoster::Connect>` to connect the source
to the destination.

-   Next, you need to set the time source for the media file's node. Normally
you'll set this to the preferred time source. The audio mixer or video
output is already slaved to an appropriate time source.

-   Finally, you can use {cpp:func}`StartNode() <BMediaRoster::StartNode>` to
start the producer, consumer, and time source. The media file should begin
playing back.

Let's look at actual sample code that does this. This example is
particular to playing movie files; in particular, it assumes that the video
is encoded ({cpp:enumerator}`B_MEDIA_ENCODED_VIDEO`) and that the audio is
in a raw audio format ({cpp:enumerator}`B_MEDIA_RAW_AUDIO`). However, it
demonstrates the principles of playing both encoded and raw media formats,
and you can easily extrapolate from it any type of playback you need. First
it's necessary to identify an appropriate node to handle the file, and to
instantiate the node and configure it for the file we want to play:

:::{code} cpp
bigtime_t     duration;
media_node      timeSourceNode;

media_node      mediaFileNode;
media_output    fileNodeOutput;
int32           fileOutputCount;

media_output    fileAudioOutput;
int32           fileAudioCount;

media_node      codecNode;
media_output    codecOutput;
media_input     codecInput;

media_node      videoNode;
media_input     videoInput;
int32           videoInputCount;

media_node      audioNode;
media_input     audioInput;
int32           audioInputCount;

dormant_node_info nodeInfo;
status_t err;

playingFlag = false;
roster = BMediaRoster::Roster();

initStatus = roster->SniffRef(*ref, 0, &nodeInfo);
if (initStatus) {
   return;
}

initStatus = roster->InstantiateDormantNode(nodeInfo, &mediaFileNode);
if (initStatus) {
   return;
}

roster->SetRefFor(mediaFileNode, *ref, false, &duration);
if ((err = Setup()) != B_OK) {
   printf("Error %08lX in Setup()\n", err);
}
else {
   Start();
}
:::

This code begins by obtaining a pointer to the media roster. It then calls
{cpp:func}`SniffRef() <BMediaRoster::SniffRef>` to get a
{ref}`dormant_node_info` structure describing the best-suited node for
reading the media data from the file specified by {hparam}`ref`.

Once a dormant_node_info structure has been filled out, the
{cpp:func}`InstantiateDormantNode() <BMediaRoster::InstantiateDormantNode>`
function is called to instantiate a node to handle the file. A dormant node
is a node whose code resides in an add-on, instead of within the
application itself. The {hparam}`nodeInfo` structure is passed into the
function, and on return, the {hparam}`mediaFileNode` has been set up for
the appropriate node.

Since the {cpp:func}`media_node <media::node>` {hparam}`mediaFileNode` is
a file handling node, the {cpp:func}`SetRefFor() <BMediaRoster::SetRefFor>`
function is then called to tell the newly-instantiated file handler node
what file it should handle. The inputs here are:

-   {hparam}`mediaFileNode` is the node whose file reference is to be set.

-   {hparam}`ref` is the file that the node should reference.

-   {cpp:expr}`false` indicates that the file must already exist. If this flag
were {cpp:expr}`true`, and the file indicated by {hparam}`ref` were
nonexistent, the node would create a new file. Since we're playing a file,
we don't want to do that.

-   {hparam}`duration` is a {htype}`bigtime_t` variable that will receive the
duration of the media file, in microseconds.

Once this has been accomplished, it's time to instantiate the other nodes
needed to perform the media playback. Note that your code should check the
error results from each of these calls and only proceed if
{cpp:enumerator}`B_OK` is returned.

The {hmethod}`Setup()` and {hmethod}`Start()` functions used in the
example above are given below. {hmethod}`Setup()` actually sets up the
connections and instantiates the various other nodes (such as codecs and
output nodes) required to play back the media data. Let's take a look at
{hmethod}`Setup()` next:

:::{code} cpp
status_t MediaPlayer::Setup(void) {
   status_t err;
   media_format tryFormat;
   dormant_node_info nodeInfo;
   int32 nodeCount;

   err = roster->GetAudioMixer(&audioNode);
   err = roster->GetVideoOutput(&videoNode);
:::

First, {cpp:func}`GetAudioMixer() <BMediaRoster::GetAudioMixer>` and
{cpp:func}`GetVideoOutput() <BMediaRoster::GetVideoOutput>` are called to
obtain an audio mixer node and a video output node. The nodes returned by
this function are based on the user's preferences in the Audio and Video
preference applications. By default, video is output to a simple video
output consumer that creates a window to contain the video display.

:::{admonition} Note
:class: note
The VideoConsumer node will be available with R4.5; it's not provided in
R4. In addition, there are no video producer nodes in R4; media add-ons for
a variety of movie file formats will also be available beginning with R4.5.
:::

:::{code} cpp
err = roster->GetTimeSource(&timeSourceNode);
   b_timesource = roster->MakeTimeSourceFor(timeSourceNode);
:::

This code obtains a {cpp:func}`media_node <media::node>` for the preferred
time source, and then creates a {cpp:class}`BTimeSource` object that refers
to the same node; we'll need to be able to make some
{cpp:class}`BTimeSource` calls to obtain some specific timing information
later.

A time source is a node that can be used to synchronize other nodes. By
default, nodes are slaved to the system time source, which is the
computer's internal clock. However, this time source, while very precise,
isn't good for synchronizing media data, since its concept of time has
nothing to do with actual media being performed. For this reason, you
typically will want to change nodes' time sources to the preferred time
source.

You can think of a media node (represented by the {cpp:func}`media_node
<media::node>` structure) as a component in a home theater system you might
have at home. It has inputs for audio and video (possibly multiple inputs
for each), and outputs to pass that audio and video along to other
components in the system. To use the component, you have to connect wires
from the outputs of some other components into the component's inputs, and
the outputs into the inputs of other components.

The Media Kit works the same way. We need to locate audio outputs from the
{hparam}`mediaFileNode` and find corresponding audio inputs on the
{hparam}`audioNode`. This is analogous to choosing an audio output from
your new DVD player and matching it to an audio input jack on your stereo
receiver. Since you can't use ports that are already in use, we call
{cpp:func}`GetFreeOutputsFor() <BMediaRoster::GetFreeOutputsFor>` to find
free output ports on the {hparam}`mediaFileNode`, and
{cpp:func}`GetFreeInputsFor() <BMediaRoster::GetFreeInputsFor>` to locate
free input ports on the {hparam}`audioNode`.

:::{code} cpp
err = roster->GetFreeOutputsFor(mediaFileNode, &fileAudioOutput, 1,
               &fileAudioCount, B_MEDIA_RAW_AUDIO);
   err = roster->GetFreeInputsFor(audioNode, &audioInput, fileAudioCount,
               &audioInputCount, B_MEDIA_RAW_AUDIO);
:::

We only want a single audio connection between the two nodes (a single
connection can carry stereo sound), and the connection is of type
{cpp:enumerator}`B_MEDIA_RAW_AUDIO`. On return, {hparam}`fileAudioOutput`
and {hparam}`audioInput` describe the output from the
{hparam}`mediaFlieNode` and the input into the {hparam}`audioNode` that
will eventually be connected to play the movie's sound.

We likewise have to find a video output from the {hparam}`mediaFileNode`
and an input into the {hparam}`videoNode`. In this case, though, we expect
the video output from the {hparam}`mediaFileNode` to be encoded, and the
{hparam}`videoNode` will want to receive raw, uncompressed video. We'll
work that out in a minute; for now, let's just find the two ports:

:::{code} cpp
err = roster->GetFreeOutputsFor(mediaFileNode, &fileNodeOutput, 1,
               &fileOutputCount, B_MEDIA_ENCODED_VIDEO)
   err = roster->GetFreeInputsFor(videoNode, &videoInput, fileOutputCount,
               &videoInputCount, B_MEDIA_RAW_VIDEO);
:::

The problem we have now is that the {hparam}`mediaFileNode` is outputting
video that's encoded somehow (like in Cinepak format, for instance). The
{hparam}`videoNode`, on the other hand, wants to display raw video. Another
node must be placed between these to decode the video (much like having an
adapter to convert PAL video into NTSC, for example). This node will be the
codec that handles decompressing the video into raw form.

We need to locate a codec node that can handle the video format being
output by the {hparam}`mediaFileNode`. This is accomplished like this:

:::{code} cpp
nodeCount = 1;
   err = roster->GetDormantNodes(&nodeInfo, &nodeCount,
               &fileNodeOutput.format);
   if (!nodeCount) {
      return -1;
   }
:::

This call to {cpp:func}`GetDormantNodes() <BMediaRoster::GetDormantNodes>`
looks for a dormant node that can handle the media format specified by the
{hparam}`mediaFileNode`'s output {cpp:func}`media_format <media::format>`
structure. Information about the node is returned in {hparam}`nodeInfo`.
{hparam}`nodeCount` indicates the number of matching nodes that were found.
If it's zero, an error is returned.

Note that in real life you should ask for several nodes, and search
through them, looking at the formats until you find one that best meets
your needs.

Then we use {cpp:func}`InstantiateDormantNode()
<BMediaRoster::InstantiateDormantNode>` to instantiate the codec node, and
locate inputs into the node (that accept encoded video) and outputs from
the node (that output raw video):

:::{code} cpp
err = roster->InstantiateDormantNode(nodeInfo, &codecNode);
   err = roster->GetFreeInputsFor(codecNode, &codecInput, 1, &nodeCount,
               B_MEDIA_ENCODED_VIDEO);
   err = roster->GetFreeOutputsFor(codecNode, &codecOutput, 1,
               &nodeCount, B_MEDIA_RAW_VIDEO);
:::

Now we're ready to start connecting these nodes together. If we were
setting up a home theater system, right about now we'd be getting rug burns
on our knees and skinned knuckles on our hands, trying to reach behind the
entertainment center to run wires. The Media Kit is way easier than that,
and doesn't involve salespeople telling you to get expensive gold-plated
cables.

We begin by connecting the file node's video output to the codec's input:

:::{code} cpp
tryFormat = fileNodeOutput.format;
   err = roster->Connect(fileNodeOutput.source, codecInput.destination,
               &tryFormat, &fileNodeOutput, &codecInput);
:::

{hparam}`tryFormat` indicates the format of the encoded video that will be
output by the {hparam}`mediaFileNode`. {cpp:func}`Connect()
<BMediaRoster::Connect>`, in essense, runs a wire between the output from
the media node's video output ({hparam}`fileNodeOutput`) to the codec
node's input.

You may wonder what's up with the
{hparam}`fileNodeOutput`.{hparam}`source` and
{hparam}`codecInput`.{hparam}`destination` structures. These
{cpp:func}`media_source <media::source>` and {cpp:func}`media_destination
<media::destination>` structures are simplified descriptors of the two ends
of the connection. They contain only the data absolutely needed for the
Media Kit to establish the connection. This saves some time when issuing
the {cpp:func}`Connect() <BMediaRoster::Connect>` call (and time is money,
especially in the media business).

Next it's necessary to connect the codec to the video output node. This
begins by setting up {hparam}`tryFormat` to describe raw video of the same
width and height as the encoded video being fed into the codec, then
calling {cpp:func}`Connect() <BMediaRoster::Connect>` to establish the
connection:

:::{code} cpp
tryFormat.type = B_MEDIA_RAW_VIDEO;
   tryFormat.u.raw_video = media_raw_video_format::wildcard;
   tryFormat.u.raw_video.display.line_width =
            codecInput.format.u.encoded_video.output.display.line_width;
   tryFormat.u.raw_video.display.line_count =
            codecInput.format.u.encoded_video.output.display.line_count;
   err = roster->Connect(codecOutput.source, videoInput.destination,
               &tryFormat, &codecOutput, &videoInput);
:::

Now we connect the audio from the media file to the audio mixer node. We
just copy the {cpp:func}`media_format <media::format>` from the file's
audio output, since both ends of the connection should exactly match.

:::{code} cpp
tryFormat = fileAudioOutput.format;
   err = roster->Connect(fileAudioOutput.source, audioInput.destination,
               &tryFormat, &fileAudioOutput, &audioInput);
:::

The last step of configuring the connections is to ensure that all the
nodes are slaved to the preferred time source. This will keep them
synchronized with the preferred time source (and by association, with each
other):

:::{code} cpp
err = roster->SetTimeSourceFor(mediaFileNode.node,
timeSourceNode.node);
   err = roster->SetTimeSourceFor(videoNode.node, timeSourceNode.node);
   err = roster->SetTimeSourceFor(codecOutput.node.node,
            timeSourceNode.node);
   err = roster->SetTimeSourceFor(audioNode.node, timeSourceNode.node);
   return B_OK;
}
:::

Finally, we return {cpp:enumerator}`B_OK` to the caller. Note that this
code should be enhanced to check the results of each
{cpp:class}`BMediaRoster` call, and to return the result code if it's not
{cpp:enumerator}`B_OK`. This has been left out of this example for brevity.

The {hmethod}`Start()` function actually starts the movie playback.
Starting playback involves starting, one at a time, all the nodes involved
in playing back the audio. This includes the audio mixer
({hparam}`audioNode`), the media file's node ({hparam}`mediaFileNode`), the
codec, and the video node.

:::{code} cpp
status_t MediaPlayer::Start(void) {
   status_t err;
   err = roster->GetStartLatencyFor(timeSourceNode, &startTime);
   startTime += b_timesource->PerformanceTimeFor(BTimeSource::RealTime()
               + 1000000 / 50);

   err = roster->StartNode(mediaFileNode, startTime);
   err = roster->StartNode(codecNode, startTime);
   err = roster->StartNode(videoNode, startTime);

   return B_OK;
}
:::

Because there's lag time between starting each of these nodes, we pick a
time a few moments in the future for playback to begin, and schedule each
node to start playing at that time. So we begin by computing that time in
the future.

The {cpp:func}`BTimeSource::RealTime` static member function is called to
obtain the current real system time. We add a fiftieth of a second to that
time, and convert it into performance time units. This is the time at which
the performance of the movie will begin (basically a fiftieth of a second
from "now"). This value is saved in {hparam}`startTime`. These are added to
the value returned by {cpp:func}`GetStartLatencyFor()
<BMediaRoster::GetStartLatencyFor>`, which returns the time required to
actually start the time source and all the nodes slaved to it.

Then we simply call {cpp:func}`BMediaRoster::StartNode` for each node,
specifying {hparam}`startTime` as the performance time at which playback
should begin.

Again, error handling should be added to actually return the error code
from these functions.

Stopping playback of the movie is even simpler:

:::{code} cpp
err = roster->StopNode(mediaFileNode, 0, true);
   err = roster->StopNode(codecNode, 0, true);
   err = roster->StopNode(videoNode, 0, true);
:::

This tells the media file, video codec, and video output nodes to stop
immediately. If we wanted them to stop together at some time in the future,
we could compute an appropriate performance time and pass that instead of
0. In this case, we would need to specify {cpp:expr}`false` for the last
argument; when this value is {cpp:expr}`true`, {cpp:func}`StopNode()
<BMediaRoster::StopNode>` stops the node immediately. We could use this
ability to schedule all three nodes to stop at the same time, so that video
and audio playback would halt simultaneously.

Note that we don't stop the audio mixer node. You should never stop the
mixer node, because other applications are probably using it.

Once you're done playing the movie, and have stopped playback, you should
disconnect the nodes from each other:

:::{code} cpp
err = roster->Disconnect(mediaFileNode.node, fileNodeOutput.source,
               codecNode.node, codecInput.destination);
   err = roster->Disconnect(codecNode.node, codecOutput.source,
               videoNode.node, videoInput.destination);
   err = roster->Disconnect(mediaFileNode.node, fileAudioOutput.source,
               audioNode.node, audioInput.destination);
:::

This will close out the connections between the media file node and the
video codec, the codec and the video output, and between the file node and
the audio mixer. You should always stop playback before disconnecting;
although nodes aren't allowed to crash if you disconnect them while
running, their behavior isn't specified, and may not be what you expect.

Once the connections are severed, you should release any dormant nodes you
instantiated. This includes not only nodes instantiated using
{cpp:func}`InstantiateDormantNode()
<BMediaRoster::InstantiateDormantNode>`, but also default nodes (those
obtained using functions like {cpp:func}`GetAudioInput()
<BMediaRoster::GetAudioInput>` and {cpp:func}`GetVideoOutput)
<BMediaRoster::GetVideoOutput>`, for example):

:::{code} cpp
roster->ReleaseNode(codecNode);
   roster->ReleaseNode(mediaFileNode);
   roster->ReleaseNode(videoNode);
   roster->ReleaseNode(audioNode);
:::

If you want to play audio, you may find it much easier to use the BSound
and {cpp:class}`BSoundPlayer` classes to do so. As of R4.5, there are no
Be-provided nodes for producing audio from a disk file.

### Detecting When Playback Is Complete

There isn't a Media Kit function that can directly tell you whether or not
the media has reached the end of the data during playback. However, the
following easy-to-implement code can do the job for you:

:::{code} cpp
bigtime_t currentTime;
bool isPlaying = true;

currentTime = b_timesource->PerformanceTimeFor(BTimeSource::RealTime());
if (currentTime >= startTime+duration) {
   isPlaying = false;
}
:::

This works by obtaining the time source's performance time and comparing
it to the time at which playback of the movie was begun plus the movie's
duration (both of which were saved when we initially set up and began
playback of the movie, as seen in the code in the previous section above).

If the current performance time is equal to or greater than the sum of the
starting time and the movie's duration, then playback is finished, and we
set {hparam}`isPlaying` to {cpp:expr}`false`; otherwise, this value remains
{cpp:expr}`true`.

### Using BMediaRoster Functions from Nodes

You can issue {cpp:class}`BMediaRoster` function calls from within your
own node, however, as a general rule, you shouldn't call
{cpp:class}`BMediaRoster` functions from within your control thread, or
while the control thread is blocked. Many {cpp:class}`BMediaRoster`
functions use synchronous turnarounds, and will deadlock in this situation.
You should assume, for safety's sake, that all {cpp:class}`BMediaRoster`
functions will deadlock if used in these cases.

For example, if you have an application that's playing video into a
window, and you call {cpp:func}`StopNode() <BMediaRoster::StopNode>` from
the window's {cpp:func}`MessageReceived() <BWindow::MessageReceived>`
function, a deadlock would occur if the video player node blocks waiting on
the window to be unlocked, and the {cpp:func}`StopNode()
<BMediaRoster::StopNode>` function is keeping the window locked while it
waits for the video producer node, which is blocked waiting on the consumer
node, and so forth. Deadlock results, and that's a bad thing.

Instead, you should consider creating a seperate {cpp:class}`BLooper` that
manages your nodes. Future versions of the Media Kit will provide
convenience classes to do some of this for you.
