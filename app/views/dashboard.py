from flask import Blueprint, render_template

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
def dashboard_page():
    return render_template('dashboard/dashboard.html')
