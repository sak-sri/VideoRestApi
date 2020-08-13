from flask import Flask,request
from flask_restful import Api,Resource,reqparse,abort,fields,marshal_with
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
api=Api(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)

class VideoModel(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(255),nullable=False)
    views=db.Column(db.Integer,nullable=False)
    likes=db.Column(db.Integer,nullable=False)



video_put_args=reqparse.RequestParser()
video_put_args.add_argument("name",type=str,help="Name of the video",required=True)
video_put_args.add_argument("views",type=int,help="Views of the video",required=True)
video_put_args.add_argument("likes",type=str,help="Likes of the video",required=True)

video_update_args=reqparse.RequestParser()
video_update_args.add_argument("name",type=str,help="Name of the video")
video_update_args.add_argument("views",type=int,help="Views of the video")
video_update_args.add_argument("likes",type=str,help="Likes of the video")

resource_fields={
    'id':fields.Integer,
    'name':fields.String,
    'views':fields.Integer,
    'likes':fields.Integer
}

class Video(Resource):
    @marshal_with(resource_fields)
    def get(self,video_id):
       result=VideoModel.query.filter_by(id=video_id).first()
       if(not result):
           abort(404,message="video doesn't exists")
       return result

    @marshal_with(resource_fields)
    def put(self,video_id):
        args=video_put_args.parse_args()
        result=VideoModel.query.filter_by(id=video_id).first()
        if(result):
            abort(409,message="Video id already exists")
        video=VideoModel(id=video_id,name=args['name'],views=args['views'],likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video,201
    
    @marshal_with(resource_fields)
    def patch(self,video_id):
        args=video_update_args.parse_args()
        result=VideoModel.query.filter_by(id=video_id).first()

        if not result:
            abort(404,message="Video doesn't exist")
        
        if args['name']:
            result.name=args['name']
        if args['views']:
            result.views=args['views']
        if args['likes']:
            result.likes=args['likes']

        db.session.commit()

        return result
    
    @marshal_with(resource_fields)
    def delete(self,video_id):
        result=VideoModel.query.filter_by(id=video_id).first()
        if(not result):
            abort(404,message="Video doesn't exists")
        db.session.delete(result)
        db.session.commit()


api.add_resource(Video,"/Video/<int:video_id>")

