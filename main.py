from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self, title, blog):
        self.title = title
        self.body = blog


@app.route('/', methods=['POST', 'GET'])
def index():

    blogs = Blog.query.all()

    return render_template('blog.html', blogs = blogs)

@app.route('/newpost', methods = ['POST','GET'])
def newpost():

    if request.method == 'POST':
        title = request.form['title']
        blog = request.form['blog']
        title_error = ''
        text_error = ''

        if title == '':
            title_error = 'Enter a title for the blog post.'
        
        if blog == '':
            text_error = 'Enter a blog post.'
        
        if title_error != '' or text_error != '':
            return render_template ('newpost.html', title_error = title_error, 
                                                    text_error = text_error)
        else:
            new_blog = Blog(title, blog)
            db.session.add(new_blog)
            db.session.commit()
            message_url = '/mypost?id=' + str(new_blog.id)
            return redirect(message_url)

    return render_template('newpost.html')


@app.route('/mypost', methods=['POST', 'GET'])
def mypost():

    id = request.args.get('id')
    post = Blog.query.get(id)

    return render_template('mypost.html', post = post)


if __name__ == '__main__':
    app.run()