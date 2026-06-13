def skill_gap(
    resume_skills,
    jd_skills
):
    return list(
        set(jd_skills)
        - set(resume_skills)
    )