const loginForm = document.getElementById("signup-form");

if (loginForm) {
  loginForm.addEventListener("submit", async (event) => {
    event.preventDefault(); // Prevent the default form submission behavior
    const formData = new FormData(loginForm as HTMLFormElement);
    const response = await fetch("/signup", {
      method: "POST",
      body: formData,
    });
    if (response.ok) {
      window.location.href = "/";
    } else {
      alert("회원가입 실패");
    }
  });
}