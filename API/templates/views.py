from flask import request, redirect, render_template

@app.route("/signin", methods=["GET", "POST"])
def sign_up():

    if request.method == "POST":

        req = request.form
        print(req)

        return redirect(request.url)

    return render_template("signin.html")