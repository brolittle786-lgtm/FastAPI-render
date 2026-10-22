from sqlalchemy import Integer,Column,String,Text
from database import base

#blog table 

class Blog(base):
    __tablename__ = "Blog"

    id = Column(Integer,primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)
        





