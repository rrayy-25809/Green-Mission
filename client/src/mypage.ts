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
            <input type="file" id="selectedFile" style="display: none;" />
            <input class="btn btn-light" type="button" value="파일변경" onclick="document.getElementById('selectedFile').click();" />
        </div>
        <div class="info-section">
            <div class="user-name">${data["유저명"]}</div>
            <div class="user-email">${data["이메일"]}</div>
            <div class="user-role">사용자 역할 : ${data["사용자 역할"]}</div>
            <div class="challenge-count">참여한 챌린지 수 : ${data["참여한 챌린지"].length}</div>
            <div class="join-date">${data["가입일"]}에 가입하셨습니다.</div>
        </div>
        <div class="button-section">
            <a class="btn btn-mypage-info" href="/logout">로그아웃</a>
            <a class="btn btn-mypage-info" href="/delete_account">계정 탈퇴하기</a>
        </div>`;
    } else {
        alert("마이페이지에서 정보를 불러오는데 실패했습니다. 다시 시도해 주세요.");
    }
    
    const fileinput = document.getElementById('selectedFile') as HTMLInputElement
    
    fileinput.addEventListener('input', async () =>{
        if (fileinput.files != null){
            const formData = new FormData();
            formData.append('image', fileinput.files[0])
            formData.append('url', window.location.href.replace("/mypage",""))
    
            const response = await fetch('/change_profile', {
                method: "POST",
                body: formData
            });
    
            if (response.ok) {
                alert("프로필 사진을 변경하셨습니다. 새로고침 해 주세요");
            } else{
                alert("프로필 사진 변경에 실패하였습니다.");
            }
        }
    });
});
