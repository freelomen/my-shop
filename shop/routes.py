from shop.__init__ import app


@app.route('/')
def home():
    return "Home page of your shop"
