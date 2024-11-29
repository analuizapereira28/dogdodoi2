from flask import Flask, render_template, redirect, url_for, request
import fdb

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

host = 'localhost'
database = r'C:\Users\Aluno\Downloads\BANCO\BANCO.FDB'
user = 'user'
password = 'password'



def connect_to_db():
    try:
        con = fdb.connect(host=host, database=database, user=user, password=password)
        return con
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None


class Cadastro:
    def __init__(self, id_cadastro, nome, email, senha, telefone, endereco, observacao):
        self.id_cadastro = id_cadastro
        self.nome = nome
        self.email = email
        self.senha = senha
        self.telefone = telefone
        self.endereco = endereco
        self.observacao = observacao


@app.route('/', methods=['GET', 'POST'])
def login_veterinario():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        con = connect_to_db()
        if con is not None:
            try:
                cursor = con.cursor()

                query = "SELECT email, senha FROM veterinarios WHERE email = ? AND senha = ?"
                cursor.execute(query, (email, password))
                user = cursor.fetchone()
                cursor.close()
                con.close()

                if user:
                    return redirect(url_for('dashboard'))
                else:
                    return render_template('login_veterinario.html', error="Email ou senha inválidos.")
            except Exception as e:
                print(f"Erro ao consultar o banco de dados: {e}")
                return "Erro ao realizar o login. Tente novamente mais tarde."
        else:
            return "Erro ao conectar ao banco de dados. Tente novamente mais tarde."

    return render_template('login_veterinario.html')


@app.route('/dashboard')
def dashboard():
    return '<h1>Bem-vindo ao painel do veterinário!</h1>'


@app.route('/cadastro_cliente', methods=['GET', 'POST'])
def cadastro_cliente():
    if request.method == 'POST':

        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        telefone = request.form['telefone']
        endereco = request.form['endereco']
        observacao = request.form['observacao']

        con = connect_to_db()
        if con is not None:
            try:
                cursor = con.cursor()

                cursor.execute("INSERT INTO clientes (nome, email, telefone, endereco, senha, observacao) VALUES (?, ?, ?, ?, ?, ?)",
                               (nome, email, telefone, endereco, senha, observacao))
                con.commit()
                cursor.close()
                con.close()
                return redirect(url_for('login_veterinario'))
            except Exception as e:
                print(f"Erro ao inserir no banco de dados: {e}")
                return "Erro ao cadastrar. Tente novamente mais tarde."
        else:
            return "Erro ao conectar ao banco de dados. Tente novamente mais tarde."

    return render_template('cadastro_cliente.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
