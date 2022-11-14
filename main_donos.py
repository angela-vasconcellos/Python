from flask import Flask, jsonify, make_response, request
from flask_mysqldb import MySQL
from config_adress import config_adress
from auth import auth_required

app = Flask(__name__)

conexao=MySQL(app)

#função para os outros metodos - utilizando o ID_animal
def ler_endereco(id_dono): #função para duplicidade de dados
    try:
        cursor = conexao.connection.cursor()
        sql = "SELECT id_animal, id_dono, nome, logradouro, numero, bairro, cidade, uf, cep, celular FROM inf_donos WHERE id_dono= '{0}'".format(id_dono)
        cursor.execute(sql)
        dados = cursor.fetchone()
        if dados != None:
            donos={'id_animal':dados[0],'id_dono':dados[1], 'nome':dados[2],'logradouro':dados[3],'numero':dados[4],'bairro':dados[5],'cidade':dados[6],'uf':dados[7],'cep':dados[8],'celular':dados[9]}
            return donos
        else:
            return None
    except Exception as ex:
        raise ex

#FUNÇÃO PARA VALIDAÇÃO DO NOVO - EVITA CRIAÇÃO DE 2 ENDEREÇOS COM CEP IGUAL PARA O MESMO CLIENTE 
def ler_endereco_cep(cep): #função para duplicidade de dados
    try:
        cursor = conexao.connection.cursor()
        sql = "SELECT id_animal, id_dono, nome, logradouro, numero, bairro, cidade, uf, cep, celular FROM inf_donos WHERE cep= '{0}'".format(cep)
        cursor.execute(sql)
        dados = cursor.fetchone()
        if dados != None:
            donos_cep={'id_animal':dados[0],'id_dono':dados[1], 'nome':dados[2],'logradouro':dados[3],'numero':dados[4],'bairro':dados[5],'cidade':dados[6],'uf':dados[7],'cep':dados[8],'celular':dados[9]}
            return donos_cep
        else:
            return None
    except Exception as ex:
        raise ex

#FUNÇÃO VALIDAÇÃO PELO ID_CLIENTE - PARA O DELETE
def ler_endereco_idcliente(id_dono): #função para duplicidade de dados
    try:
        cursor = conexao.connection.cursor()
        sql = "SELECT id_animal, id_dono, nome, logradouro, numero, bairro, cidade, uf, cep, celular FROM inf_donos WHERE id_dono= '{0}'".format(id_dono)
        cursor.execute(sql)
        dados = cursor.fetchone()
        if dados != None:
            enderecos_idcliente ={'id_animal':dados[0],'id_dono':dados[1], 'nome':dados[2],'logradouro':dados[3],'numero':dados[4],'bairro':dados[5],'cidade':dados[6],'uf':dados[7],'cep':dados[8],'celular':dados[9]}
            return enderecos_idcliente
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


#CONSULTAR TODOS OS ENDEREÇOS CADASTRADOS
@app.route('/donos', methods=['GET']) #leitura - todos os clientes (read)
@auth_required
def listar_endereco():
    try:
        cursor = conexao.connection.cursor()
        sql = "SELECT id_animal, id_dono, nome, logradouro, numero, bairro, cidade, uf, cep, celular FROM inf_donos"
        cursor.execute(sql)
        dados=cursor.fetchall()
        todos_donos=[]
        for fila in dados:
            donos={'id_animal':fila[0],'id_dono':fila[1], 'nome':fila[2],'logradouro':fila[3],'numero':fila[4],'bairro':fila[5],'cidade':fila[6],'uf':fila[7],'cep':fila[8],'celular':fila[9]}
            todos_donos.append(donos)
        return jsonify({'todos_donos': todos_donos, 'Mensagem': "Lista de Endereços!"})
    except Exception as e:
        reponse = jsonify({"Message": f"{e}"})


#CONSULTAR ENDEREÇOS DE UM CLIENTE ESPECIFICO
@app.route('/enderecos/<id_animal>', methods=['GET']) #leitura - cada cliente (read)
@auth_required
def ler_endereco_individual(id_cliente):
    try:
        cursor = conexao.connection.cursor()
        sql = "SELECT id_animal, id_dono, nome, logradouro, numero, bairro, cidade, uf, cep, celular FROM inf_donos WHERE id_dono = '{0}'".format(id_cliente)
        cursor.execute(sql)
        dados=cursor.fetchall()
        todos_enderecos_dono=[]
        if dados != None:
            for fila in dados:
                enderecos={'id_animal':fila[0],'id_dono':fila[1], 'nome':fila[2],'logradouro':fila[3],'numero':fila[4],'bairro':fila[5],'cidade':fila[6],'uf':fila[7],'cep':fila[8],'celular':fila[9]}
                todos_enderecos_dono.append(enderecos)
            return jsonify({'todos_enderecos_dono': todos_enderecos_dono, 'Mensagem': "Endereco Encontrado."})
        else:
            return jsonify({'Mensagem': "Endereço Não Encontrado!"})
    except Exception as e:
        reponse = jsonify({"Message": f"{e}"})

#ADICIONAR NOVO ENDERECO
@app.route('/novo', methods= ['POST']) #criar (create)
@auth_required
def registrar_endereco():
    #print (request.json)
    try:
        enderecos = ler_endereco_cep (request.json['cep'])
        if enderecos != None:
            return jsonify({'mensagem': "Dono já cadastrado.", 'exito': False})
        else:
            cursor = conexao.connection.cursor()
            sql = """INSERT INTO inf_donos (id_animal, nome, logradouro, numero, bairro, cidade, uf, cep, celular) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}')""".format(request.json['id_animal'], request.json['nome'], request.json['logradouro'], request.json['numero'], request.json['bairro'], request.json['cidade'], request.json['uf'], request.json['cep'], request.json['celular'])
            cursor.execute(sql)
            conexao.connection.commit() #confirma a ação da inserção
            return jsonify({'mensagem:': 'Dono cadastrado com sucesso!', 'exito': True})
    except Exception as e:
        reponse = jsonify({"mensagem": f"{e}", 'exito': False})


@app.route('/atualizar/<id_dono>', methods=['PUT']) #atualizar (update)
@auth_required
def atualizar_endereco(id_dono):
    try:
        endereco = ler_endereco (request.json['id_dono'])
        if endereco != None:
            cursor = conexao.connection.cursor()
            sql = """UPDATE inf_donos SET id_animal = '{0}', nome = '{1}', logradouro = '{2}', numero = '{3}', bairro = '{4}', cidade = '{5}', uf = '{6}', cep = '{7}', celular = '{8}' WHERE  id_endereco ='{9}'""".format(request.json['id_animal'], request.json['nome'], request.json['logradouro'], request.json['numero'], request.json['bairro'], request.json['cidade'], request.json['uf'], request.json['cep'], request.json['celular'], id_dono)
            cursor.execute(sql)
            conexao.connection.commit() #confirma a ação da inserção
            return jsonify({'mensagem:': 'Dono atualizado','exito': True })
        else:
            return jsonify({'mensagem': "ID não encontrado.", 'exito': False})
    except Exception as e:
        reponse = jsonify({"Message": f"{e}", 'exito': False})

#DELETAR APENAS 1 ENDEREÇO - PELO id_dono
@app.route('/deletar/endereco/<id_dono>', methods=['DELETE'])
@auth_required
def deletar_dono(id_dono):
    try:
        dono = ler_endereco (id_dono)
        if dono != None:
                cursor = conexao.connection.cursor()
                sql = "DELETE FROM endereco_cliente WHERE id_dono ='{0}'".format(id_dono)
                cursor.execute(sql)
                conexao.connection.commit() #confirma a ação da inserção
                return jsonify({'mensagem': "Dono excluído.",  'exito': True})
        else:
            return jsonify({'mensagem': "ID não encontrado.", 'exito': False})
    except Exception as e:
                reponse = jsonify({"Message": f"{e}", 'exito': False})


def pagina_nao_encontrada(error):
    return '<h1>Página não encontrada</h1>', 404


if __name__=='__main__':
    app.config.from_object(config_adress['development'])
    app.register_error_handler(404, pagina_nao_encontrada)
    app.run(port=5003)
