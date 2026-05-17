from typing import Any, Dict, List, Tuple

DEFAULT_LANGUAGES: Dict[str, Dict[str, str]] = {
    "cpp": {"label": "C++", "ext": "cpp"},
    "c": {"label": "C", "ext": "c"},
    "python": {"label": "Python", "ext": "py"},
    "go": {"label": "Go", "ext": "go"},
}


def normalize_languages(config_languages: Dict[str, Any]) -> Dict[str, Dict[str, str]]:
    if not config_languages:
        return DEFAULT_LANGUAGES.copy()

    normalized: Dict[str, Dict[str, str]] = {}

    for key, value in config_languages.items():
        label = DEFAULT_LANGUAGES.get(key, {}).get("label", key.capitalize())
        ext = None

        if isinstance(value, dict):
            ext = value.get("ext") or value.get("extension")
            label = value.get("label", label)
        else:
            ext = str(value)

        if not ext:
            continue

        normalized[key] = {
            "label": label,
            "ext": ext.lstrip("."),
        }

    if not normalized:
        return DEFAULT_LANGUAGES.copy()

    return normalized


def get_default_language_key(languages: Dict[str, Dict[str, str]], default_key: str) -> str:
    if default_key in languages:
        return default_key
    return next(iter(languages.keys()))


def get_language_choices(
    languages: Dict[str, Dict[str, str]],
    default_key: str,
) -> Tuple[List[str], Dict[str, str]]:
    choices: List[str] = []
    mapping: Dict[str, str] = {}

    for key, info in languages.items():
        label = f"{info['label']} ({info['ext']})"
        if key == default_key:
            label += " (default)"
        choices.append(label)
        mapping[label] = key

    return choices, mapping


def get_language_by_extension(
    languages: Dict[str, Dict[str, str]],
    extension: str,
) -> str:
    ext = extension.lstrip(".").lower()
    for key, info in languages.items():
        if info["ext"].lower() == ext:
            return key
    return ""


def build_problem_header(
    language_key: str,
    problem_num: str,
    title: str,
    link: str,
    difficulty: str,
    tags_str: str,
    structure: str,
) -> str:
    lines = [
        f"LeetCode Problem {problem_num}: {title}",
        f"Link: {link}",
        f"Difficulty: {difficulty}",
        f"Tags: {tags_str}",
        f"Data Structure: {structure}",
    ]

    if language_key == "python":
        return '"""\n' + "\n".join(lines) + '\n"""\n\n'

    return "/*\n" + "\n".join(lines) + "\n*/\n\n"


def build_problem_template(
    language_key: str,
    problem_num: str,
    title: str,
    link: str,
    difficulty: str,
    tags_str: str,
    structure: str,
) -> str:
    header = build_problem_header(
        language_key,
        problem_num,
        title,
        link,
        difficulty,
        tags_str,
        structure,
    )

    if language_key == "python":
        return (
            header
            + "from typing import List\n\n"
            + "class Solution:\n"
            + "    pass\n\n"
            + "if __name__ == \"__main__\":\n"
            + "    print(\"Test cases go here!\")\n"
        )

    if language_key == "go":
        return (
            header
            + "package main\n\n"
            + "import \"fmt\"\n\n"
            + "func main() {\n"
            + "    fmt.Println(\"Test cases go here!\")\n"
            + "}\n"
        )

    if language_key == "c":
        return (
            header
            + "#include <stdio.h>\n\n"
            + "int main() {\n"
            + "    printf(\"Test cases go here!\\n\");\n"
            + "    return 0;\n"
            + "}\n"
        )

    return (
        header
        + "#include <iostream>\n"
        + "#include <vector>\n"
        + "#include <string>\n\n"
        + "using namespace std;\n\n"
        + "// class Solution {\n"
        + "// public:\n"
        + "//     \n"
        + "// };\n\n"
        + "int main() {\n"
        + "    // Solution sol;\n"
        + "    cout << \"Test cases go here!\" << endl;\n"
        + "    return 0;\n"
        + "}\n"
    )


def build_solution_block(
    language_key: str,
    sol_num: int,
    method: str,
    time: str,
    space: str,
    code: str,
) -> str:
    if language_key == "python":
        return (
            f"\n\n# ================== Solution {sol_num} ==================\n"
            + '"""\n'
            + f"Method: {method}\n"
            + f"Time Complexity: {time}\n"
            + f"Space Complexity: {space}\n"
            + '"""\n\n'
            + code
            + "\n"
        )

    return (
        f"\n\n// ================== Solution {sol_num} ==================\n"
        + "/*\n"
        + f"Method: {method}\n"
        + f"Time Complexity: {time}\n"
        + f"Space Complexity: {space}\n"
        + "*/\n\n"
        + code
        + "\n"
    )
