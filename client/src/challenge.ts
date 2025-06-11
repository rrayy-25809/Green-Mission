document.addEventListener('DOMContentLoaded', async () => {
    const challenge_list = document.getElementsByClassName("challenge-list")[0] as HTMLDivElement;
    if (!challenge_list) { // 챌린지 기능이 필요 없을 경우 예외 처리(그럴리는 없겠지만 혹시 모르니까)
        console.error("Challenge list element not found.");
        return;
    }

    const loading = `<div id="loading-overlay">
      <div class="spinner-border text-secondary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>`; // 로딩 표시를 위한 HTML 코드
    challenge_list.innerHTML = loading; //innerHTML를 사용하면 기존의 내용을 모두 지우고 새로운 내용을 삽입

    let path = "";
    if (window.location.pathname == "/mypage") {
        path = "/user";
    } else if (window.location.pathname.startsWith("/challenge")) {
        path = window.location.pathname.replace("/challenge", "");
    } else{
        path = "/s"
    }

    const response = await fetch(`/challenge${path}`, {
        method: "POST",
    });

    if (response.ok) {
        challenge_list.innerHTML = ''; // 로딩 표시를 제거하고 챌린지 목록을 비웁니다.
        const data = await response.json();
        for (let index = 0; index < data.length; index++) {
            const i = data[index];
            const challenge = `<div class="row g-0 challenge-item">
                <div class="col-auto challenge-img-box">
                    <img src="${i["챌린지 아이콘"]}" alt="챌린지 이미지 1">
                </div>
                <div class="col challenge-main">
                    <div class="row challenge-header">
                        <div class="col-auto challenge-title">
                            <h3>${i["챌린지 제목"]}</h3>
                        </div>
                        <div class="col-auto challenge-user">
                            <span>${i["챌린지 작성자"]}</span>
                        </div>
                    </div>
                    <div class="challenge-desc">${i["챌린지 설명"]}</div>
                    <div class="challenge-hashtag">#${'태준함'}</div>
                </div>
                <div class="challenge-divider d-none d-md-block"></div>
                <div class="col-auto challenge-side">
                    <span class="challenge-period">참여기간 : ${'2025.06.02~2025.06.04'}</span>
                    <span class="challenge-participants">현재 참여 인원 : ${1}명</span>
                    <div class="challenge-side-bottom">
                        <div class="challenge-cheer">
                            <i class="bi bi-fire"></i>
                            <span>1</span>
                        </div>
                        <i class="challenge-share bi bi-share"></i>
                        <a type="button" class="btn challenge-join-btn btn-secondary">참여요청</a>
                    </div>
                </div>
            </div>`;
            challenge_list.appendChild(
                new DOMParser().parseFromString(challenge, 'text/html').body.firstChild as HTMLElement
            );
        }
    } else {
        const responseText = await response.text();
        console.error("Error fetching today's challenge:", responseText);
    }
});