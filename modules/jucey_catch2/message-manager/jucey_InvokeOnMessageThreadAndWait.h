#pragma once

namespace jucey
{
    void invokeOnMessageThreadAndWait (const std::function<void()>& function);
} // jucey