import os
import numpy as np
import cv2
from insightface.app import FaceAnalysis

class FaceProcessor:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FaceProcessor, cls).__new__(cls)
            cls._instance.app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
            cls._instance.app.prepare(ctx_id=-1)
        return cls._instance

    def get_embedding(self, image_path):
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not found: {image_path}")
        faces = self.app.get(img)
        if len(faces) == 0:
            raise ValueError("No faces detected")
        return faces[0].normed_embedding

def build_database(images_folder, output_file="children_embeddings.npy"):
    processor = FaceProcessor()
    embeddings = []
    names = []
    
    if not os.path.exists(images_folder):
        os.makedirs(images_folder, exist_ok=True)  
        print(f"Done: {images_folder}")
        print(f"Add children images to: {os.path.abspath(images_folder)}")
        return  
    
    
    
    for img_file in os.listdir(images_folder):
        if not img_file.lower().endswith(('.jpg', '.png', '.jpeg')):
            continue
        
        try:
            emb = processor.get_embedding(os.path.join(images_folder, img_file))
            embeddings.append(emb)
            names.append(img_file)
            print(f"processing {img_file}")
        except Exception as e:
            print(f"Error processing {img_file}: {str(e)}")
    
    if embeddings:
        arr = np.asarray(embeddings, dtype=np.float32)
        np.save(output_file, arr)
        np.save("children_names.npy", names)
        print(f"Done: {len(embeddings)}")

    else:
        print("No embeddings generated")

class FamilyMatcher:
    def __init__(self, min_similarity_threshold=0.45):
        self.face_processor = FaceProcessor()
        self.min_similarity_threshold = min_similarity_threshold
    
    def create_family_embedding(self, mother_path, father_path, alpha=0.6):
        mother_emb = self.face_processor.get_embedding(mother_path)
        father_emb = self.face_processor.get_embedding(father_path)
        
        family_emb = alpha * mother_emb + (1 - alpha) * father_emb
        family_emb = family_emb / np.linalg.norm(family_emb)
        return family_emb.astype(np.float32, copy=False)    
    
    def find_best_alpha(self, mother_path, father_path, child_path,
                      alpha_range=np.arange(0.3, 0.8, 0.1)):

        child_emb = self.face_processor.get_embedding(child_path)
        best_alpha, best_similarity = 0.5, -1.0
        for alpha in alpha_range:
            family_emb = self.create_family_embedding(mother_path, father_path, alpha)
            similarity = float(np.dot(family_emb, child_emb))
            if similarity > best_similarity:
                best_similarity, best_alpha = similarity, alpha
        return best_alpha, best_similarity

    def find_similar_children(self, family_embedding, children_db_path, top_k=3):
        """
        Find the most similar children to the family based on face embeddings
        
        Args:
            family_embedding: Combined family embedding (mixture of mother and father)
            children_db_path: Path to the children's embeddings database
            top_k: Number of top results to return
            
        Returns:
            List of dictionaries containing information about similar children, ordered by similarity
        """
        # Load children data if not already loaded
        if not hasattr(self, '_children_names') or getattr(self, '_children_db_path', None) != children_db_path:
            self._children_names = np.load("children_names.npy", allow_pickle=True) 
            self._children_embs = np.load(children_db_path, mmap_mode='r')
            self._children_db_path = children_db_path

        # Calculate similarity scores using dot product
        similarities = np.dot(self._children_embs, family_embedding)
        print(f"Similarity stats -> min:{similarities.min():.3f} mean:{similarities.mean():.3f} max:{similarities.max():.3f}")

        # Get indices of top-k matches (regardless of threshold)
        top_k = min(top_k, len(similarities))
        top_indices = np.argsort(similarities)[-top_k:][::-1]  # Sort in descending order
        
        # Prepare results
        results = []
        for idx in top_indices:
            sim = float(similarities[idx])
            is_above_threshold = sim >= self.min_similarity_threshold
            
            # Add child's result with all relevant information
            results.append({
                "child_id": int(idx),                    # Child's index
                "child_name": self._children_names[idx],  # Child's image filename
                "similarity": sim,                       # Similarity score (-1 to 1)
                "display_score": int(((sim + 1) / 2) * 100),  # Convert to percentage (0-100%)
                "low_confidence": not is_above_threshold,     # Mark if below confidence threshold
            })
        
        # Print results for debugging/verification
        print(f"Top {len(results)} results found:")
        for i, res in enumerate(results, 1):
            flag = " (low confidence)" if res["low_confidence"] else ""
            print(f"  {i}. {res['child_name']}: {res['display_score']}%{flag}")
            
        return results
        
    def find_similar_children_weighted(self, mother_path, father_path, alpha, children_db_path, top_k=5):
        if not hasattr(self, '_children_names') or getattr(self, '_children_db_path', None) != children_db_path:
            self._children_names = np.load("children_names.npy", allow_pickle=True) 
            self._children_embs = np.load(children_db_path, mmap_mode='r')
            self._children_db_path = children_db_path

        m = self.face_processor.get_embedding(mother_path)
        f = self.face_processor.get_embedding(father_path)

        sims = alpha * (self._children_embs @ m) + (1 - alpha) * (self._children_embs @ f)
        print(f"Weighted stats -> min:{sims.min():.3f} mean:{sims.mean():.3f} max:{sims.max():.3f}")

        valid = np.where(sims >= self.min_similarity_threshold)[0]
        if valid.size == 0:
            order = np.argsort(sims)[-min(top_k, sims.size):][::-1]
            return [{"child_id": int(i),
                     "child_name": self._children_names[i],
                     "similarity": float(sims[i]),
                     "display_score": int(((sims[i] + 1)/2)*100),
                 "low_confidence": True} for i in order]

        order_local = np.argsort(sims[valid])[-min(top_k, valid.size):][::-1]
        return [{"child_id": int(valid[j]),
                 "child_name": self._children_names[valid[j]],
                 "similarity": float(sims[valid[j]]),
                 "display_score": int(((float(sims[valid[j]]) + 1)/2)*100),
                 "low_confidence": False} for j in order_local]

    def pick_method(self, mother_path, father_path, alpha, children_db_path, top_k=3):
        # حمّل قاعدة الأطفال مع كاش مثل باقي الدوال
        if not hasattr(self, '_children_embs') or getattr(self, '_children_db_path', None) != children_db_path:
            self._children_embs = np.load(children_db_path, mmap_mode='r')
            self._children_db_path = children_db_path
        E = self._children_embs

        # A) طريقة المتجه الموحّد
        f = self.create_family_embedding(mother_path, father_path, alpha)
        scores_A = E @ f  # cosine
        minA, meanA, maxA = float(scores_A.min()), float(scores_A.mean()), float(scores_A.max())

        # B) الطريقة الموزونة (أم/أب كلٌ على حدة)
        m = self.face_processor.get_embedding(mother_path)
        d = self.face_processor.get_embedding(father_path)
        scores_B = alpha * (E @ m) + (1 - alpha) * (E @ d)
        minB, meanB, maxB = float(scores_B.min()), float(scores_B.mean()), float(scores_B.max())

        # اطبع إحصائيات الطريقتين
        print(f"[Family-Vector] stats -> min:{minA:.3f} mean:{meanA:.3f} max:{maxA:.3f}")
        print(f"[Weighted]      stats -> min:{minB:.3f} mean:{meanB:.3f} max:{maxB:.3f}")

        # اختر الأفضل بناءً على أعلى قيمة قصوى (تقدر تغيّر المعيار لِـ mean مثلاً)
        choice = "weighted" if maxB >= maxA else "family"
        if choice == "weighted":
            print(f"=> Picked: WEIGHTED (higher max: {maxB:.3f} vs {maxA:.3f})")
            chosen_scores = scores_B
        else:
            print(f"=> Picked: FAMILY (higher max: {maxA:.3f} vs {maxB:.3f})")
            chosen_scores = scores_A

        # اطبع Top-K للطريقة المختارة (مع تحويل الكوزاين إلى نسبة %)
        if top_k is not None and top_k > 0:
            k = int(min(top_k, chosen_scores.size))
            order = np.argsort(chosen_scores)[-k:][::-1]
            print(f"Top-{k} by {choice}:")
            for rank, idx in enumerate(order, 1):
                cos = float(chosen_scores[idx])
                display = int(((cos + 1.0) / 2.0) * 100.0)
                print(f"{rank}. child #{int(idx)} -> cos={cos:.3f} ({display}%)")

        return choice, {
            "family":   {"min": minA, "mean": meanA, "max": maxA},
            "weighted": {"min": minB, "mean": meanB, "max": maxB},
        }



def test_system():
    print("Building database...")
    build_database("children_db")
    
    matcher = FamilyMatcher(min_similarity_threshold=0.3)     
    try:
        best_alpha = 0.6
        
        known_child_path = ""
        if os.path.exists(known_child_path):
            print("Found known child image. Optimizing alpha value...")
            best_alpha, best_similarity = matcher.find_best_alpha(
                mother_path="mother2.jpg",
                father_path="father2.jpg",
                child_path=known_child_path
            )
            print(f"Best alpha: {best_alpha:.2f} with similarity: {best_similarity:.2f}")
        else:
            print("No known child image found. Using default alpha=0.6")
            best_alpha = 0.6
        
        family_emb = matcher.create_family_embedding(
            mother_path="mother2.jpg",
            father_path="father2.jpg",
            alpha=best_alpha
        )
        
        print("\nSearching for similar children...")

# خلي الكود يقرّر: family أو weighted
        choice, stats = matcher.pick_method(
            mother_path="mother2.jpg",
            father_path="father2.jpg",
            alpha=best_alpha,
            children_db_path="children_embeddings.npy",
            top_k=3
)

# استدعِ الطريقة المختارة فعلياً وأعرض النتائج النهائية
        if choice == "weighted":
            results = matcher.find_similar_children_weighted(
                mother_path="mother2.jpg",
                father_path="father2.jpg",
                alpha=best_alpha,
                children_db_path="children_embeddings.npy",
                top_k=3
            )
        else:
            family_emb = matcher.create_family_embedding(
                mother_path="mother2.jpg",
                father_path="father2.jpg",
                alpha=best_alpha
            )
            results = matcher.find_similar_children(
                family_embedding=family_emb,
                children_db_path="children_embeddings.npy",
                top_k=3
            )

        print("\nFinal Results (method =", choice, "):")
        print("="*50)
        if not results:
            print("No children found with the minimum similarity threshold")
        else:
            for i, res in enumerate(results, 1):
                flag = " (low confidence)" if res.get("low_confidence", False) else ""
                print(f"{i}. {res['child_name']}: {res['display_score']}%{flag}")

    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    test_system()