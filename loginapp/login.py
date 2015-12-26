
gin/', methods=["GET","POST"])
def login_page():
    error = ''
    try:
        conn = connection()
        collection=MongoClient()["blog"]["users"]
        if request.method == "POST":
            #collection = MongoClient()["blog"]["users"]

            data = collection.find({"username":(request.form['username'])})
            data1=collection.find({"password":(request.form['password'])})
            #data = c.fetchone()[2]

            if sha256_crypt.verify(request.form.password, data):
                session['logged_in'] = True
                session['username'] = request.form['username']

                flash("You are now logged in")
                return redirect(url_for("dashboard"))

            else:
                error = "Invalid credentials, try again."

       # gc.collect()

        return render_template("login.html", error=error)

					
					
					
	  
	  
	  
