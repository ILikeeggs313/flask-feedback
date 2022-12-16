from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()
def connect_db(app):
    """Connect the app to the database"""
    db.app = app
    db.init_app(app)

#part 1
class User(db.Model):
    """User model with username, pwd, email, first_name, last_name"""
    __tablename__ = 'users'
    username = db.Column(db.String(20), primary_key = True)
    password = db.Column(db.Text, nullable = False)
    email = db.Column(db.String(50), unique = True)
    first_name = db.Column(db.String(30), nullable = False)
    last_name = db.Column(db.String(30), nullable = False)
    #part 3,4,5
    #register method first
    @classmethod
    def register(cls, username,pwd, email, first_name, last_name):
        """Register user with hashed pwd, return users"""
        hashed = bcrypt.generate_password_hash(pwd)
        #turn bytestring into UTF8 string
        hashed_utf8 = hashed.decode('utf8')
        #return instance of user w/username,pwd, email, etc.
        return cls(username = username, password = hashed_utf8, 
        email = email, first_name = first_name, last_name = last_name)
    #authentication method
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate user exists and password is correct"""
        u = User.query.filter_by(username = username).first()
        if u and bcrypt.check_password_hash(u.password, pwd):
            #return user instance
            return u
        else:
            return False
class Secret(db.Model):
    ___tablename__ = 'secrets'
    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)
    username = db.Column(db.Text, db.ForeignKey('users.username'))

    user = db.relationship('User', backref = "secrets")

