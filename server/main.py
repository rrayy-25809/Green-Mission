from flask import Flask, render_template
from server.routes.auth import bp as auth_bp
from server.routes.user import bp as user_bp
from server.routes.today import bp as today_bp
from server.routes.challenge import bp as challenge_bp
import logging

# 플라스크 기본 설정
flask = Flask(__name__, template_folder='../dist/client', static_folder='../dist/assets')
logging.getLogger('werkzeug').setLevel(logging.WARNING)
flask.secret_key = 'LN$oaYB9-5KBT7G'
flask.logger.setLevel(logging.INFO)
logger = flask.logger

# 라우트 설정
flask.register_blueprint(auth_bp)
flask.register_blueprint(user_bp)
flask.register_blueprint(today_bp)
flask.register_blueprint(challenge_bp)

@flask.route("/") # 메인 페이지 라우트
def main():
    return render_template("index.html")
