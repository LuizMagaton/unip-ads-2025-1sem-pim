from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
import os

app = Flask(__name__)
app.secret_key = "sua_chave_secreta"
ARQUIVO_USUARIOS = "usuarios.json"


def carregar_usuarios():
    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, "r") as f:
            return json.load(f)
    return {}


def salvar_usuarios(usuarios):
    with open(ARQUIVO_USUARIOS, "w") as f:
        json.dump(usuarios, f, indent=4)


@app.route("/", methods=["GET", "POST"])
def login():
    usuarios = carregar_usuarios()

    if request.method == "POST":
        usuario = request.form["usuario"].strip().lower()
        senha = request.form["senha"]
        if usuario in usuarios and usuarios[usuario]["senha"] == senha:
            session["usuario"] = usuario
            flash("Login bem-sucedido!", "success")
            return redirect(url_for("final"))
        else:
            flash("Usuário ou senha incorretos.", "danger")
    return render_template("login.html")


@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    usuarios = carregar_usuarios()

    if request.method == "POST":
        usuario = request.form["usuario"].strip().lower()
        senha = request.form["senha"]
        confirmar = request.form["confirmar"]

        if not usuario:
            flash("Usuário não pode estar vazio.", "danger")
        elif senha != confirmar:
            flash("As senhas não coincidem.", "danger")
        elif usuario in usuarios:
            flash("Usuário já existe.", "danger")
        else:
            usuarios[usuario] = {"senha": senha}
            salvar_usuarios(usuarios)
            flash("Usuário registrado com sucesso!", "success")
            return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/excluir", methods=["POST"])
def excluir():
    usuarios = carregar_usuarios()
    usuario = request.form["usuario"].strip().lower()

    if usuario in usuarios:
        usuarios.pop(usuario)
        salvar_usuarios(usuarios)
        flash(f"Usuário '{usuario}' excluído com sucesso.", "success")
    else:
        flash("Usuário não encontrado.", "danger")
    return redirect(url_for("login"))


@app.route("/final")
def final():
    if "usuario" not in session:
        return redirect(url_for("login"))

    return render_template("final.html", usuario=session["usuario"])


@app.route("/logout")
def logout():
    session.pop("usuario", None)
    flash("Logout realizado com sucesso.", "info")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
