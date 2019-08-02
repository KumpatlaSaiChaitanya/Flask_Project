from flask import Flask,redirect,url_for,render_template,request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from project_database import Register,Base

engine=create_engine('sqlite:///bvc.db',connect_args={'check_same_thread':False},echo=True)
Base.metadata.bind=engine

DBSession=sessionmaker(bind=engine)
session=DBSession()

app=Flask('__name__')
@app.route("/home")
def hello():
	return "hello welcome to homepage"
@app.route("/about")
def about():
	return "<h1>about page</h1>"
@app.route("/data/<name>")
def data(name):
	name="chaitu"
	return "hello{}".format(name)

@app.route("/admin")
def admin():
	return render_template("sample.html")


@app.route("/person/<uname>/<int:age>/<float:percentage>")
def person(uname,age,percentage):
	return render_template("sample2.html",name=uname,age=age,percentage=percentage)


@app.route("/table/<int:num>")
def table(num):
	return render_template("table.html",n=num)
	

@app.route("/student")
def student():
	return "<font color='red'>hello welcome to student page"
@app.route("/std/<name>")
def std(name):
	if name=='student':
		return redirect(url_for('student'))
@app.route("/faculty")
def faculty():
	return "welcome  to faculty data"
@app.route("/user/<name>")
def user(name):
	if name=='faculty':
		return redirect(url_for('faculty'))
	elif name=='student':
		return redirect(url_for('student'))
	elif name=='admin':
		return redirect(url_for('admin'))
	else:
		return "no url found"

dummy_data=[{'name':'chaitu','branch':'cse','rollno':'556'},{'name':'manee','branch':'cse','rollqno':'515'}]
@app.route("/show")
def data_show():
	return render_template("show_data.html",d=dummy_data)

@app.route("/file")
def file_upload():
	return render_template("fileuploading.html")

@app.route("/success",methods=["POST"])
def success():
	if request.method=='POST':
		f=request.files["file"]
		f.save(f.filename)
		return render_template("display.html",name=f.filename)

@app.route("/register")
def reg():
	return render_template("register.html")

@app.route("/show_data")
def showData():
	register=session.query(Register).all()
	return render_template('show.html',register=register)

@app.route("/add",methods=["POST","GET"])
def addData():
	if request.method=='POST':
		newData=Register(name=request.form['name'],
			surname=request.form['surname'],roll_no=request.form['roll_no'],mobile=request.form['mobile'],branch=request.form['branch'])
		session.add(newData)
		session.commit()
		return redirect(url_for('showData'))
	else:
		return render_template('new.html')

@app.route('/<int:register_id>/edit',methods=["POST","GET"])
def editData(register_id):
	editedData=session.query(Register).filter_by(id=register_id).one()
	if request.method=="POST":
		editedData.name=request.form['name']
		editedData.surname=request.form['surname']
		editedData.roll_no=request.form['roll_no']
		editedData.mobile=request.form['mobile']
		editedData.branch=request.form['branch']
		session.add(editedData)
		session.commit()
		return redirect(url_for('showData'))
	else:
		return render_template('edit.html',register=editedData)

@app.route('/<int:register_id>/delete',methods=["POST","GET"])
def deleteData(register_id):
	deletedData=session.query(Register).filter_by(id=register_id).one()
	if request.method=="POST":
		session.delete(deletedData)
		session.commit()
		return redirect(url_for('showData',register_id=register_id))
	else:
		return render_template('delete.html',register=deletedData)


if __name__=='__main__':
	app.run(debug=True)