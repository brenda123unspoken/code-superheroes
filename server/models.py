from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


# class Hero(db.Model, SerializerMixin):
#     __tablename__ = 'heroes'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     super_name = db.Column(db.String)

#     # add relationship

#     # add serialization rules

#     def __repr__(self):
#         return f'<Hero {self.id}>'


# class Power(db.Model, SerializerMixin):
#     __tablename__ = 'powers'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     description = db.Column(db.String)

#     # add relationship

#     # add serialization rules

#     # add validation

#     def __repr__(self):
#         return f'<Power {self.id}>'


# class HeroPower(db.Model, SerializerMixin):
#     __tablename__ = 'hero_powers'

#     id = db.Column(db.Integer, primary_key=True)
#     strength = db.Column(db.String, nullable=False)

#     # add relationships

#     # add serialization rules

#     # add validation

#     def __repr__(self):
#         return f'<HeroPower {self.id}>'
class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)

    # Define relationship to HeroPower
    hero_powers = db.relationship('HeroPower', back_populates='hero', cascade='all, delete-orphan')

    # Define relationship to Power through HeroPower
    powers = association_proxy('hero_powers', 'power')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'super_name': self.super_name,
            'hero_powers': [hp.to_dict() for hp in self.hero_powers]
        }

    # Serialization rules
    serialize_rules = ('-hero_powers',)

    def __repr__(self):
        return f'<Hero {self.id}>'

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
    # Define relationship to HeroPower
    hero_powers = db.relationship('HeroPower', back_populates='power', cascade='all, delete-orphan')

    # Define relationship to Hero through HeroPower
    heroes = association_proxy('hero_powers', 'hero')

    # Serialization rules
    serialize_rules = ('-hero_powers',)

    # Validation
    @validates('description')
    def validate_description(self, key, description):
        if not description or len(description) < 20:
            raise ValueError("Description must be at least 20 characters long")
        return description

    def __repr__(self):
        return f'<Power {self.id}>'

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)

    # Define relationships
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    hero = db.relationship('Hero', back_populates='hero_powers')

    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)
    power = db.relationship('Power', back_populates='hero_powers')

    def to_dict(self):
        return {
           'id': self.id,
           'hero_id': self.hero_id,
           'power_id': self.power_id,
           'strength': self.strength,
           'hero': self.hero.to_dict() if self.hero else None,
           'power': self.power.to_dict() if self.power else None
        }
        # Serialization rules
    serialize_rules = ('-hero', '-power',)

    # Validation
    @validates('strength')
    def validate_strength(self, key, strength):
        valid_strengths = ['Strong', 'Weak', 'Average']
        if strength not in valid_strengths:
            raise ValueError(f"Strength must be one of {valid_strengths}")
        return strength

    def __repr__(self):
        return f'<HeroPower {self.id}>'
