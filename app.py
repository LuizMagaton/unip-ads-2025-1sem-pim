
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
        {"id": 1, "titulo": "Lógica de Programação",
            "link": "/curso/logica-programacao"},
        {"id": 2, "titulo": "Python para Iniciantes: Do Zero ao Código",
            "link": "/curso/python-iniciantes"},
        {"id": 3, "titulo": "Cibersegurança", "link": "/curso/Cibersegurança"},
        {"id": 4, "titulo": "Design Gráfico Profissional",
            "link": "/curso/design-grafico"}
    ]
    return render_template("cursos.html", cursos=cursos)


@app.route('/curso/logica-programacao')
def curso_logica_programacao():
    modulos = [
        {"titulo": "Módulo 1: Introdução aos Algoritmos", "aulas": [
            {"titulo": "Introdução aos Algoritmos",
                "link": "/aula/logica-python-intro"},
            {"titulo": "Primeiro Algoritmo",
                "link": "/aula/logica-python-instalacao"},
        ]},
        {"titulo": "Módulo 2: Operadores e Lógica", "aulas": [
            {"titulo": "Comando de Entrada e Operadores",
                "link": "/aula/logica-tipos-dados"},
            {"titulo": "Operadores Lógicos e Relacionais",
                "link": "/aula/logica-operadores-logicos"}
        ]},
        {"titulo": "Módulo 3: Estruturas de Controle", "aulas": [
            {"titulo": "Estruturas Condicionais",
                "link": "/aula/logica-Instruções_Condicionais"},
            {"titulo": "Estruturas de Repetição", "link": "/aula/logica-else"},
        ]},
        {"titulo": "Módulo 4: Modularização de Algoritmos", "aulas": [
            {"titulo": "Procedimentos e Funções", "link": "/aula/logica-for"},
        ]},
        {"titulo": "Módulo 5: Prática com Projetos", "aulas": [
            {"titulo": "Estruturas de Dados",
                "link": "/aula/logica-definir-funcoes"},
        ]},
    ]
    return render_template("logica_programacao.html", modulos=modulos)


@app.route('/curso/python-iniciantes')
def curso_python_iniciantes():
    modulos = [
        {"titulo": "Módulo 1: Primeiros Passos com Python", "aulas": [
            {"titulo": "O que é Python e suas aplicações",
                "link": "/aula/python-intro"},
            {"titulo": "Instalação do Python", "link": "/aula/python-instalacao"},
        ]},
        {"titulo": "Módulo 2: Fundamentos da Programação", "aulas": [
            {"titulo": "Variáveis e Tipos de Dados", "link": "/aula/tipos-dados"},
            {"titulo": "Operadores em Python", "link": "/aula/operadores-logicos"}
        ]},
        {"titulo": "Módulo 3: Controle de Fluxo e Funções", "aulas": [
            {"titulo": "Instruções Condicionais (if, elif, else)",
             "link": "/aula/Instruções_Condicionais"},
            {"titulo": "Loops (for, while, break, continue)",
             "link": "/aula/loops"},
            {"titulo": "Funções: definição, parâmetros, retorno",
                "link": "/aula/Funcoes"},
        ]},
        {"titulo": "Módulo 4: Modularização e Tratamento de Erros", "aulas": [
            {"titulo": "Módulos e pacotes (inclui import e built-ins)",
             "link": "/aula/import"},
            {"titulo": "Tratamento de exceções: try, except, finally",
                "link": "/aula/iteracao"},
        ]},
        {"titulo": "Módulo 5: Prática com Projetos", "aulas": [
            {"titulo": "Projeto 1: Calculadora simples",
                "link": "/aula/definir-Projeto1"},
            {"titulo": "Projeto 2: Jogo de adivinhação",
                "link": "/aula/chamar-Projeto2"},
        ]},
    ]
    return render_template("curso_python.html", modulos=modulos)


@app.route('/curso/Cibersegurança')
def curso_Cibersegurança():
    modulos = [
        {"titulo": "Módulo 1: Fundamentos da Cibersegurança", "aulas": [
            {"titulo": "Introdução à Cibersegurança",
                "link": "/aula/Cibersegurança"},
            {"titulo": "Conceitos Essenciais de Segurança da Informação",
                "link": "/aula/Conceitos_Essenciais"},
        ]},
        {"titulo": "Módulo 2: Ameaças e Vulnerabilidades", "aulas": [
            {"titulo": "Tipos de Malware", "link": "/aula/Tipos_Malware"},
            {"titulo": "Tipos de ataques", "link": "/aula/Tipos_ataques"}
        ]},
        {"titulo": "Módulo 3: Defesas Essenciais", "aulas": [
            {"titulo": "Criptografia, autenticação e firewalls",
                "link": "/aula/Criptografia"},
            {"titulo": "Proteção de redes, servidores e dispositivos móveis.",
                "link": "/aula/Proteção"},
        ]},
        {"titulo": "Módulo 4: Prática e Casos Reais", "aulas": [
            {"titulo": "Análise de ataques e introdução a testes de segurança.",
                "link": "/aula/Análise_ataques"},
        ]},
    ]
    return render_template("ciberseguranca.html", modulos=modulos)


video_data = {
    "python-intro": {
        "titulo": "O que é Python e suas aplicações",
        "youtube_id": "3hng-hmSv2Y"
    },
    "instalacao-python": {
        "titulo": "Instalação do Python",
        "youtube_id": "gqrySQQzvvQ"
    },
    "outro-video": {  # Dados para o novo vídeo
        "titulo": "Outro Vídeo",
        "youtube_id": "NEW_VIDEO_ID"  # Substitua com o ID do seu novo vídeo
    }
    # Adicione mais vídeos conforme necessário
}


@app.route('/aula/<video_id>')
def show_video(video_id):
    if video_id not in video_data:
        return redirect(url_for('curso_python_iniciantes'))

    video = video_data[video_id]
    return render_template('video.html', video=video)


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
            usuarios[usuario] = {"senha": hashed_senha,
                                 "email": email, "numero": numero}
            salvar_usuarios(usuarios)
            flash("Usuário registrado com sucesso! ✅", "info")
            return redirect(url_for("login"))
    return render_template("register.html")


@app.route('/politica-de-dados')
def politica_de_dados():
    return render_template('politica_de_dados.html')


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
            flash(
                f"Usuário '{usuario_para_excluir}' excluído com sucesso.", "danger")
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
