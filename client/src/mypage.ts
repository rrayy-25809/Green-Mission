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

    footprint.addEventListener('mousemove', (event) => {
        // Code to execute when the mouse moves over 'myElement'
        const card = document.querySelector('.goal-card') as HTMLElement;
        card.style.left = `${event.clientX - 50}px`;
        card.style.top = `${event.clientY - 50}px`;
        console.log(`Mouse moved to: ${event.clientX}, ${event.clientY}`);
    });
});
