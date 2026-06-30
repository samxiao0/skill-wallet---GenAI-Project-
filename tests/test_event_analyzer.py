from app.services.event_analyzer import analyze_event


def test_analyze_event():
    description = "AI and Machine Learning conference"

    topics = analyze_event(description)

    assert isinstance(topics, list)
    assert len(topics) > 0