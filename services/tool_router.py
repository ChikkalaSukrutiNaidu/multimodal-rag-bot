from services.skill_loader import load_skill

def detect_skill(question):

    q = question.lower()

    if any(
        word in q
        for word in [
            "compare",
            "better",
            "average",
            "strike rate",
            "centuries",
            "runs",
            "wickets"
        ]
    ):
        return load_skill(
            "player_comparison"
        )

    if any(
        word in q
        for word in [
            "between",
            "before",
            "after",
            "since",
            "during",
            "2019",
            "2020",
            "2021",
            "2022",
            "2023",
            "2024",
            "2025",
            "2026"
        ]
    ):
        return load_skill(
            "temporal_analysis"
        )

    if any(
        word in q
        for word in [
            "venue",
            "stadium",
            "pitch"
        ]
    ):
        return load_skill(
            "venue_analysis"
        )

    if any(
        word in q
        for word in [
            "he",
            "him",
            "his",
            "they",
            "them",
            "that player",
            "that team"
        ]
    ):
        return load_skill(
            "memory_reasoning"
        )

    return ""