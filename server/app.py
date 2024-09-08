# #!/usr/bin/env python3

# from flask import Flask, request, make_response, jsonify
# from flask_migrate import Migrate
# from flask_restful import Api, Resource
# from models import db, Hero, Power, HeroPower
# from sqlalchemy.exc import IntegrityError
# import os
# import logging
# from logging import FileHandler

# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# DATABASE = os.environ.get(
#     "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.json.compact = False


# api = Api(app)
# migrate = Migrate(app, db)

# db.init_app(app)
# # Set up logging
# if not app.debug:
#     file_handler = FileHandler('errorlog.txt')
#     file_handler.setLevel(logging.ERROR)
#     app.logger.addHandler(file_handler)

# class HeroListResource(Resource):
#     def get(self):
#         try:
#             heroes = Hero.query.all()
#             return [hero.to_dict() for hero in heroes], 200
#         except Exception as e:
#             app.logger.error(f"Error retrieving heroes: {e}")    
#             return {'error': str(e)}, 500
# class HeroResource(Resource):
#     def get(self, id):
#            hero = Hero.query.get(id)
#            if hero:
#               return hero.to_dict(), 200
#            return {'error': 'Hero not found'}, 404
#         except Exception as e:
#            app.logger.error(f"Error retrieving hero with id {id}: {e}")
#            return {'error': 'An error occurred while retrieving the hero'}, 500

    

# class PowerListResource(Resource):
#     def get(self):
#            powers = Power.query.all()
#            return [power.to_dict() for power in powers], 200
#         except Exception as e:
#            app.logger.error(f"Error retrieving powers: {e}")
#            return {'error': 'An error occurred while retrieving powers'}, 500

# class PowerResource(Resource):
#     def get(self, id):
#            power = Power.query.get(id)
#            if power:
#                return power.to_dict(), 200
#         return {'error': 'Power not found'}, 404
#         except Exception as e:
#             app.logger.error(f"Error retrieving power with id {id}: {e}")
#             return {'error': 'An error occurred while retrieving the power'}, 500

#     def patch(self, id):
#         power = Power.query.get(id)
#         if not power:
#             return {'error': 'Power not found'}, 404

#         data = request.get_json()
#         description = data.get('description')
#         if description is none:
#             return {'errors': ['description is required']}, 400
#         if not isinstance(description, str) or len(description) < 20:
#             return {'errors': ['description must be at least 20 characters long']}, 400
            
#             try:
#                 power.description = description
#                 db.session.commit()
#                 return power.to_dict(), 200
#             return {'errors': ['Description is required']}, 400
#         except Exception as e:
#             app.logger.error(f"Error updating power with id {id}: {e}")
#             return {'error': 'An error occurred while updating the power'}, 500

               
# class HeroPowerResource(Resource):
#     def post(self):
#         data = request.get_json()
#         hero_id = data.get('hero_id')
#         power_id = data.get('power_id')
#         strength = data.get('strength')

#         if not hero_id or not power_id or not strength:
#             return {'errors': ['hero_id, power_id, and strength are required']}, 400
        
#         if strength not in ['Strong', 'Weak', 'Average']:
#              return {'errors': ['Strength must be one of: Strong, Weak, Average']}, 400

#         try:
#             hero = Hero.query.get(hero_id)
#             power = Power.query.get(power_id)
#             if not hero or not power:
#                 return {'errors': ['Hero or Power not found']}, 404

#             hero_power = HeroPower(hero_id=hero_id, power_id=power_id, strength=strength)
#             db.session.add(hero_power)
#             db.session.commit()
            
#             return hero_power.to_dict(), 201
#         except Exception as e:
#             app.logger.error(f"Error creating hero_power: {e}")
#             return {'errors': [str(e)]}, 500
#         except IntegrityError:
#             db.session.rollback()
#             return {'errors': ['Invalid hero_id or power_id']}, 400

# api.add_resource(HeroListResource, '/heroes')
# api.add_resource(HeroResource, '/heroes/<int:id>')
# api.add_resource(PowerListResource, '/powers')
# api.add_resource(PowerResource, '/powers/<int:id>')
# api.add_resource(HeroPowerResource, '/hero_powers')
  
    

# @app.route('/')
# def index():
#     return '<h1>Code challenge</h1>'


# if __name__ == '__main__':
#     app.run(port=5555, debug=True)
#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower
from sqlalchemy.exc import IntegrityError
import os
import logging
from logging import FileHandler

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

api = Api(app)
migrate = Migrate(app, db)

db.init_app(app)

# Set up logging
if not app.debug:
    file_handler = FileHandler('errorlog.txt')
    file_handler.setLevel(logging.ERROR)
    app.logger.addHandler(file_handler)

class HeroListResource(Resource):
    def get(self):
        try:
            heroes = Hero.query.all()
            return [hero.to_dict() for hero in heroes], 200
        except Exception as e:
            app.logger.error(f"Error retrieving heroes: {e}")    
            return {'error': str(e)}, 500

class HeroResource(Resource):
    def get(self, id):
        try:
            hero = Hero.query.get(id)
            if hero:
                return hero.to_dict(), 200
            return {'error': 'Hero not found'}, 404
        except Exception as e:
            app.logger.error(f"Error retrieving hero with id {id}: {e}")
            return {'error': 'An error occurred while retrieving the hero'}, 500

class PowerListResource(Resource):
    def get(self):
        try:
            powers = Power.query.all()
            return [power.to_dict() for power in powers], 200
        except Exception as e:
            app.logger.error(f"Error retrieving powers: {e}")
            return {'error': 'An error occurred while retrieving powers'}, 500

class PowerResource(Resource):
    def get(self, id):
        try:
            power = Power.query.get(id)
            if power:
                return power.to_dict(), 200
            return {'error': 'Power not found'}, 404
        except Exception as e:
            app.logger.error(f"Error retrieving power with id {id}: {e}")
            return {'error': 'An error occurred while retrieving the power'}, 500

    def patch(self, id):
        try:
            power = Power.query.get(id)
            if not power:
                return {'error': 'Power not found'}, 404

            data = request.get_json()
            description = data.get('description')
            if description is None:
                return {'errors': ['description is required']}, 400
            if not isinstance(description, str) or len(description) < 20:
                return {'errors': ['description must be at least 20 characters long']}, 400

            power.description = description
            db.session.commit()
            return power.to_dict(), 200
        except Exception as e:
            app.logger.error(f"Error updating power with id {id}: {e}")
            return {'error': 'An error occurred while updating the power'}, 500

class HeroPowerResource(Resource):
    def post(self):
        data = request.get_json()
        hero_id = data.get('hero_id')
        power_id = data.get('power_id')
        strength = data.get('strength')

        if not hero_id or not power_id or not strength:
            return {'errors': ['hero_id, power_id, and strength are required']}, 400
        
        if strength not in ['Strong', 'Weak', 'Average']:
            return {'errors': ['Strength must be one of: Strong, Weak, Average']}, 400

        try:
            hero = Hero.query.get(hero_id)
            power = Power.query.get(power_id)
            if not hero or not power:
                return {'errors': ['Hero or Power not found']}, 404

            hero_power = HeroPower(hero_id=hero_id, power_id=power_id, strength=strength)
            db.session.add(hero_power)
            db.session.commit()
            
            return hero_power.to_dict(), 201
        except IntegrityError:
            db.session.rollback()
            return {'errors': ['Invalid hero_id or power_id']}, 400
        except Exception as e:
            app.logger.error(f"Error creating hero_power: {e}")
            return {'errors': [str(e)]}, 500

api.add_resource(HeroListResource, '/heroes')
api.add_resource(HeroResource, '/heroes/<int:id>')
api.add_resource(PowerListResource, '/powers')
api.add_resource(PowerResource, '/powers/<int:id>')
api.add_resource(HeroPowerResource, '/hero_powers')

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

if __name__ == '__main__':
    app.run(port=5555, debug=True)
