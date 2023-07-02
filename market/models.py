from market import db
from market import login_manager
from market import app
from market import bcrypt
from flask_login import UserMixin

# Define a user loader function that retrieves a User object from the database
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ''' the User class inherits from both UserMixin and db.Model '''
class User(db.Model, UserMixin):
    __tablename__ = 'userlist'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        # used to check if a plain text password matches a hashed password.
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price

    def can_sell(self, item_obj):
        return item_obj in self.items

    def __repr__(self):
        return f'User {self.id} {self.username} {self.email_address} {self.password_hash}'


class Item(db.Model):
    __tablename__ = 'itemlist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(1024), nullable=False, unique=True)
    owner = db.Column(db.Integer, db.ForeignKey('userlist.id'))

    def __repr__(self):
        return f'<Item {self.id} {self.name} {self.barcode} {self.price} {self.description}>'

    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()

    def sell(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()

with app.app_context():
    db.create_all()