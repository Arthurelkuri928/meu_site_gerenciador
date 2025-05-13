from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return """
        <html>
            <head>
                <title>Deploy bem-sucedido</title>
                <style>
                    body {
                        font-family: 'Segoe UI', sans-serif;
                        background-color: #0d1117;
                        color: #e6edf3;
                        text-align: center;
                        padding: 100px;
                    }
                    h1 {
                        color: #58a6ff;
                        font-size: 2.5em;
                    }
                    p {
                        font-size: 1.2em;
                        margin-top: 20px;
                    }
                </style>
            </head>
            <body>
                <h1>🚀 Deploy realizado com sucesso</h1>
                <p>A aplicação está no ar.</p>
                <p>Conecte ao banco de dados MySQL para habilitar funcionalidades completas.</p>
            </body>
        </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
