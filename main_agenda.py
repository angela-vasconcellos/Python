from flask import Flask, jsonify, make_response, request
from flask_mysqldb import MySQL
from auth import auth_required
from config_catalogo import config_catalogo

app = Flask(__name__)

conexao=MySQL(app)

#função para os outros metodos - utilizando o ID_cliente
def ler_produto(id_agenda): #função para duplicidade de dados
    try:
        cursor = conexao.connection.cursor()
        sql = "SELECT id_agenda, id_animal, data, horario FROM agenda_pets WHERE id_agenda = '{0}'".format(id_agenda)
        cursor.execute(sql)
        dados = cursor.fetchone()
        if dados != None:
            agenda={'id_agenda':dados[0],'id_animal':dados[1], 'data':dados[2],'horario':dados[3]}
            return agenda
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


#CONSULTAR TODOS OS PRODUTOS
@app.route('/agenda', methods=['GET']) #leitura - todos os clientes (read)
@auth_required
def listar_produtos():
    try:
        cursor = conexao.connection.cursor()
        sql = "SELECT id_agenda, id_animal, data, horario FROM agenda_pets"
        cursor.execute(sql)
        dados=cursor.fetchall()
        toda_agenda=[]
        for fila in dados:
            produtos={'id_agenda':fila[0],'id_animal':fila[1], 'data':fila[2],'horario':fila[3]}
            toda_agenda.append(produtos)
        return jsonify({'toda_agenda': toda_agenda, 'Mensagem': "Agenda listada!"})
    except Exception as e:
        reponse = jsonify({"Message": f"{e}"})
        return reponse


#CONSULTAR UM PRODUTO ESPECIFICO
@app.route('/agenda/<id_agenda>', methods=['GET']) 
@auth_required
def ler_agendamento_individual(id_agenda):
    try:
        cursor = conexao.connection.cursor()
        sql = "SELECT id_agenda, id_animal, data, horario FROM agenda_pets WHERE id_agenda = '{0}'".format(id_agenda)
        cursor.execute(sql)
        dados=cursor.fetchall()
        todos_agendamentos=[]
        if dados != None:
            for fila in dados:
                produtos={'id_produto':fila[0],'produto':fila[1], 'preço':fila[2],'estoque':fila[3]}
                todos_agendamentos.append(produtos)
            return jsonify({'todos_agendamentos': todos_agendamentos, 'Mensagem': "Agendamento Encontrado."})
        else:
            return jsonify({'Mensagem': "Agendamento Não Encontrado!"})
    except Exception as e:
        reponse = jsonify({"Message": f"{e}"})
        return reponse

#CRIAR UM NOVO PRODUTO
@app.route('/novo', methods= ['POST']) #criar (create)
@auth_required
def registrar_produto():
    #print (request.json)
    try:
        cursor = conexao.connection.cursor()
        sql = """INSERT INTO agenda_pets (id_animal, data, horario) VALUES ('{0}', '{1}', '{2}')""".format(request.json['id_animal'], request.json['data'], request.json['horario'])
        cursor.execute(sql)
        conexao.connection.commit() #confirma a ação da inserção
        return jsonify({'mensagem:': 'Agendamento realizado com sucesso!', 'exito': True})
    except Exception as e:
        reponse = jsonify({"Message": f"{e}"})
        return reponse


@app.route('/atualizar/<id_agenda>', methods=['PUT']) #atualizar (update)
@auth_required
def atualizar_produto(id_agenda):
    try:
        produtos = ler_produto (request.json['id_agenda'])
        if produtos != None:
            cursor = conexao.connection.cursor()
            sql = """UPDATE agenda_pets SET id_animal = '{0}', data = '{1}', horario = '{2}' WHERE  id_agenda ='{3}'""".format(request.json['id_animal'], request.json['data'], request.json['horario'], id_agenda)
            cursor.execute(sql)
            conexao.connection.commit() #confirma a ação da inserção
            return jsonify({'mensagem:': 'Agendamento atualizado','exito': True })
        else:
            return jsonify({'mensagem': "Agendamento não encontrado.", 'exito': False})
    except Exception as e:
        reponse = jsonify({"Message": f"{e}"})
        return reponse


@app.route('/deletar/<id_agenda>', methods=['DELETE'])
@auth_required
def deletar_produto(id_agenda):
    try:
        produtos = ler_produto (request.json['id_agenda'])
        if produtos != None:
            cursor = conexao.connection.cursor()
            sql = "DELETE FROM agenda_pets WHERE id_agenda ='{0}'".format(id_agenda)
            cursor.execute(sql)
            conexao.connection.commit() #confirma a ação da inserção
            return jsonify({'mensagem': "Agendamento excluído.",  'exito': True})
        else:
            return jsonify({'mensagem': "ID não encontrado.", 'exito': False})
    except Exception as e:
        reponse = jsonify({"Message": f"{e}"})
        return reponse


def pagina_nao_encontrada(error):
    return '<h1>Página não encontrada</h1>', 404


if __name__=='__main__':
    app.config.from_object(config_catalogo['development'])
    app.register_error_handler(404, pagina_nao_encontrada)
    app.run(port=5004)
