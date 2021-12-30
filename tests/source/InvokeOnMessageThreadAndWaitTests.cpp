#include <catch2/catch_test_macros.hpp>
#include <juce_gui_basics/juce_gui_basics.h>
#include <jucey_catch2/jucey_catch2.h>
#include <thread>

SCENARIO ("Functions can be run on the message thread synchronously, from another thread")
{
    GIVEN ("There is a message thread")
    {
        juce::MessageManager* manager {juce::MessageManager::getInstanceWithoutCreating()};
        REQUIRE (manager != nullptr);

        AND_GIVEN ("The current thread is not the message thread")
        {
            REQUIRE_FALSE (manager->isThisTheMessageThread());

            WHEN ("A function is invoked on the message thread")
            {
                std::optional<bool> didFunctionRunOnTheMessageThread {std::nullopt};

                jucey::invokeOnMessageThreadAndWait ([&manager, &didFunctionRunOnTheMessageThread]() {
                    const auto enoughTimeToEnsureThisRunsSynchronously {std::chrono::milliseconds {100}};
                    std::this_thread::sleep_for (enoughTimeToEnsureThisRunsSynchronously);
                    didFunctionRunOnTheMessageThread = manager->isThisTheMessageThread();
                });

                THEN ("The function is invoked synchronously") { REQUIRE (didFunctionRunOnTheMessageThread.has_value()); }
                THEN ("The function is invoked on the message thread") { REQUIRE (didFunctionRunOnTheMessageThread.value()); }
            }
        }
    }
}
