from data.database import query_count, insert_query


def is_member(category_id: int, user_id: int) -> bool:
    query = "SELECT * FROM category_members WHERE category_id = ? AND user_id = ?"

    data = query_count(query, (category_id, user_id))

    return True if data == 1 else False

def can_write(category_id, user_id):
    query = "SELECT * FROM category_members WHERE category_id = ? AND user_id = ? AND write_access = 1"

    data = query_count(query, (category_id, user_id))

    return True if data == 1 else False

def give_access(category_id, user_id):
    query = "INSERT INTO category_members (category_id, user_id, write_access) VALUES (?, ?, 1)"

    data = insert_query(query, (category_id, user_id))

    return True if data else False


# TODO: Pesho
def revoke_access(category_id, user_id): 
    pass

def update_write_access(category_id, user_id, access: bool):
    pass

def view_privileged_users(category_id):
    pass