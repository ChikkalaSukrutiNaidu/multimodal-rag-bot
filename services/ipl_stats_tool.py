def is_ipl_stats_query(question):

    question = question.lower()

    keywords = [
    "most runs",
    "most wickets",
    "highest score",
    "orange cap",
    "purple cap",

    "ipl",
    "title",
    "titles",
    "champion",
    "winner",

    "rcb",
    "csk",
    "mi",
    "mumbai indians",
    "kkr",
    "rr",
    "gt",
    "pbks",
    "srh",
    "dc",
    "lsg",

    "virat",
    "rohit",
    "dhoni",
    "captain",
    "team"
]

    return any(
        keyword in question
        for keyword in keywords
    )