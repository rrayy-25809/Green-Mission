document.addEventListener('DOMContentLoaded', async () => {
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
            goalText.innerText = `목표 ${index + 1}의 내용입니다. 여기에 목표에 대한 자세한 설명을 추가할 수 있습니다.`;
        });

        circle.addEventListener('mouseleave', () => {
            card.style.display = 'none'; // 마우스가 떠나면 카드 숨김
        });
    });
});
