from main import agent_loop


def router(user_input):

    try:
        return agent_loop(user_input)

    except Exception:
        return (
            "Sorry! OpenRouter is currently busy.\n"
            "Please try again in a few moments."
        )