from flask import Flask, render_template, request , redirect, session, flash, url_for
#import webview
# render_template  ira buscar o html dentro da pasta templates
# requeste biblioteca para fazer requisição do html
#redirect faz o redirecionamento para onde a pagina devera apontar
#session cucks do navegador, guarda informações como login
# Url_for url/caminho dinamico atraves da função que estancia

class Jogo:                     # Criando objeto jogo
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

jogo1 = Jogo('Tetris', 'Puzzle', 'Atari')
jogo2 = Jogo('God of War', 'Hack n Slash', 'PS2')        # Iniciando o objeto
jogo3 = Jogo('Formula 1', 'Corrida', 'Xbox One')
lista = [jogo1, jogo2, jogo3]                           # Passando os parametros da lista /variavel no HTML

class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha
      

usuario1 = Usuario('Douglas', 'landim', 'olamundo')
usuario2 = Usuario('Thor', 'thorzinho', 'nervosinho')
usuario3 = Usuario('Tita', 'tita', 'bagunça')        

app = Flask(__name__)  # inicio
#window = webview.create_window('teste.app', app)
app.secret_key = 'alura'        #necesario para add criptografia no login

usuarios = {usuario1.nickname : usuario1, usuario2.nickname : usuario2, usuario3.nickname : usuario3}


@app.route('/')  # ecolhendo a rota no navegador
def index():
    ip = 'http://127.0.0.1:5000/novo'
    # Criar uma variavel {{titulo}} no html/ mudar o conteudo via python
    return render_template('lista.html', titulo='jogos', jogos=lista, link=ip)



@app.route('/novo')
def novo():
    
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
       # return redirect('/login?proximaPg=novo') # Query screeam recurso que  redireciona para uma pagina
        return redirect(url_for('login', proximaPg=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')




@app.route('/criar', methods=['POST',])
def criar():
    # request faz requisição a tag [form] no html e buca pela tag [name]
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)              #append methodo de introduzir informação em lista no python
    return redirect (url_for('index'))  #Fazendo o redirecionamento para pagina inicial




@app.route('/login')
def login():
    proximaPg = request.args.get('proximaPg') # informação do query screeam passada para variavel
    return render_template('login.html', proximaPg = proximaPg) #passando variavel para o login.HTML




'''@app.route('/autenticar', methods=['POST',])
def autenticar():
    if 'olamundo' == request.form['senha']:
        session['usuario_logado'] = request.form['usuario']     #obtendo o usuario
        flash(request.form['usuario'] + ' logado com sucesso!') # mensagem de ususrio logado
        proxima_pagina = request.form['proximaPg']       # buscando informação POST no (name variavel) html               
        #return redirect('/{}'.format(proxima_pagina)) # Formatando para receber caminho da variavel
        return redirect(proxima_pagina)
    else:
        flash('Usuario incorreto!')
        return redirect(url_for('login'))'''

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha :
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + 'Logado com sucesso!')
            proxima_pagina = request.form['proximaPg']
            return redirect(proxima_pagina)
        else:
            flash('Usuario incorreto!')
        return redirect(url_for('login'))



@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Usuario deslogado!')
    return redirect(url_for('index'))

app.run(debug=True)                                                    # rodar aplicação
app.run(host='0.0.0.0', port=8080)    #definindo qual porta ira roda a aplicação

#if __name__ == '__main__':
    #webview.start()
    #usado par app ficar como desktop
