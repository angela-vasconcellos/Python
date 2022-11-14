import json
from flask import Flask, jsonify, make_response, request
from flask_mysqldb import MySQL
import requests
from auth import auth_required
from config_historico import config_historico
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

conexao=MySQL(app)


#função para os outros metodos - utilizando o id_animal
def ler_historico(id_historico): #função para duplicidade de dados
    try:
        cursor = conexao.connection.cursor()
        sql = "SELECT id_historico, id_animal, id_agenda FROM historico_agenda WHERE id_historico = '{0}'".format(id_historico)
        cursor.execute(sql)
        dados = cursor.fetchone()
        if dados != None:
            historico={'id_historico':dados[0],'id_animal':dados[1], 'id_agenda':dados[2]}
            return historico
        else:
            return None
    except Exception as ex:
        raise ex


#LOGIN - AUTENTICACAO
@app.route ('/', methods=['GET'])
def index():
    if request.authorization and request.authorization.username == 'username1' and request.authorization.password == 'password':
        return '<h1>Você está logado!</h1>'

    return make_response ('Login/senha inválidos!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


#CONSULTAR BASE DE INVENTÁRIO
@app.route('/historico', methods=['GET']) #leitura - todos os animais (read)
@auth_required
def listar_agenda():
    try:
        cursor = conexao.connection.cursor()
        sql = "SELECT id_historico, id_animal, id_agenda FROM historico_agenda FROM historico_agenda"
        cursor.execute(sql)
        dados=cursor.fetchall()
        todo_historico=[]
        for fila in dados:
            historico={'id_historico':fila[0],'id_animal':fila[1], 'id_agenda':fila[2]}
            todo_historico.append(historico)
        return jsonify({'todo_historico': todo_historico, 'Mensagem': "Lista de agenda!"})
    except Exception as e:
        reponse = jsonify({"Message": f"{e}"})
        return reponse


#CONSULTAR UM INVENTÁRIO ESPECIFICO
@app.route('/historico/<id_historico>', methods=['GET']) #leitura - cada animais (read)
@auth_required
def ler_historico_individual(id_historico):
    try:
        cursor = conexao.connection.cursor()
        sql = "SELECT id_historico, id_animal, id_agenda FROM historico_agenda FROM historico_agenda WHERE id_historico = '{0}'".format(id_historico)
        cursor.execute(sql)
        dados=cursor.fetchall()
        todo_historico_agenda=[]
        if dados != None:
            for fila in dados:
                historico={'id_historico':fila[0],'id_animal':fila[1], 'id_agenda':fila[2]}
                todo_historico_agenda.append(historico)
            return jsonify({'todo_historico_agenda': todo_historico_agenda, 'Mensagem': "Inventário Encontrado."})
        else:
            return jsonify({'Mensagem': "Inventário Não Encontrado!"})
    except Exception as e:
        reponse = jsonify({"Message": f"{e}"})
        return reponse

#INSERIR NOVO INVENTÁRIO
@app.route('/novo', methods= ['POST']) #criar (create)
@auth_required
def registrar_historico():
    #print (request.json)
    try:
        cursor = conexao.connection.cursor()
        sql = """INSERT INTO historico_agenda (id_animal, id_agenda) VALUES ('{0}', '{1}')""".format(request.json['id_animal'], request.json['id_agenda'])
        cursor.execute(sql)
        conexao.connection.commit() #confirma a ação da inserção
        return jsonify({'mensagem:': 'Inventário cadastrado com sucesso!', 'exito': True})
    except Exception as e:
        reponse = jsonify({"Message": f"{e}"})
        return reponse

#ATUALIZAR INVENTÁRIO
@app.route('/atualizar/<id_historico>', methods=['PUT']) #atualizar (update)
@auth_required
def atualizar_historico(id_historico):
    try:
        historico = ler_historico (request.json['id_historico'])
        if historico != None:
            cursor = conexao.connection.cursor()
            sql = """UPDATE historico_agenda SET id_animal = '{0}', id_agenda = '{1}' WHERE  id_historico ='{2}'""".format(request.json['id_animal'], request.json['id_agenda'], id_historico)
            cursor.execute(sql)
            conexao.connection.commit() #confirma a ação da inserção
            return jsonify({'mensagem:': 'Inventário atualizado','exito': True })
        else:
            return jsonify({'mensagem': "Inventário não encontrado.", 'exito': False})
    except Exception as e:
        reponse = jsonify({"Message": f"{e}"})
        return reponse


@app.route('/deletar/<id_historico>', methods=['DELETE'])
@auth_required
def deletar_historico(id_historico):
    try:
        historico = ler_historico (request.json['id_historico'])
        if historico != None:
            cursor = conexao.connection.cursor()
            sql = "DELETE FROM historico_agenda WHERE id_historico ='{0}'".format(id_historico)
            cursor.execute(sql)
            conexao.connection.commit() #confirma a ação da inserção
            return jsonify({'mensagem': "Inventário excluído.",  'exito': True})
        else:
            return jsonify({'mensagem': "ID não encontrado.", 'exito': False})
    except Exception as e:
        reponse = jsonify({"Message": f"{e}"})
        return reponse




        #LIGAÇÕES ENTRE APIs

#API de animais 

#LIGAÇÃO ENTRE animais E INVENTÁRIO 
@app.route ('/historico/animais/<id_animal>')
def historico_animais(id_animal):
    animais_historico = requests.get('http://localhost:porta/animais', auth= HTTPBasicAuth ("username1", "password"))
    text = animais_historico.text
    data = (json.loads(text))
    animais = data['todas_pessoas']
    response = {}
    lista = []
    
    try:
        for animais in animais:
            if int(animais['id']) == int(id_animal): 
                lista.append(animais)

            cursor = conexao.connection.cursor()
            sql = "SELECT id_historico, id_animal, id_agenda FROM historico_agenda FROM historico_agenda WHERE id_animal = '{0}'".format(id_animal)
            cursor.execute(sql)
            cliRow = cursor.fetchall()
            response['Inventário'] = cliRow
            response['animais'] = lista[0]
            return response
    except Exception as e:
        reponse = jsonify({"Message": f"{e}"})
        return reponse



    # API de agenda
#LIGAÇÃO ENTRE historico E PRODUTO
@app.route ('/historico/agenda/<id_agenda>')
def historico_produto(id_agenda):
    agenda_historico = requests.get('http://localhost:port/agenda', auth= HTTPBasicAuth ("username1", "password"))
    text = agenda_historico.text
    data = (json.loads(text))
    agenda = data['todos_agenda']
    response = {}
    lista = []
    
    for produto in agenda:
        if int(produto['id_agenda']) == int(id_agenda): 
            lista.append(produto)

    try:
        cursor = conexao.connection.cursor()
        sql = "SELECT id_historico, id_animal, id_agenda FROM historico_agenda FROM historico_agenda WHERE id_agenda = '{0}'".format(id_agenda)
        cursor.execute(sql)
        cliRow = cursor.fetchall()
        response['Inventário'] = cliRow[0]
        response['Produto'] = lista 
        return response
    except Exception as e:
        reponse = jsonify({"Message": f"{e}"})
        return reponse

#MOSTRA O animais ESPECIFICO COM OS INVENTÁRIOS E agenda 
#API DE animais, historico E agenda
@app.route ('/historico/todos/<id_animal>')
def historico_animais_agenda(id_animal):
    cursor = conexao.connection.cursor()
    sql = "SELECT id_historico, id_animal, id_agenda FROM historico_agenda FROM historico_agenda WHERE id_animal = '{0}'".format(id_animal)
    cursor.execute(sql)
    cliRow = cursor.fetchall()
    #REQUEST animais
    animais_historico = requests.get('http://localhost:port/animais/{}'.format(id_animal), auth= HTTPBasicAuth ("username1", "password"))
    text = animais_historico.text
    data = json.loads(text)
    animais = data['pessoas']
    lista2=[]
    #REQUEST - agenda
    for compra in cliRow:
        produto_historico = requests.get('http://127.0.0.1:5004/agenda/{}'.format(compra[2]), auth= HTTPBasicAuth ("username1", "password"))
        text1 = produto_historico.text
        data1 = json.loads(text1)
        lista2.append(data1)
    try:
        response={}
        #historico
        cursor = conexao.connection.cursor()
        sql3 = "SELECT * FROM historico_agenda WHERE id_animal = '{0}'".format(id_animal)
        cursor.execute(sql3)
        cliRow2 = cursor.fetchall()
        response['Inventário'] = cliRow2
        response['animais'] = animais
        response['Produto'] = lista2
        return response
    except Exception as e:
        reponse = jsonify({"Message": f"{e}"})
        return reponse


#MOSTRAR TUDO - animais, INVENTÁRIOS E agenda 

@app.route ('/historico/todos')
def historico_todos():

    try:
        cursor = conexao.connection.cursor()
        sql = "SELECT * FROM historico_agenda"
        cursor.execute(sql)
        cliRow = cursor.fetchall()
        lista1=[]
        lista2=[]

        for compra in cliRow:
            animais_historico = requests.get('http://127.0.0.1:5002/animais/{}'.format(compra[1]), auth= HTTPBasicAuth ("username1", "password"))
            produto_historico = requests.get('http://127.0.0.1:5004/agenda/{}'.format(compra[2]), auth= HTTPBasicAuth ("username1", "password"))
            text1 = animais_historico.text
            text2 = produto_historico.text
            data1 = json.loads(text1)
            data2 = json.loads(text2)
            lista1.append(data1)
            lista2.append(data2)
        response={}
        response['Inventário'] = cliRow
        response['animais'] = lista1
        response['Produto'] = lista2

        return response
    except Exception as e:
        reponse = jsonify({"Message": f"{e}"})
        return reponse


def pagina_nao_encontrada(error):
    return '<h1>Página não encontrada</h1>', 404


if __name__=='__main__':
    app.config.from_object(config_historico['development'])
    app.register_error_handler(404, pagina_nao_encontrada)
    app.run(port=5005)
