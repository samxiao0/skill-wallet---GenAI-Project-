from transformers import pipeline

classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)


CANDIDATE_TOPICS = [
    "Artificial Intelligence",
    "Machine Learning",
    "Cloud Computing",
    "Cybersecurity",
    "Data Science",
    "Startups",
    "Entrepreneurship",
    "Software Development",
    "Healthcare",
    "Finance",
    "Education"
]


def analyze_event(description: str):
    result = classifier(
        description,
        CANDIDATE_TOPICS,
        multi_label=True
    )

    topics = []

    for label, score in zip(result["labels"], result["scores"]):
        if score > 0.3:
            topics.append(label)

    return topics