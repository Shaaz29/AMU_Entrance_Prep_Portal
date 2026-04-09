import os

def process_models():
    path = "prep/models.py"
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    with open(path, "w", encoding="utf-8") as f:
        for line in lines:
            if "concept = models.TextField" in line or "NEW FIELD for deeper concept explanation" in line:
                continue
            f.write(line)
    print("models.py updated")

def process_views():
    path = "prep/views.py"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    target = """    if question.concept:
        points.append(f"Concept: {question.concept}")
    elif question.explanation:"""
    replacement = """    if question.explanation:"""
    
    content = content.replace(target.replace('\n', '\r\n'), replacement.replace('\n', '\r\n'))
    content = content.replace(target, replacement) # Fallback for \n
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("views.py updated")

if __name__ == "__main__":
    process_models()
    process_views()
