from fastapi import APIRouter, HTTPException, Header, Body
from services import reply_service
from jose import JWTError
from security.jwt_auth import verify_access_token


replies_router = APIRouter(prefix='/replies', tags=['Replies'])

@replies_router.post("/{topic_id}", status_code=201)
def create_reply(
        topic_id: int,
        reply: str = Body(..., min_length=1, max_length=400),
        token: str = Header()
):
    """
    Create a reply under a specific topic.

    This function enables a user to post a reply associated with a particular topic.
    The user must provide valid credentials in the form of a JWT token in the HTTP
    header for authentication. The reply content must conform to the length
    requirements, and once validated, the reply is stored in the database.

    Arguments:\n
        topic_id (int): The ID of the topic where the reply is being posted.\n
        reply (str, optional): The textual content of the reply, constrained to a
            length of 1 to 400 characters.\n
        token (str): A JSON Web Token (JWT) provided in the 'Authorization' header
            to authenticate the user initiating the action.

    Returns:
        dict: A dictionary containing a success message upon successful creation
            of the reply.

    Raises:
        HTTPException: Raised with a 401 status code if the provided token is invalid.
        HTTPException: Raised with a 422 status code if the reply content is invalid.
    """

    # token verification
    payload = verify_access_token(token)

    # DB creator_id extract from token
    user_id = payload["id"]

    # insert reply in the DB
    try:
        reply_service.create_reply(reply, topic_id, user_id)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    return {"message": "Reply created successfully"}

@replies_router.put("/{topic_id}/vote/{reply_id}", status_code=201)
def vote_on_reply(
        topic_id: int,
        reply_id: int,
        vote: str = Body(regex='^(-1|1)$'),
        token: str = Header()
):
    """
    Vote on a specific reply.

    This endpoint allows a user to upvote or downvote a particular reply within a
    specified topic. Authentication is required, and the user's token must be
    provided in the request header. It returns a success message upon a successful
    vote or an error if there are issues with the process.

    Args:\n
        topic_id: int
            The ID of the topic containing the reply to be voted on.\n
        reply_id: int
            The ID of the reply being voted on.\n
        vote: str
            The voting value, which must be either `-1` for a downvote or `1` for
            an upvote. This should match the provided regex pattern '^(-1|1)$'.\n
        token: str
            The user's access token, provided as a header in the request, used for
            authentication.

    Raises:
        HTTPException:
            - If the provided token is invalid, raises an HTTPException with a
              status code of 401.
            - If the voting process fails due to the reply or topic ID not being
              found, raises an HTTPException with a status code of 404.

    Returns:
        dict:
            A JSON response containing a success message indicating that the
            voting process completed successfully.
    """

    # token verification
    payload = verify_access_token(token)


    # TODO:
    # check category is_private; topic lock; category_member can_write

    # DB creator_id extract from token
    user_id = payload["id"]

    try:
        result = reply_service.vote_on_r(topic_id, reply_id, user_id, vote)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    if result:
        return {"message": "Vote was updated. Long live democracy!"}

@replies_router.put("/{topic_id}/top/{reply_id}", status_code=201)
def mark_best_reply(
        topic_id: int,
        reply_id: int,
        token: str = Header()
):
    """
    Marks a specific reply as the best reply for the given topic.

    The endpoint allows a user to mark a reply within a discussion topic as the
    top reply. The user authentication token is required, and the user must
    be authorized to perform this operation.

    Args:\n
        topic_id (int): The ID of the topic in which the reply is posted.\n
        reply_id (int): The ID of the reply being marked as the best one.\n
        token (str, optional): The authentication token for the user, provided
                               in the Header.

    Returns:
        dict: A dictionary containing a success message indicating that the
              reply was successfully designated as the best.

    Raises:
        HTTPException: If the user is unauthorized due to invalid or missing
                       token.
        HTTPException: If the user is not the author of the topic.
    """
    # token verification
    payload = verify_access_token(token)

    # DB creator_id extract from token
    user_id = payload["key"]["id"]

    try:
        result = reply_service.mark_best_reply(topic_id, reply_id, user_id)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    if result:
        return {"message": "Best reply marked successfully"}






