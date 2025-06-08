document.addEventListener('DOMContentLoaded', async () => {
    const response = await fetch(`/mypage`, {
        method: "POST",
    });

    if (response.ok) {
        const data = await response.json();
        console.log(data);

        const userInfo = document.getElementsByClassName("mypage-info-container")[0];
        userInfo.innerHTML = `<div class="profile-section">
            <img class="profile-image" src="${data["프로필 사진"]}" alt="클릭하여 프로필 사진 변경"></img>
        </div>
        <div class="info-section">
            <div class="user-name">${data["유저명"]}</div>
            <div class="user-email">${data["이메일"]}</div>
            <div class="user-role">사용자 역할 : ${data["사용자 역할"]}</div>
            <div class="challenge-count">성공한 챌린지 수 : ${10}</div>
            <div class="join-date">${data["가입일"]}에 가입하셨습니다.</div>
        </div>
        <div class="button-section">
            <a class="btn btn-mypage-info" href="/logout">로그아웃</a>
            <a class="btn btn-mypage-info" href="/delete_account">계정 탈퇴하기</a>
        </div>`;
    } else {
        
    }
});