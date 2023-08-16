def profiler(query_result):
    result = {}
    for row in query_result:
        value = {}
        value["username"] = row.username
        value["email_id"] = row.email_id
        value["mobile_no"] = row.mobile_no
        value["first_name"] = row.first_name
        value["last_name"] = row.last_name
        value["avatar_url"] = row.avatar_url
        value["jid"] = row.jid
        result[row.jid] = value
    return result

def file_profiler(query_result):
    result = []
    for row in query_result:
        value = {}
        value["id"] = row.id
        value["type"] = row.type
        value["url"] = row.url
        value["ext"] = row.ext
        value["uploaded_at"] = row.uploaded_at
        result.append(value)
    return result