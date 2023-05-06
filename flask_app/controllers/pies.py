from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.pie import Pie
from flask_app.models.user import User
from flask_app.models.vote import Vote

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    user = User.get_by_id({"id":session['user_id']})
    if not user:
        return redirect('/logout')
    return render_template('dashboard.html', user=user, pies=Pie.get_all())

@app.route('/pies')
def derby_pie():
    if 'user_id' not in session:
        return redirect('/login')
    user = User.get_by_id({"id":session['user_id']})
    if not user:
        return redirect('/logout')
    return render_template('pie_derby.html', user=user, pies=Pie.get_all())

@app.route('/create/pie', methods=['POST'])
def create_pie():
    if 'user_id' not in session:
        return redirect('/login')
    if not Pie.validate_pie(request.form):
        return redirect('/dashboard')

    data = {
        'user_id': session['user_id'],
        'name': request.form['name'],
        'filling': request.form['filling'],
        'crust': request.form['crust'],
    }
    Pie.save(data)
    flash('pieError')
    return redirect('/dashboard')


@app.route('/pies/edit/<int:id>')
def edit_pie(id):
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('pie_edit.html',pie = Pie.get_by_id({'id': id}))

@app.route('/pies/update/<int:id>', methods=['POST'])
def update(id):
    if 'user_id' not in session:
        return redirect('/login')
    if not Pie.validate_pie(request.form):
        return redirect(f'/pies/edit/{id}')

    data = {
        'id':id,
        'name': request.form['name'],
        'filling': request.form['filling'],
        'crust': request.form['crust'],
    }
    Pie.update(data)
    return redirect('/dashboard')

@app.route('/pies/destroy/<int:id>')
def destroy_pie(id):
    if 'user_id' not in session:
        return redirect('/login')

    Pie.destroy({'id':id})
    return redirect('/dashboard')

@app.route('/pies/show/<int:id>')
def show_pie(id):
    if 'user_id' not in session:
        return redirect('/login')
    user = User.get_by_id({"id":session['user_id']})
    if not user:
        return redirect('/logout')
    return render_template('pie_show.html', user=user, pie=Pie.get_by_id({'id': id}))

@app.route('/pies/vote/<int:pie_id>', methods=['POST'])
def vote_pie(pie_id):
    if 'user_id' not in session:
        return redirect('/login')
    user_id = session['user_id']
    vote = Vote.get_by_user_id({'id': user_id})
    if vote == []:
        Vote.save({
            'vote': 1,
            'pie_id': pie_id,
            'user_id': user_id
        })
    if vote.vote == 1:
        print('You already voted')
    else:
        return redirect('/pies')
    user = User.get_by_id({'id': session['user_id']})
    pie = Pie.get_by_id({'id': pie_id})
    return render_template('pie_derby.html', user=user, pie=pie, vote=session['vote'])