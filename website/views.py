
from flask import Blueprint, render_template, request, flash, jsonify
import json
from . import db


from flask_login import login_required, current_user

from .auth import login
from .models import Note
# A view is a endpoint in URL that takes us to a webpage
views = Blueprint('views', __name__)

#Main page ('/' page of our website = Home) will run

#now you cannot go to the home page without being logged in
@views.route('/', methods = ['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short!', category = 'error')
        else:
            #add the note to the database
            new_note = Note(data = note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category = 'success')
    return render_template("home.html", user = current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
