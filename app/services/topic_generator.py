def generate_conversation_topics(
        event_topics,
        user_interests):

    suggestions = []

    for topic in event_topics:

        suggestions.append(
            f"What inspired you to explore {topic}?"
        )

        suggestions.append(
            f"How do you see the future of {topic} evolving?"
        )

    for interest in user_interests:

        suggestions.append(
            f"I noticed you're interested in {interest}. What projects have you worked on recently?"
        )

    return suggestions[:10]