"""Rule-based interview question generator.

No external LLM/Ollama dependency — questions (and model answers) are built from
the skills found in the resume plus the job description, so it works fully
offline.
"""

from app.ai.skills import extract_skills

# Per-skill (question, model answer) pairs. A fallback is used for any skill
# not listed below.
SKILL_QA = {
    "python": [
        (
            "Explain the difference between a list and a tuple in Python, and when you'd use each.",
            "A list is mutable (you can add, remove, or change items) while a tuple is immutable. Use a list for a collection that changes over time, and a tuple for fixed data — e.g. coordinates or a record — which also lets it be used as a dictionary key and is slightly faster to access.",
        ),
        (
            "How does Python's garbage collection work, and what are reference cycles?",
            "Python primarily uses reference counting: an object is freed when its reference count drops to zero. Reference cycles (objects referencing each other) can't be freed by counting alone, so a generational cyclic garbage collector periodically detects and collects them. You can tune or disable it via the `gc` module.",
        ),
    ],
    "java": [
        (
            "What is the difference between an abstract class and an interface in Java?",
            "An abstract class can hold state (fields), constructors, and a mix of implemented and abstract methods, and a class can extend only one. An interface defines a contract — historically only abstract methods, now also default/static methods — and a class can implement many. Use an abstract class for shared base behavior, an interface for capability that crosses unrelated hierarchies.",
        ),
        (
            "Explain how the JVM handles memory management and garbage collection.",
            "The JVM splits the heap into young and old generations. New objects go in the young generation; minor GCs collect short-lived ones, and survivors are promoted to the old generation, collected by less frequent major GCs. Collectors like G1 aim to minimize pause times. The developer doesn't free memory manually — unreachable objects are reclaimed automatically.",
        ),
    ],
    "fastapi": [
        (
            "How does dependency injection work in FastAPI, and why is it useful?",
            "You declare dependencies as function parameters using `Depends(...)`. FastAPI resolves and caches them per request, injecting things like DB sessions, auth, or config. It's useful for reusing logic, keeping endpoints clean, and making code testable by overriding dependencies in tests.",
        ),
        (
            "How would you handle async database calls in a FastAPI endpoint?",
            "Define the endpoint with `async def` and use an async driver/ORM (e.g. asyncpg or SQLAlchemy's async engine), awaiting queries so the event loop isn't blocked. Provide the session through a dependency. For blocking/sync libraries, run them in a threadpool (e.g. `run_in_threadpool`) so they don't stall the loop.",
        ),
    ],
    "spring boot": [
        (
            "What problem does Spring Boot auto-configuration solve?",
            "It removes most boilerplate configuration by inspecting the classpath and beans present, then wiring sensible defaults automatically — e.g. configuring a datasource when a JDBC driver is found. You override defaults via properties or your own beans, so you start fast but keep full control.",
        ),
        (
            "How do you manage application configuration across environments in Spring Boot?",
            "Use profile-specific property files (application-dev.yml, application-prod.yml) activated via `spring.profiles.active`, plus environment variables or a config server for secrets. This keeps one codebase that adapts per environment without hardcoding values.",
        ),
    ],
    "aws": [
        (
            "Describe a time you chose between EC2, ECS, and Lambda for a workload.",
            "Frame it by workload shape: Lambda for short, event-driven, spiky tasks where you want zero server management; ECS/Fargate for containerized services needing more control or long-running processes; EC2 when you need full OS control, special hardware, or steady high utilization. Tie your choice to cost, scaling, and operational overhead.",
        ),
        (
            "How would you design a cost-effective, highly available app on AWS?",
            "Spread across multiple Availability Zones, put compute behind an Application Load Balancer with an Auto Scaling Group, use a managed multi-AZ database (RDS), cache with ElastiCache/CloudFront, and store static assets in S3. Control cost with right-sizing, auto-scaling to demand, and spot/savings plans where appropriate.",
        ),
    ],
    "docker": [
        (
            "What is the difference between a Docker image and a container?",
            "An image is an immutable, layered template (your app plus its dependencies). A container is a running instance of an image with its own writable layer and isolated process space. One image can spawn many containers — like a class versus its objects.",
        ),
        (
            "How would you reduce the size of a production Docker image?",
            "Use a small base image (alpine/slim), multi-stage builds to drop build tools from the final image, combine and clean up package installs in one layer, add a .dockerignore, and copy only what's needed. This shrinks the image, speeds pulls, and reduces attack surface.",
        ),
    ],
    "kubernetes": [
        (
            "Explain the role of a Deployment vs a StatefulSet in Kubernetes.",
            "A Deployment manages stateless, interchangeable pods with easy rolling updates and scaling. A StatefulSet gives pods stable identities, ordered startup/shutdown, and stable persistent storage — needed for stateful systems like databases where each replica is distinct.",
        ),
        (
            "How does a Kubernetes Service route traffic to pods?",
            "A Service has a stable virtual IP and selects pods by labels. kube-proxy programs the node's networking to load-balance traffic across the matching pod IPs, and an Endpoints/EndpointSlice object tracks the current healthy pods, so traffic follows pods as they come and go.",
        ),
    ],
    "sql": [
        (
            "What is the difference between an INNER JOIN and a LEFT JOIN?",
            "An INNER JOIN returns only rows with a match in both tables. A LEFT JOIN returns all rows from the left table plus matches from the right, filling unmatched right-side columns with NULL. Use LEFT JOIN when you want to keep all left-side rows regardless of a match.",
        ),
        (
            "How would you identify and fix a slow SQL query?",
            "Run EXPLAIN/EXPLAIN ANALYZE to see the plan and spot full table scans or bad join orders. Common fixes: add indexes on filtered/joined columns, avoid SELECT *, rewrite correlated subqueries, and reduce the scanned row count. Re-measure after each change to confirm the improvement.",
        ),
    ],
    "mysql": [
        (
            "How do indexes improve query performance in MySQL, and what are their costs?",
            "An index (usually a B-tree) lets MySQL find rows without scanning the whole table, drastically speeding up WHERE, JOIN, and ORDER BY on indexed columns. The cost is extra storage and slower writes, since every INSERT/UPDATE/DELETE must also maintain the index — so index selectively.",
        ),
        (
            "Explain the difference between InnoDB and MyISAM storage engines.",
            "InnoDB supports transactions, foreign keys, and row-level locking with crash recovery, making it the default for reliable concurrent writes. MyISAM is older, lacks transactions and foreign keys, and uses table-level locking — faster for read-heavy, simple workloads but unsafe for concurrent writes.",
        ),
    ],
    "postgresql": [
        (
            "What are the advantages of PostgreSQL's JSONB over plain JSON?",
            "JSONB stores data in a decomposed binary form, so it's faster to query and supports indexing (GIN) and operators, at the cost of slightly slower inserts and not preserving key order/whitespace. Plain JSON keeps the exact text but must be reparsed on each access. Use JSONB when you query into the document.",
        ),
        (
            "How does MVCC work in PostgreSQL?",
            "Multi-Version Concurrency Control keeps multiple row versions so readers never block writers and vice versa — each transaction sees a consistent snapshot. Old versions are cleaned up later by VACUUM. This gives high concurrency without read locks.",
        ),
    ],
    "mongodb": [
        (
            "When would you choose MongoDB over a relational database?",
            "Choose MongoDB when your data is document-shaped, the schema evolves, and you want to scale out horizontally — e.g. catalogs, user profiles, or event data. A relational DB is better when you need strong multi-row transactions, complex joins, and a rigid, normalized schema.",
        ),
        (
            "How do you model a one-to-many relationship in MongoDB?",
            "Two common patterns: embed the 'many' documents inside the parent when they're bounded and usually read together, or reference them by storing the parent's _id in the child documents when the set is large or grows unbounded. The choice depends on access patterns and document size limits.",
        ),
    ],
    "react": [
        (
            "Explain the difference between state and props in React.",
            "Props are read-only inputs passed from a parent to configure a component. State is data a component owns and can change over time, triggering a re-render. Props flow down; state is local — lifting state up or using context shares it across components.",
        ),
        (
            "What problems do the useEffect dependency array solve, and how can it go wrong?",
            "The dependency array tells React when to re-run the effect — only when a listed value changes — preventing unnecessary work and stale closures. It goes wrong when you omit a used value (stale data) or include an unstable one like a recreated object/function (infinite loops); fix with correct deps, useCallback/useMemo, or a ref.",
        ),
    ],
    "angular": [
        (
            "What is the role of services and dependency injection in Angular?",
            "Services hold reusable logic and shared state (e.g. HTTP calls), keeping components thin. Angular's DI provides them where needed via constructor injection, and providedIn:'root' gives a singleton. This improves reuse, testability (easy to mock), and separation of concerns.",
        ),
        (
            "How does change detection work in Angular?",
            "Angular runs change detection (via Zone.js) after async events, walking the component tree to update the DOM where bound data changed. You can optimize with the OnPush strategy, which only checks a component when its inputs change or an event fires, reducing work in large apps.",
        ),
    ],
    "javascript": [
        (
            "Explain closures in JavaScript with a practical example.",
            "A closure is a function that remembers variables from the scope where it was created, even after that scope has returned. For example, a `makeCounter()` that returns an inner function incrementing a private `count` — each returned counter keeps its own `count`. Closures enable data privacy and factory functions.",
        ),
        (
            "What is the event loop, and how do promises and async/await fit into it?",
            "JavaScript is single-threaded; the event loop pulls callbacks from queues onto the call stack when it's empty. Promise callbacks go to the microtask queue, which runs before the macrotask queue (timers, I/O). async/await is syntactic sugar over promises — `await` pauses the function and resumes via a microtask when the promise settles.",
        ),
    ],
    "machine learning": [
        (
            "How do you handle overfitting in a machine learning model?",
            "Overfitting is memorizing training data and failing to generalize. Combat it with more/representative data, regularization (L1/L2, dropout), simpler models, cross-validation, early stopping, and feature selection. Always validate on a held-out set to confirm generalization.",
        ),
        (
            "Walk me through how you'd evaluate a classification model.",
            "Split data (train/validation/test), then look beyond accuracy — especially for imbalanced classes — at precision, recall, F1, and the confusion matrix, plus ROC-AUC. Choose the metric that matches the cost of errors (e.g. recall when missing positives is expensive) and use cross-validation for a robust estimate.",
        ),
    ],
    "deep learning": [
        (
            "What is the vanishing gradient problem, and how is it mitigated?",
            "In deep networks, gradients can shrink toward zero as they backpropagate through many layers, stalling learning in early layers. Mitigations include ReLU-type activations, careful weight initialization (He/Xavier), batch normalization, and residual (skip) connections that give gradients a shortcut.",
        ),
        (
            "Explain the difference between a CNN and an RNN and where each is used.",
            "CNNs use convolutional filters to capture spatial patterns and are ideal for images. RNNs (and LSTMs/GRUs) process sequences with a hidden state carrying context, suited to text, speech, and time series. In short: CNN for spatial data, RNN for sequential data — though transformers now often replace RNNs.",
        ),
    ],
    "gen ai": [
        (
            "What are the main risks of using generative AI in production, and how do you mitigate them?",
            "Key risks are hallucinations, leaking sensitive data, bias, and prompt injection. Mitigate with retrieval-augmented generation for grounding, input/output validation and guardrails, human review for high-stakes outputs, PII filtering, and monitoring/logging to catch regressions.",
        ),
        (
            "Explain how retrieval-augmented generation (RAG) improves an LLM's answers.",
            "RAG retrieves relevant documents (often via vector search over embeddings) and feeds them into the prompt as context, so the model answers from real, up-to-date sources instead of only its training memory. This reduces hallucinations and lets you cite sources without retraining the model.",
        ),
    ],
    "llm": [
        (
            "What is the difference between fine-tuning and prompt engineering for an LLM?",
            "Prompt engineering shapes behavior at inference time via instructions and examples — cheap, fast, no training. Fine-tuning updates the model's weights on your data for consistent, specialized behavior — more powerful but costlier and slower to iterate. Start with prompting (and RAG); fine-tune when prompting can't reach the needed quality.",
        ),
        (
            "How would you reduce hallucinations in an LLM-powered application?",
            "Ground responses with RAG over trusted sources, instruct the model to say 'I don't know' when unsure, lower temperature, constrain outputs to a schema, and verify critical facts with a second check or tool call. Showing citations also lets users catch errors.",
        ),
    ],
    "langchain": [
        (
            "What problem does LangChain solve when building LLM applications?",
            "It provides reusable abstractions — prompts, chains, memory, retrievers, and tool/agent integrations — so you can compose multi-step LLM workflows without rebuilding plumbing. It standardizes connecting models to data sources and external tools.",
        ),
        (
            "Explain how chains and agents differ in LangChain.",
            "A chain runs a fixed, predetermined sequence of steps. An agent uses the LLM to decide dynamically which tools to call and in what order, looping until it reaches an answer. Chains are predictable; agents are flexible but harder to control and debug.",
        ),
    ],
    "pandas": [
        (
            "How would you handle missing data in a pandas DataFrame?",
            "First inspect it with isna().sum(). Then choose based on context: drop rows/columns with dropna() when sparse, or fill with fillna() using a constant, mean/median, or forward/backward fill. The right choice depends on how much is missing and whether the gap is informative.",
        ),
        (
            "Explain the difference between .loc and .iloc in pandas.",
            ".loc selects by label (row/column names and boolean masks) and is inclusive of the end label. .iloc selects by integer position and is end-exclusive like normal Python slicing. Use .loc for named access and .iloc for positional access.",
        ),
    ],
    "numpy": [
        (
            "Why are NumPy operations faster than equivalent pure-Python loops?",
            "NumPy stores data in contiguous, typed arrays and runs vectorized operations in optimized C under the hood, avoiding Python's per-element interpreter overhead and using CPU cache and SIMD efficiently. So one array operation replaces a slow Python loop.",
        ),
        (
            "Explain broadcasting in NumPy with an example.",
            "Broadcasting lets NumPy apply operations to arrays of different shapes by virtually stretching the smaller one — without copying data. For example, adding a shape-(3,) vector to a shape-(2,3) matrix adds the vector to each row. Dimensions must be equal or one of them must be 1.",
        ),
    ],
}

BEHAVIORAL_QA = [
    (
        "Tell me about a challenging project from your resume and the impact you had.",
        "Pick a real project and use STAR: briefly set the Situation and your Task, spend most of the time on the Actions you personally took and the decisions you made, then quantify the Result (time saved, users served, bug reduced). Emphasize your specific contribution, not just the team's.",
    ),
    (
        "Describe a time you disagreed with a teammate. How did you resolve it?",
        "Show maturity: state the disagreement objectively, explain how you listened to their reasoning, brought data or a small prototype, and focused on the shared goal rather than ego. End with the outcome and what you learned about collaboration.",
    ),
    (
        "How do you prioritize tasks when everything feels urgent?",
        "Explain a system: assess impact vs. effort and deadlines (e.g. an impact/urgency matrix), confirm priorities with stakeholders, break work into small deliverables, and communicate trade-offs early. Give a concrete example where this kept a deadline on track.",
    ),
    (
        "Tell me about a time you failed and what you learned from it.",
        "Choose a genuine, low-drama failure, own your part without blaming others, and focus on the lesson and the concrete change you made afterward (a new habit, test, or process). Interviewers want self-awareness and growth, not a flawless record.",
    ),
]


def generate_questions(resume: str, jd: str = "", limit: int = 10):
    """Return a list of tailored interview questions, each with a model answer.

    Questions are derived from the skills detected in the resume (and any extra
    skills mentioned in the job description), then padded with behavioral
    questions so there are always up to `limit` of them. Every item includes an
    `answer` field with a concise model answer.
    """
    resume_skills = extract_skills(resume or "")
    jd_skills = extract_skills(jd or "")

    # Skills in the resume come first; JD-only skills next (gaps worth probing).
    ordered = list(dict.fromkeys(resume_skills + jd_skills))

    questions = []
    for skill in ordered:
        pairs = SKILL_QA.get(
            skill,
            [
                (
                    f"Can you describe your experience with {skill}?",
                    f"Give a concrete example of a project where you used {skill}: what you built, the decisions you made, the challenges you hit, and the outcome. Tie it back to the role's needs.",
                )
            ],
        )
        for q, a in pairs:
            questions.append(
                {"type": "technical", "skill": skill, "question": q, "answer": a}
            )

    # Add behavioral questions to round things out.
    for q, a in BEHAVIORAL_QA:
        questions.append(
            {"type": "behavioral", "skill": None, "question": q, "answer": a}
        )

    return questions[:limit]
