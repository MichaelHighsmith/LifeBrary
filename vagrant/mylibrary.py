from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from library_setup import Base, Genre, Book

engine = create_engine('sqlite:///library.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#return the list of genres (JSON)
@app.route('/genres/JSON')
def genresJSON():
	genres = session.query(Genre).all()
	return jsonify(Genres = [i.serialize for i in genres])

#return a list of books in the genre(JSON)
@app.route('/genres/<int:genre_id>/books/JSON')
def bookListJSON(genre_id):
	genre = session.query(Genre).filter_by(id = genre_id).one()
	books = session.query(Book).filter_by(genre_id = genre_id).all()
	return jsonify(Books = [i.serialize for i in books])

#return a specific book (JSON)
@app.route('/genres/<int:genre_id>/books/<int:book_id>/JSON')
def bookJSON(genre_id, book_id):
	book = session.query(Book).filter_by(id = book_id).one()
	return jsonify(Book = book.serialize)


@app.route('/')
@app.route('/genres/')
def genreMenu():
	allGenres = session.query(Genre).all()
	return render_template('genres.html', genres = allGenres)

@app.route('/genre/new', methods=['GET', 'POST'])
def newGenre():
	if request.method == 'POST':
		newGenre = Genre(name = request.form['name'])
		session.add(newGenre)
		session.commit()
		return redirect(url_for('genreMenu'))
	else:
		return render_template('newgenre.html')


@app.route('/genre/<int:genre_id>/edit', methods=['GET','POST'])
def editGenre(genre_id):
	editedItem = session.query(Genre).filter_by(id = genre_id).one()
	if request.method == 'POST':
		if request.form['name']:
			#if the edittext is filled out, set that as editedItem's name
			editedItem.name = request.form['name']
		session.add(editedItem)
		session.commit()
		return redirect(url_for('genreMenu'))
	else:
		return render_template('editgenre.html', genre_id = genre_id, genre = editedItem)

@app.route('/genre/<int:genre_id>/delete', methods=['GET', 'POST'])
def deleteGenre(genre_id):
	itemToDelete = session.query(Genre).filter_by(id = genre_id).one()
	if request.method == 'POST':
		session.delete(itemToDelete)
		session.commit()
		return redirect(url_for('genreMenu'))
	else:
		return render_template('deletegenre.html', genre_id = genre_id, genre = itemToDelete)

@app.route('/genre/<int:genre_id>/books')
def booksInGenre(genre_id):
	bookGenre= session.query(Genre).filter_by(id = genre_id).one()
	books = session.query(Book).filter_by(genre_id = genre_id)
	return render_template('books.html', genre = bookGenre ,books = books)

@app.route('/genre/<int:genre_id>/books/new', methods=['GET','POST'])
def newBook(genre_id):
	if request.method=='POST':
		newItem = Book(name = request.form['name'], genre_id = genre_id)
		session.add(newItem)
		session.commit()
		return redirect(url_for('booksInGenre', genre_id = genre_id))
	else:
		return render_template('newbook.html', genre_id = genre_id)

@app.route('/genre/<int:genre_id>/books/<int:book_id>/edit', methods=['GET','POST'])
def editBook(genre_id, book_id):
	editedItem = session.query(Book).filter_by(id = book_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
		session.add(editedItem)
		session.commit()
		return redirect(url_for('booksInGenre', genre_id = genre_id))
	else:
		return render_template('editbook.html', genre_id = genre_id, book_id = book_id, book = editedItem)

@app.route('/genre/<int:genre_id>/books/<int:book_id>/delete', methods=['GET','POST'])
def deleteBook(genre_id, book_id):
	bookToDelete = session.query(Book).filter_by(id = book_id).one()
	if request.method == 'POST':
		session.delete(bookToDelete)
		session.commit()
		return redirect(url_for('booksInGenre', genre_id = genre_id))
	else:
		return render_template('deletebook.html', genre_id = genre_id, book_id = book_id, book = bookToDelete)








if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)