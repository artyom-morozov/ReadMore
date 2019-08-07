from flask import Flask, escape, request

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/about')
def about():
    name = request.args.get("name", "World")
    return "<h1> About Page </h1>"

if __name__ == '__main__':
    app.run(debug=True)