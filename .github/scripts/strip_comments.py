import io
import subprocess
import tokenize
from pathlib import Path

TARGET_DIR = Path("production")


def remove_comments(file_path):
    with open(file_path, encoding="utf-8") as f:
        source_code = f.read()

    result = []
    tokens = tokenize.generate_tokens(io.StringIO(source_code).readline)

    for toknum, tokval, _, _, _ in tokens:
        if toknum != tokenize.COMMENT:
            result.append((toknum, tokval))

    return tokenize.untokenize(result)


def build():
    for py_file in Path(".").rglob("*.py"):
        if "production" in py_file.parts or py_file.name == "strip_comments.py" or ".github" in py_file.parts:
            continue

        clean_code = remove_comments(py_file)

        target_file = TARGET_DIR / py_file
        target_file.parent.mkdir(parents=True, exist_ok=True)

        with open(target_file, "w", encoding="utf-8") as f:
            f.write(clean_code)
        print(f"✅ Nettoyé : {py_file}")

    # 🛠️ Application automatique de Ruff sur le code de production
    print("🧹 Formatage et tri des imports avec Ruff sur le dossier production...")
    subprocess.run(["ruff", "format", "production"], check=False)
    subprocess.run(["ruff", "check", "--fix", "production"], check=False)


if __name__ == "__main__":
    build()
