from flask import Flask, request, session, render_template, redirect,url_for, flash
from db.api import db, methods

#init flask app
app = Flask(__name__)
#flask session secret key
app.secret_key = "verysecretkey!"




#session functions----------------------------------
def createSession(userInformation):
  session["account"] = userInformation[0]
  session["password"] = userInformation[1]
  session["name"] = userInformation[2]
  session["age"] = userInformation[3]
  session["sex"] = userInformation[4]
  session["birthday"] = userInformation[5]

def clearSession():
  if len(session):
    entries = [x for x in session.keys()]
    for i in entries:
      del session[i]



#flask app routes------------------------------------
@app.route("/")
def home():
  return render_template("index.html")



@app.route("/login",methods=["GET","POST"])
def login():
  if request.method == "POST":
    account = request.form["account"]
    password = request.form["password"]
    if methods.checkAccount(account, password):
      clearSession()
      createSession(methods.fetchAccount(account))
      return redirect(url_for("profile"))
    else:
      return redirect(url_for("login"))
  return render_template("login.html")



@app.route("/signup",methods=["GET","POST"])
def signup():
  if request.method == "POST":
    account = request.form["account"]
    if account in db["userInfo"]:
      return redirect(url_for("signup"))
    else:
      password = request.form["password"]
      name = request.form["name"]
      age = request.form["age"]
      sex = request.form["sex"]
      birthday = request.form["birthday"]
      if account not in db["userInfo"]:
        methods.storeAccount(account, password, name, age, sex, birthday)
        return redirect(url_for("login"))
  return render_template("signup.html")   



@app.route("/logout")
def logout():
  clearSession()
  return render_template("index.html")


@app.route("/reminders",methods = ["GET","POST"])
def reminder():
  if not len(session):
    return redirect(url_for("login"))
  else:
    res = methods.fetchReminder(session["account"])
    if res:
      return render_template("reminders.html",reminders = list(res))
      
      
    else:
      return render_template("reminders.html", reminders = False)
      



@app.route("/profile")
def profile():
  if not len(session):
    return redirect(url_for("login"))
  else:
    userInformation = methods.fetchAccount(session["account"])
    account,_,name,age,sex,birthday = userInformation 
    return render_template("profile.html",account = account,name=name,age=age,sex=sex,birthday=birthday)


@app.route("/contact", methods=["GET","POST"])
def contact():
  return render_template("contact.html")



@app.route("/appointments",methods = ["GET","POST"])
def appointments():
  if not len(session):
    return redirect(url_for("login"))
  if request.method == "POST":
    appReminderTime = request.form["appointmenttime"]
    doctorName = request.form["doctorName"]
    methods.storeReminder(session["account"],doctorName,appReminderTime)
  return render_template("appointments.html")




@app.route("/diagnosis",methods = ["GET","POST"])
def diagnosis():
  if not len(session):
   return redirect(url_for("login"))
  return render_template("diagnosis.html")





if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080",debug=True)

