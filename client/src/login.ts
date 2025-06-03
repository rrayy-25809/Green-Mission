const loginForm = document.getElementById("login-form");

if (loginForm) {
  loginForm.addEventListener("submit", async (event) => {
    event.preventDefault(); // Prevent the default form submission behavior
    const formData = new FormData(loginForm as HTMLFormElement);
    const response = await fetch("/login", {
      method: "POST",
      body: formData,
    });
    if (response.ok) {
      window.location.href = "/";
    } else {
      alert("로그인 실패");
    }
  });
}