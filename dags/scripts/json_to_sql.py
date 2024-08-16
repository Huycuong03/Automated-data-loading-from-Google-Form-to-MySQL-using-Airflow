from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine

DB_URL = "postgresql+psycopg2://airflow:airflow@postgres/airflow"

def json_to_sql(ti):
    data = ti.xcom_pull(key="json_data", task_ids="task1")
    response_list = data["responses"]
    response_meta_data = []
    response_single_valued_data = []
    response_multi_valued_data = []

    for response in response_list:
        response_meta_data.append(
            get_meta(response)
        )

        response_single_valued_data.append(
            get_single_valued_answers(response)
        )

        response_multi_valued_data.extend(
            get_multi_valued_answers(response)
        )
    
    engine = create_engine(DB_URL)
    pd.DataFrame(response_meta_data).to_sql("response_meta", engine, if_exists="append", index=False)
    pd.DataFrame(response_single_valued_data).to_sql("single_valued_answer", engine, if_exists="append", index=False)
    pd.DataFrame(response_multi_valued_data).to_sql("multi_valued_answer", engine, if_exists="append", index=False)

    return 0

def get_meta(response):
    return {
        "response_id": response['responseId'],
        "create_time": datetime.strptime(response['createTime'], '%Y-%m-%dT%H:%M:%S.%fZ'),
        "last_submitted_time": datetime.strptime(response['lastSubmittedTime'], '%Y-%m-%dT%H:%M:%S.%fZ'),
    }

def get_single_valued_answers(response):
    answer_list = response['answers'].values()
    single_valued_answers = {
        "response_id": response['responseId']
    }
    for answer in answer_list:
        if len(answer['textAnswers']['answers']) == 1:
            answer_value = answer['textAnswers']['answers'][0]
            single_valued_answers[answer['questionId']] = answer_value['value']
    return single_valued_answers

def get_multi_valued_answers(response):
    answer_list = response['answers'].values()
    multi_valued_answers = []
    for answer in answer_list:
        if len(answer['textAnswers']['answers']) > 1:
            for answer_value in answer['textAnswers']['answers']:
                multi_valued_answers.append(
                    {
                        "response_id": response['responseId'],
                        "question_id": answer['questionId'],
                        "answer_value": answer_value['value'] 
                    }
                )
    return multi_valued_answers