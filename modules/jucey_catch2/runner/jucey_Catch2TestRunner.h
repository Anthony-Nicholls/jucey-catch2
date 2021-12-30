#pragma once

namespace jucey
{
    class Catch2TestRunner : public juce::JUCEApplicationBase
    {
    public:
        Catch2TestRunner() = default;
        ~Catch2TestRunner() = default;

    private:
        const juce::String getApplicationName() final;

        const juce::String getApplicationVersion() final;

        bool moreThanOneInstanceAllowed() final;

        void initialise (const juce::String&) final;

        void shutdown() final;

        void anotherInstanceStarted (const juce::String&) final;

        void systemRequestedQuit() final;

        void suspended() final;

        void resumed() final;

        void unhandledException (const std::exception*,
                                 const juce::String&,
                                 int) final;

        JUCE_DECLARE_NON_COPYABLE (Catch2TestRunner)
        JUCE_DECLARE_NON_MOVEABLE (Catch2TestRunner)
    };
} // namespace jucey
