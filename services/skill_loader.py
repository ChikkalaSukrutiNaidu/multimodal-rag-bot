import os

SKILLS_DIR = "skills"

def load_skill(skill_name):

    file_path = os.path.join(
        SKILLS_DIR,
        f"{skill_name}.md"
    )

    if not os.path.exists(file_path):
        return ""

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:

        return f.read()