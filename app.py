from flask import Flask, request, flash, url_for, redirect, render_template, session, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, current_user, logout_user, UserMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students11.sqlite3'
app.config['SECRET_KEY'] = "pefx86764asyuys23424rgwrhz2553462"
#app.config['SERVER_NAME'] = "192.168.0.100:5000"

db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(db.Model):
   __tablename__ = "user"
   id = db.Column('user_id', db.Integer, primary_key = True)
   username = db.Column(db.String(100),unique=True)
   password = db.Column(db.String(100))

   def __init__(self,username,password):
      self.username = username
      self.password = password

   def is_active(self):
     """True, as all users are active."""
     return True

   def get_id(self):
     """Return the id to satisfy Flask-Login's requirements."""
     return self.username

   def is_authenticated(self):
     """Return True if the user is authenticated."""
     return True

   def is_anonymous(self):
     """False, as anonymous users aren't supported."""
     return False


@login_manager.user_loader
def load_user(user_id):
    """Given *user_id*, return the associated User object."""    
    return User.query.filter_by(username=user_id).first()




class students(db.Model):
      id = db.Column('student_id', db.Integer, primary_key = True)
      name = db.Column(db.String(100))
      roll_no = db.Column(db.Integer)
      studentid = db.Column(db.String(50), unique=True)
      attendance = db.Column(db.Integer)

      def __init__(self, name, roll_no,studentid,attendance):
         self.name = name
         self.roll_no = roll_no
         self.studentid = studentid
         self.attendance = attendance 



@app.route('/register' , methods=['GET','POST'])
def register():
    #if request.method == 'GET':
    #   return render_template('register.html')
    #user = User(request.form['username'] , request.form['password'],request.form['email'])
    user = User(username='admin' , password='123it')
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('login'))



@app.route('/', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':      
        username = request.form['username']
        password = request.form['password']
        registered_user = User.query.filter_by(username=username,password=password).first()
        if registered_user is None:
            flash('Username or Password is invalid' , 'error')
        else:            
            login_user(registered_user,remember=True)
            flash('Logged in successfully')
            return redirect(request.args.get('next') or url_for('main'))
    return render_template('login.html')

@app.route("/logout", methods=["GET","POST"])
@login_required
def logout():
    """Logout the current user."""
    logout_user()
    return redirect(url_for('login'))


@app.route('/main',methods = ['GET', 'POST'])
@login_required
def main():
   return render_template('main.html',studentsall = students.query.order_by('roll_no').all())
   

@app.route('/insert',methods = ['GET', 'POST'])
def insert():
   if request.method == 'POST':
      name = request.form['name']
      roll_no = int(request.form['roll_no'])
      studentid = request.form['studentid']
      attendance = round(eval(request.form['attendance'])*100,2)
      query = "INSERT INTO students (name, roll_no, studentid,attendance) VALUES ('{}', '{}', '{}', '{}');".format(name, roll_no, studentid, attendance)
      db.engine.execute(query)
   return redirect(url_for('main'))


@app.route('/update',methods = ['GET', 'POST'])
def update():
   if request.method == 'POST':
      old_studentid = request.form['old_studentid']
      name = request.form['name']
      roll_no = int(request.form['roll_no'])
      studentid = request.form['studentid']
      attendance = round(eval(request.form['attendance'])*100,2)
      query = "UPDATE students SET name = '{}',roll_no = '{}', studentid = '{}', attendance = '{}' WHERE studentid = '{}';".format(name, roll_no, studentid, attendance, old_studentid)
      db.engine.execute(query)
   return redirect(url_for('main'))


@app.route('/delete',methods = ['GET', 'POST'])
def delete():
   if request.method == 'POST':
      studentid = request.form['studentid']
      query = "DELETE FROM students WHERE studentid = '{}';".format(studentid)
      db.engine.execute(query)         
   return redirect(url_for('main'))




if __name__ == '__main__':
   db.create_all()
   #app.run(debug=True,host='192.168.0.100')
   app.run(debug=True)
