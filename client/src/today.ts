//copilot: 페이지가 로딩되었을 때를 감지하는는 이벤트 리스너 가져와줘
document.addEventListener('DOMContentLoaded', async () => {
    const response = await fetch("/today", {
        method: "POST",
    });
    if (response.ok) {
        const responseText = await response.text();
        const todayText = document.getElementById("todayis") as HTMLElement;
        todayText.innerHTML = "";
        for (let i = 0; i < responseText.length; i++) {
            setTimeout(() => {
            todayText.innerHTML += responseText[i];
            }, i * 100); // 100ms 간격으로 한 글자씩 출력
        }
    } else {
        const responseText = await response.text();
        console.error("Error fetching today's date:", responseText);
    }
});

