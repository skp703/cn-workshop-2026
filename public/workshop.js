(() => {
  function initialize() {
    const root = document.documentElement;
    const choices = [...document.querySelectorAll("[data-path-choice]")];
    const descriptions = [...document.querySelectorAll("[data-path-description]")];

    function setPath(path, persist = true) {
      if (path !== "core" && path !== "gee") return;
      root.dataset.path = path;
      choices.forEach((button) => {
        const selected = button.dataset.pathChoice === path;
        button.setAttribute("aria-pressed", String(selected));
      });
      descriptions.forEach((description) => {
        description.hidden = description.dataset.pathDescription !== path;
      });
      if (persist) {
        try {
          localStorage.setItem("cn-workshop-path", path);
        } catch {
          // Storage may be unavailable in privacy-restricted browser contexts.
        }
      }
    }

    choices.forEach((button) => {
      button.addEventListener("click", () => setPath(button.dataset.pathChoice));
    });

    try {
      setPath(localStorage.getItem("cn-workshop-path") || "core", false);
    } catch {
      setPath("core", false);
    }
  }

  if (document.readyState === "complete") initialize();
  else window.addEventListener("load", initialize, { once: true });
})();
