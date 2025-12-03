
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

async function loadAndRenderMarkdown(title_id, he_id, url_md) {
  const mdText = await fetchMarkdown(url_md);
  const mdHtml = marked.parse(mdText);
	const parser = new DOMParser();
	const doc = parser.parseFromString(mdHtml, "text/html");
	const h1 = doc.querySelector("h1");
      
  document.getElementById(title_id).textContent = h1?.textContent;
  document.getElementById(he_id).innerHTML = mdHtml;
}

function getUrlParams() {
	const queryString = window.location.search;
	const urlParams = new URLSearchParams(queryString);
	const params = {};
	for (const [key, value] of urlParams.entries()) {
		params[key] = value;
	}
	return params;
}

