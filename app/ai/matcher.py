from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

def match_resume(
    resume,
    jd
):

    emb1 = model.encode([resume])
    emb2 = model.encode([jd])

    score = cosine_similarity(
        emb1,
        emb2
    )[0][0]

    return round(
        score * 100,
        2
    )