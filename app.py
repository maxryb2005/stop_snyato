import threading
from flask import Flask, render_template, request, jsonify, redirect, url_for
from extensions import db
from models import Fact
from bot import run_bot

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://047084354_hvatit:Innovatika_317@mysql.j1007852.myjino.ru:3306/j1007852_ort_d8"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "x%@Mv8Cg2BYkDE^7k&5aGB"
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fun', methods=['GET', 'POST'])
def facts():
    if request.method == 'POST':
        fun_text = request.form.get('fun_text')
        if fun_text:
            new_fun = Fun(text=fun_text)
            db.session.add(new_fun)
            db.session.commit()
            return redirect(url_for('fun'))
    all_fun = Fun.query.all()
    return render_template('fun.html', facts=all_fun)

@app.route('/delete_fun/<string:fun_id>', methods=['POST'])
def delete_fun(fun_id):
    fun_to_delete = Fun.query.get(fun_id)
    if fun_to_delete:
        db.session.delete(fun_to_delete)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False}), 400

if __name__ == "__main__":
    # Создаем поток для запуска бота
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()

    # Запускаем Flask
    with app.app_context():
        db.create_all()
    app.run(debug=True)