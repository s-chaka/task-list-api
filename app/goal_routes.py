from app import db
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, request,abort
from app.models.task import Task
from app.task_routes import validate_model


goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return make_response({"details": "Invalid data"},400)
    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()
    
    return {"goal":new_goal.to_dict()},201

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()
    
    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())

    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_model(Goal,goal_id)

    return {"goal":goal.to_dict()},200

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal,goal_id)

    db.session.delete(goal)
    db.session.commit()
    
    return {'details': f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal,goal_id)
    request_body = request.get_json()
    
    goal.title = request_body["title"]
    db.session.commit()
    return{"goal": goal.to_dict()},200


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_tasks_to_goal(goal_id):
    goal = validate_model(Goal,goal_id)
    request_body = request.get_json()
    task_ids= []
    for task_id in request_body["task_ids"]:
        task = validate_model(Task,task_id)
        goal.tasks.append(task)
        task_ids.append(task_id)
    db.session.commit()
    return {"id":goal.goal_id,
            "task_ids":task_ids},200
    
    
@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_task_with_goal_id(goal_id):
    
    goal = validate_model(Goal,goal_id)

    response_body = []
    for task in goal.tasks:
        response_body.append(task.other_dict())
        
    return {"id": goal.goal_id,
            "title": goal.title,
            "tasks": response_body}
