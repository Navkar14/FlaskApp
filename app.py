from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(100), nullable= False)
    content = db.Column(db.Text, nullable= False)
    author = db.Column(db.String(100), nullable=False, default= 'None')
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return str(self.id)

urls = [
    {'img_title' : '1', 'url': ''},
    {'img_title' : '1', 'url': ''},
     {'img_title' : '1', 'url': ''},
      {'img_title' : '1', 'url': ''},
]
@app.route('/', methods=['GET','POST'])
def signin():
    return render_template('login.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    return render_template('signup.html')

@app.route('/home', methods=['GET','POST'])

def home():
    s = 'Hello Universe!'
    return render_template('index.html')


@app.route('/gallery')

def gallery():
    img_url = 'empty for now'
    return render_template('gallery.html', pickture = urls)

@app.route('/posts', methods = ['GET','POST'])

def posts():
    if request.method == 'POST':
        pTitle = request.form['title']
        pContent = request.form['content']
        new_post = Blog(title=pTitle, content=pContent, author='Navi')
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = Blog.query.order_by(Blog.title).all()
        return render_template('posts.html', posts = all_posts)

@app.route('/create', methods = ['GET','POST'])
def create():
    if request.method == 'POST':
        pTitle = request.form['title']
        pContent = request.form['content']
        new_post = Blog(title=pTitle, content=pContent, author='Navi')
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('add-post.html')
   

@app.route('/posts/delete/<int:id>')
def delete(id):
    del_id = Blog.query.get_or_404(id)
    db.session.delete(del_id)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods = ['GET','POST'])
def edit(id):
    editPost = Blog.query.get_or_404(id)
    if request.method == 'POST':
        
        editPost.title = request.form['title']
        editPost.content = request.form['content']
        editPost.author = request.form['author']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit-post.html', post = editPost)



if __name__ == "__main__":
    app.run(debug = True)