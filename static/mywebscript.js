/* Connect the IBM starter HTML to the Flask /emotionDetector route. */
function RunSentimentAnalysis() {
    const textToAnalyze = document.getElementById("textToAnalyze").value;
    const systemResponse = document.getElementById("system_response");

    if (!textToAnalyze.trim()) {
        systemResponse.textContent = "Invalid text! Please try again!";
        return;
    }

    fetch("/emotionDetector?textToAnalyze=" + encodeURIComponent(textToAnalyze))
        .then((response) => response.text().then((text) => ({
            ok: response.ok,
            text: text,
        })))
        .then((result) => {
            systemResponse.textContent = result.text;
        })
        .catch(() => {
            systemResponse.textContent = "Service unavailable. Please try again.";
        });
}
