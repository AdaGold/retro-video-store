from flask import current_app
from app import db
from datetime import datetime

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    title = db.Column(db.String) # name of movie
    # date/time when video was released - not now
    release_date = db.Column(db.DateTime, nullable=False)
    # default=datetime(0).strftime("%a, %d %b %Y %X %z")
    total_inventory = db.Column(db.Integer, nullable=False)
    available_inventory = db.Column(db.Integer, nullable=False) # set it to false, ok?
    # Video has many Rentals, and a Rental belongs to a Video
    rentals = db.relationship("Rental", backref="video")

    def video_to_json_response(self):
        '''
        Converts a Video instance into JSON format
        Output: Returns a Python dictionary in the shape of JSON response 
        that the API returns in the route that is called (GET route).
        '''
        #  Release date should be this format:  "1979-01-18",("%Y-%m-%d")
        return  {"id": self.id,
                "title": self.title,
                "release_date": self.release_date.strftime("%Y-%m-%d"), 
                "total_inventory": self.total_inventory,
                "available_inventory": self.available_inventory}
                
    @staticmethod
    def from_json_to_video(request_body):
        '''
        Converts JSON request body into a new instance of Customer
        input: Takes in a dictionary in the shape of the JSON the API 
        receives. 
        '''
        # could add an if to check that the request body is good -
        # then create customer
    
        new_video = Video(title=request_body["title"],
                release_date=request_body["release_date"],
                available_inventory = request_body["total_inventory"],
                total_inventory = request_body["total_inventory"])

        return new_video

    ## TASK MODEL --------------------------------------
    # description = db.Column(db.String)
    # completed_at = db.Column(db.DateTime, nullable=True)
    # adding one to many relationship  tasks to goal ==> dog to person 
    # nullable = task might not belong to a goal
    # goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True) 

    # def to_json_response(self):
    #     '''
    #     Converts a Task instance into JSON
    #     Output: Returns a Python dictionary in the shape of JSON response 
    #     that the API returns in the route that is called (GET).
    #     '''
    #     return {"task": 
    #                     {"id": self.id,
    #                     "title": self.title,
    #                     "description": self.description,
    #                     "is_complete": bool(self.completed_at)}
    #             }
                
    # def task_to_json_response(self):
    #     '''
    #     Converts a Task's instance into JSON response
    #     Output: Returns a Python dictionary in the shape JSON response
    #     for only one task.
    #     '''
    #     return {"id": self.id,
    #             "title": self.title,
    #             "description": self.description,
    #             "is_complete": bool(self.completed_at)}

    # def task_to_json_response_w_goal(self):
    #     '''
    #     Converts a Task's instance columns (atributes) into JSON response including
    #     the foreign key goal id.
    #     Output: Returns a Python dictionary in the shape JSON response
    #     for a task that is part of a goal.
    #     '''
    #     json_response_goal = self.task_to_json_response()
    #     json_response_goal["goal_id"] =  self.goal_id
    #     return json_response_goal
                

    # def set_completion(self):   
    #     '''
    #     Updates the attribute completed_at of the instance of a Task
    #     to the current date/time.
    #     '''
    #     complete_time = (datetime.now()).strftime("%c")  
    #     self.completed_at = complete_time 

    # @staticmethod
    # def from_json_to_task(request_body):
    #     '''
    #     Converts JSON into a new instance of Task
    #     input: Takes in a dictionary in the shape of the JSON the API 
    #     receives. 
    #     '''
    #     new_task = Task(title=request_body["title"],
    #             description=request_body["description"],
    #             completed_at = request_body["completed_at"])
    #     return new_task
