from fastapi import FastAPI,Depends,HTTPException,Query,Header
from typing import Optional
from sqlalchemy.orm import Session
from database import engine,SessionLocal
import models,schemas
from auth import create_token
from jose import jwt, JWTError
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Simple token verification without OAuth2PasswordBearer
def verify_token_simple(authorization: Optional[str] = Header(None)):
    print(f"DEBUG: Authorization header received: {authorization}")

    if not authorization:
        print("DEBUG: No authorization header")
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        # Remove "Bearer " prefix if present
        token = authorization.replace("Bearer ", "").strip()
        print(f"DEBUG: Token after removing Bearer: {token[:50]}...")

        SECRET_KEY = os.getenv("SECRET_KEY", "mysecret")
        ALGORITHM = os.getenv("ALGORITHM", "HS256")

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"DEBUG: Token decoded successfully: {payload}")
        return payload
    except JWTError as e:
        print(f"DEBUG: JWT Error: {e}")
        raise HTTPException(status_code=401, detail="Invalid Token")
    except Exception as e:
        print(f"DEBUG: Unexpected error: {e}")
        raise HTTPException(status_code=401, detail="Authentication failed")

#Login API
@app.post("/login")
def login():
    return{
        "access_token": create_token({"user":"admin"}),
        "token_type": "bearer"
    }

#Home
@app.get("/")
def home():
    return{
        "message":"Blog API Started"
    }

#Create Blog (Protected)
@app.post("/blogs", response_model=schemas.BlogResponse)
def create_blog(blog:schemas.BlogCreate, db:Session = Depends(get_db), user = Depends(verify_token_simple)):
    new_blog = models.Blog(
        title = blog.title,
        content = blog.content
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog

#Read All Blog
@app.get("/blogs")
def get_blogs(page: int =1,
              limit: int = 5,
              search:str = Query(default=""),
              db: Session = Depends(get_db)):
    query = db.query(models.Blog)
    if search:
        query = query.filter(models.Blog.title.ilike(f"%{search}%"))

    total = query.count()
    start = (page-1)*limit
    blogs = query.offset(start).limit(limit).all()

    return{
        "page": page,
        "limit": limit,
        "total": total,
        "data":blogs
    }

#Read One Blog
@app.get("/blogs/{id}", response_model=schemas.BlogResponse)
def get_blog(id:int,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

#Update Blog API(protected)
@app.put("/blogs/{id}",response_model=schemas.BlogResponse)
def update_blog(id:int,blog:schemas.BlogCreate,db: Session = Depends(get_db), user = Depends(verify_token_simple)):
    existing_blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not existing_blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    existing_blog.title = blog.title
    existing_blog.content = blog.content

    db.commit()

    return existing_blog

#Delete Blog API(Protected)
@app.delete("/blogs/{id}")
def delete_blog(id:int,db: Session = Depends(get_db), user = Depends(verify_token_simple)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=404, detail="Blog not found")

    blog.delete()
    db.commit()

    return{
        "message":"Blog deleted Successfully"
    }