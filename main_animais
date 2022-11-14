from flask import Flask, jsonify, make_response, request
from flask_mysqldb import MySQL
from config import config
from validar import validar_cpf, validar_email, validar_nome, validar_celular, validar_id
from auth import auth_required
import requests
from requests.auth import HTTPBasicAuth
import json

app = Flask(__name__)

conexao=MySQL(app)

#FUNÇÃO PARA VALIDAÇÃO
def ler_cliente(id): #função para duplicidade de dados
    try:
        cursor = conexao.connection.cursor()
        sql = "SELECT id, animal, raça, tamanho, idade FROM bichos WHERE id = '{0}'".format(id)
        cursor.execute(sql)
        dados = cursor.fetchone()
        if dados != None:
            bichos={'id':dados[0],'animal':dados[1],'raça':dados[2],'tamanho':dados[3],'idade':dados[4]}
            return bichos
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


#CONSULTA DE TODA A BASE DE CLIENTES
@app.route('/animais', methods=['GET']) #leitura - todos os clientes (read)
@auth_required
def listar_clientes():
    try:
        cursor = conexao.connection.cursor()
        sql = "SELECT id, animal, raça, tamanho, idade FROM bichos"
        cursor.execute(sql)
        dados=cursor.fetchall()
        todas_bichos=[]
        for fila in dados:
            bichos={'id':fila[0],'animal':fila[1],'raça':fila[2],'tamanho':fila[3],'idade':fila[4]}
            todas_bichos.append(bichos)
        return jsonify({'todas_bichos': todas_bichos, 'Mensagem': "Animais listados!"})
    except Exception as e:
        reponse = jsonify({"Message": f"{e}"})


#LEITURA - CLIENTE INDIVIDUAL
@app.route('/animais/<id>', methods=['GET']) #leitura - cada cliente (read)
@auth_required
def ler_cliente_individual(id):
    try:
        cursor = conexao.connection.cursor()
        sql = "SELECT id, animal, raça, tamanho, idade FROM bichos WHERE id = '{0}'".format(id)
        cursor.execute(sql)
        dados=cursor.fetchone()
        if dados != None:
            bichos={'id':dados[0],'animal':dados[1],'raça':dados[2],'tamanho':dados[3],'idade':dados[4]}
            return jsonify({'bichos': bichos, 'Mensagem': "Animal Encontrado."})
        else:
            return jsonify({'Mensagem': "Animal Não Encontrado!"})
    except Exception as ex:
        return jsonify({'Mensagem': "Error!"})


#INSERÇÃO DE NOVO CLIENTE
@app.route('/novo', methods= ['POST']) #criar (create)
@auth_required
def registrar_cliente():
    #print (request.json)
    if (validar_animal(request.json['animal']) and validar_raca(request.json['raça']) and validar_tamanho(request.json['tamanho']) and validar_idade(request.json['idade'])):
        try:
                cursor = conexao.connection.cursor()
                sql = """INSERT INTO bichos (animal, raca, tamanho, idade) 
                VALUES ('{0}', '{1}', '{2}', '{3}')""".format(request.json['animal'], request.json['raça'], request.json['tamanho'], request.json['idade'])
                cursor.execute(sql)
                conexao.connection.commit() #confirma a ação da inserção
                return jsonify({'mensagem:': 'Animal registrado', 'exito': True})
        except Exception as e:
            reponse = jsonify({"Message": f"{e}", 'exito': False})
    else:
        return jsonify({'mensagem': "Parámetros inválidos...", 'exito': False})



@app.route('/atualizar/<id>', methods=['PUT']) #atualizar (update)
@auth_required
def atualizar_cliente(id):
    if (validar_animal(request.json['animal']) and validar_raca(request.json['raça']) and validar_tamanho(request.json['tamanho']) and validar_idade(request.json['idade'])):
        try:
            bichos = ler_cliente(id)
            if bichos != None:
                cursor = conexao.connection.cursor()
                sql = """UPDATE bichos SET animal ='{0}', raça ='{1}', tamanho ='{2}', idade ='{3}' WHERE  id ='{4}'""".format(request.json['animal'], request.json['raça'], request.json['tamanho'], request.json['idade'], id)
                cursor.execute(sql)
                conexao.connection.commit() #confirma a ação da inserção
                return jsonify({'mensagem:': 'Animal Atualizado!', 'exito': True})
            else:
                return jsonify({'mensagem': "Animal Não Encontrado.", 'exito': False})
        except Exception as e:
            reponse = jsonify({"Message": f"{e}", 'exito': False})
    else:
        return jsonify({'mensagem': "Parámetros inválidos...", 'exito': False})


@app.route('/deletar/<id>', methods=['DELETE'])
@auth_required
def deletar_cliente(id):
    try:
        bichos = ler_cliente(id)
        if bichos != None:
            cursor = conexao.connection.cursor()
            sql = "DELETE FROM bichos WHERE id ='{0}'".format(id)
            cursor.execute(sql)
            conexao.connection.commit() #confirma a ação da inserção
            return jsonify({'mensagem': "Animal excluído.", 'exito': True})
        else:
            return jsonify({'mensagem': "Animal não encontrado.", 'exito': False})
    except Exception as e:
            reponse = jsonify({"Message": f"{e}", 'exito': False})


def pagina_nao_encontrada(error):
    return '<h1>Página não encontrada</h1>', 404


if __name__=='__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_nao_encontrada)
    app.run(port=5002)
