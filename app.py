from flask import Flask, render_template, redirect, url_for, request, session
from flask_pymongo import PyMongo
from flask import session
import hashlib
from datetime import datetime


app = Flask(__name__)
app.secret_key = '2006'  # Change this to a random, secure value

# Configure MongoDB
app.config['MONGO_URI'] = 'mongodb://localhost:27017/elderly-care-db'
mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('platform.html')

@app.route('/register', methods=['POST'])
def register():
    try:
        user_data = {
            'username': request.form['username'],
            'email': request.form['email'],
            'password': request.form['password']
        }
        mongo.db.users.insert_one(user_data)
        return render_template('next_page.html')
    except Exception as e:
        print(e)
        return 'Internal Server Error', 500

@app.route('/login', methods=['POST'])
def login():
    try:
        email = request.form['login-email']
        password = request.form['login-password']

        # Check if the user exists in the database
        user = mongo.db.users.find_one({'email': email, 'password': password})

        if user:
            # Set the user as logged in using Flask session
            session['user'] = {
                'username': user['username'],
                'email': user['email']
                # Add any other user information you want to store
            }
            return redirect(url_for('next_page'))
        else:
            # Invalid credentials, redirect back to the login page
            return render_template('platform.html')
    except Exception as e:
        print(e)
        return 'Internal Server Error', 500
        
"""@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.json
        email = data.get('email')
        entered_password = data.get('password')

        # Query the user from MongoDB
        user = users_collection.find_one({'email': email})

        if user:
            # Check the entered password against the stored hashed password
            stored_password = user.get('password', '')
            if verify_password(entered_password, stored_password):
                # Passwords match, set session and login successful
                session['email'] = email
                return redirect(url_for('next_page'))

        # If email or password is incorrect, return an error message
        return jsonify(message='Invalid email or password entered.')

def verify_password(entered_password, stored_password):
    entered_password_hash = hashlib.sha256(entered_password.encode('utf-8')).hexdigest()
    return entered_password_hash == stored_password"""
    
    
def calculate_pension(service_duration, average_salary, contribution_rate, retirement_age, date_of_birth, retirement_type):

    basic_pension = (service_duration * average_salary * contribution_rate) / 100

    # Adjustments based on retirement age and type (hypothetical factors)
    current_year = datetime.now().year
    year_of_birth = int(date_of_birth.split('-')[2])
    age_at_retirement = (current_year - year_of_birth) - retirement_age
    retirement_factor = 0.02 * age_at_retirement  # Hypothetical retirement factor

    # Apply different factors based on retirement type
    if retirement_type == 'normal':
        total_pension = basic_pension + (basic_pension * retirement_factor)
    elif retirement_type == 'voluntary':
        total_pension = basic_pension + (basic_pension * 0.1)  # Hypothetical voluntary retirement factor
    else:
        total_pension = basic_pension  # For other retirement types

    return total_pension

@app.route('/pension_calculator')
def pension_calculator():
    return render_template('pension_calculator.html')

@app.route('/calculate_pension', methods=['POST'])
def calculate_pension_route():
    # Get form data
    service_duration = int(request.form['service_duration'])
    average_salary = int(request.form['average_salary'])
    contribution_rate = float(request.form['contribution_rate'])
    retirement_age = int(request.form['retirement_age'])
    date_of_birth = request.form['date_of_birth']

    retirement_type = request.form['retirement_type']

    # Calculate pension using the algorithm
    total_pension = calculate_pension(service_duration, average_salary, contribution_rate, retirement_age, date_of_birth, retirement_type)

    # Render pension result template with the calculated total_pension
    return render_template('pension_result.html', total_pension=total_pension)
    
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
        
@app.route('/volunteer_hub')
def volunteer_hub():
    return render_template('volunteer_hub.html')

@app.route('/get_involved')
def get_involved():
    return render_template('get_involved.html')

@app.route('/assistance_center')
def assistance_center():
    return render_template('assistance_center.html')
    
@app.route('/explore_services')
def explore_services():
    return render_template('explore_services.html')

@app.route('/community_forum')
def community_forum():
    return render_template('community_forum.html')

@app.route('/join_forum')
def join_forum():
    return render_template('join_forum.html')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/logout')
def logout():
    # Clear the user session
    session.pop('user', None)
    return render_template('logout.html')

@app.route('/help')
def help():
    return render_template('help.html')

"""@app.route('/logout')
def logout():
    # Clear the user session
    session.pop('user', None)
    return redirect(url_for('index'))"""

@app.route('/next_page')
def next_page():
    # Check if the user is logged in
    if 'user' in session:
        return render_template('next_page.html')
    else:
        # Redirect to the login page if the user is not logged in
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)