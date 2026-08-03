import secrets
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse

app = FastAPI()
security = HTTPBasic()

USUARIO_MESTRE = "admin"
SENHA_MESTRE = "J@D@072502"

def verificar_credenciais(credentials: HTTPBasicCredentials = Depends(security)):
    is_user_ok = secrets.compare_digest(credentials.username, USUARIO_MESTRE)
    is_pass_ok = secrets.compare_digest(credentials.password, SENHA_MESTRE)
    
    if not (is_user_ok and is_pass_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/", response_class=HTMLResponse)
def painel_ferramentas(username: str = Depends(verificar_credenciais)):
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            conteudo = f.read()
        return conteudo.replace("{username}", username)
    except FileNotFoundError:
        return "<h1>Erro: Arquivo index.html não encontrado no servidor.</h1>"