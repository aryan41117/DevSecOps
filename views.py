from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models import Workout, Goal
from __init__ import db
import matplotlib
import matplotlib.pyplot as plt
import os

# Use the Agg backend for matplotlib to avoid tkinter issues
matplotlib.use('Agg')

# Create the blueprint for views
views = Blueprint('views', __name__)

# Defining a constant for the 'views.home' route
VIEWS_HOME = 'views.home'

# Route for the home page where users can add workouts
@views.route('/', methods=['GET', 'POST'])
@login_required  # Ensures that the user is logged in to access this route
def home():
    if request.method == 'POST':  # If the user submits the form to add a workout
        activity = request.form.get('activity')  # Get the activity from the form
        try:
            duration = int(request.form.get('duration'))  # Get the duration and convert to an integer
        except ValueError:
            flash('Duration must be a number!', category='error')
            return redirect(url_for(VIEWS_HOME))

        # Validate that the activity is not too short
        if len(activity) < 1:
            flash('Activity is too short!', category='error')
        else:
            # Check if the same workout already exists for the user to avoid duplication
            existing_workout = Workout.query.filter_by(user_id=current_user.id, activity=activity).first()
            if existing_workout:
                flash('This workout already exists!', category='error')
            else:
                # Create a new workout entry and add it to the database
                new_workout = Workout(activity=activity, duration=duration, user_id=current_user.id)
                db.session.add(new_workout)
                db.session.commit()
                flash('Workout added!', category='success')

    # Query all workouts and goals for the logged-in user
    workouts = Workout.query.filter_by(user_id=current_user.id).all()
    goals = Goal.query.filter_by(user_id=current_user.id).all()

    # Render the home template and pass the user, workouts, and goals
    return render_template("home.html", user=current_user, workouts=workouts, goals=goals)

# Route to delete a workout
@views.route('/delete_workout/<int:id>', methods=['POST'])
@login_required
def delete_workout(id):
    workout = Workout.query.get(id)
    if workout and workout.user_id == current_user.id:
        db.session.delete(workout)
        db.session.commit()
        flash('Workout deleted successfully!', category='success')
    else:
        flash('Workout not found or unauthorized!', category='error')
    return redirect(url_for(VIEWS_HOME))

# Route to set a new goal for the user
@views.route('/set-goal', methods=['POST'])
@login_required  # User must be logged in to set a goal
def set_goal():
    description = request.form.get('description')  # Get the goal description from the form
    try:
        target = int(request.form.get('target'))  # Get the target value and convert it to an integer
    except ValueError:
        flash('Target must be a number!', category='error')
        return redirect(url_for(VIEWS_HOME))

    # Create a new goal and add it to the database
    new_goal = Goal(description=description, target=target, user_id=current_user.id)
    db.session.add(new_goal)
    db.session.commit()

    flash('Goal set!', category='success')
    return redirect(url_for(VIEWS_HOME))  # Redirect back to the home page

# Route to delete a goal
@views.route('/delete_goal/<int:id>', methods=['POST'])
@login_required
def delete_goal(id):
    goal = Goal.query.get(id)
    if goal and goal.user_id == current_user.id:
        db.session.delete(goal)
        db.session.commit()
        flash('Goal deleted successfully!', category='success')
    else:
        flash('Goal not found or unauthorized!', category='error')
    return redirect(url_for(VIEWS_HOME))


@views.route('/generate-report')
@login_required  # Ensure that the user is logged in to access this route
def generate_report():
    # Query all workouts for the current user
    workouts = Workout.query.filter_by(user_id=current_user.id).all()
    goals = Goal.query.filter_by(user_id=current_user.id).all()

    # Extract activities and durations for workout plotting
    activities = [workout.activity for workout in workouts]
    durations = [workout.duration for workout in workouts]

    # Create a bar chart for workouts
    plt.figure(figsize=(10, 5))
    plt.bar(activities, durations, color='blue')
    plt.xlabel('Activity')
    plt.ylabel('Duration (minutes)')
    plt.title('Workout Report')

    # Save the workout chart to a file in the static directory
    workout_img_path = os.path.join('static', 'workout_report.png')
    plt.savefig(workout_img_path)
    plt.close()

    # Extract goal descriptions and targets for goal plotting
    goal_descriptions = [goal.description for goal in goals]
    goal_targets = [goal.target for goal in goals]
    goal_durations = [sum([w.duration for w in workouts if w.activity == goal.description]) for goal in goals]

    # Create a bar chart for goals (Progress vs. Target)
    plt.figure(figsize=(10, 5))
    plt.bar(goal_descriptions, goal_targets, color='green', label='Target')
    plt.bar(goal_descriptions, goal_durations, color='orange', label='Progress', alpha=0.7)
    plt.xlabel('Goal')
    plt.ylabel('Minutes')
    plt.title('Goal Progress Report')
    plt.legend()

    # Save the goal chart to a file in the static directory
    goal_img_path = os.path.join('static', 'goal_report.png')
    plt.savefig(goal_img_path)
    plt.close()

    # Render the report template and pass the paths for both charts
    return render_template("report.html", workout_img_path=workout_img_path, goal_img_path=goal_img_path, user=current_user)
