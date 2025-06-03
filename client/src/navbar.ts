document.addEventListener("DOMContentLoaded", () => {
    const navbarHtml = `
    <nav class="navbar" data-bs-theme="light">
        <a type="button" class="btn btn-secondary" href="/mypage">마이 페이지</a>
        <a type="button" class="btn btn-secondary" href="/login">로그인</a>
    </nav>`;

    const navbarPlaceholder = document.getElementById('navbar-placeholder') as HTMLDivElement;
    navbarPlaceholder.innerHTML = navbarHtml;
});