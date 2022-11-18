from fastapi import APIRouter,Path,Response,status, HTTPException, Depends
from app.Request.CreatePost import UserPost
from app.models.posts import Post
from app.database.db import get_db
from app.database.connection import connecting_rule
from sqlalchemy.orm import Session



post_router = APIRouter()

@post_router.get("/sql")
async def text_posts(db: Session = Depends(get_db)) :
      post = db.query(Post).all()
      return {"status":post}

@post_router.get("/post")

async def get_all_post():
    payload = connecting_rule();
    response= payload['cursor'];
    response.execute(""" SELECT * from posts """)
    result=response.fetchall()
    return {"payload": result}

@post_router.post('/post',status_code=status.HTTP_201_CREATED)

async def post(user_post : UserPost) :
    post= connecting_rule();
    cursor=post['cursor']
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)  RETURNING * """,
        (user_post.title, user_post.content, user_post.published)) 
    new_post =cursor.fetchone()
    post['connect'].commit()

    return {"message": new_post}


@post_router.get('/post/{id}')
async def get_single_post(id:int):
   payload= connecting_rule()
   posts=payload['cursor'].execute(""" SELECT * FROM posts WHERE id= %s """, (str(id)))
   response = payload['cursor'].fetchone()
 
   if not response:
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found")
     
   return {"post":response}


# delete 
@post_router.delete('/post/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_single(id:int) -> dict :

    payload = connecting_rule()
    payload['cursor'].execute("""DELETE FROM posts where id= %s returning * """, (str(id),))
    single_post= payload['cursor'].fetchone()
    
    payload['connect'].commit()

    if single_post == None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post not avaliable"
        )
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# update 

@post_router.put('/post/{id}')
async def update_post(id:int, post:UserPost):
    payload = connecting_rule()
    payload['cursor'].execute(""" UPDATE posts SET title = %s, content = %s , published = %s WHERE id= %s RETURNING *""",
        (post.title, post.content, post.published, str(id) ))
    updated_post =payload['cursor'].fetchone()
    payload['connect'].commit()
    

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post id is not found"
        )
   
    return {"data": updated_post}