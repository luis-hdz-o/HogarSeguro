#!/usr/bin/env python
# -*- coding: utf-8 -*-

######################################
#
# Primera api taller de programacion
#
######################################

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask import jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

#######################################
#
#			CONFIG DATABASE		
#
#######################################
'''
# BD de clase
app.config['MYSQL_HOST']= '34.86.12.131'
app.config['MYSQL_USER']= 'luish_lux'
app.config['MYSQL_PASSWORD']= 'yegnA7fwsH_cwZYh'
app.config['MYSQL_DB']= 'db_luis_lux'

'''

# BD del proyecto en AWS

app.config['MYSQL_HOST']= 'hogarseguro-1.cfldksk2uori.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER']= 'Admin'
app.config['MYSQL_PASSWORD']= 'UNILUX202020'
app.config['MYSQL_DB']= 'hogarseguro'


# SESSION
app.secret_key= 'mysecrectkey'

#INITIALIZE MySQL
mysql= MySQL(app)

#######################################
#
#			FUNCIONES		
#
#######################################
@app.route("/")
def main():
	return render_template('index.html', isIndex=True)


@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/login', methods=['GET','POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
		# Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
		# Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['id_role'] = 1
            # Redirect to home page
            return redirect(url_for('home'))
        elif account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['id_role'] = 2
            # Redirect to home page
            return redirect(url_for('home_user'))
        else:
			# Account doesnt exist or username/password incorrect
            flash('Incorrect username/password!')
    return render_template('login.html',isIndex=True)


@app.route('/userregister', methods=['GET', 'POST'])
def register():
    msg= ''
    if request.method == 'POST' and 'fullname' in request.form and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        fullname= request.form['fullname']
        username= request.form['username']
        password= request.form['password']
        email= request.form['email']
        cursor= mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT* FROM accounts WHERE username= %s', (username,))
        account= cursor.fetchone()

        #If account exists show error and validate checks
        if account:
            flash('La cuenta ya existe!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Email invalido!')
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash('El username debe contener solo letras y numeros!')
        elif not username or not password or not email:
            flash('Por favor llene la forma!')
        else: 
            #Acct doesnt exists and the form data is valid, now INSERT
            cursor.execute('INSERT INTO accounts (fullname,username,password,email) VALUES (%s, %s, %s, %s)', (fullname, username, password, email))
            mysql.connection.commit()
            # msg= 'Registro exitoso'
            flash('Contacto actualizado correctamente')
    elif request.method == 'POST':
            flash('Por favor llene la forma')
    
    return render_template('register.html', isIndex=True)

@app.route("/login", methods=['GET','POST'])
def sinlogin():
	msg = ''
	return render_template('login.html', msg = '')

@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    
    return redirect(url_for('login'))


@app.route('/profile_user')
def profile_user():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile_user.html', account=account)
    
    return redirect(url_for('login'))


@app.route('/edit/<id>')
def edit(id):
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the edit page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query= """
        SELECT * FROM accounts 
        WHERE id = {id}""".format(id= id)
        cursor.execute(query)
        account = cursor.fetchone()
        return render_template('edit.html', accounts =account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/update/<id>', methods= ['POST'])
def update(id):
    if request.method == 'POST':
        fullname= request.form['fullname']
        username= request.form['username']
        password= request.form['password']
        email= request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query= """
        UPDATE accounts
        SET fullname= {fullname}, username= {username}, password= {password}, email= {email}
        WHERE id = {id}""".format(fullname = fullname, username = username, password = password, email = email, id = id)
        cursor.execute(query)
        mysql.connection.commit()
        # msg= 'Registro exitoso'
        flash('Contacto actualizado correctamente')
        return render_template('edit.html')
    flash('Error al enviar formulario')
    return redirect(url_for('edit.html'))

'''
UPDATE accounts
        SET fullname= {fullname}, username= {username}, password= {password}, email= {email}
        WHERE id = {id}""".format((fullname= fullname, username= username, password= password, email= email, id= id)
'''

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))


@app.route("/history")
# @login_required
def history():
    if 'loggedin' in session: # primero confirmar si el usuario esta logueado
        """Tu historial de transacciones."""
        bls = []
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from history where id = %s order by fecha DESC", (session['id'],))
        row = cursor.fetchall() # fetchall para que se puedan jalar todos los renglones que cumplen la condicion

        for each in row: #muestra los valores del historial en una  tabla
            ls = []
            ls.append(each["id"])
            ls.append(each["articulo"])
            ls.append(each["precio"])
            ls.append(each['cantidad'])
            ls.append(each['fecha'])
            bls.append(ls)
            
        return render_template("history.html", bls = bls)

    return redirect(url_for('login'))



if __name__ == "__main__":

	app.run(host='0.0.0.0',
			debug=True,
			port=8080)
