from tensorflow.keras.models import load_model
import numpy as np
import cv2
from paddyrecom import get_solution

# ===============================
# 1️⃣ Load Trained Model
# ===============================
model = load_model("PADDY.h5")

# ===============================
# 2️⃣ Define Class Names
# ⚠ IMPORTANT: Order must match training order
# ===============================
class_names = [
    "bacterial_leaf_blight",
    "bacterial_leaf_streak",
    "bacterial_panicle_blight",
    "blast",
    "brown_spot",
    "dead_heart",
    "downy_mildew",
    "hispa",
    "normal",
    "tungro"
]

# ===============================
# 3️⃣ Read Test Image
# ===============================
image_path = "test.jpg"   # Make sure test.jpg exists
img = cv2.imread(image_path)

if img is None:
    print("❌ Image not found. Check file name.")
    exit()

# ===============================
# 4️⃣ Preprocess Image
# ===============================
img = cv2.resize(img, (224, 224))
img = img / 255.0
img = np.reshape(img, (1, 224, 224, 3))

# ===============================
# 5️⃣ Predict Disease
# ===============================
prediction = model.predict(img)
predicted_index = np.argmax(prediction)
predicted_class = class_names[predicted_index]

print("\n✅ Predicted Disease:", predicted_class)

# ===============================
# 6️⃣ Get Recommendation
# ===============================
solution = get_solution(predicted_class)

print("\n🌱 --- Recommendation ---")

if "error" in solution:
    print(solution["error"])
else:
    print("Organic Fertilizer :", solution["organic_fertilizer"])
    print("Bio Pesticide      :", solution["bio_pesticide"])
    print("Dosage             :", solution["dosage"])
    print("Crop Rotation      :", solution["crop_rotation"])
    print("Prevention         :", solution["prevention"])