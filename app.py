from flask import Flask, request, render_template, redirect, url_for
import cx_Oracle

app = Flask(__name__)

# Função para conexão ao banco Oracle
def get_db_connection():
    dsn = cx_Oracle.makedsn('host_do_banco', 'porta', sid='nome_do_servico')
    connection = cx_Oracle.connect(user='usuario', password='senha', dsn=dsn)
    return connection

# Rota para a página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        connection = get_db_connection()
        cursor = connection.cursor()

        # Verifica se o usuário existe e a senha corresponde
        query = 'SELECT * FROM usuarios WHERE login = :login AND senha = :senha'
        cursor.execute(query, login=login, senha=password)
        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user:
            return redirect(url_for('dashboard'))  # Redireciona para o dashboard
        else:
            return 'Login ou senha incorretos!', 401

    return render_template('login.html')

# Rota para o dashboard
@app.route('/dashboard')
def dashboard():
    return 'Bem-vindo ao Dashboard!'

if __name__ == '__main__':
    app.run(debug=True)
