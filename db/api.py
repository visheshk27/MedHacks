from replit import db

db["userInfo"] = {}
db["userReminders"] = {}

#API methods----------------------------------
class apiMethods:
  def checkAccount(self, account, password):
    if account in db["userInfo"] and password in db["userInfo"][account]:
      return True
    else:
      return False

  def storeAccount(self,account, password, name, age, sex, birthday):
    db["userInfo"][account] = [account, password, name, age, sex, birthday]
    db["userReminders"][account] = []

  def fetchAccount(self,account):
    #print(db["userInfo"])
    return db["userInfo"][account]

  def storeReminder(self,account, remindernum, reminder):
    db["userReminders"][account].append([remindernum,reminder])
    

  def fetchReminder(self,account):
    if len(db["userReminders"][account]) > 0:
      return db["userReminders"][account]
    else: 
      #when user has no reminders
      return False


methods = apiMethods()