SKILLS = [
    "python",
    "java",
    "fastapi",
    "spring boot",
    "aws",
    "docker",
    "kubernetes",       
    "sql",
    "mysql",
    "postgresql",
    "mongodb",      
    "react",
    "angular",
    "javascript",
    "machine learning",
    "deep learning",
    "gen ai",
    "llm",
    "langchain",
    "pandas",
    "numpy"
]

def extract_skills(text):

    found_skills = []

    text = text.lower()

    for skill in SKILLS:
        if skill.lower() in text:
            found_skills.append(skill)

    return found_skills



def extract_jd_skills(jd):

    skills =  []

    jd = jd.lower()

    for skill in jd:
        skills.append(skill)

    return skills