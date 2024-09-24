from flask import Flask, request, render_template, redirect, flash, session  
from flask_debugtoolbar import DebugToolbarExtension  
from surveys import satisfaction_survey as survey

RESPONSES_KEY = "responses"

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret_key"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route("/")
def show_survey_start():
    """Show the start page for the survey."""
    return render_template("survey_start.html", survey=survey)

@app.route("/questions/<int:qid>")
def show_questions(qid):
    """Show the current question."""
    responses = session.get(RESPONSES_KEY)
    
    if responses is None:
        return redirect("/")
    
    if len(responses) != qid:
        flash("You're trying to access an invalid question!")
        return redirect(f"/questions/{len(responses)}")
    question = survey.questions[qid]
    return render_template("question.html", question_num=qid, question=question)

@app.route("/answer", methods=["POST"])
def show_answer():
    """Show the user answer and redirect to next question."""
    choice = request.form['answer']
    responses = session.get(RESPONSES_KEY)

    if responses is None:
        return redirect("/")
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if len(responses) >= len(survey.questions):
        return redirect("/complete")
    
    return redirect(f"/questions/{len(session[RESPONSES_KEY])}")

@app.route("/complete")
def complete():
    """Survey complete. Show the thank you page."""
    return render_template("completion.html")

@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear session responses and start the survey."""
    session[RESPONSES_KEY] = []
    return redirect("/questions/0")