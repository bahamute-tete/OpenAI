import openai
import sys
import os
import datetime
from flask import Flask,url_for,redirect,request,render_template ,session,flash,jsonify
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail,Message
from werkzeug.security import generate_password_hash,check_password_hash
from nltk.tokenize import sent_tokenize
import nltk

nltk.download('punkt')

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] ='12344322'

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICTIONS']=False
db = SQLAlchemy(app)

app.config['MAIL_SERVER'] = 'stmp.qq.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = '330378164@qq.com'
app.config['MAIL_PASSWORD'] = 'Shufang112cv'
'''
TLS是SSL(Secure Sockets Layer)的更新和更安全的版本,有时也被称为SSL 3.1。
MAIL_USE_TLS通常使用端口587;
MAIL_USE_SSL通常使用端口465。
'''
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail= Mail(app)

bootstrap = Bootstrap(app)
moment = Moment(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),unique=True)
    '''Role 表添加了一个users属性。为user表定义了一个role属性,关联到User表上 这样User表可以使用使用role属性,
    user.role 和role.users 双向访问'''
    users = db.relationship('User',backref='role')

    # '''除了 str 类型之外，还有一些其他的字符串类型，
    # 例如 bytes，bytearray，memoryview 等4。
    # 这些类型都是用来表示二进制数据的，
    # 它们和 str 类型有一些区别和相互转换的方法4。'''
    def __repr__(self) -> str:#返回一个字符串 但这个串不一定是string 类型的 需要注解强调
        return '<Role %r>' %self.name
    

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64),unique=True,index =True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    def __repr__(self) -> str:
        return '<User %r>' %self.username

    password_hash =db.Column(db.String(128))
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)  

class NewForm(FlaskForm):
    def __init__(self):
        super(NewForm, self).__init__()
    name = StringField('What`s you name?',validators=[DataRequired()])
    submit = SubmitField('submit')
# m= openai.Model.list()
# s= openai.Model.retrieve("text-davinci-003")
# response = openai.Completion.create(
#     #Model
#     model ='text-davinci-003',
#     #Prompt
#     prompt ='hello who are you?',
#     # integer Optional Defaults to 16
#     max_tokens =1024,
#     #range(0,2) higher value = more random number Optional Defaults to 1
#     temperature =1,
#     #0.1 means only the tokens comprising the top 10% probability mass are considered.
#     #number Optional Defaults to 1
#     top_p=1
# )

@app.route('/')
def index():
    return render_template('chatTest.html')

conversation_history =[]

@app.route('/process_message',methods=["POST"])
def process_message():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    user_message = request.json.get("message")

    if user_message:
        
        
        conversation_history.append({'role':'user','content':user_message})
        
        chat_message =[
            {'role':'system','content':'You are a help assistant'},
        ]+conversation_history

        response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=chat_message,
        max_tokens= 2048,
        n=1,
        temperature=0.5)
                
        ai_message = response['choices'][0]['message']['content'].strip()

        ai_message_sentences = sent_tokenize(ai_message)
        formatted_ai_message='\n'.join(ai_message_sentences)

        conversation_history.append({'role':'assistant','content':formatted_ai_message})   

        return jsonify({"message": formatted_ai_message,"time": current_time})
    
    return jsonify({"message": "Error! Empty message","time": current_time})



@app.shell_context_processor
def make_shell_context():
    return dict(db=db,Role=Role,User=User)


# @app.route('/',methods=['GET', 'POST'])
# def index():
    # msg =Message('Hello',sender='330378164@qq.com',recipients=['330378164@qq.com'])
    # msg.body = 'Hello'
    # mail.send(msg)

    # form =NewForm()
    # if form.validate_on_submit():
    #     user = User.query.filter_by(username=form.name.data).first()
    #     if user is None:
    #         user = User(username=form.name.data)
    #         db.session.add(user)
    #         db.session.commit()
    #         session['known'] =False
    #     else:
    #         session['known']=True
    #     session['name'] =form.name.data
    #     form.name.data =''
    #     return redirect(url_for('index'))
    # return render_template('index.html',current_time=datetime.utcnow(),form=form,name=session.get('name'),
    #                        known=session.get('known'))

# def creat_prompt(content):
#     return content


@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'),500

if __name__ ==('__main__'):
    app.run(port=2020,host='0.0.0.0',debug=True)

