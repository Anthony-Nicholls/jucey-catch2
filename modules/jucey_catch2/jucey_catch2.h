#pragma once

/*******************************************************************************

 BEGIN_JUCE_MODULE_DECLARATION

  ID:                 jucey_catch2
  vendor:             jucey
  version:            1.0.0
  name:               JUCEY Catch2
  description:        Handy utilities for running Cacth2 tests from a JUCE console application.

  dependencies:       juce_gui_basics
  linuxLibs:          Catch2
  OSXLibs:            Catch2
  windowsLibs:        Catch2

 END_JUCE_MODULE_DECLARATION

*******************************************************************************/

#include <juce_gui_basics/juce_gui_basics.h>

#include "message-manager/jucey_InvokeOnMessageThreadAndWait.h"
#include "runner/jucey_Catch2TestRunner.h"
