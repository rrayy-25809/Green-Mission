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
    case '/mission':
        title = 'Green Mission - 미션';
        break;
    default:
        title = 'Green Mission - '+path.replace('/', '');
}
document.title = title;

