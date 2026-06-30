import wikipediaapi

wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent='networking-assistant'
)


def verify_topic(query: str):

    page = wiki.page(query)

    if page.exists():
        return page.summary[:500]

    return "No verified information found."