from json import load
import pandas as pd


def jsontocsv(ti):
    meta = load(open("data/meta.json"))
    question_list = []
    for item in meta["items"]:
        if "questionItem" in item:
            question = item["questionItem"]["question"]
            question_id = question["questionId"]
            title = item["title"]
            required = question["required"]
            type = question.get("choiceQuestion", {"type": "SCALE"})["type"]
            question_list.append(
                {
                    "question_id": question_id,
                    "title": title,
                    "required": required,
                    "type": type,
                }
            )
    question_df = pd.DataFrame(question_list)

    reponse_list = load(
        open(ti.xcom_pull(key="response_json_file_path", task_ids="task_1"))
    )["responses"]
