from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField, 
                     RadioField, SelectField, TextField, 
                     TextAreaField, SubmitField)
from wtforms.validators import DataRequired

# create the app
app = Flask(__name__)
# Set the secret key
app.config['SECRET_KEY'] = 'superkey'

# Default Route
@app.route('/')  # 127.0.0.1:5000
def index():
    return render_template('home.html')  # render the basic template

# Custom Basic Route
@app.route('/info')  # 127.0.0.1:5000/info
def info():
    return "<h1>Puppies are cute!</h1>"

# Dynamic Route: Passaggio parametro semplice (stringa)
@app.route('/puppy/<name>')
def puppy(name):
    puppy_avail_list = ['bob', 'tom', 'timmy']
    return render_template('puppy.html', puppy_name=name, puppy_list=puppy_avail_list)

# Jinja Iterators Route usage
@app.route('/iterators')
def iterthings():
    user_logged_in = True
    puppy_avail_list = ['bob', 'tom', 'timmy', 'molly', 'gnegni']
    return render_template('puppy.html', log_ok=user_logged_in,
                           puppy_iter_list=puppy_avail_list)

# Error route to test debug function of flask
@app.route('/error/<name>')
def puppy_error(name):
    return "<h1>This is a page for (100th letter): {}</h1>".format(name[100])

###############
# Sign in up form routes

# Sign up form to compile
@app.route('/signup')
def signup_form():
    return render_template('signup.html')

# Thank you page after form compiled
@app.route('/thankyou')
def thank_you_easy():
    # grab first name variable from signup html page
    first_name = request.args.get('first')
    last_name = request.args.get('last')

    # save to database

    return render_template('signup_thanks.html', first=first_name, last=last_name)

## Page 404 error
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

################################################
#### ADVANCE FORMS WITH wtforms and flask_wtf
class InfoForm(FlaskForm): #Inherit from FlaskForm
    breed = StringField("What Breed are you?")
    submit = SubmitField("Submit")

# Route for the advance form
@app.route('/advanceform',methods=['GET', 'POST'])
def advance_form():
    breed = False #placeholder iniziale
    form = InfoForm() #Oggetto InfoForm
    
    #Logic of the form
    if form.validate_on_submit(): #if you press: submit, this is what happend
        breed = form.breed.data # get the data
        form.breed.data = '' # reset
    return render_template('advanceform.html', advance_form=form, form_breed=breed)

################################################
#### SUPER ADVANCE FORMS with validators, session, url for, ...
class AdvanceForm(FlaskForm):
    
    breed = StringField("What Breed are you?", validators=[DataRequired()])
    neutered = BooleanField("Puppy have been neutered?")
    mood = RadioField('Please choose your mood:', 
                      choices=[('mood_one','Happy'),('mood_two','Excited'),('mood_three','Sad')])
    food_choice = SelectField(u'Pick your favorite food:', 
                              choices=[('chi','Chicken'),('bf','Beef'),('fish','Fish')])
    # the u before the string is the casting to unicode
    feedback = TextAreaField()
    submit = SubmitField('Submit')
    
@app.route('/complicateform',methods=['GET','POST'])
def super_form():
    #Actions for the complicate form
    form = AdvanceForm()
    
    if form.validate_on_submit(): #if the form is compiled
        session['breed'] = form.breed.data #save form information into session user cookie
        session['neutered'] = form.neutered.data
        session['mood'] = form.mood.data
        session['food'] = form.food_choice.data
        session['feedback'] = form.feedback.data
        form.breed.data = ''
        form.neutered.data = ''
        form.mood.data = ''
        form.food_choice.data = ''
        form.feedback.data = ''
        
        #go to the thankyou template page (thankyou function in python file)
        return redirect(url_for('puppy_form_result')) 
    
    return render_template('superform.html',form=form)

@app.route('/puppy-form-result')
def puppy_form_result():
    return render_template('puppy_form_result.html')

###### Flash Messages Test
#remember to import flash in Flask

class FlashForm(FlaskForm):
    submit = SubmitField('Launch Alert!')

@app.route('/flash', methods=['GET','POST']) #remember to use the methods to define the route
def flash_message():
    flash_form = FlashForm()
    
    #visualize the alert after user pressed the button in the form
    if flash_form.validate_on_submit():
        flash('Alert launched from the User') #flash an alert message to the user
        
        return redirect(url_for('flash_message'))
    
    return render_template('flash.html', form=flash_form)

## Main function (app run)
if __name__ == '__main__':
    app.run(debug=True) #use the debug (you can use the pin in terminal to debug on webpage)
