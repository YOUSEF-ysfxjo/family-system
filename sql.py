import sqlite3
import numpy as np
from pathlib import Path

EMB_PATH = "children_embeddings.npy"
DB_PATH = "family_database.db"

# حمل الـ embeddings (لازم تكون مصفوفة شكلها (N, D))
embeddings = np.load(EMB_PATH)
embeddings = embeddings.astype(np.float32, copy=False)

if embeddings.ndim != 2:
    raise ValueError(f"Expected a 2D array (N, D), got shape {embeddings.shape}")

N, D = embeddings.shape

# جهّز أسماء صور (لو ما عندك أسماء فعلية)
image_names = [f"child_{i}.jpg" for i in range(N)]

# أنشئ قاعدة البيانات والجدول مع معلومات إضافية تساعدنا نسترجع الـBLOB
create_sql = """
CREATE TABLE IF NOT EXISTS children (
    id          INTEGER PRIMARY KEY,
    image_name  TEXT UNIQUE,
    embedding   BLOB NOT NULL,
    dim         INTEGER NOT NULL,
    dtype       TEXT NOT NULL
);
"""

insert_sql = """
INSERT INTO children (image_name, embedding, dim, dtype)
VALUES (?, ?, ?, ?)
ON CONFLICT(image_name) DO UPDATE SET
    embedding=excluded.embedding,
    dim=excluded.dim,
    dtype=excluded.dtype;
"""

Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
with sqlite3.connect(DB_PATH) as conn:
    cur = conn.cursor()
    cur.execute(create_sql)

    rows = []
    for name, emb in zip(image_names, embeddings):
        rows.append((name, emb.tobytes(), D, str(emb.dtype)))

    cur.executemany(insert_sql, rows)
    conn.commit()

print(f"تم تحويل {N} embedding إلى SQLite بنجاح في: {DB_PATH}")
