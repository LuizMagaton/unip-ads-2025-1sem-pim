from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os
import bcrypt

app = Flask(__name__)
app.secret_key = "sua_chave_secreta"
ARQUIVO_USUARIOS = "usuarios.json"


def carregar_usuarios():
    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def salvar_usuarios(usuarios):
    with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4)


def gerar_hash_senha(senha):
    senha_codificada = senha.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_senha = bcrypt.hashpw(senha_codificada, salt)
    return hashed_senha.decode('utf-8')


def verificar_senha(senha_fornecida, hash_armazenado):
    senha_codificada = senha_fornecida.encode('utf-8')
    hash_codificado = hash_armazenado.encode('utf-8')
    return bcrypt.checkpw(senha_codificada, hash_codificado)


@app.route("/")
def pagina_inicial():
    return render_template("pagina_inicial.html")


@app.route("/contato")
def contato():
    return render_template("contato.html")


@app.route("/sobrenos")
def sobrenos():
    if "usuario" not in session:
        return redirect(url_for("login"))
    return render_template("sobrenos.html", usuario=session["usuario"])


@app.route("/cursos")
def listar_cursos():
    cursos = [
        {"id": 1, "titulo": "Curso de Introdução à Programação", "link": "/curso/introducao-programacao"},
        {"id": 2, "titulo": "Python para Iniciantes: Do Zero ao Código", "link": "/curso/python_iniciantes"},
        {"id": 3, "titulo": "Marketing Digital para Iniciantes", "link": "/curso/marketing-digital"},
        {"id": 4, "titulo": "Design Gráfico Profissional", "link": "/curso/design-grafico"}
    ]
    return render_template("cursos.html", cursos=cursos)


@app.route('/curso/python-iniciantes')
def curso_python_iniciantes():
    modulos = [
        {"titulo": "Módulo 1: Introdução ao Python e Configuração do Ambiente", "aulas": [
            {"titulo": "O que é Python e suas aplicações", "link": "/aula/python-intro"},
            {"titulo": "Instalação do Python", "link": "/aula/python-instalacao"},
            {"titulo": "Primeiro contato com o IDE", "link": "/aula/python-ide"}
        ]},
        {"titulo": "Módulo 2: Fundamentos da Linguagem: Variáveis, Tipos de Dados e Operadores", "aulas": [
            {"titulo": "Variáveis e atribuições", "link": "/aula/variaveis"},
            {"titulo": "Tipos de dados (int, float, str, bool)", "link": "/aula/tipos-dados"},
            {"titulo": "Operadores aritméticos", "link": "/aula/operadores-aritmeticos"},
            {"titulo": "Operadores de comparação", "link": "/aula/operadores-comparacao"},
            {"titulo": "Operadores lógicos", "link": "/aula/operadores-logicos"}
        ]},
        {"titulo": "Módulo 3: Estruturas de Controle: Condicionais (if, else, elif)", "aulas": [
            {"titulo": "A instrução if", "link": "/aula/if"},
            {"titulo": "A instrução else", "link": "/aula/else"},
            {"titulo": "A instrução elif", "link": "/aula/elif"},
            {"titulo": "Condicionais aninhados", "link": "/aula/if-aninhado"}
        ]},
        {"titulo": "Módulo 4: Estruturas de Controle: Loops (for e while)", "aulas": [
            {"titulo": "O loop for", "link": "/aula/for"},
            {"titulo": "Iterando sobre sequências", "link": "/aula/iteracao"},
            {"titulo": "O loop while", "link": "/aula/while"},
            {"titulo": "Controle de loops (break e continue)", "link": "/aula/controle-loop"}
        ]},
        {"titulo": "Módulo 5: Funções: Organizando seu Código", "aulas": [
            {"titulo": "Definindo funções", "link": "/aula/definir-funcoes"},
            {"titulo": "Chamando funções", "link": "/aula/chamar-funcoes"},
            {"titulo": "Parâmetros e argumentos", "link": "/aula/parametros"},
            {"titulo": "Retornando valores", "link": "/aula/retorno-funcoes"}
        ]},
        {"titulo": "Módulo 6: Módulos e Pacotes: Expandindo as Funcionalidades do Python", "aulas": [
            {"titulo": "O que são módulos", "link": "/aula/modulos"},
            {"titulo": "Importando módulos", "link": "/aula/importar-modulos"},
            {"titulo": "Usando módulos built-in", "link": "/aula/modulos-builtin"},
            {"titulo": "Introdução a pacotes", "link": "/aula/pacotes"}
        ]},
        {"titulo": "Módulo 7: Tratamento de Erros e Exceções", "aulas": [
            {"titulo": "O que são erros e exceções", "link": "/aula/erros-excecoes"},
            {"titulo": "Tratando exceções com try-except", "link": "/aula/try-except"},
            {"titulo": "Cláusula finally", "link": "/aula/finally"}
        ]},
        {"titulo": "Módulo 8: Projetos Práticos Iniciais", "aulas": [
            {"titulo": "Projeto 1: Calculadora simples", "link": "/projeto/calculadora"},
            {"titulo": "Projeto 2: Jogo de adivinhação", "link": "/projeto/adivinhacao"}
        ]}
    ]
    return render_template("curso_python.html", modulos=modulos)


@app.route("/login", methods=["GET", "POST"])
def login():
    usuarios = carregar_usuarios()

    if request.method == "POST":
        usuario = request.form["usuario"].strip().lower()
        senha = request.form["senha"]
        if usuario in usuarios and verificar_senha(senha, usuarios[usuario]["senha"]):
            session["usuario"] = usuario
            return redirect(url_for("pagina_inicial"))
        else:
            flash("Usuário ou senha incorretos ! ❌", "danger")
    return render_template("login.html")


@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    usuarios = carregar_usuarios()

    if request.method == "POST":
        usuario = request.form["usuario"].strip().lower()
        senha = request.form["senha"]
        confirmar = request.form["confirmar"]
        email = request.form.get("email", "").strip()
        numero = request.form.get("numero", "").strip()

        if not usuario:
            flash("Usuário não pode estar vazio.", "danger")
        elif senha != confirmar:
            flash("As senhas não coincidem.", "danger")
        elif usuario in usuarios:
            flash("Usuário já existe.", "danger")
        else:
            hashed_senha = gerar_hash_senha(senha)
            usuarios[usuario] = {"senha": hashed_senha, "email": email, "numero": numero}
            salvar_usuarios(usuarios)
            flash("Usuário registrado com sucesso! ✅", "info")
            return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/excluir", methods=["POST"])
def excluir():
    usuarios = carregar_usuarios()
    usuario_para_excluir = request.form["usuario"].strip().lower()
    senha_digitada = request.form["senha"]

    if "usuario" not in session:
        flash("Você precisa estar logado para excluir sua conta.", "warning")
        return redirect(url_for("login"))

    if usuario_para_excluir == session["usuario"]:
        if usuario_para_excluir in usuarios and verificar_senha(senha_digitada, usuarios[usuario_para_excluir]["senha"]):
            usuarios.pop(usuario_para_excluir)
            salvar_usuarios(usuarios)
            session.pop("usuario", None)
            flash(f"Usuário '{usuario_para_excluir}' excluído com sucesso.", "danger")
            return redirect(url_for("login"))
        else:
            flash("Senha incorreta. Não foi possível excluir a conta.", "danger")
            return render_template("excluir_conta.html")
    else:
        flash("Nome de usuário incorreto.", "danger")
        return render_template("excluir_conta.html")


@app.route("/esqueci_senha")
def esqueci_senha():
    return render_template("esqueci_senha.html")


@app.route("/redefinir_senha", methods=["POST"])
def redefinir_senha():
    usuario = request.form["usuario"].strip().lower()
    nova_senha = request.form["nova_senha"]
    confirmar_senha = request.form["confirmar_senha"]

    if nova_senha != confirmar_senha:
        flash("As novas senhas não coincidem.", "danger")
        return render_template("esqueci_senha.html")

    usuarios = carregar_usuarios()
    if usuario in usuarios:
        hashed_nova_senha = gerar_hash_senha(nova_senha)
        usuarios[usuario]["senha"] = hashed_nova_senha
        salvar_usuarios(usuarios)
        flash("Senha redefinida com sucesso. Faça login com a nova senha.", "success")
        return redirect(url_for("login"))
    else:
        flash("Usuário não encontrado.", "danger")
        return render_template("esqueci_senha.html")


@app.route("/excluir_conta")
def excluir_conta_pagina():
    return render_template("excluir_conta.html")


@app.route("/minha_conta", methods=["GET", "POST"])
def minha_conta():
    if "usuario" not in session:
        return redirect(url_for("login"))

    usuarios = carregar_usuarios()
    usuario_info = usuarios.get(session["usuario"])

    if request.method == "POST":
        novo_email = request.form.get("email", "").strip()
        novo_numero = request.form.get("numero", "").strip()
        novo_usuario = request.form.get("usuario", "").strip().lower()

        erros = {}

        if not novo_email:
            erros["email"] = "O e-mail não pode estar vazio."
        if not novo_numero:
            erros["numero"] = "O número não pode estar vazio."
        if not novo_usuario:
            erros["usuario"] = "O usuário não pode estar vazio."
        elif novo_usuario != session["usuario"] and novo_usuario in usuarios:
            erros["usuario"] = "Este usuário já existe."

        if erros:
            for campo, mensagem in erros.items():
                flash(mensagem, "danger")
            return render_template("minha_conta.html", usuario_info=usuario_info)
        else:
            usuarios[session["usuario"]]["email"] = novo_email
            usuarios[session["usuario"]]["numero"] = novo_numero
            if novo_usuario != session["usuario"]:
                usuarios[novo_usuario] = usuarios.pop(session["usuario"])
                session["usuario"] = novo_usuario
                flash("Informações atualizadas com sucesso!", "success")
                return redirect(url_for("minha_conta"))
            else:
                salvar_usuarios(usuarios)
                flash("Informações atualizadas com sucesso!", "success")
                return render_template("minha_conta.html", usuario_info=usuario_info)

    return render_template("minha_conta.html", usuario_info=usuario_info)


@app.route("/logout")
def logout():
    session.pop("usuario", None)
    flash("Logout realizado com sucesso !", "info")
    return redirect(url_for("pagina_inicial"))


# ✅ INÍCIO DO SERVIDOR FLASK (único app.run)
if __name__ == "__main__":
    app.run(debug=True)
