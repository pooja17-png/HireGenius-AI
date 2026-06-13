from app.ai.skills import SKILLS


def calculate_ats(skills):
    total_skills = len(SKILLS)

    if total_skills == 0:
        return 0

    score = (len(skills) / total_skills) * 100

    return round(score)
