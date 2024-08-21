#!/bin/bash

set -e

PYTHON3="sem -j+0 python3"

$PYTHON3 html2myst/html2myst.py _source_html/BAlert.html kits/interface/alert.md
$PYTHON3 html2myst/html2myst.py _source_html/BApplication.html kits/application/application.md
$PYTHON3 html2myst/html2myst.py _source_html/BAppFileInfo.html kits/storage/app-file-info.md
$PYTHON3 html2myst/html2myst.py _source_html/BBitmap.html kits/interface/bitmap.md
$PYTHON3 html2myst/html2myst.py _source_html/BBox.html kits/interface/box.md
$PYTHON3 html2myst/html2myst.py _source_html/BBufferConsumer.html kits/media/buffer-consumer.md
$PYTHON3 html2myst/html2myst.py _source_html/BBufferGroup.html kits/media/buffer-group.md
$PYTHON3 html2myst/html2myst.py _source_html/BBuffer.html kits/media/buffer.md
$PYTHON3 html2myst/html2myst.py _source_html/BBufferProducer.html kits/media/buffer-producer.md
$PYTHON3 html2myst/html2myst.py _source_html/BButton.html kits/interface/button.md
$PYTHON3 html2myst/html2myst.py _source_html/BCheckBox.html kits/interface/check-box.md
$PYTHON3 html2myst/html2myst.py _source_html/BCheckBox.html kits/interface/checkbox.md
$PYTHON3 html2myst/html2myst.py _source_html/BClipboard.html kits/application/clipboard.md
$PYTHON3 html2myst/html2myst.py _source_html/BColorControl.html kits/interface/color-control.md
$PYTHON3 html2myst/html2myst.py _source_html/BContinuousParameter.html kits/media/continuous-parameter.md
$PYTHON3 html2myst/html2myst.py _source_html/BControl.html kits/interface/control.md
$PYTHON3 html2myst/html2myst.py _source_html/BControllable.html kits/media/controllable.md
$PYTHON3 html2myst/html2myst.py _source_html/BCursor.html kits/application/cursor.md
$PYTHON3 html2myst/html2myst.py _source_html/BDirectory.html kits/storage/directory.md
$PYTHON3 html2myst/html2myst.py _source_html/BDirectWindow.html kits/game/direct-window.md
$PYTHON3 html2myst/html2myst.py _source_html/BDiscreteParameter.html kits/media/discrete-parameter.md
$PYTHON3 html2myst/html2myst.py _source_html/BDragger.html kits/interface/dragger.md
$PYTHON3 html2myst/html2myst.py _source_html/BEntry.html kits/storage/entry.md
$PYTHON3 html2myst/html2myst.py _source_html/BEntryList.html kits/storage/entry-list.md
$PYTHON3 html2myst/html2myst.py _source_html/BFileGameSound.html kits/game/file-game-sound.md
$PYTHON3 html2myst/html2myst.py _source_html/BFile.html kits/storage/file.md
$PYTHON3 html2myst/html2myst.py _source_html/BFileInterface.html kits/media/file-interface.md
$PYTHON3 html2myst/html2myst.py _source_html/BFilePanel.html kits/storage/file-panel.md
$PYTHON3 html2myst/html2myst.py _source_html/BFont.html kits/interface/font.md
$PYTHON3 html2myst/html2myst.py _source_html/BGLView.html kits/opengl/gl-view.md
$PYTHON3 html2myst/html2myst.py _source_html/BHandler.html kits/application/handler.md
$PYTHON3 html2myst/html2myst.py _source_html/BInputDevice.html kits/input/input-device.md
$PYTHON3 html2myst/html2myst.py _source_html/BInputServerDevice.html kits/input/input-server-device.md
$PYTHON3 html2myst/html2myst.py _source_html/BInputServerFilter.html kits/input/input-server-filter.md
$PYTHON3 html2myst/html2myst.py _source_html/BInputServerMethod.html kits/input/input-server-method.md
$PYTHON3 html2myst/html2myst.py _source_html/BInvoker.html kits/application/invoker.md
$PYTHON3 html2myst/html2myst.py _source_html/BJoystick.html kits/device/joystick.md
$PYTHON3 html2myst/html2myst.py _source_html/BListItem.html kits/interface/list-item.md
$PYTHON3 html2myst/html2myst.py _source_html/BLooper.html kits/application/looper.md
$PYTHON3 html2myst/html2myst.py _source_html/BMailMessage.html kits/mail/mail-message.md
$PYTHON3 html2myst/html2myst.py _source_html/BMediaAddOn.html kits/media/media-add-on.md
$PYTHON3 html2myst/html2myst.py _source_html/BMediaBufferDecoder.html kits/media/media-buffer-decoder.md
$PYTHON3 html2myst/html2myst.py _source_html/BMediaBufferEncoder.html kits/media/media-buffer-encoder.md
$PYTHON3 html2myst/html2myst.py _source_html/BMediaDecoder.html kits/media/media-decoder.md
$PYTHON3 html2myst/html2myst.py _source_html/BMediaEncoder.html kits/media/media-encoder.md
$PYTHON3 html2myst/html2myst.py _source_html/BMediaEventLooper.html kits/media/media-event-looper.md
$PYTHON3 html2myst/html2myst.py _source_html/BMediaFile.html kits/media/media-file.md
$PYTHON3 html2myst/html2myst.py _source_html/BMediaFiles.html kits/media/media-files.md
$PYTHON3 html2myst/html2myst.py _source_html/BMediaFormats.html kits/media/media-formats.md
$PYTHON3 html2myst/html2myst.py _source_html/BMediaNode.html kits/media/media-node.md
$PYTHON3 html2myst/html2myst.py _source_html/BMediaRoster.html kits/media/media-roster.md
$PYTHON3 html2myst/html2myst.py _source_html/BMediaTheme.html kits/media/media-theme.md
$PYTHON3 html2myst/html2myst.py _source_html/BMediaTrack.html kits/media/media-track.md
$PYTHON3 html2myst/html2myst.py _source_html/BMenuBar.html kits/interface/menu-bar.md
$PYTHON3 html2myst/html2myst.py _source_html/BMenuField.html kits/interface/menu-field.md
$PYTHON3 html2myst/html2myst.py _source_html/BMenu.html kits/interface/menu.md
$PYTHON3 html2myst/html2myst.py _source_html/BMenuItem.html kits/interface/menu-item.md
$PYTHON3 html2myst/html2myst.py _source_html/BMessageFilter.html kits/application/message-filter.md
$PYTHON3 html2myst/html2myst.py _source_html/BMessage.html kits/application/message.md
$PYTHON3 html2myst/html2myst.py _source_html/BMessageQueue.html kits/application/message-queue.md
$PYTHON3 html2myst/html2myst.py _source_html/BMessenger.html kits/application/messenger.md
$PYTHON3 html2myst/html2myst.py _source_html/BMimeType.html kits/storage/mime-type.md
$PYTHON3 html2myst/html2myst.py _source_html/BNetAddress.html kits/network/net-address.md
$PYTHON3 html2myst/html2myst.py _source_html/BNetBuffer.html kits/network/net-buffer.md
$PYTHON3 html2myst/html2myst.py _source_html/BNetDebug.html kits/network/net-debug.md
$PYTHON3 html2myst/html2myst.py _source_html/BNetEndpoint.html kits/network/net-endpoint.md
$PYTHON3 html2myst/html2myst.py _source_html/BNode.html kits/storage/node.md
$PYTHON3 html2myst/html2myst.py _source_html/BNodeInfo.html kits/storage/node-info.md
$PYTHON3 html2myst/html2myst.py _source_html/BNullParameter.html kits/media/null-parameter.md
$PYTHON3 html2myst/html2myst.py _source_html/BOutlineListView.html kits/interface/outline-list-view.md
$PYTHON3 html2myst/html2myst.py _source_html/BParameterGroup.html kits/media/parameter-group.md
$PYTHON3 html2myst/html2myst.py _source_html/BParameter.html kits/media/parameter.md
$PYTHON3 html2myst/html2myst.py _source_html/BParameterWeb.html kits/media/parameter-web.md
$PYTHON3 html2myst/html2myst.py _source_html/BPath.html kits/storage/path.md
$PYTHON3 html2myst/html2myst.py _source_html/BPictureButton.html kits/interface/picture-button.md
$PYTHON3 html2myst/html2myst.py _source_html/BPicture.html kits/interface/picture.md
$PYTHON3 html2myst/html2myst.py _source_html/BPoint.html kits/interface/point.md
$PYTHON3 html2myst/html2myst.py _source_html/BPolygon.html kits/interface/polygon.md
$PYTHON3 html2myst/html2myst.py _source_html/BPopUpMenu.html kits/interface/pop-up-menu.md
$PYTHON3 html2myst/html2myst.py _source_html/BPrintJob.html kits/interface/print-job.md
$PYTHON3 html2myst/html2myst.py _source_html/BPropertyInfo.html kits/application/property-info.md
$PYTHON3 html2myst/html2myst.py _source_html/BPushGameSound.html kits/game/push-game-sound.md
$PYTHON3 html2myst/html2myst.py _source_html/BQuery.html kits/storage/query.md
$PYTHON3 html2myst/html2myst.py _source_html/BRadioButton.html kits/interface/radio-button.md
$PYTHON3 html2myst/html2myst.py _source_html/BRect.html kits/interface/rect.md
$PYTHON3 html2myst/html2myst.py _source_html/BRefFilter.html kits/storage/ref-filter.md
$PYTHON3 html2myst/html2myst.py _source_html/BRegion.html kits/interface/region.md
$PYTHON3 html2myst/html2myst.py _source_html/BResources.html kits/storage/resources.md
$PYTHON3 html2myst/html2myst.py _source_html/BRoster.html kits/application/roster.md
$PYTHON3 html2myst/html2myst.py _source_html/BScreen.html kits/interface/screen.md
$PYTHON3 html2myst/html2myst.py _source_html/BScrollBar.html kits/interface/scroll-bar.md
$PYTHON3 html2myst/html2myst.py _source_html/BScrollView.html kits/interface/scroll-view.md
$PYTHON3 html2myst/html2myst.py _source_html/BSeparatorItem.html kits/interface/separator-item.md
$PYTHON3 html2myst/html2myst.py _source_html/BSerialPort.html kits/device/serial-port.md
$PYTHON3 html2myst/html2myst.py _source_html/BShape.html kits/interface/shape.md
$PYTHON3 html2myst/html2myst.py _source_html/BShapeIterator.html kits/interface/shape-iterator.md
$PYTHON3 html2myst/html2myst.py _source_html/BShelf.html kits/interface/shelf.md
$PYTHON3 html2myst/html2myst.py _source_html/BSimpleGameSound.html kits/game/simple-game-sound.md
$PYTHON3 html2myst/html2myst.py _source_html/BSlider.html kits/interface/slider.md
$PYTHON3 html2myst/html2myst.py _source_html/BSmallBuffer.html kits/media/small-buffer.md
$PYTHON3 html2myst/html2myst.py _source_html/BSoundPlayer.html kits/media/sound-player.md
$PYTHON3 html2myst/html2myst.py _source_html/BStatable.html kits/storage/statable.md
$PYTHON3 html2myst/html2myst.py _source_html/BStatusBar.html kits/interface/status-bar.md
$PYTHON3 html2myst/html2myst.py _source_html/BStreamingGameSound.html kits/game/streaming-game-sound.md
$PYTHON3 html2myst/html2myst.py _source_html/BStringItem.html kits/interface/string-item.md
$PYTHON3 html2myst/html2myst.py _source_html/BStringView.html kits/interface/string-view.md
$PYTHON3 html2myst/html2myst.py _source_html/BSymLink.html kits/storage/sym-link.md
$PYTHON3 html2myst/html2myst.py _source_html/BTab.html kits/interface/tab.md
$PYTHON3 html2myst/html2myst.py _source_html/BTabView.html kits/interface/tab-view.md
$PYTHON3 html2myst/html2myst.py _source_html/BTextView.html kits/interface/text-view.md
$PYTHON3 html2myst/html2myst.py _source_html/BTimeCode.html kits/media/time-code.md
$PYTHON3 html2myst/html2myst.py _source_html/BTimedEventQueue.html kits/media/timed-event-queue.md
$PYTHON3 html2myst/html2myst.py _source_html/BTimeSource.html kits/media/time-source.md
$PYTHON3 html2myst/html2myst.py _source_html/BTranslationUtils.html kits/translation/translation-utils.md
$PYTHON3 html2myst/html2myst.py _source_html/BTranslator.html kits/translation/translator.md
$PYTHON3 html2myst/html2myst.py _source_html/BView.html kits/interface/view.md
$PYTHON3 html2myst/html2myst.py _source_html/BVolume.html kits/storage/volume.md
$PYTHON3 html2myst/html2myst.py _source_html/BVolumeRoster.html kits/storage/volume-roster.md
$PYTHON3 html2myst/html2myst.py _source_html/BWindow.html kits/interface/window.md
$PYTHON3 html2myst/html2myst.py _source_html/BWindowScreen.html kits/game/window-screen.md
$PYTHON3 html2myst/html2myst.py _source_html/NetworkSockets.html kits/network/network-sockets.md
$PYTHON3 html2myst/html2myst.py _source_html/TheApplicationKit_MessageConstants.html kits/application/message-constants.md
$PYTHON3 html2myst/html2myst.py _source_html/TheGameKit_CardHooks.html kits/game/graphics-card-hook-functions.md
$PYTHON3 html2myst/html2myst.py _source_html/TheGameKit_Constants.html kits/game/constants.md
$PYTHON3 html2myst/html2myst.py _source_html/TheGameKit_DefinedTypes.html kits/game/defined-types.md
$PYTHON3 html2myst/html2myst.py _source_html/TheGameKit_Functions.html kits/game/global-functions.md
$PYTHON3 html2myst/html2myst.py _source_html/TheInputServer_Functions.html kits/input/functions.md
$PYTHON3 html2myst/html2myst.py _source_html/TheInputServer_Messages.html kits/input/message-constants.md
$PYTHON3 html2myst/html2myst.py _source_html/TheInterfaceKit_Functions.html kits/interface/functions.md
$PYTHON3 html2myst/html2myst.py _source_html/TheInterfaceKit_GeneralConstants.html kits/interface/general-constants.md
$PYTHON3 html2myst/html2myst.py _source_html/TheInterfaceKit_MessageConstants.html kits/interface/message-constants.md
$PYTHON3 html2myst/html2myst.py _source_html/TheKernelKit_Areas.html kits/kernel/areas.md
$PYTHON3 html2myst/html2myst.py _source_html/TheKernelKit_Images.html kits/kernel/images.md
$PYTHON3 html2myst/html2myst.py _source_html/TheKernelKit_Miscellaneous.html kits/kernel/miscellaneous.md
$PYTHON3 html2myst/html2myst.py _source_html/TheKernelKit_Ports.html kits/kernel/ports.md
$PYTHON3 html2myst/html2myst.py _source_html/TheKernelKit_Semaphores.html kits/kernel/semaphores.md
$PYTHON3 html2myst/html2myst.py _source_html/TheKernelKit_SystemInfo.html kits/kernel/system-info.md
$PYTHON3 html2myst/html2myst.py _source_html/TheKernelKit_ThreadsAndTeams.html kits/kernel/threads-and-teams.md
$PYTHON3 html2myst/html2myst.py _source_html/TheKernelKit_Time.html kits/kernel/time.md
$PYTHON3 html2myst/html2myst.py _source_html/TheMailDaemon_Functions.html kits/mail/mail-daemon-functions.md
$PYTHON3 html2myst/html2myst.py _source_html/The_Node_Monitor.html kits/storage/the-node-monitor.md

# $PYTHON3 html2myst/html2myst.py _source_html/TheApplicationKit_Overview.html system-overview/application/index.md
# $PYTHON3 html2myst/html2myst.py _source_html/TheDeviceKit_Overview.html system-overview/device/index.md
# $PYTHON3 html2myst/html2myst.py _source_html/TheGameKit_Overview.html system-overview/game/index.md
# $PYTHON3 html2myst/html2myst.py _source_html/TheInputServer_Overview.html system-overview/input/index.md
# $PYTHON3 html2myst/html2myst.py _source_html/TheInterfaceKit_Overview.html system-overview/interface/index.md
# $PYTHON3 html2myst/html2myst.py _source_html/TheKernelKit_Overview.html system-overview/kernel/index.md
# $PYTHON3 html2myst/html2myst.py _source_html/TheMailKit_Overview.html system-overview/mail/index.md
# $PYTHON3 html2myst/html2myst.py _source_html/TheMediaKit_Overview.html system-overview/media/index.md
# $PYTHON3 html2myst/html2myst.py _source_html/TheMidiKit_Overview.html system-overview/midi/index.md
# $PYTHON3 html2myst/html2myst.py _source_html/TheNetworkKit_Overview.html system-overview/network/index.md
# $PYTHON3 html2myst/html2myst.py _source_html/TheOpenGLKit_Overview.html system-overview/opengl/index.md
# $PYTHON3 html2myst/html2myst.py _source_html/TheStorageKit_Overview.html system-overview/storage/index.md
# $PYTHON3 html2myst/html2myst.py _source_html/TheSupportKit_Overview.html system-overview/support/index.md
# $PYTHON3 html2myst/html2myst.py _source_html/TheTranslationKit_Overview.html system-overview/translation/index.md

# $PYTHON3 html2myst/html2myst.py _source_html/DeviceDrivers.html topic/device-drivers.md
# $PYTHON3 html2myst/html2myst.py _source_html/TheDeskbar.html topic/the-deskbar.md
# $PYTHON3 html2myst/html2myst.py _source_html/TheKeyboard.html topic/the-keyboard.md
# $PYTHON3 html2myst/html2myst.py _source_html/TheTracker.html topic/the-tracker.md

$PYTHON3 html2myst/html2myst.py _source_html/DeviceDrivers_Introduction.html topics/device-drivers/introduction.md
$PYTHON3 html2myst/html2myst.py _source_html/DeviceDrivers_WritingDrivers.html topics/device-drivers/writing-drivers.md
$PYTHON3 html2myst/html2myst.py _source_html/DeviceDrivers_WritingModules.html topics/device-drivers/writing-modules.md
$PYTHON3 html2myst/html2myst.py _source_html/DeviceDrivers_UsingModules.html topics/device-drivers/using-modules.md
$PYTHON3 html2myst/html2myst.py _source_html/DeviceDrivers_area_malloc.html topics/device-drivers/area-malloc.md
$PYTHON3 html2myst/html2myst.py _source_html/DeviceDrivers_DriverSettingsAPI.html topics/device-drivers/driver-settings-api.md
$PYTHON3 html2myst/html2myst.py _source_html/DeviceDrivers_ConstantsDefinedTypes.html topics/device-drivers/constants-defined-types.md
$PYTHON3 html2myst/html2myst.py _source_html/DeviceDrivers_Functions.html topics/device-drivers/functions.md
$PYTHON3 html2myst/html2myst.py _source_html/DeviceDrivers_MessageConstants.html topics/device-drivers/message-constants.md

$PYTHON3 html2myst/html2myst.py _source_html/BDeskbar.html topics/deskbar/deskbar.md

# could probably combine this into a single page, tbh
$PYTHON3 html2myst/html2myst.py _source_html/TheKeyboard_Introduction.html topics/keyboard/introduction.md
$PYTHON3 html2myst/html2myst.py _source_html/TheKeyboard_Definitions.html topics/keyboard/definitions.md
$PYTHON3 html2myst/html2myst.py _source_html/TheKeyboard_ModifierKeys.html topics/keyboard/modifier-keys.md
$PYTHON3 html2myst/html2myst.py _source_html/TheKeyboard_MoreOnKeyboardMapping.html topics/keyboard/mapping.md
$PYTHON3 html2myst/html2myst.py _source_html/TheKeyboard_CharacterConstants.html topics/keyboard/character-constants.md
$PYTHON3 html2myst/html2myst.py _source_html/TheKeyboard_JourneyOfAKeystroke.html topics/keyboard/journey.md
$PYTHON3 html2myst/html2myst.py _source_html/TheKeyboard_KeyboardMessages.html topics/keyboard/messages.md
$PYTHON3 html2myst/html2myst.py _source_html/TheKeyboard_KeyCodes.html topics/keyboard/key-codes.md
$PYTHON3 html2myst/html2myst.py _source_html/TheKeyboard_KeyStates.html topics/keyboard/key-states.md

$PYTHON3 html2myst/html2myst.py _source_html/TheTracker_Scripting.html topics/tracker/scripting.md
$PYTHON3 html2myst/html2myst.py _source_html/TheTracker_AddOnProtocol.html topics/tracker/add-on-protocol.md
$PYTHON3 html2myst/html2myst.py _source_html/TheTracker_BackgroundImages.html topics/tracker/background-images.md

#$PYTHON3 html2myst/html2myst.py _source_html/.html system-overview/kit/.md

$PYTHON3 html2myst/html2myst.py _source_html/BAlert_Overview.html system-overview/interface/alert.md
$PYTHON3 html2myst/html2myst.py _source_html/BApplication_Overview.html system-overview/application/application.md
$PYTHON3 html2myst/html2myst.py _source_html/BAppFileInfo_Overview.html system-overview/storage/app-file-info.md
$PYTHON3 html2myst/html2myst.py _source_html/BBitmap_Overview.html system-overview/interface/bitmap.md
$PYTHON3 html2myst/html2myst.py _source_html/BBox_Overview.html system-overview/interface/box.md
$PYTHON3 html2myst/html2myst.py _source_html/BBufferConsumer_Overview.html system-overview/media/buffer-consumer.md
$PYTHON3 html2myst/html2myst.py _source_html/BBufferGroup_Overview.html system-overview/media/buffer-group.md
$PYTHON3 html2myst/html2myst.py _source_html/BBuffer_Overview.html system-overview/media/buffer.md
$PYTHON3 html2myst/html2myst.py _source_html/BBufferProducer_Overview.html system-overview/media/buffer-producer.md
$PYTHON3 html2myst/html2myst.py _source_html/BButton_Overview.html system-overview/interface/button.md
$PYTHON3 html2myst/html2myst.py _source_html/BCheckBox_Overview.html system-overview/interface/check-box.md
$PYTHON3 html2myst/html2myst.py _source_html/BClipboard_Overview.html system-overview/application/clipboard.md
$PYTHON3 html2myst/html2myst.py _source_html/BColorControl_Overview.html system-overview/interface/color-control.md
$PYTHON3 html2myst/html2myst.py _source_html/BContinuousParameter_Overview.html system-overview/media/continuous-parameter.md
$PYTHON3 html2myst/html2myst.py _source_html/BControl_Overview.html system-overview/interface/control.md
$PYTHON3 html2myst/html2myst.py _source_html/BControllable_Overview.html system-overview/media/controllable.md
$PYTHON3 html2myst/html2myst.py _source_html/BCursor_Overview.html system-overview/application/cursor.md
$PYTHON3 html2myst/html2myst.py _source_html/BDirectory_Overview.html system-overview/storage/directory.md
$PYTHON3 html2myst/html2myst.py _source_html/BDirectWindow_Overview.html system-overview/game/direct-window.md
$PYTHON3 html2myst/html2myst.py _source_html/BDiscreteParameter_Overview.html system-overview/media/discrete-parameter.md
$PYTHON3 html2myst/html2myst.py _source_html/BDragger_Overview.html system-overview/interface/dragger.md
$PYTHON3 html2myst/html2myst.py _source_html/BEntry_Overview.html system-overview/storage/entry.md
$PYTHON3 html2myst/html2myst.py _source_html/BEntryList_Overview.html system-overview/storage/entry-list.md
$PYTHON3 html2myst/html2myst.py _source_html/BFileGameSound_Overview.html system-overview/game/file-game-sound.md
$PYTHON3 html2myst/html2myst.py _source_html/BFile_Overview.html system-overview/storage/file.md
$PYTHON3 html2myst/html2myst.py _source_html/BFileInterface_Overview.html system-overview/media/file-interface.md
$PYTHON3 html2myst/html2myst.py _source_html/BFilePanel_Overview.html system-overview/storage/file-panel.md
$PYTHON3 html2myst/html2myst.py _source_html/BFont_Overview.html system-overview/interface/font.md
$PYTHON3 html2myst/html2myst.py _source_html/BGLView_Overview.html system-overview/opengl/gl-view.md
$PYTHON3 html2myst/html2myst.py _source_html/BHandler_Overview.html system-overview/application/handler.md
$PYTHON3 html2myst/html2myst.py _source_html/BInputDevice_Overview.html system-overview/input/input-device.md
$PYTHON3 html2myst/html2myst.py _source_html/BInputServerDevice_Overview.html system-overview/input/input-server-device.md
$PYTHON3 html2myst/html2myst.py _source_html/BInputServerFilter_Overview.html system-overview/input/input-server-filter.md
$PYTHON3 html2myst/html2myst.py _source_html/BInputServerMethod_Overview.html system-overview/input/input-server-method.md
$PYTHON3 html2myst/html2myst.py _source_html/BInvoker_Overview.html system-overview/application/invoker.md
$PYTHON3 html2myst/html2myst.py _source_html/BJoystick_Overview.html system-overview/device/joystick.md
$PYTHON3 html2myst/html2myst.py _source_html/BListItem_Overview.html system-overview/interface/list-item.md
$PYTHON3 html2myst/html2myst.py _source_html/BLooper_Overview.html system-overview/application/looper.md
$PYTHON3 html2myst/html2myst.py _source_html/BMailMessage_Overview.html system-overview/mail/mail-message.md
$PYTHON3 html2myst/html2myst.py _source_html/BMediaAddOn_Overview.html system-overview/media/media-add-on.md
$PYTHON3 html2myst/html2myst.py _source_html/BMediaEventLooper_Overview.html system-overview/media/media-event-looper.md
$PYTHON3 html2myst/html2myst.py _source_html/BMediaFile_Overview.html system-overview/media/media-file.md
$PYTHON3 html2myst/html2myst.py _source_html/BMediaFiles_Overview.html system-overview/media/media-files.md
$PYTHON3 html2myst/html2myst.py _source_html/BMediaFormats_Overview.html system-overview/media/media-formats.md
$PYTHON3 html2myst/html2myst.py _source_html/BMediaNode_Overview.html system-overview/media/media-node.md
$PYTHON3 html2myst/html2myst.py _source_html/BMediaRoster_Overview.html system-overview/media/media-roster.md
$PYTHON3 html2myst/html2myst.py _source_html/BMediaTheme_Overview.html system-overview/media/media-theme.md
$PYTHON3 html2myst/html2myst.py _source_html/BMediaTrack_Overview.html system-overview/media/media-track.md
$PYTHON3 html2myst/html2myst.py _source_html/BMenuBar_Overview.html system-overview/interface/menu-bar.md
$PYTHON3 html2myst/html2myst.py _source_html/BMenuField_Overview.html system-overview/interface/menu-field.md
$PYTHON3 html2myst/html2myst.py _source_html/BMenu_Overview.html system-overview/interface/menu.md
$PYTHON3 html2myst/html2myst.py _source_html/BMenuItem_Overview.html system-overview/interface/menu-item.md
$PYTHON3 html2myst/html2myst.py _source_html/BMessageFilter_Overview.html system-overview/application/message-filter.md
$PYTHON3 html2myst/html2myst.py _source_html/BMessage_Overview.html system-overview/application/message.md
$PYTHON3 html2myst/html2myst.py _source_html/BMessageQueue_Overview.html system-overview/application/message-queue.md
$PYTHON3 html2myst/html2myst.py _source_html/BMessenger_Overview.html system-overview/application/messenger.md
$PYTHON3 html2myst/html2myst.py _source_html/BMimeType_Overview.html system-overview/storage/mime-type.md
$PYTHON3 html2myst/html2myst.py _source_html/BNetAddress_Overview.html system-overview/network/net-address.md
$PYTHON3 html2myst/html2myst.py _source_html/BNetBuffer_Overview.html system-overview/network/net-buffer.md
$PYTHON3 html2myst/html2myst.py _source_html/BNetDebug_Overview.html system-overview/network/net-debug.md
$PYTHON3 html2myst/html2myst.py _source_html/BNetEndpoint_Overview.html system-overview/network/net-endpoint.md
$PYTHON3 html2myst/html2myst.py _source_html/BNode_Overview.html system-overview/storage/node.md
$PYTHON3 html2myst/html2myst.py _source_html/BNodeInfo_Overview.html system-overview/storage/node-info.md
$PYTHON3 html2myst/html2myst.py _source_html/BNullParameter_Overview.html system-overview/media/null-parameter.md
$PYTHON3 html2myst/html2myst.py _source_html/BOutlineListView_Overview.html system-overview/interface/outline-list-view.md
$PYTHON3 html2myst/html2myst.py _source_html/BParameterGroup_Overview.html system-overview/media/parameter-group.md
$PYTHON3 html2myst/html2myst.py _source_html/BParameter_Overview.html system-overview/media/parameter.md
$PYTHON3 html2myst/html2myst.py _source_html/BParameterWeb_Overview.html system-overview/media/parameter-web.md
$PYTHON3 html2myst/html2myst.py _source_html/BPath_Overview.html system-overview/storage/path.md
$PYTHON3 html2myst/html2myst.py _source_html/BPictureButton_Overview.html system-overview/interface/picture-button.md
$PYTHON3 html2myst/html2myst.py _source_html/BPicture_Overview.html system-overview/interface/picture.md
$PYTHON3 html2myst/html2myst.py _source_html/BPoint_Overview.html system-overview/interface/point.md
$PYTHON3 html2myst/html2myst.py _source_html/BPolygon_Overview.html system-overview/interface/polygon.md
$PYTHON3 html2myst/html2myst.py _source_html/BPopUpMenu_Overview.html system-overview/interface/pop-up-menu.md
$PYTHON3 html2myst/html2myst.py _source_html/BPrintJob_Overview.html system-overview/interface/print-job.md
$PYTHON3 html2myst/html2myst.py _source_html/BPropertyInfo_Overview.html system-overview/application/property-info.md
$PYTHON3 html2myst/html2myst.py _source_html/BPushGameSound_Overview.html system-overview/game/push-game-sound.md
$PYTHON3 html2myst/html2myst.py _source_html/BQuery_Overview.html system-overview/storage/query.md
$PYTHON3 html2myst/html2myst.py _source_html/BRadioButton_Overview.html system-overview/interface/radio-button.md
$PYTHON3 html2myst/html2myst.py _source_html/BRect_Overview.html system-overview/interface/rect.md
$PYTHON3 html2myst/html2myst.py _source_html/BRefFilter_Overview.html system-overview/storage/ref-filter.md
$PYTHON3 html2myst/html2myst.py _source_html/BRegion_Overview.html system-overview/interface/region.md
$PYTHON3 html2myst/html2myst.py _source_html/BResources_Overview.html system-overview/storage/resources.md
$PYTHON3 html2myst/html2myst.py _source_html/BRoster_Overview.html system-overview/application/roster.md
$PYTHON3 html2myst/html2myst.py _source_html/BScreen_Overview.html system-overview/interface/screen.md
$PYTHON3 html2myst/html2myst.py _source_html/BScrollBar_Overview.html system-overview/interface/scroll-bar.md
$PYTHON3 html2myst/html2myst.py _source_html/BScrollView_Overview.html system-overview/interface/scroll-view.md
$PYTHON3 html2myst/html2myst.py _source_html/BSeparatorItem_Overview.html system-overview/interface/separator-item.md
$PYTHON3 html2myst/html2myst.py _source_html/BSerialPort_Overview.html system-overview/device/serial-port.md
$PYTHON3 html2myst/html2myst.py _source_html/BShape_Overview.html system-overview/interface/shape.md
$PYTHON3 html2myst/html2myst.py _source_html/BShapeIterator_Overview.html system-overview/interface/shape-iterator.md
$PYTHON3 html2myst/html2myst.py _source_html/BShelf_Overview.html system-overview/interface/shelf.md
$PYTHON3 html2myst/html2myst.py _source_html/BSimpleGameSound_Overview.html system-overview/game/simple-game-sound.md
$PYTHON3 html2myst/html2myst.py _source_html/BSlider_Overview.html system-overview/interface/slider.md
$PYTHON3 html2myst/html2myst.py _source_html/BSmallBuffer_Overview.html system-overview/media/small-buffer.md
$PYTHON3 html2myst/html2myst.py _source_html/BSoundPlayer_Overview.html system-overview/media/sound-player.md
$PYTHON3 html2myst/html2myst.py _source_html/BStatable_Overview.html system-overview/storage/statable.md
$PYTHON3 html2myst/html2myst.py _source_html/BStatusBar_Overview.html system-overview/interface/status-bar.md
$PYTHON3 html2myst/html2myst.py _source_html/BStreamingGameSound_Overview.html system-overview/game/streaming-game-sound.md
$PYTHON3 html2myst/html2myst.py _source_html/BStringItem_Overview.html system-overview/interface/string-item.md
$PYTHON3 html2myst/html2myst.py _source_html/BStringView_Overview.html system-overview/interface/string-view.md
$PYTHON3 html2myst/html2myst.py _source_html/BSymLink_Overview.html system-overview/storage/sym-link.md
$PYTHON3 html2myst/html2myst.py _source_html/BTab_Overview.html system-overview/interface/tab.md
$PYTHON3 html2myst/html2myst.py _source_html/BTabView_Overview.html system-overview/interface/tab-view.md
$PYTHON3 html2myst/html2myst.py _source_html/BTextView_Overview.html system-overview/interface/text-view.md
$PYTHON3 html2myst/html2myst.py _source_html/BTimeCode_Overview.html system-overview/media/time-code.md
$PYTHON3 html2myst/html2myst.py _source_html/BTimedEventQueue_Overview.html system-overview/media/timed-event-queue.md
$PYTHON3 html2myst/html2myst.py _source_html/BTimeSource_Overview.html system-overview/media/time-source.md
$PYTHON3 html2myst/html2myst.py _source_html/BTranslationUtils_Overview.html system-overview/translation/translation-utils.md
$PYTHON3 html2myst/html2myst.py _source_html/BTranslator_Overview.html system-overview/translation/translator.md
$PYTHON3 html2myst/html2myst.py _source_html/BView_Overview.html system-overview/interface/view.md
$PYTHON3 html2myst/html2myst.py _source_html/BVolume_Overview.html system-overview/storage/volume.md
$PYTHON3 html2myst/html2myst.py _source_html/BVolumeRoster_Overview.html system-overview/storage/volume-roster.md
$PYTHON3 html2myst/html2myst.py _source_html/BWindow_Overview.html system-overview/interface/window.md 
$PYTHON3 html2myst/html2myst.py _source_html/BWindowScreen_Overview.html system-overview/game/window-screen.md

sem --wait
