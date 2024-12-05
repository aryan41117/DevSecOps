from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_wtf import CSRFProtect
from models import get_db
import matplotlib.pyplot as plt
import os

views = Blueprint('views', __name__)
VIEWS_HOME = 'views.home'
csrf = CSRFProtect()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    if one:
        return rv[0] if rv else None
    else:
        return rv


@views.route('/', methods=['GET', 'POST'])
@login_required
@csrf.exempt
def home():
    if request.method == 'POST':
        activity = request.form.get('activity')
        try:
            duration = int(request.form.get('duration'))
        except ValueError:
            flash('Duration must be a number!', category='error')
            return redirect(url_for(VIEWS_HOME))

        if len(activity) < 1:
            flash('Activity is too short!', category='error')
        else:
            db = get_db()
            existing_workout = query_db("SELECT * FROM Workout WHERE user_id = ? AND activity = ?",
                                        (current_user.id, activity), one=True)
            if existing_workout:
                flash('This workout already exists!', category='error')
            else:
                db.execute("INSERT INTO Workout (activity, duration, user_id) VALUES (?, ?, ?)",
                           (activity, duration, current_user.id))
                db.commit()
                flash('Workout added!', category='success')

    workouts = query_db("SELECT * FROM Workout WHERE user_id = ?", (current_user.id,))
    goals = query_db("SELECT * FROM Goal WHERE user_id = ?", (current_user.id,))

    return render_template("home.html", user=current_user, workouts=workouts, goals=goals)

@views.route('/delete_workout/<int:id>', methods=['POST'])
@login_required
@csrf.exempt
def delete_workout(id):
    db = get_db()
    db.execute("DELETE FROM Workout WHERE id = ? AND user_id = ?", (id, current_user.id))
    db.commit()
    flash('Workout deleted successfully!', category='success')
    return redirect(url_for(VIEWS_HOME))

@views.route('/set-goal', methods=['POST'])
@login_required
@csrf.exempt
def set_goal():
    description = request.form.get('description')
    try:
        target = int(request.form.get('target'))
    except ValueError:
        flash('Target must be a number!', category='error')
        return redirect(url_for(VIEWS_HOME))

    db = get_db()
    db.execute("INSERT INTO Goal (description, target, user_id) VALUES (?, ?, ?)",
               (description, target, current_user.id))
    db.commit()
    flash('Goal set!', category='success')
    return redirect(url_for(VIEWS_HOME))

@views.route('/delete_goal/<int:id>', methods=['POST'])
@login_required
@csrf.exempt
def delete_goal(id):
    db = get_db()
    db.execute("DELETE FROM Goal WHERE id = ? AND user_id = ?", (id, current_user.id))
    db.commit()
    flash('Goal deleted successfully!', category='success')
    return redirect(url_for(VIEWS_HOME))

@views.route('/generate-report')
@login_required
def generate_report():
    workouts = query_db("SELECT * FROM Workout WHERE user_id = ?", (current_user.id,))
    goals = query_db("SELECT * FROM Goal WHERE user_id = ?", (current_user.id,))

    activities = [workout['activity'] for workout in workouts]
    durations = [workout['duration'] for workout in workouts]

    plt.figure(figsize=(10, 5))
    plt.bar(activities, durations, color='blue')
    plt.xlabel('Activity')
    plt.ylabel('Duration (minutes)')
    plt.title('Workout Report')
    workout_img_path = os.path.join('static', 'workout_report.png')
    plt.savefig(workout_img_path)
    plt.close()

    goal_descriptions = [goal['description'] for goal in goals]
    goal_targets = [goal['target'] for goal in goals]
    goal_durations = [sum([w['duration'] for w in workouts if w['activity'] == goal['description']]) for goal in goals]

    plt.figure(figsize=(10, 5))
    plt.bar(goal_descriptions, goal_targets, color='green', label='Target')
    plt.bar(goal_descriptions, goal_durations, color='orange', label='Progress', alpha=0.7)
    plt.xlabel('Goal')
    plt.ylabel('Minutes')
    plt.title('Goal Progress Report')
    plt.legend()
    goal_img_path = os.path.join('static', 'goal_report.png')
    plt.savefig(goal_img_path)
    plt.close()

    return render_template("report.html", workout_img_path=workout_img_path, goal_img_path=goal_img_path, user=current_user)
