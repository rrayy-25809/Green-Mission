import 'bootstrap/dist/js/bootstrap.bundle.min.js';

// 페이지 제목 설정
const path = window.location.pathname;
let title = 'Green Mission';

switch (path) {
    case '/':
        title = 'Green Mission - 홈';
        break;
    case '/mypage':
        title = 'Green Mission - 마이페이지';
        break;
    case '/login':
        title = 'Green Mission - 로그인';
        break;
    case '/signup':
        title = 'Green Mission - 회원가입';
        break;
    default:
        title = 'Green Mission - '+path.split('/')[0]
}
document.title = title;

document.addEventListener("DOMContentLoaded", () => {
    const navbarHtml = `
    <nav class="navbar" data-bs-theme="light">
        <a type="button" class="btn btn-dark" href="/mypage">마이 페이지</a>
        <a type="button" class="btn btn-dark" href="/login">로그인</a>
    </nav>`;

    const footerHtml = `<p>© 2025 Green Mission</p>
    <p>이 사이트는 Green Mission의 공식 웹사이트입니다.</p>
    <p>Green Mission은 <a href="https://idg.icehs.kr/main.do">인천대건고등학교</a> 소속의 학생들이 만든 단체이며 환경 보호 챌린지 서포팅을 목표로 합니다.</p>
    <p>이 사이트는 오픈소스로 개발되었으며, <a href="https://github.com/rrayy-25809/Green-Mission">GitHub</a>에서 소스 코드를 확인할 수 있습니다.</p>
    <p>이 사이트는 <a href="https://www.gnu.org/licenses/gpl-3.0.html">GNU General Public License v3.0</a>에 따라 라이선스가 부여됩니다.</p>`;
            
    const navbarPlaceholder = document.getElementById('navbar-placeholder') as HTMLDivElement;
    navbarPlaceholder.innerHTML = navbarHtml;

    const footerPlaceholder = document.getElementsByClassName('footer')[0] as HTMLDivElement;
    footerPlaceholder.innerHTML = footerHtml;
});