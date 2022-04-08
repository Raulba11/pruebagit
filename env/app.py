from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///friends.db'
db=SQLAlchemy(app)

class Friends(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(seLf):
        return '<Name %r>' %seLf.id


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    
    names=["Raul","Marcos","Alex"]
    return render_template("about.html",names=names)

    
@app.route('/form')
def form():
    return render_template("form.html")

@app.route('/gg', methods=["POST"])
def gg():
    fn=request.form.get("first_name")
    ln=request.form.get("last_name")
    nac=request.form.get("nac")
    if not fn or not ln or not nac:
        error="All fields required"
        return render_template("form.html",error=error,fn=fn,ln=ln,nac=nac)
    
    return render_template("gg.html",nac=nac,last_name=ln,first_name=fn)

@app.route('/friends',methods=['POST','GET'])
def friends():
    if request.method=="POST":
        friend_name=request.form['name']
        new_friend=Friends(name=friend_name)
        friends=Friends.query.order_by(Friends.date_created)
        if not friend_name:
            error="You have to fill the field"
            return render_template("friends.html",error=error,friends=friends)
        else:
            new_friend=Friends(name=friend_name)
            try:
                db.session.add(new_friend)
                db.session.commit()
                return redirect('/friends')
            except:
                return "There was an error"
    else:
        friends=Friends.query.order_by(Friends.date_created)
        return render_template("friends.html",friends=friends)


@app.route('/update/<int:id>',methods=['POST','GET'])
def update(id):
    friend_to_update=Friends.query.get_or_404(id)
    if request.method=="POST":
        friend_to_update.name=request.form["name"]
        if not friend_to_update.name:
            error="You have to fill the field"
            return render_template("update.html",error=error,friend_to_update=friend_to_update)
        else:
            try:
                db.session.commit()
                return redirect('/friends')
            except:
                return 'There was an error'
    else:
        return render_template('update.html',friend_to_update=friend_to_update)


@app.route('/delete/<int:id>')
def delete(id):
    friend_to_delete=Friends.query.get_or_404(id)
   
    try:
        db.session.delete(friend_to_delete)
        db.session.commit()
        return redirect('/friends')
    except:
        return 'There was an error'


