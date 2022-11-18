from flask import (Flask, Response)
from datetime import datetime
from peewee import *

app = Flask(__name__)

database = PostgresqlDatabase('notes', user='johndoe',
                              password='12345', host='localhost', port=5433)


def Connect():
    print("connecting to Notes database")
    database.connect()
    print("Successfully connected to Notes database")


Connect()


class BaseModel(Model):
    class Meta:
        database = database


class Note(BaseModel):
    title = CharField()
    content = CharField()
    create_date = DateTimeField()


def create_tables():
    with database:
        database.create_tables([Note])


create_tables()


def createNote(noteTitle, noteContent):
    output = "<p>Creating a new Note</p>"
    newNote = Note.create(
        title=noteTitle,
        content=noteContent,
        create_date=datetime.now())
    newNote.save()
    output += "<br/><p>Successfully created new note</p>"
    return output


def viewAllNotes():
    print("Below are all the created Notes:")
    output = "<p>Below are all the created Notes:</p>"
    for currentNote in Note.select():
        output += "<br/><p>" + currentNote.title + ": " + currentNote.content + "</p>"
    return output


def viewSpecificnote(noteTitle):
    query = Note.select().where(Note.title == noteTitle)
    output = ""
    for currentNote in query:
        output += "<p>" + currentNote.title + ": " + currentNote.content + "</p>"
    return output


def deleteSpecificNote(noteTitle):
    noteToBeDeleted = Note.select().where(Note.title == noteTitle)
    for note in noteToBeDeleted:
        note.delete_instance()
    return "<p>Notes have been deleted with that title</p>"


def updateSpecificNote(noteTitle, noteContent):
    noteToBeUpdated = Note.select().where(Note.title == noteTitle)
    for note in noteToBeUpdated:
        note.content = noteContent
        note.save()
    return "<p>Updated Notes with the title: " + noteTitle + "</p>"


@app.route('/create/<noteTitle>/<noteContent>')
def createNewNoteEndpoint(noteTitle, noteContent):
    return createNote(noteTitle, noteContent)


@app.route('/viewAll')
def viewAllNotesEndpoint():
    return viewAllNotes()


@app.route('/view/<noteTitle>')
def viewSpecificNoteEndpoint(noteTitle):
    return viewSpecificnote(noteTitle)


@app.route('/delete/<noteTitle>')
def deleteSpecificNoteEndpoint(noteTitle):
    return deleteSpecificNote(noteTitle)


@app.route('/update/<noteTitle>/<noteContent>')
def updateSpecificNoteEndpoint(noteTitle, noteContent):
    return updateSpecificNote(noteTitle, noteContent)


@app.errorhandler(404)
def not_found(exc):
    return Response('<h3>URL Page Not found</h3>'), 404


@app.route("/")
def start_db():
    return "<p>Welcome to your personalized Notes App!</p><br/><p>To Create a new Note please go to '/create/{noteTitle}/{noteContent}'<br/>To View All notes please go to '/viewAll'<br/>To View a Specific Note please go to '/view/{noteTitle}'<br/>To Delete a Specific Note please go to '/delete/{noteTitle}'<br/>To Update a specific Note please go to '/update/{noteTitle}/{newNoteContent}'</p>"


if "__name__" == "__main__":
    app.run(host='127.0.0.1', port=5000)
