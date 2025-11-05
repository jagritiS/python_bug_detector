import os
import ast
import json
import subprocess
import random
import csv

repos = [
    "https://github.com/jagritiS/pythonProgramming",
    "https://github.com/jagritiS/all-captcha",
    "https://github.com/jagritiS/AIMLN-Projects",
    "https://github.com/jagritiS/mini-python-projects",
    "https://github.com/jagritiS/django_auth_package",
    "https://github.com/jagritiS/python_package_cleaner",
    "https://github.com/jagritiS/NamedEntityRecognitionExamples"
]

# --- Clone repo ---
def clone_repo(repo_url, base_dir="repos"):
    os.makedirs(base_dir, exist_ok=True)
    repo_name = repo_url.split("/")[-1]
    repo_path = os.path.join(base_dir, repo_name)
    if not os.path.exists(repo_path):
        print(f"⬇️ Cloning {repo_name}...")
        subprocess.run(["git", "clone", "--depth", "1", repo_url, repo_path])
    else:
        print(f"✅ Repo already exists: {repo_name}")
    return repo_path

# --- Extract function/class snippets ---
def extract_snippets_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()
    snippets = []
    try:
        tree = ast.parse(code)
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                snippet = ast.get_source_segment(code, node)
                snippets.append(snippet)
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
    return snippets

# --- Label snippet ---
def label_snippet(snippet):
    try:
        exec(snippet, {})
        return 0  # clean
    except Exception:
        return 1  # buggy

# --- Realistic Bug Transformations ---
def bug_name_error(snippet):
    # rename a variable that exists in snippet
    words = snippet.split()
    for w in words:
        if w.isidentifier() and w not in ["def", "return", "class"]:
            return snippet.replace(w, w + "_bug", 1)
    return snippet

def bug_type_error(snippet):
    # introduce type conflict: add str to int
    if "return" in snippet:
        return snippet.replace("return", "return str('bug') + ", 1)
    return snippet + "\nreturn 'bug' + 1"

def bug_index_error(snippet):
    # access index 100 in lists (common error)
    if "[" in snippet:
        return snippet.replace("[", "[100", 1)
    return snippet + "\nlst = [1,2]\nprint(lst[100])"

def bug_zero_division(snippet):
    if "/" in snippet:
        return snippet.replace("/", "/0", 1)
    return snippet + "\nreturn 1/0"

def bug_attribute_error(snippet):
    # call a method on int
    return snippet + "\n5.append(3)"

BUG_TRANSFORMS = [bug_name_error, bug_type_error, bug_index_error, bug_zero_division, bug_attribute_error]

# --- Process repo ---
def find_code_snippet(repo_url):
    repo_dir = clone_repo(repo_url)
    data = []

    for root, _, files in os.walk(repo_dir):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                snippets = extract_snippets_from_file(file_path)
                for snip in snippets:
                    # Clean snippet
                    label = label_snippet(snip)
                    data.append({
                        "snippet": snip,
                        "label": label
                    })

                    # Auto-generate buggy variant if clean
                    if label == 0:
                        buggy_snip = random.choice(BUG_TRANSFORMS)(snip)
                        data.append({
                            "snippet": buggy_snip,
                            "label": 1
                        })
    return data

# --- Convert JSON dataset to CSV for Kaggle ---
def save_json_to_csv(json_file, csv_file):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Shuffle data
    random.shuffle(data)

    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # Write header
        writer.writerow(["id", "snippet", "label"])
        # Write data with unique IDs
        for idx, item in enumerate(data, start=1):
            writer.writerow([idx, item["snippet"].replace("\n", "\\n"), item["label"]])

    print(f"✅ Kaggle-ready CSV saved to {csv_file}")


# --- Run for all repos ---
if __name__ == "__main__":
    all_data = []
    json_file = "dataset_realistic_bug.json"
    for repo in repos:
        all_data.extend(find_code_snippet(repo))

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=4)

    print(f"✅ Total snippets collected: {len(all_data)}")
    # --- Save CSV for Kaggle ---
    save_json_to_csv(json_file, "dataset_realistic_bug.csv")
