from flask import Flask, render_template
from server.routes.auth import bp as auth_bp
from server.routes.user import bp as user_bp

# 플라스크 기본 설정
flask = Flask(__name__, template_folder='../dist/client', static_folder='../dist/assets')
flask.secret_key = 'LN$oaYB9-5KBT7G'
logger = flask.logger

# 라우트 설정
flask.register_blueprint(auth_bp)
flask.register_blueprint(user_bp)

@flask.route("/") # 메인 페이지 라우트
def main():
    return render_template("index.html")
