from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from newspaper import Article
import nltk
nltk.download('punkt')

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
print("line12")
class News_model(db.Model):
    News_id = db.Column(db.Integer, primary_key = True)
    News_url = db.Column(db.String, nullable = False)
    News_out = db.Column(db.String, nullable = False)

    def __repr__(self):
        return f"News(News_id={self.News_id}, News_url={self.News_url}, News_out={self.News_out})" 

db.create_all() # run_once
print("line22")
News_put_args = reqparse.RequestParser()
News_put_args.add_argument("News_url", type = str, help = "News_url needed", required = True)

News_update_args = reqparse.RequestParser()
News_update_args.add_argument("News_out", type = str, help = "News_out needed")
News_update_args.add_argument("News_url", type = str, help = "News_url needed")

resource_fields = {
    "News_id": fields.Integer,
    "News_url": fields.String,
    'News_out': fields.String
}


# app
print("line38")
class HelloWorld2(Resource):
    @app.route('/')
    def index():
        return "<h1>Welcome to our server !!</h1>"

    @marshal_with(resource_fields)
    def get(self, News_id):
        result = News_model.query.filter_by(id = News_id).first()
        if not result:
            abort(404, message = "No such id")
        return result

    @marshal_with(resource_fields)
    def put(self, News_id):
        args = News_put_args.parse_args()
        result = News_model.query.filter_by(News_id = News_id).first()
        if result:
            abort(409, message = "News id existed")
        
        try:
            article = Article(args['News_url'])
            article.download()
            article.parse()
            article.nlp()
            News_out = article.text
        except:
            News_out = "Cannot read link"

        # print("Hoho", args["News_in"])
        News = News_model(News_id = News_id, News_url = args["News_url"],   
                         News_out = News_out)

        # print("haha", News)
        db.session.add(News)
        db.session.commit()
        return News, 201

    @marshal_with(resource_fields)
    def patch(self, News_id):
        args = News_update_args.parse_args()
        result = News_model.query.filter_by(News_id = News_id).first()
        if not result:
            abort(404, message = "No such id, cannot update")
        
        if args["News_url"]:
            result.News_url = args['News_url']
        if args["News_out"]:
            result.News_out = args['News_out']
        # if args['views']:
        #     result.views = args['views']
        # if args['likes']:
        #     result.likes = args['likes']
        db.session.commit()

        return result
        
    def delete(self, News_id):
        abort_if_News_id_not_existed(News_id)
        del Newss[News_id]
        return "Done", 204


print("line101")    
# registering resources
api.add_resource(HelloWorld2, "/<int:News_id>")
print("line104")
# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=3001, debug=True)
#     # app.run(port=5000, debug=True)