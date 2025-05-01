from datetime import datetime
from data.models import MessageOut
from data import database


def create(sender_id: int, receiver_id: int, text: str, insert_data_func = None):

    if insert_data_func is None:
        insert_data_func = database.insert_query

    message = insert_data_func('INSERT INTO messages (text, sender_id, receiver_id) VALUES (?,?,?)', (text, sender_id, receiver_id))
    return message

def list_messages(con_partner_1: int, con_partner_2: int, get_data_func = None):

    if get_data_func is None:
        get_data_func = database.read_query

    messages_data = get_data_func('''SELECT m.id, m.text, m.sent_on, sender.username, receiver.username
                                FROM messages as m 
                               JOIN users as sender ON sender.id = m.sender_id 
                               JOIN users as receiver ON receiver.id = m.receiver_id 
                               WHERE sender_id = ? AND receiver_id = ?''', (con_partner_1, con_partner_2))


    return [MessageOut.from_query_result(*row) for row in messages_data]

def list_conversations(user_id: int, get_data_func = None):

    if get_data_func is None:
        get_data_func = database.read_query

    conversations_data = get_data_func('SELECT DISTINCT users.username ' \
                                    ' FROM users' \
                                    ' JOIN (SELECT sender_id as con_partner FROM messages WHERE receiver_id = ? UNION SELECT receiver_id FROM messages WHERE sender_id = ?) as un' \
                                    ' on users.id = un.con_partner', (user_id, user_id))

    return [(row[0]) for row in conversations_data]