from app.services.fact_checker import verify_topic


def test_fact_check():

    result = verify_topic("Artificial Intelligence")

    assert isinstance(result, str)
    assert len(result) > 0