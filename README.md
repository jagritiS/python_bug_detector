#  Python Bug Detector

Detect buggy vs clean Python code snippets using machine learning.

This project includes:
- 🧩 **Dataset** on Kaggle  
- 🤖 **Trained Model** on Hugging Face  
- 📓 **Training Notebook** for reproducibility  

---

## 📊 Dataset
**Kaggle Dataset:**  
👉 [Python Code Snippets for Bug Detection](https://www.kaggle.com/datasets/jagritisrivastava/python-code-snippets-for-bug-detection)

The dataset contains Python functions labeled as:
- `0` → Clean code
- `1` → Buggy code

---

## 🤖 Trained Model
**Hugging Face Model:**  
👉 [jagritiS/python-bug-detector](https://huggingface.co/jagritiS/python-bug-detector)

You can load the model in Python:
```python
import joblib

model = joblib.load("bug_detector_model.pkl")
vectorizer = joblib.load("bug_vectorizer.pkl")

code = "def divide(a,b): return a/b"
X = vectorizer.transform([code])
print(model.predict(X))  # Output: [0] or [1]
```
## 💻 Kaggle Notebook


**Kaggle Notebook:**
👉 Bug Detection Model using Python Code Snippets

The notebook demonstrates:

- Data loading and visualization

- Model training (Logistic Regression)

- Evaluation metrics and confusion matrix

## ⚙️ Tech Stack

- Python

- Scikit-learn

- Pandas

- Matplotlib

- Joblib

## 🪴 Author

Jagriti Srivastava

  [Kaggle](https://www.kaggle.com/jagritisrivastava)
 | [Hugging Face](https://huggingface.co/jagritisrvstv)

⭐ If you like this project, please give it a star and follow my Kaggle profile!


---
