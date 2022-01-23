#pragma once

namespace jucey
{
    template<typename Invokable>
    void invokeOnMessageThreadAndWait (Invokable&& invokable)
    {
        if (auto* messageManager = juce::MessageManager::getInstance())
        {
            std::promise<void> promise;
            auto future = promise.get_future();

            const auto asyncFunction = [invokable, &promise]() {
                try
                {
                    invokable();
                    promise.set_value();
                }
                catch (...)
                {
                    promise.set_exception (std::current_exception());
                }
            };

            if (! messageManager->callAsync (asyncFunction))
                throw std::runtime_error {"Failed to post a message to the message thread"};

            future.get();
        }
        else
        {
            throw std::runtime_error {"Failed to get an instance of the MessageManager"};
        }
    }
} // namespace jucey
