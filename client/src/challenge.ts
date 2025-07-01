function load_challenge(responseText: string, challenge_list: HTMLDivElement) {
    const data = JSON.parse(responseText);
    for (let index = 0; index < data.length; index++) {
        const i = data[index];
        const challenge = `<div class="row g-0 challenge-item">
                <a class="col-auto challenge-img-box" href="/challenge/${i["챌린지_ID"]}">
                    <img src="${i["챌린지_아이콘"]}" alt="챌린지 이미지 1">
                </a>
                <div class="col challenge-main">
                    <div class="row challenge-header">
                        <div class="col-auto challenge-title">
                            <h3>${i["챌린지_제목"]}</h3>
                        </div>
                        <div class="col-auto challenge-user">
                            <span>${i["챌린지_작성자"]}</span>
                        </div>
                    </div>
                    <div class="challenge-desc">${i["챌린지_설명"]}</div>
                    <div class="challenge-hashtag">${i["챌린지_태그"][0]}</div>
                </div>
                <div class="challenge-divider d-none d-md-block"></div>
                <div class="col-auto challenge-side">
                    <span class="challenge-period">참여기간 : ${i["챌린지_시작기한"]+'~'+i["챌린지_종료기한"]}</span>
                    <span class="challenge-participants">현재 참여 인원 : ${i["챌린지_참여자"].length}명</span>
                    <div class="challenge-side-bottom">
                        <div class="challenge-cheer" data-id="${i["챌린지_ID"]}">
                            <i class="bi bi-fire"></i>
                            <span>${i["챌린지_응원수"]}</span>
                        </div>
                        <i class="challenge-share bi bi-share" data-id="${i["챌린지_ID"]}"></i>
                        <a type="button" class="btn challenge-join-btn btn-secondary" href="/challenge/${i["챌린지_ID"]}">상세 정보</a>
                    </div>
                </div>
            </div>`;
        challenge_list.appendChild(
            new DOMParser().parseFromString(challenge, 'text/html').body.firstChild as HTMLElement
        );
    }
}

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
        const responseText = await response.text();
        if (responseText == "참여한 챌린지가 없습니다.") {
            challenge_list.innerHTML = `<h2>참여한 챌린지가 없습니다.</h2>
            <a type="button" class="btn btn-primary btn-lg" href="/#challenges">참여 가능한 챌린지 확인하기</a>`;
            return;
        }
        challenge_list.innerHTML = ''; // 로딩 표시를 제거하고 챌린지 목록을 비웁니다.
        load_challenge(responseText, challenge_list); // 챌린지 목록을 로드합니다.
    } else {
        const responseText = await response.text();
        console.error("Error fetching today's challenge:", responseText);
    }

    // 챌린지 공유 버튼 이벤트 리스너 추가
    Array.from(document.getElementsByClassName("challenge-share")).forEach((element) => {
        if (element) {
            element.addEventListener("click", () => {
                const id = element.getAttribute("data-id");
                const url = `${window.location.origin}/challenge/${id}`;
                
                window.navigator.clipboard.writeText(url).then(() => {
                    alert("챌린지 공유 링크를 복사했습니다!");
                });
            });
        }
    });

    // 챌린지 응원 버튼 이벤트 리스너 추가
    Array.from(document.getElementsByClassName("challenge-cheer")).forEach((element) => {
        if (element) {
            element.addEventListener("click", async () => {
                const id = element.getAttribute("data-id");
                const formData = new FormData();
                formData.append("challenge_id", id || "");

                const response = await fetch("/cheer", {
                    method: "POST",
                    body: formData,
                })

                if (response.ok) {
                    alert("해당 챌린지를 응원합니다. 취소할 수 없습니다.")
                } else {
                    alert("이미 응원한 챌린지입니다.");
                }
            });
        }
    });
});