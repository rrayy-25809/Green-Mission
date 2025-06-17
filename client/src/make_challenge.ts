document.addEventListener('DOMContentLoaded', async () => {
    const make_challenge = document.getElementById("make_challenge");

    if (make_challenge) {
        make_challenge.addEventListener("submit", async (event) => {
            event.preventDefault(); // Prevent the default form submission behavior
            const formData = new FormData(make_challenge as HTMLFormElement);
            console.log(formData)
            const response = await fetch("/make_challenge", {
                method: "POST",
                body: formData,
            });
            if (response.ok) {
                alert("챌린지 제작 성공!")
            } else {
                alert("챌린지 제작 실패");
            }
        });
        }
});