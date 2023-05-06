from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
mydb = 'pie'

class Vote:
    def __init__(self,data):
        self.id = data['id']
        self.vote = data['vote']
        self.user_id = data['user_id']
        self.pie_id = data['pie_id']

    @classmethod
    def save(cls, data):
        query = '''
        INSERT INTO votes (vote, pie_id, user_id)
        VALUES(%(vote)s, %(pie_id)s, %(user_id)s);
        '''
        return connectToMySQL(mydb).query_db(query, data)
    
    @classmethod
    def get_by_user_id(cls, data):
        query = '''
        SELECT *
        From votes
        JOIN users
        on votes.user_id = %(id)s
        '''
        results = connectToMySQL(mydb).query_db(query, data)
        output = []

        if not results:
            return output
        
        for row in results:
            this_vote = cls(row)
            user_data = {
                'id': row['id'],
                'user_id': row['user_id'],
                'vote': row['vote'],
                'pie_id': row['pie_id']
            }
            this_vote.creator = Vote(user_data)
            output.append(this_vote)
            
        return output[0]

    @classmethod
    def get_all_join_user(cls, data):
        query = '''
        SELECT *
        FROM votes
        JOIN users
        ON votes.user_id = users.id
        WHERE votes.pie_id = %(id)s;'''
        results = connectToMySQL(mydb).query_db(query, data)
        output = []
        for row in results:
            this_vote = cls(row)
            user_data = {
                'id' : row['users.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at']
            }
            this_vote.sender = User(user_data)
            output.append(this_vote)
        return output
    
