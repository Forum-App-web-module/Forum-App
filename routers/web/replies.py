# @replies_router.post("/{topic_id}", status_code=201)
# def create_reply(
#         topic_id: int,
#         reply: str = Body(..., min_length=1, max_length=400),
#         token: str = Header()
# ):
#     payload = verify_access_token(token)
#     user_id = payload["key"]["id"]
#     category_id = topic_service.get_category_id(topic_id)

#     if category_service.is_locked(topic_id):
#         return BadRequest(content="This topic is locked")

#     if user_has_access(payload, topic_id, category_id):
#         reply_service.create_reply(reply, topic_id, user_id)
#         return Created(content="Reply created successfully")

#     return BadRequest(content="Access  restricted. Contact an Admin.")