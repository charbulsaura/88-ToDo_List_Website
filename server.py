# ToDo List Website
"""
Build a to-do list website.
"""
"""
Today, you are going to build a to-do list website. 
This is a right of passage for any developer.

You can choose the type of to-do list you want to build. 
It could be as simple as a website where you can list some items and cross them out. 
Or as complex as a Kanban-style task list like Trello.

Here is a website for inspiration:
https://flask.io/new

Top Secret: Most developer jobs will be interviewed by someone who is a manager. 
The top piece of technology a manager uses is a task-manager like Trello or Jira. 
If you can build a good task-manager, you will definitely impress your future interviewer!
"""

"""Using Flask/SQLAlchemy --- Still learning Nodejs/MongoDB so still not familiar with it
# MULTIPLE To-Do LISTS  --> Returns random routes
-(N) Save Todo List (of different Day/Week/Month)
-(N) Navigate through different Todo Lists - Day/Week/Month View? (Need another database for to-do list dates)

MAIN FEATURES:
0.(Y/but flask problem, will hang if timer is counting)
    --Include countdown timer to end of year to remind users to not procrastinate
        #python count number of days remaining : https://stackoverflow.com/questions/151199/how-to-calculate-number-of-days-between-two-given-dates
    --How to run function in flask route? 
1.(Y) Get the current date/time
2.(Y) Display relevant todo list header & table with buttons to add/remove items (Add entry to list when button clicked?)
3.(Y) Save & load todo (to database for persistence instead of python variables)
4. MAIN FUNCTIONS (CRUD)- No U yet
4.0 -(Y) ADD NEW TASKS/TODO ITEMS
4.1 -(Y) COMPLETED? --- SELECT/DESELECT ALL checkboxes; Mark all as done 
    >>NEED MINOR FIX TO RESTRICT ALREADY CHECKED & HIDDEN ITEMS FROM BEING DESELECTED... NEED A task_hidden VARIABLE
4.2 -(Y); EDIT items? #WANT TO BE ABLE TO EDIT ON SAME PAGE ;(PATCH) ---PROBLEM--- Multiple WTForms on one page/a single route; ADD instead of PATCH current
        #SENDING FLASK FORM TO ANOTHER ROUTE
        https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request
        -- add flask form on current HTML element when edit <a href> clicked; render item as href/urlfor then load flask form in route
4.3 -(Y) DELETE/Clear marked To-do's
    >>ADD A CLEAR BUTTON-REDIRECT TO DELETE ROUTE TO DELETE ITEM FROM DATABASE
4.4 -(Y) HIDE/SHOW marked To-do's >>>Can hide but <div> still there... How to fix? ---> REMOVE CHECKED ITEMS FROM LIST BEFORE SENDING TO HTML
    >> (Y/FIXED) Hide_Task acts as a toggle, dynamic hiding not available
    >> (Y/FIXED- Added SHOW button to reduce confusion) HIDE TASKS SHOULD CHECK FOR REMAINING UNHIDDEN TASKS BEFORE UNHIDING EVERY OTHER TASK
    >> (Y/FIXED- Through task_hidden variable) COMPLETED TASKS SHOULD NOT BE AUTOMATICALLY HIDDEN
        currently unmarked items will instantly vanish when checked instead of waiting for user input to press hide items again
        
ADDITIONAL FEATURES?
-(Y) HIDDEN ITEM STATUSES SHOULDN'T BE AFFECTED BY FAVORITE/CHECK ALL --Need minor fix for favorite
-(Y); Star/Favorite items -- add task_favourite variable
 (Y/N Still cannot set yet); Due Date -- add task_date variable
 (N); GROUP FAVORITE ITEMS AT TOP OF LIST - Troublesome to do with HTML; need JS
 (N); ADD TASK IMPORTANCE LEVEL ; ToDo task set importance level
 (N); Shift items? 
 (N); Change ToDo List name?
 (N); Change color category?
 
-(N) Move marked items to bottom of list? How to REORDER? Marked To-dos have Boolean = 1 aft checkbox marked
    >> (Y) HOW TO USE CHECKMARK TO CHANGE DATABASE VALUE (Boolean)?
    >> (Y) Use for loop- If True; Just hide & don't display on to-do list in index.html; don't have to delete item from database (unless user requests)
    >> (Y) Allow user to toggle whether to show or hide completed items (Boolean=1) 
    >> (N) Flask sortable widget?
"""
"""
ISSUES:
Flask optional parameters/set flask default route without arguments
https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request
-HOW TO LINK UP DIFFERENT TODO DATABASE TO DIFFERENT ROUTES?
-HOW TO RUN FUNCTION WITH WHILE LOOP WITH FLASK RUNNING? ---if while loop running flask doesnt load (flask route hang during function run)
- Flask POST not working when not on "/" route
    Does Flask POST request always go through home "/" route?
-(FIXED) WHY IS EXTERNAL CSS NOT SHOWING??? flask css not working. DARN. NEED STATIC FILE
-(FIXED -Alternative -using bg color of box) How to remove gaps in html box
-(FIXED) HOW TO ADD ITEM TO DATABASE? Currently its a form in html. validate on submit & db.commit

MISC: 
#Spending too much time on design/CSS. Focus on the important features first
-(Y) css footer color not changing
-css gradient patterns
-html change checkbox color
-How to add css labels to WTForm?
-How to push down/fix HTML elements to bottom of page? ('fixed')
https://www.w3schools.com/cssref/pr_pos_bottom.asp#:~:text=If%20position%3A%20absolute%3B%20or%20position,above%2Fbelow%20its%20normal%20position.
 /certain distance from bottom? ('margin'?) but still collides with footer; maybe reduce html size
-How to center HTML elements on page?
-How to tag position of elements to the bottom of another element?
-(Y) WTForm placeholder :https://stackoverflow.com/questions/9749742/wtforms-can-i-add-a-placeholder-attribute-when-i-init-a-field
-(N) Add dynamic font size (shrink todo list font size while keeping todo list height + width constant)
-(N) CHANGE WTForm SUBMIT BUTTON DISPLAY
-(N) WTForm change submit button/field style/design /style WTForm submit field
-(Y) REMOVE WTForm control-label class? (Cant even find on ur css file)
-(Y: FINALLY FIXED!!!) WTForm css formatting/WTForm remove html element/wtform remove label
https://stackoverflow.com/questions/49037015/is-posible-to-render-wtf-form-field-with-out-label
-(Y): Flask form auto-focus

-(N) Flash previous notification message aft user input to inform them of successful action
-(N) HTML BOX TEXT FORMATTING
    - html box prevent text from going out of box / overflowing
    - html box push overflowing text out of box to next line
    - Prevent form element from going out of box - Format text positioning
-(Y) Why is there underline on all your HTML?  (remove <a href> automatic underline)

20220617,1830 
Resolved most basic features; some premium/QOL features remaining
Just need some polishing
20220618 1300
Finishing touches
20220619 0300-0340 YAY FIXED!
Adding EDIT/DATE feature... 
20220619 0340-0748 
Adding more features!!!!
"""
from flask_sqlalchemy import SQLAlchemy

from countdown_timer import Countdown_Timer
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, IntegerField
from wtforms.validators import DataRequired, URL

import datetime
from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///to-do-list.db"
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///to-do-list_additional_features_more.db"

# Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

Hide_Task = False


class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(250), unique=False, nullable=False)
    task_hidden = db.Column(db.Boolean, default=False, nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    task_date = db.Column(db.DateTime, default=(date.today()+datetime.timedelta(days=1)), nullable=False)
    task_favorite = db.Column(db.Boolean, default= False, nullable=False)
    task_edit = db.Column(db.Boolean, default= False, nullable=False)
    task_edit_date = db.Column(db.Boolean, default=False, nullable=False)
    # color = db.Column(db.String(250), default= "#b02046" , unique=False, nullable=False) #Allow color change through editing css property?



db.create_all()


class ToDo_List(FlaskForm):
    task = StringField(validators=[DataRequired()],
                       render_kw={"show":False,"placeholder": "Lock in your wishes...", "autocomplete": "off"})
    submit_new = SubmitField(label='+')

class ToDo_Edit(FlaskForm):
    task = StringField(validators=[DataRequired()],
                       render_kw={"show":False,"placeholder": "Edit Wish...", "autocomplete": "off" ,'autofocus': True})
    # submit_edit = SubmitField(label='Lock changes')
    submit_edit = SubmitField(label='+')

countdown_timer = Countdown_Timer()


# TIME REMAINING TILL TOMORROW
def countdown_till_tmr():
    date_year_end = date(datetime.datetime.now().year, 12, 31)
    countdown_timer.date_line = date_year_end
    countdown_timer.time_left()
    countdown_timer.count_down()


# @app.route("/", methods = ["GET","POST","PATCH"])
# def home():
# #     #ALLOW USERS TO ENTER DATE - To access specific to-do list
#     print("Accessed todo home")
#     to_do_form = ToDo_List()
#     return redirect(url_for('to_do_page')

# Change route to current date to allow for access to different To-Do lists
# Why is adding to database not working if not added on "/" route?
# Flask POST not working when not on "/" route
# Does Flask POST request always go through home "/" route?
# >> WTForm urlfor
# >> Set method= POST in html- https://wtforms.readthedocs.io/en/2.3.x/forms/

@app.route("/", methods=["GET", "POST"])
# @app.route("/today", methods = ["GET","POST"])
def to_do_page():
    global Hide_Task, all_favorited
    countdown_till_tmr()
    current_year = countdown_timer.d_time_curr.year
    # Queries for all tasks in database; then display on index.html
    tasks = db.session.query(ToDo.id, ToDo.task, ToDo.completed, ToDo.task_hidden, ToDo.task_favorite, ToDo.task_date, ToDo.task_edit, ToDo.task_edit_date).all()
    all_tasks_id = db.session.query(ToDo.id).all()
    unmarked_tasks = []
    incomplete_task_count = 0
    # for item in all_tasks_id:
    #     print(f"id of item: {item[0]}")
    # for item in tasks:
    #     print(item)

    # if Hide_Task:
    #     print("when Hide Task clicked; remove all marked & hidden tasks before sending to HTML")

    # ONLY SHOW UNHIDDEN TASKS IN HTML DETERMINED USING task_hidden VARIABLE
    # WHY ARE COMPLETED BUT UNHIDDEN ITEMS NOT SENT FOR DISPLAY??? ... DIDNT REMOVE WRONG CONDITIONAL FROM BEFORE
    # Dont need to check for task.completed anymore bcos its all going to be displayed unless task.hidden
    for task in tasks:
        #Reset task_edit status to False once page refreshed
        # print("Reset task_edit status to False")
        task_edit_status = ToDo.query.get(int(task[0]))
        # print(task_edit_status)
        task_edit_status.task_edit = False
        # print(task_edit_status.task_edit)
        db.session.commit()
        if not task.task_hidden:
            if task.completed==False:
                incomplete_task_count +=1
            unmarked_tasks.append(task)
    tasks = unmarked_tasks
    print(tasks)
    print(f"All tasks favorited: {all_favorited}?")

    # edit_id = request.args.get("id")
    # print(f"edit_id: {edit_id} ")
    # try:
    #     task_to_edit = ToDo.query.get(int(edit_id))
    #     print(f"Task to edit: {task_to_edit} {task_to_edit.task_edit}")
    # except TypeError:
    #     pass


    to_do_form = ToDo_List()
    if to_do_form.validate_on_submit():
        new_to_do = ToDo(
            task=request.form.get("task"),
            completed=False,
        )
        db.session.add(new_to_do)
        db.session.commit()
        print("To-Do added!")
        return redirect(url_for('to_do_page'))

    try:
        to_do_edit_form = request.form()
    except TypeError:
        to_do_edit_form = ToDo_Edit()

    # if to_do_edit_form.validate_on_submit():
    #     task_to_edit.task = request.form.get("task")
    #     task_to_edit.task_edit=True
    #     db.session.commit()
    #     return redirect(url_for('to_do_page'))

    to_do_date_form = ToDo_Date()

    return render_template("todo.html", all_favorited = all_favorited, tasks=tasks, hide_task=Hide_Task, date_form= to_do_date_form, edit_form=to_do_edit_form, form=to_do_form,
                           months=countdown_timer.months,
                           weeks=countdown_timer.weeks, days=countdown_timer.days, hours=countdown_timer.hours,
                           minutes=countdown_timer.minutes,
                           seconds=countdown_timer.seconds_remaining_5, date_time=countdown_timer.d_time_curr_fmtt,
                           current_year=current_year, incomplete_task_count = incomplete_task_count)
    # id=all_tasks_id,


# if task_edit == True; send WTForm to HTML... (another variable required ...)
# EDITING ON SAME PAGE IS SO TROUBLESOME; 2 WTForms on page and only 1 gets sent
# Send to_do_edit_form to to_do_page()
@app.route("/edit_task/<int:id>", methods=["GET", "POST", "PATCH"])
def to_do_edit_task(id):
    print("to_do_edit_task")
    print("--------------------------------------")
    task_to_edit = ToDo.query.get(int(id))
    print(task_to_edit.task)
    to_do_edit_form = ToDo_Edit(
        #Prefill task description when editing
        task= task_to_edit.task,
    )
    if task_to_edit.task_edit== False:
        task_to_edit.task_edit = True
        db.session.commit()
        print(task_to_edit)
        print(task_to_edit.task_edit)
    try:
        task_to_edit = ToDo.query.get(int(id))
        print(f"Task to edit: {task_to_edit} {task_to_edit.task_edit}")
        print(to_do_edit_form)
        print(request.form.get("task"))
    except TypeError:
        pass
    if to_do_edit_form.validate_on_submit():
        task_to_edit.task = request.form.get("task")
        task_to_edit.task_edit=False
        db.session.commit()
    print("--------------------------------------")
    #SENDING FLASK FORM TO ANOTHER ROUTE
    return redirect(url_for('to_do_page',form=to_do_edit_form))


# @app.route("/<int:to-do-id>", methods = ["GET","POST"])
# def to_do_page_specific_date():
#     return render_template("index.html")
all_favorited= False
@app.route("/favorite_task/<int:id>", methods=["GET", "POST", "PATCH"])
def to_do_favorite_task(id):
    print("to_do_favorite_task")
    print("-----------------------------------------------------------------------")
    global all_favorited
    all_tasks = db.session.query(ToDo.id, ToDo.task_favorite).all()
    all_tasks_favorited = []
    if id == 0 and all_favorited == False:
        # FAVORITE ALL UNFAVORITED items
        # SELECT ALL
        for task in all_tasks:
            toggle_favorite_status = ToDo.query.get(int(task[0]))
            if toggle_favorite_status.task_favorite == False and toggle_favorite_status.task_hidden==False:
                toggle_favorite_status.task_favorite = True
                db.session.commit()
            #     print(f"TASK FAVORITE STATUS SET TO TRUE! {toggle_favorite_status}")
        all_favorited = True

    elif id == 0 and all_favorited == True:
        # UNFAVORITE ALL favorited items --but will become a toggle instead;
        # IN DIFFERENT LOOP; CHECK THROUGH ALL ITEMS AGAIN AND SWITCH OFF CHECKMARK AFTER 1ST ROUND OF CHECK?
        for task in all_tasks:
            toggle_favorite_status = ToDo.query.get(int(task[0]))
            #FIXED; WHY IS HIDDEN FLAG IGNORED? (But working for to_do_complete_task ?)
            # print("Is Task Hidden? If so dont change status")
            # print(toggle_favorite_status.task_hidden)
            if toggle_favorite_status.task_favorite == True and toggle_favorite_status.task_hidden==False:
                toggle_favorite_status.task_favorite = False
                # RESTRICT ALREADY CHECKED & HIDDEN ITEMS FROM BEING UNFAVORITED... NEED A task_hidden VARIABLE
                db.session.commit()
                print(f"TASKS FAVORITE STATUS SET TO FALSE! {toggle_favorite_status}")
        all_favorited = False

    if id == 0:
        # print(f"all_favorited: {all_favorited}")
        for task in all_tasks:  # Loops through all tasks and selects all checkboxes
            toggle_favorite_status = ToDo.query.get(int(task[0]))  # gets ToDo id
            # print(f"toggle_favorite_status: {toggle_favorite_status}")

            # If item not hidden,
            # Adds all objects to a list to check if all tasks favorited
            if toggle_favorite_status.task_hidden==False:
                all_tasks_favorited.append(toggle_favorite_status.task_favorite)
        print(f"all_tasks_favorited: {all_tasks_favorited}")

        if False in all_tasks_favorited:
            all_favorited = False
            print(f"all_favorited set to: {all_favorited}")
        else:
            all_favorited = True
            print(f"all_favorited set to: {all_favorited}")

    # FAVORITES/UNFAVORITES INDIVIDUAL ITEMS
    elif int(id)>0:
        toggle_favorite_status = ToDo.query.get(int(id))
        print(toggle_favorite_status)
        if toggle_favorite_status.task_favorite == False:
            toggle_favorite_status.task_favorite = True
            db.session.commit()
            print(f"item{toggle_favorite_status.id} set to favorite: {toggle_favorite_status.task_favorite}")
        else:
            toggle_favorite_status.task_favorite = False
            db.session.commit()

    print("-----------------------------------------------------------------------")
    return redirect(url_for('to_do_page'))


# EDITS TASK'S COMPLETION STATUS
# How to get HTML checkbox value?
# https://stackoverflow.com/questions/36674846/how-can-i-check-if-some-checkboxes-in-html-are-checked
# https://stackoverflow.com/questions/11599666/get-the-value-of-checked-checkbox

# ALTERNATE SOLUTION: JUST UPDATE TEXT DECORATION BASED ON COMPLETION STATUS;
# Dont use checkbox but just use URL and update to completed if clicked; but if clicked again ; toggle off
all_selected = False
@app.route("/complete_task/<int:id>", methods=["GET", "POST", "PATCH"])
def to_do_complete_task(id):
    global all_selected
    all_tasks = db.session.query(ToDo.id, ToDo.task, ToDo.completed).all()
    all_tasks_checked = []
    if id == 0 and all_selected == False:
        for task in all_tasks:  # Loops through all tasks and selects all checkboxes
            print(task)
            toggle_completion_status = ToDo.query.get(int(task[0]))  # gets ToDo id
            # Check if all items already selected & change flag:
            # Adds all objects to a list to check if all tasks checked/unchecked
            all_tasks_checked.append(toggle_completion_status.completed)
            print(all_tasks_checked)

            print(f"toggle_completion_status: {toggle_completion_status}")
            # SELECT ALL
            if toggle_completion_status.completed == False:
                toggle_completion_status.completed = True
                db.session.commit()
                print(f"ALL TASKS COMPLETION STATUS SET TO TRUE! {toggle_completion_status}")

        if False in all_tasks_checked:
            print("SOME ITEMS UNSELECTED!")
            all_selected = False
        else:
            print("ALL ITEMS ALREADY SELECTED BEFORE CLICK")
            all_selected = True

    if id == 0 and all_selected == True:
        # DESELECT ALL checked items --but will become a toggle instead;
        # IN DIFFERENT LOOP; CHECK THROUGH ALL ITEMS AGAIN AND SWITCH OFF CHECKMARK AFTER 1ST ROUND OF CHECK?
        for task in all_tasks:
            toggle_completion_status = ToDo.query.get(int(task[0]))
            if toggle_completion_status.completed == True and toggle_completion_status.task_hidden==False:
                toggle_completion_status.completed = False
                # RESTRICT ALREADY CHECKED & HIDDEN ITEMS FROM BEING DESELECTED... NEED A task_hidden VARIABLE
                db.session.commit()
                print(f"ALL TASKS COMPLETION STATUS SET TO FALSE! {toggle_completion_status}")
        all_selected = False

    # CHECKS/UNCHECKS INDIVIDUAL ITEMS
    elif int(id) > 0:
        toggle_completion_status = ToDo.query.get(int(id))
        print(toggle_completion_status)
        # Only toggles unhidden tasks; but hidden tasks are not affected
        if toggle_completion_status.completed == False and toggle_completion_status.task_hidden == False:
            toggle_completion_status.completed = True
            toggle_completion_status.task_favorite = True

            print("TASK'S COMPLETION STATUS CHANGED!")
            print(toggle_completion_status.completed)
            db.session.commit()
        else:
            toggle_completion_status.completed = False
            toggle_completion_status.task_favorite = False
            print(toggle_completion_status.completed)
            db.session.commit()

    # TRYING TO OBTAIN CHECKBOX VALUE...
    # completed_1 = request.form.get("1")
    # completed_task = ToDo.query.get(1)
    # if completed_1:
    #     completed_task.completed = True
    #     db.session.commit()
    # print(completed_task, completed_task.completed)

    return redirect(url_for('to_do_page'))

class ToDo_Date(FlaskForm):
    # task_date = SelectField(label="Wish Expiry?", validators=[DataRequired()],choices=["1 Day", "2 Days", "3 Days", "4 Days", "5 Days", "6 Days", "1 Week", "2 Weeks", "1 Month"])
    task_date = IntegerField(validators=[DataRequired()],render_kw={"placeholder": "Wish Expiry?...","autocomplete": "off",'autofocus': True})
    submit_edit_date = SubmitField(label='+')

@app.route("/date_task/<int:id>", methods=["GET", "POST", "PATCH"])
def to_do_date(id):
    to_do_date_form = ToDo_Date()
    task_date_edit = ToDo.query.get(int(id))
    choices = ["1 Day", "2 Days", "3 Days", "4 Days", "5 Days", "6 Days", "1 Week", "2 Weeks", "1 Month"]
    days = [1,2,3,4,5,6,7,14,30]
    if task_date_edit.task_edit_date== False:
        task_date_edit.task_edit_date = True
        db.session.commit()
    if to_do_date_form.validate_on_submit():
        for i in range(len(choices)):
            # if request.form.get("task_date") == choices[i]:
            #     task_date_edit.task_date = (date.today() + datetime.timedelta(days=int(days[i])))
            task_date_edit.task_date = (date.today() + datetime.timedelta(days=int(request.form.get("task_date"))))
            task_date_edit.task_edit_date = False
            db.session.commit()
            print(task_date_edit.task_date )
    return redirect(url_for('to_do_page',form=to_do_date_form))

# ADD VARIABLE TO TOGGLE HIDE/SHOW COMPLETED ITEMS
@app.route("/show_task", methods=["GET", "POST","PATCH"])
def to_do_show_task():
    global Hide_Task
    tasks = db.session.query(ToDo.id, ToDo.task, ToDo.completed, ToDo.task_hidden).all()
    if Hide_Task:
        Hide_Task = False
    # WHEN CLICKED, TOGGLE task_hidden STATE OF ALL TASKS IF IT IS COMPLETED.
    if not Hide_Task:
        for task in tasks:
            toggle_hidden_status = ToDo.query.get(int(task[0]))
            print(f"Task hidden? {toggle_hidden_status.task_hidden}")
            toggle_hidden_status.task_hidden = False
            db.session.commit()
        print(tasks)
    return redirect(url_for('to_do_page'))

@app.route("/hide_task", methods=["GET", "POST","PATCH"])
def to_do_hide_task():
    global Hide_Task
    tasks = db.session.query(ToDo.id, ToDo.task, ToDo.completed, ToDo.task_hidden).all()
    hide_click_count = 0
    # -- But still need to determine whether completed item should still be added to HTML? Seems like dont need anymore. HTML element controlled by task_hidden
    # DONT NEED Hide_Task FLAG ANYMORE IN "/" ; USE task_hidden VARIABLE TO CONTROL IF TASK IS SHOWN OR HIDDEN


    #HIDE COMPLETED ITEMS HERE & CHANGE TASK HIDDEN FLAG
    if not Hide_Task:
        # print("Completed Tasks hidden successfully!")
        print("HIDE TASK BUTTON CLICKED! Determining whether completed item should still be displayed ")
        Hide_Task = True

    # WHEN CLICKED, TOGGLE task_hidden STATE OF ALL TASKS IF IT IS COMPLETED.
    if Hide_Task:
        for task in tasks:
            #Don't want to automatically hide completed items.
            # Only hide when hide_click_count = 1 (triggered by what?)
            if task.completed and not task.task_hidden:
                toggle_hidden_status = ToDo.query.get(int(task[0]))
                print(f"Task hidden? {toggle_hidden_status.task_hidden}")
                toggle_hidden_status.task_hidden = True
                db.session.commit()
            # if task.task_hidden:
        print(tasks)


    # completed_tasks = db.session.query(ToDo.id).all()
    # print(f"HIDE completed_tasks : {completed_tasks}")
    # for item_id in completed_tasks:
    #     task_to_hide = ToDo.query.get(item_id[0])
    #     if task_to_hide.completed == True:
    # Re-render to-do tasks display...
    return redirect(url_for('to_do_page'))


# SQLAlchemy delete all entries that fulfill condition
# Task has duplicate names; need to refer to task through unique identifier/ id
@app.route("/delete_task", methods=["GET", "POST", "DELETE"])
def to_do_delete_task():
    completed_tasks = db.session.query(ToDo.id).all()
    print(f"completed_tasks : {completed_tasks}")

    for item_id in completed_tasks:
        task_to_delete = ToDo.query.get(item_id[0])
        # print(task_to_delete.completed)
        if task_to_delete.completed == True and task_to_delete.task_hidden==True:
            db.session.delete(task_to_delete)
            db.session.commit()
    return redirect(url_for('to_do_page'))


if __name__ == "__main__":
    app.run(debug=True)
