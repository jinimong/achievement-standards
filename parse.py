import json
import re
import sys


def run(new_file_name: str):
    with open(new_file_name) as f:
        rows = json.loads(f.read())

    # Parsing Dictonary
    r = {}
    for row in rows:
        school = r.setdefault(row.get("학교급"), {})
        subject_category = row.get("교과")
        subject = row.get("과목")
        school.setdefault(subject_category, {}).setdefault(subject, []).append(
            {
                "id": re.sub(r"\[(.+)\]", r"\1", row.get("성취기준코드")),  # 대괄호 제거
                "chapter": row.get("영역(단원)"),
                "grade": row.get("학년"),
                "title": row.get("성취기준명"),
            }
        )

    # Sorting Id
    for school in r.values():
        for subject_category in school.values():
            for subject in subject_category.values():
                subject.sort(key=lambda x: x["id"])

    # Add extra datas
    r2 = {}
    for school_level, school_detail in r.items():
        subjects = []
        for subject_category, subject_detail in school_detail.items():
            for subject in subject_detail.keys():
                subjects.append(
                    {"subject_category": subject_category, "subject": subject}
                )
        r2["subjects"] = {school_level: subjects}
    r = {**r, **r2}

    # Save
    with open("db.json", "w") as f:
        json.dump(r, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "new.json")
