from my_app import app

@app.route("/test")
def home():
    return "Flask is running here"

# I don't need app.run() since we're using "python -m flask run" from launch.json
#if __name__ == "__main__":
#    app.run()
