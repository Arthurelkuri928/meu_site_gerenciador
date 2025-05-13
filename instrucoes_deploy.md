 # Instruções para Deploy Manual da Aplicação Flask

Este guia descreve os passos para realizar o deploy manual da aplicação `meu_site_gerenciador` em um ambiente de sua escolha.

## Pré-requisitos

1.  **Python 3.8+ e Pip:** Certifique-se de que Python e pip estão instalados no servidor de deploy.
2.  **Servidor MySQL:** A aplicação requer um servidor MySQL acessível. Você precisará das credenciais (host, porta, usuário, senha, nome do banco de dados).
3.  **Git (opcional):** Para clonar o repositório, se aplicável.
4.  **Virtualenv (recomendado):** Para isolar as dependências do projeto.

## Passos para o Deploy

1.  **Transferir os Arquivos do Projeto:**
    *   Descompacte o arquivo `meu_site_gerenciador.zip` no diretório desejado no seu servidor.

2.  **Configurar o Ambiente Virtual (Recomendado):**
    ```bash
    cd caminho/para/meu_site_gerenciador
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instalar as Dependências:**
    *   Com o ambiente virtual ativado, instale as dependências listadas no arquivo `requirements.txt`:
        ```bash
        pip install -r requirements.txt
        ```

4.  **Configurar Variáveis de Ambiente para o Banco de Dados:**
    *   A aplicação utiliza variáveis de ambiente para a configuração do banco de dados MySQL. Exporte as seguintes variáveis antes de iniciar a aplicação:
        ```bash
        export DB_USERNAME=\"seu_usuario_mysql\"
        export DB_PASSWORD=\"sua_senha_mysql\"
        export DB_HOST=\"seu_host_mysql\" # Ex: localhost ou IP do servidor DB
        export DB_PORT=\"sua_porta_mysql\"  # Ex: 3306
        export DB_NAME=\"seu_banco_de_dados_mysql\"
        export SECRET_KEY=\"uma_chave_secreta_bem_forte_e_aleatoria\" # Gere uma chave segura para produção
        ```
    *   **Importante:** Substitua os valores entre aspas pelos seus dados reais. Para a `SECRET_KEY`, utilize uma string longa, aleatória e segura.

5.  **Inicializar o Banco de Dados (se necessário):**
    *   O `main.py` já inclui `db.create_all()` dentro do contexto da aplicação, o que deve criar as tabelas automaticamente na primeira execução se elas não existirem. Certifique-se de que o banco de dados (`DB_NAME`) já existe no servidor MySQL e que o usuário (`DB_USERNAME`) tem permissões para criar tabelas nele.

6.  **Executar a Aplicação com um Servidor WSGI (Recomendado para Produção):**
    *   Para produção, não utilize o servidor de desenvolvimento do Flask (`app.run()`). Em vez disso, use um servidor WSGI como Gunicorn ou uWSGI.
    *   **Exemplo com Gunicorn:**
        1.  Instale o Gunicorn (se ainda não estiver no `requirements.txt`, adicione-o e reinstale as dependências):
            ```bash
            pip install gunicorn
            ```
        2.  Execute a aplicação com Gunicorn (a partir do diretório raiz do projeto `meu_site_gerenciador`):
            ```bash
            gunicorn --bind 0.0.0.0:8000 src.main:app
            ```
            Isso iniciará a aplicação na porta 8000, acessível por todos os IPs. Ajuste a porta conforme necessário.
            O `src.main:app` refere-se ao arquivo `main.py` dentro do diretório `src` e à instância `app` do Flask dentro desse arquivo.

7.  **Configurar um Servidor Web como Proxy Reverso (Opcional, mas Recomendado):**
    *   Para funcionalidades como SSL/TLS, servir arquivos estáticos de forma eficiente e balanceamento de carga, configure um servidor web como Nginx ou Apache para atuar como um proxy reverso para o Gunicorn.
    *   **Exemplo de configuração básica do Nginx:**
        ```nginx
        server {
            listen 80;
            server_name seu_dominio.com www.seu_dominio.com;

            location /static {
                alias /caminho/para/meu_site_gerenciador/src/static;
            }

            location / {
                proxy_pass http://127.0.0.1:8000; # Endereço onde o Gunicorn está rodando
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
            }
        }
        ```
        Lembre-se de ajustar os caminhos e o `server_name`.

## Considerações Adicionais

*   **Segurança:** Certifique-se de que as credenciais do banco de dados e a `SECRET_KEY` não sejam expostas publicamente. Utilize variáveis de ambiente ou um sistema de gerenciamento de segredos.
*   **Logs:** Configure o Gunicorn e o servidor web para registrar logs de acesso e erro, facilitando o monitoramento e a depuração.
*   **Arquivos Estáticos:** Em produção, é mais eficiente servir arquivos estáticos diretamente pelo servidor web (Nginx/Apache) em vez do Flask/Gunicorn.
*   **Primeiro Usuário Administrador:** Ao registrar o primeiro usuário através do formulário de registro da aplicação, ele será automaticamente definido como administrador se não houver outros administradores no sistema. Alternativamente, um administrador existente pode promover outros usuários.

Seguindo estes passos, você deverá conseguir realizar o deploy da aplicação `meu_site_gerenciador` em seu ambiente de produção.
