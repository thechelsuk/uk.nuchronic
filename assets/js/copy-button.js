function fallbackCopy(text) {
    var textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.setAttribute("readonly", "");
    textarea.style.position = "absolute";
    textarea.style.left = "-9999px";
    document.body.appendChild(textarea);
    textarea.select();
    try {
        document.execCommand("copy");
    } catch (err) {
        /* clipboard unavailable; nothing more we can do */
    }
    document.body.removeChild(textarea);
}

document.querySelectorAll(".copy-button").forEach(function (button) {
    button.addEventListener("click", function () {
        var target = document.getElementById(button.getAttribute("data-copy-target"));
        if (!target) {
            return;
        }

        var text = target.textContent;
        var label = button.querySelector(".copy-button-label");

        var showCopied = function () {
            button.classList.add("is-copied");
            if (label) {
                label.textContent = "Copied";
            }
            setTimeout(function () {
                button.classList.remove("is-copied");
                if (label) {
                    label.textContent = "Copy";
                }
            }, 1600);
        };

        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(text).then(showCopied, function () {
                fallbackCopy(text);
                showCopied();
            });
        } else {
            fallbackCopy(text);
            showCopied();
        }
    });
});
