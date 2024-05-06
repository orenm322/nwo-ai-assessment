from database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True)

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email
        }
    
    def __repr__(self):
        return '<User %r>' % self.username
    
class Sector(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def __repr__(self):
        return '<Sector %r>' % self.name
    
class Source(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }
    
    def __repr__(self):
        return '<Source %r>' % self.name
    
class Subcategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }
    
    def __repr__(self):
        return '<Subcategory %r>' % self.name

class UserSubscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    sector_id = db.Column(db.Integer, db.ForeignKey('sector.id'), nullable=False)
    source_id = db.Column(db.Integer, db.ForeignKey('source.id'), nullable=False)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategory.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True)

    def serialize(self, user=None, sector=None, source=None, subcategory=None):
        if not user:
            user = User.query.filter_by(id=self.user_id).filter(User.deleted_at.is_(None)).first()
        if not sector:
            sector = Sector.query.filter_by(id=self.sector_id).filter(Sector.deleted_at.is_(None)).first()
        if not source:
            source = Source.query.filter_by(id=self.source_id).filter(Source.deleted_at.is_(None)).first()
        if not subcategory:
            subcategory = Subcategory.query.filter_by(id=self.subcategory_id).filter(Subcategory.deleted_at.is_(None)).first()
        return {
            'id': self.id,
            'user': user.serialize() if user else None,
            'sector': sector.serialize() if sector else None,
            'source': source.serialize() if source else None,
            'subcategory': subcategory.serialize() if subcategory else None,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        return '<UserSubscription %r>' % self.id