document.addEventListener('DOMContentLoaded', async () => {
    const fileinput = document.getElementById('challenge_input') as HTMLInputElement
    
    fileinput.addEventListener('input', async () =>{
        if (fileinput.files != null){
            const formData = new FormData();
            const splitUrl = window.location.href.split('/challenge/')

            formData.append('image', fileinput.files[0])
            formData.append('url', splitUrl[0]);
    
            const response = await fetch(`/join/${splitUrl[1]}`, {
                method: "POST",
                body: formData
            });
    
            if (response.ok) {
                alert("챌린지 참여가 완료되었습니다.");
            } else{
                alert("챌린지 참여에 실패하였습니다. 다시 시도해주세요.");
            }
        }
    });
});