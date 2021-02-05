from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
# from flask_sqlalchemy import SQLAlchemy
from newspaper import Article
import nltk
# nltk.download('punkt')

application = Flask(__name__)
api = Api(application)


News_put_args = reqparse.RequestParser()
News_put_args.add_argument("News_url", type = str, help = "News_url needed", required = True)


class Read_news(Resource):
    @application.route('/')
    def index():
        return "<h1>Welcome to our read_news server !!</h1>"

    def put(self, running):
        if running != "running":
            return {"outcome": "method not exist", 'val': running}, 405

        args = News_put_args.parse_args()
        try:
            article = Article(args['News_url'])
            article.download()
            article.parse()
            article.nlp()
            text_out = article.text

            output = {"url": args["News_url"], "text": text_out}

        except:
            output = {"url": args["News_url"], "text": "Error!!!"}
        # print(output)
        resp = jsonify(output)
        resp.status_code = 200
        return resp

        # return output, 200


# registering resources
api.add_resource(Read_news, "/<string:running>")

if __name__ == "__main__":
    # app.run(host='0.0.0.0', port = 3000, debug=True)
    application.debug = True
    application.run()