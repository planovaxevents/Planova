document.addEventListener("DOMContentLoaded", () => {
    let user = JSON.parse(localStorage.getItem("planova_user"));
    const navRight = document.querySelector(".nav-right");

    if (!navRight) return;

    // Hide Sign In / Register buttons on auth pages
    const path = window.location.pathname;

    const isAuthPage =
        path.includes("signin.html") ||
        path.includes("register.html");

    if (isAuthPage) {
        navRight.innerHTML = "";
        return;
    }

    // Normal navbar behaviour
    if (user) {
        navRight.innerHTML = `
            <div class="user-icon" onclick="window.location.href='profile.html'">
                <a href="account.html" class="nav-user-btn">Account</a>
            </div>
        `;
    } else {
        navRight.innerHTML = `
            <a href="signin.html" class="nav-btn">Sign In</a>
            <a href="register.html" class="nav-btn">Register</a>
        `;
    }
});