from flask import Flask, render_template, request, url_for, redirect, session
import pymongo
import bcrypt

app = Flask(__name__)
app.secret_key = "testing"
client = pymongo.MongoClient('mongodb+srv://joshuadinham:r3aXI4eNJonNbDsk@cluster0.kjxtcjv.mongodb.net/?retryWrites=true&w=majority')

db = client.get_database('total_records')
records = db.register

@app.route('/', methods=['post', 'get'])
def index():
    message = ""
    
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method =="POST":
        user = request.form.get("fullname")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user_found = records.find_one({"name":user})
        email_found = records.find_one({"email":email})

        if user_found:
            message = "There is already a user by that name"
            return render_template("index.html", message=message)
        if email_found:
            message = "This email is already in use"
            return render_template("index.html", message=message)
        if password1 != password2:
            message = "Passwords do not match!"
            return render_template("index.html", message=message)
        else:
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            user_input = {'name':user, "email":email, 'password':hashed}
            records.insert_one(user_input)

            user_data = records.find_one({"email":email})
            new_email = user_data["email"]
            return render_template('logged_in.html', email=new_email)


    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    message = "Please login to your account"
    if "email" in session:
        return redirect(url_for("logged_in"))
    
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        email_found = records.find_one({"email": email})
        if email_found:
            email_val = email_found["email"]
            password_check = email_found["password"]

            if bcrypt.checkpw(password.encode('utf-8'), password_check):
                session["email"] = email_val
                return redirect(url_for('logged_in', email=email_val))
            else:
                if "email" in session:
                    return redirect(url_for("logged_in"))
                message = "Invalid username or password"
                return render_template('login.html', message = message)
        else:
            message="No accounts associated with this email"
            return render_template("login.html", message=message)
    return render_template("login.html", message=message)

@app.route('/logged_in')
def logged_in():
    if "email" in session:
        email = session["email"]
        return render_template('logged_in.html', email=email)
    else:
        return redirect(url_for("login"))
    
@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("signout.html")
    else:
        render_template("index.html")
if __name__ == "__main__":
    app.run(debug=True)