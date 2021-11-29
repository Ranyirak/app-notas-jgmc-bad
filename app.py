from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

app = Flask(__name__)
#Habilitando el uso del ORM en la app flask mediante el objeto "db"
db = SQLAlchemy(app)

#postgresql://<nombre_usuario>:<password>@<host>:<puerto>/<nombre_basededatos>
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://qcunbxigxpunkp:4f948b7111e4d3ec18a2830ab0a7bec4f468356a794285a6d478d70e4b78157b@ec2-52-86-193-24.compute-1.amazonaws.com:5432/d9mcacm57vh3a1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']  = False

class Notas(db.Model):
    '''Clase Notas'''
    __tablename__ = "notas"
    idNota = db.Column(db.Integer, primary_key = True)
    tituloNota = db.Column(db.String(80))
    cuerpoNota = db.Column(db.String(150))

    def __init__(self,tituloNota,cuerpoNota):
        self.tituloNota = tituloNota
        self.cuerpoNota = cuerpoNota

@app.route('/')
def index():
    return render_template ("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/crearnota", methods=['POST'])
def crearnota():
    campotitulo = request.form["campotitulo"]
    campocuerpo = request.form["campocuerpo"]
    print(campotitulo)
    print(campocuerpo)
    notaNueva = Notas(tituloNota=campotitulo,cuerpoNota=campocuerpo)
    db.session.add(notaNueva)
    db.session.commit()
    return redirect("/leernotas")
    #return render_template("index.html", titulo = campotitulo, cuerpo = campocuerpo)

@app.route("/leernotas")
def leernotas():
    consulta_notas = Notas.query.all()
    print(consulta_notas)
    for nota in consulta_notas:
        titulo = nota.tituloNota;
        cuerpo = nota.cuerpoNota;
        print(nota.tituloNota)
        print(nota.cuerpoNota)

    return render_template("leernotas.html", consulta = consulta_notas)

@app.route("/eliminarnota/<id>")
def eliminar(id):
    nota = Notas.query.filter_by(idNota = int(id)).delete()
    print(nota)
    db.session.commit()
    return redirect("/leernotas")

@app.route("/editarnota/<id>")
def editar(id):
    nota = Notas.query.filter_by(idNota = int(id)).first()
    print(nota)
    print(nota.tituloNota)
    print(nota.cuerpoNota)
    return render_template("modificar.html", nota = nota)

@app.route("/modificar", methods=['POST'])
def modificar():
    idnota = request.form["idnota"]
    nuevo_titulo = request.form["campotitulo"]
    nuevo_cuerpo = request.form["campocuerpo"]
    nota = Notas.query.filter_by(idNota = int(idnota)).first()
    nota.tituloNota = nuevo_titulo
    nota.cuerpoNota = nuevo_cuerpo
    db.session.commit()
    return redirect("/leernotas")

if __name__ == "__main__":
    db.create_all()
    app.run()
    
