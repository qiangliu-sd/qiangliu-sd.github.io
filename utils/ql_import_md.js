
async function fetchMarkdown(url) {
  try {
	const response = await fetch(url);
	if (!response.ok) throw new Error(`HTTP XCP: ${response.status}`);
	const markdownText = await response.text();
	return markdownText;
  } catch (error) {
	console.error("Failed to fetch markdown:", error);
	return `XCP: ${error.message}`;
  }
}

async function loadAndRenderMarkdown(he_id, url_md) {
  const mdText = await fetchMarkdown(url_md);
  const mdHtml = marked.parse(mdText);
  document.getElementById(he_id).innerHTML = mdHtml;
}