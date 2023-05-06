from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash
db = "pie"

class Pie:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.filling = data['filling']
        self.crust = data['crust']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None

    @classmethod
    def get_all(cls):
        query = """
                SELECT * FROM pies
                JOIN users on pies.user_id = users.id;
                """
        results = connectToMySQL(db).query_db(query)
        pies = []
        for row in results:
            this_pie = cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": "",
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            this_pie.creator = user.User(user_data)
            pies.append(this_pie)
        return pies
    
    @classmethod
    def get_by_id(cls,data):
        query = """
                SELECT * FROM pies
                JOIN users on pies.user_id = users.id
                WHERE pies.id = %(id)s;
                """
        result = connectToMySQL(db).query_db(query,data)
        if not result:
            return False

        result = result[0]
        this_pie = cls(result)
        user_data = {
                "id": result['users.id'],
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "email": result['email'],
                "password": "",
                "created_at": result['users.created_at'],
                "updated_at": result['users.updated_at']
        }
        this_pie.creator = user.User(user_data)
        return this_pie

    @classmethod
    def save(cls, data):
        query = """
                INSERT INTO pies (name,filling,crust,user_id)
                VALUES (%(name)s,%(filling)s,%(crust)s,%(user_id)s);
                """
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def update(cls, data):
        query = """
                UPDATE pies
                SET name=%(name)s,
                filling=%(filling)s,
                crust=%(crust)s
                WHERE id=%(id)s;
                """
        return connectToMySQL(db).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = """
                DELETE FROM pies
                WHERE id = %(id)s;
                """
        return connectToMySQL(db).query_db(query,data)
    
    @staticmethod
    def validate_pie(form_data):
        is_valid = True
        if len(form_data['name']) < 3:
            flash("Name must be at least 3 characters long.", "pieError")
            is_valid = False
        if len(form_data['filling']) < 3:
            flash("Filling must be at least 3 characters long.", "pieError")
            is_valid = False
        if len(form_data['crust']) < 3:
            flash("Crust must be at least 3 characters long.", "pieError")
            is_valid = False
        return is_valid