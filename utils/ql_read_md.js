
async function qlReadServerFile(url_md) {
      try {
        const response = await fetch(url_md); 

		const htmlObj  = document.getElementById('markdownOut')

        if (!response.ok) throw new Error(`HTTP XCP: ${response.status}`);
        const text = await response.text();
		  const htmlTxt = marked.parse(text);
        htmlObj.textContent = htmlTxt;
      } catch (error) {
        htmlObj.textContent = 'XCP fetch file: ' + error.message;
      }

    }
