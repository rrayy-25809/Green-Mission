const make_challenge = document.getElementById("make_challenge");

if (make_challenge) {
    make_challenge.addEventListener("submit", async (event) => {
        event.preventDefault(); // Prevent the default form submission behavior
        const formData = new FormData(make_challenge as HTMLFormElement);
        formData.append('url', window.location.href.replace("/make_challenge",""));

        const response = await fetch("/make_challenge", {
            method: "POST",
            body: formData,
        });

        if (response.ok) {
            alert("챌린지 제작 성공!");
            window.location.href = "/"; // Redirect to the home page or another page
        } else {
            alert(await response.text());
        }
    });
}
