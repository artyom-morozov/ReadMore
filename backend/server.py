from flask import Flask, escape, request, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
app = Flask(__name__)
app.config['SECRET_KEY'] = '979f8db96cff32584f2974f7e9b9338b'

books = [
    {
        'author': 'Jack London',
        'title': 'Martin Eden',
        'ISBN': '731324'
    },
    {
        'author': 'Remarque',
        'title': 'All quite',
        'ISBN': '313123'
    }
]

@app.route('/')
@app.route('/home')
def hello():
    return render_template('index.html', books=books)

@app.route('/about')
def about():
    name = request.args.get("name", "World")
    return "<h1> About Page </h1>"


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

if __name__ == '__main__':
    app.run(debug=True)