def is_ipl_stats_query(question):

    question = question.lower()

    keywords = [
        "most runs",
        "most wickets",
        "highest score",
        "orange cap",
        "purple cap",
        "compare",
        "virat",
        "rohit",
        "dhoni",
        "team",
        "captain"
    ]

    return any(
        keyword in question
        for keyword in keywords
    )