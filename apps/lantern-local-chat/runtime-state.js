// Default placeholder. The batch launcher writes runtime-state.generated.js locally.
// No GPT call, no network request, no command execution from browser.
window.LANTERN_LOCAL_STATE = null;

(function loadGeneratedLanternRuntimeState() {
  if (typeof document === "undefined") return;
  const script = document.createElement("script");
  script.src = "runtime-state.generated.js?t=" + Date.now();
  script.async = false;
  script.onerror = function () {
    window.LANTERN_LOCAL_STATE = window.LANTERN_LOCAL_STATE || null;
  };
  document.head.appendChild(script);
}());
