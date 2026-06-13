function sanitizeTitle(rawText, fallbackText) {
    let cleanText = rawText.trim();
    return (cleanText === '') ? fallbackText : cleanText;
}