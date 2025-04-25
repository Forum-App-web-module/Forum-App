from data.database import read_query
from data.models import Category, Topic
from fastapi import Response

def get_all():
    sql = '''SELECT id, name, is_private, lock from categories'''
    rows = read_query(sql)

    return [Category.from_query_result(row) for row in rows]

def get_category_by_id(category_id: int):
    sql = '''SELECT id, name, is_private, lock FROM categories WHERE id = ?'''
    rows = read_query(sql, (category_id,))
#    if not rows:                   moved to router
#        return Response(content='{"message":"No category found with this id"}', status_code=404)
    
    return Category.from_query_result(rows[0])

def get_topics_by_category(category_id):
    sql = '''
        SELECT id, title, categories_id, author_id, best_reply_id, lock
        FROM topics
        WHERE categories_id = ?
    '''
    rows = read_query(sql, (category_id,))
#    if not rows:                   moved to router
#        return Response(content='{"message":"No topics found in this category"}', status_code=204)
    
    return [Topic.from_query_result(row) for row in rows]

