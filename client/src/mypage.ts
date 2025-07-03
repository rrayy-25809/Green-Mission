document.addEventListener('DOMContentLoaded', async () => {
    const footprint = document.getElementById('my-footprint') as HTMLElement;
    const circles = footprint.querySelectorAll('circle');
    const line = footprint.querySelectorAll('line');
    
    const challenge_elm = document.getElementsByClassName('challenge-count')[0] as HTMLElement;
    const challenge_count = challenge_elm?.textContent? Number(challenge_elm.textContent.replace("참여한 챌린지 수 : ", "")): 0;
    const cheer_challenge = Number(challenge_elm.getAttribute('data-cheer-challenge')) || 0;
    const make_count = Number(challenge_elm.getAttribute('data-make-challenge')) || 0;
    
    const goal = ["그린미션 가입하기", `챌린지 달성하기 ${challenge_count}/1`, `챌린지 응원하기 ${cheer_challenge}/1\n챌린지 달성하기 ${challenge_count}/2`, `챌린지 작성하기 ${make_count}/1`, `챌린지 달성하기 ${challenge_count}/5`, `챌린지 달성하기 ${challenge_count}/8`];
    const goal_bool = [true, challenge_count >= 1, cheer_challenge >= 1 && challenge_count >= 2, make_count >= 1, challenge_count >= 5, challenge_count >= 8];

    circles.forEach((circle, index) => {
        if (goal_bool[index]) {
            circle.setAttribute("stroke","#828282")
            circle.setAttribute("fill","#4DFF00")
        } else {
            circle.setAttribute("stroke","#ADADAD")
            circle.setAttribute("fill","#E1E1E1")
        }
    });

    line.forEach((line, index) => {
        if (goal_bool[index]) {
            line.setAttribute("stroke","#828282")
            line.setAttribute("stroke-width","5")
        } else {
            line.setAttribute("stroke","#999999")
            line.setAttribute("stroke-width","2")
        }
    });

    changeprofile();
    circlehover(goal, goal_bool);
});

function circlehover(goal:string[], goal_bool:boolean[]) {
    const footprint = document.getElementById('my-footprint') as HTMLElement;
    const card = document.querySelector('.goal-card') as HTMLElement;
    const circles = footprint.querySelectorAll('circle');

    circles.forEach((circle, index) => {
        circle.addEventListener('mouseenter', () => {
            card.style.display = 'block'; // 클릭 시 카드 표시
            console.log(circle.getBoundingClientRect());
            card.style.top = `${circle.getBoundingClientRect().top + window.scrollY - 250}px`;
            card.style.left = `${circle.getBoundingClientRect().left + window.scrollX -185}px`;

            const goalText = document.getElementsByClassName('goal-content')[0] as HTMLElement;
            goalText.innerText = goal[index] || "목표가 설정되지 않았습니다.";

            if (goal_bool[index]) {
                goalText.style.color = "#4DFF00"; // 목표 달성
            } else {
                goalText.style.color = "#FF0000"; // 목표 미달성
            }
        });

        circle.addEventListener('mouseleave', () => {
            card.style.display = 'none'; // 마우스가 떠나면 카드 숨김
        });
    });
}

function changeprofile() {
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
}