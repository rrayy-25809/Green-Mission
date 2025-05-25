import subprocess
import sys
import server.main as server

# Vite 앱 빌드
try:
    process = subprocess.run("npm run build", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')  # Vite 빌드 명령어 실행
    
    # 실시간 로그 출력
    for line in process.stdout:
        print(line, end="")
    for line in process.stderr:
        print(line, end="")

    if process.returncode != 0:
        print("❌ 빌드 실패!")
        sys.exit(1)  # 빌드 실패 시 프로그램 종료
except Exception as e:
    print(f"🚨 오류 발생: {e}")
    sys.exit(1)

# 서버 실행
if hasattr(server, "flask"):
    server.flask.run(debug=True, host="0.0.0.0")
else:
    print("❌ server.main에 flask 객체가 없습니다!")
    sys.exit(1)
