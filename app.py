from flask import Flask, render_template, request, redirect, jsonify, flash, url_for
from flask_mysqldb import MySQL
import pymysql
import os
from config import Config

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)

@app.route('/')
def index():
    with mysql.connection.cursor() as cursor:
        cursor.execute("SELECT * FROM blog_posts ORDER BY date DESC LIMIT 5")
        blog_posts_data = cursor.fetchall()
    return render_template('index.html', blog_posts=blog_posts_data)

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/products')
def products():
    with mysql.connection.cursor() as cursor:
        cursor.execute('SELECT * FROM products') 
        products_data = cursor.fetchall()
    return render_template('products.html', products=products_data)

@app.route('/industries')
def industries():
    with mysql.connection.cursor() as cursor:
        cursor.execute("SELECT * FROM industries")
        industries_data = cursor.fetchall()
    return render_template('industries.html', industries=industries_data)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    if name and email and message:
        try:
            with mysql.connection.cursor() as cursor:
                cursor.execute('INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)', (name, email, message))
                mysql.connection.commit()
            flash('Your message has been submitted successfully!', 'success')
        except Exception as e:
            flash(f'Error submitting your message: {str(e)}', 'error')
    else:
        flash('Please fill out all fields before submitting the form.', 'error')
    
    return redirect(url_for('contact'))

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if not query:
        return redirect(url_for('index'))
    
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM products WHERE name LIKE %s OR description LIKE %s', ('%' + query + '%', '%' + query + '%'))
        search_results = cursor.fetchall()
        cursor.close()
    except Exception as e:
        print(f"Error during search: {e}")
        search_results = []

    print(f"Search results: {search_results}")  
    
    return render_template('search.html', query=query, results=search_results)

@app.route('/post/<int:post_id>')
def post(post_id):
    with mysql.connection.cursor() as cursor:
        cursor.execute("SELECT * FROM blog_posts WHERE id = %s", (post_id,))
        post_data = cursor.fetchone()
        
        if not post_data:
            return redirect(url_for('index'))
        
        cursor.execute("SELECT * FROM blog_posts WHERE id != %s ORDER BY date DESC LIMIT 5", (post_id,))
        related_posts_data = cursor.fetchall()

    return render_template('blog.html', post=post_data, related_posts=related_posts_data)

if __name__ == '__main__':
    app.run(debug=True)