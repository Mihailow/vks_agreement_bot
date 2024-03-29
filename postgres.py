import json

from postgres_queries import *


async def get_admin(user_id):
    admin = await postgres_select_one("SELECT * FROM admins WHERE user_id = %s AND send_files_bot = true;",
                                      (user_id,))
    return admin


async def get_admins():
    admins = await postgres_select_all("SELECT * FROM admins WHERE send_files_bot = true;",
                                       None)
    ret_admins = {}
    for admin in admins:
        tmp = {"name": admin["name"], "necessary": admin["send_files_bot_necessary"]}
        ret_admins[admin["user_id"]] = tmp
    return ret_admins


async def get_companies():
    return await postgres_select_all("SELECT * FROM companies WHERE status = true ORDER BY name;",
                                     None)


async def get_company(company_id):
    return await postgres_select_one("SELECT * FROM companies WHERE company_id = %s;",
                                     (company_id,))


async def get_objects(company_id):
    return await postgres_select_all("SELECT * FROM objects WHERE status = true and company_id = %s "
                                     "ORDER BY name;",
                                     (company_id,))


async def insert_document(data):
    doc = await postgres_select_one("INSERT INTO documents (user_id, text, document_name, company, object, "
                                    "confirms, comments, status) "
                                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;",
                                    (data["user_id"], data["text"], data["document_name"],
                                     data["company"], data["object"], json.dumps(data["confirms"], ensure_ascii=True),
                                     data["comments"], data["status"]))
    return doc["id"]


async def update_document_file_id(doc_id, file_id):
    await postgres_do_query("UPDATE documents SET file_id = %s WHERE id = %s;",
                            (file_id, doc_id))


async def update_document_message_id(doc_id, messages):
    await postgres_do_query("UPDATE documents SET message_id = %s WHERE id = %s;",
                            (json.dumps(messages, ensure_ascii=True), doc_id))


async def update_document_confirms(doc_id, user_id, confirm):
    document = await get_document(doc_id)
    confirms = document["confirms"]
    confirms[user_id] = confirm
    await postgres_do_query("UPDATE documents SET confirms = %s WHERE id = %s;",
                            (json.dumps(confirms, ensure_ascii=True), doc_id))


async def update_document_comments(doc_id, user_name, comment):
    document = await get_document(doc_id)
    comments = document["comments"]
    comments.append(f"{user_name}: {comment}")
    await postgres_do_query("UPDATE documents SET comments = %s WHERE id = %s;",
                            (comments, doc_id))


async def update_document_status(doc_id, status):
    await postgres_do_query("UPDATE documents SET status = %s WHERE id = %s;",
                            (status, doc_id))


async def get_document(doc_id):
    document = await postgres_select_one("SELECT * FROM documents WHERE id = %s;",
                                         (doc_id,))
    try:
        confirms = {}
        for confirm in document["confirms"]:
            confirms[int(confirm)] = document["confirms"][confirm]
        document["confirms"] = confirms
        if document["message_id"] is not None:
            messages_id = {}
            for message_id in document["message_id"]:
                messages_id[int(message_id)] = document["message_id"][message_id]
            document["message_id"] = messages_id
    except Exception as e:
        pass
    return document
