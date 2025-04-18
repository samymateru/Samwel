import uuid
def unique_key():
    uuid_str = str(uuid.uuid4()).split("-")
    key = uuid_str[0] + uuid_str[1]
    return key
