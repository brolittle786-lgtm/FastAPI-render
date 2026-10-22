from fastapi import FastAPI, Depends,HTTPException,Query
from sqlalchemy.orm import Session
from database import engine , SessionLocal
import models,schemas
from auth import create_token,verify_token
models.base.metadata.create_all(bind=engine)

app = FastAPI()

# DB Dependency
def get_db():
    db = SessionLocal()
    try :
        yield db
    finally:
        db.close()
        
# login API
@app.post("/login")
def login():
    return{
        "access_token" : create_token({"user":"admin"}),
        "token_type":"bearer"  
    }

# home route
@app.get("/")
def hello():
    return{
        "messsage ":"Fastpai project is runnig fine "
    }
    
    
# create blog  (protected)
@app.post("/blogs", response_model=schemas.BlogResponse)
def create_Fastapi(blog:schemas.BlogCreate, db:Session = Depends(get_db),user = Depends(verify_token)):
    new_blog = models.Blog(
        title = blog.title,
        content = blog.content  
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# read all blog read api 
@app.get("/blogs")
def get_blogs(page:int = 1,
              limit: int = 5,
              search: str = Query(default=""),
              db: Session =  Depends(get_db)):
    query =  db.query(models.Blog)
    if search :
        query =  query.filter(models.Blog.title.ilike(f"%{search}%"))

    total = query.count()
    start = (page-1) * limit
    blogs = query.offset(start).limit(limit).all()

    return {
        "page":page,
        "limit":limit,
        "total": total,
        "data":blogs
            
    }
    
    
#  read each blog based on id 
@app.get("/blogs/{id}",response_model=schemas.BlogResponse)
def get_id(id:int,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
     
    if not blog:
        raise HTTPException(status_code=404, detail="blog not found")
    return blog
    
    
# update api (protected)
@app.put("/blogs/{id}",response_model=schemas.BlogResponse)
def update_api(id : int,blog: schemas.BlogCreate, db : Session =  Depends(get_db),user = Depends(verify_token)):
    existing_blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    
    if not existing_blog:
            raise HTTPException(status_code=404, detail="blog not found")
        
    existing_blog.title =  blog.title
    existing_blog.content = blog.content
    
    db.commit()
    return existing_blog


#  delete api (protected)
@app.delete("/blogs/{id}")
def delete_api(id : int,db : Session = Depends(get_db),user = Depends(verify_token)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    
    if not blog.first():
                raise HTTPException(status_code=404, detail="blog not found")

    blog.delete()
    db.commit()
    return {
        "message":"API blog successfully deleted"
    }