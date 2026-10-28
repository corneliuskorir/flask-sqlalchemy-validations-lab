from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def name_validation(self,key,value):
        if not value:
            raise ValueError('Name cannot be an empty value.')
        unique_name = db.session.query(Author.id).filter_by(name=value).first()
        print(unique_name)
        if unique_name is not None:
            raise ValueError('The Author name must be unique')

        return value

    @validates('phone_number')
    def phone_number_validation(self,key,value):
        if len(value) != 10:
            raise ValueError('Phone number must be ten digits.')

        if not value.isdigit():
            raise ValueError('Phone number can only have digits.')

        return value

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  

    @validates('content')
    def content_validation(self,key,value):
        if not len(value) >= 250:
            raise ValueError('Content must be atleast 250 characters long.')

        return value
    
    @validates('summary')
    def summary_validation(self,key,value):
        if not len(value) <= 250:
            raise ValueError('Summary must be atmost 250 characters long.')

        return value
    
    @validates('category')
    def category_validation(self,key,value):
        if not value in ['Fiction','Non-Fiction']:
            raise ValueError('Category must be Fiction or Non-Fiction.')

        return value
    @validates('title')
    def title_validation(self,key,value):
        checks = ["Won't Believe","Secret","Top","Guess"]

        if not any(word in value for word in checks):
            raise ValueError(f'tile must contain atleast one of the following {checks}')

        return value
    
    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
