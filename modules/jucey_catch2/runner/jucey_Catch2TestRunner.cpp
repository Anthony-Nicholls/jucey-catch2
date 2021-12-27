namespace juce
{
    // declared in juce_core
    extern int juce_argc;
    extern const char* const* juce_argv;
    
} // juce

namespace jucey
{
    const juce::String Catch2TestRunner::getApplicationName()
    {
        return {};
    }
    
    const juce::String Catch2TestRunner::getApplicationVersion()
    {
        return {};
    }
    
    bool Catch2TestRunner::moreThanOneInstanceAllowed()
    {
        return false;
    }
    
    void Catch2TestRunner::initialise (const juce::String&)
    {
        juce::Thread::launch ([this](){
            Catch::Session session;
            setApplicationReturnValue (session.run (juce::juce_argc,
                                                    juce::juce_argv));
            quit();
        });
    }
    
    void Catch2TestRunner::shutdown()
    {
        
    }
    
    void Catch2TestRunner::anotherInstanceStarted (const juce::String&)
    {

    }
    
    void Catch2TestRunner::systemRequestedQuit()
    {
        jassertfalse;
    }
    
    void Catch2TestRunner::suspended()
    {
        jassertfalse;
    }
    
    void Catch2TestRunner::resumed()
    {
        jassertfalse;
    }
    
    void Catch2TestRunner::unhandledException (const std::exception*,
                                               const juce::String&,
                                               int)
    {
        jassertfalse;
    }
    
} // jucey
