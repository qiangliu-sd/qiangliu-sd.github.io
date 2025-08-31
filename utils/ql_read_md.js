
async function qlReadServerFile(url_md) {
      try {
        const response = await fetch(url_md); 
		// LOAD the ql_read_md.js, which contains this function (qlReadServerFile), after markdownOut is defined
		const htmlObj  = document.getElementById('markdownOut')

        if (!response.ok) throw new Error(`HTTP XCP: ${response.status}`);
        const text = await response.text();
		  // LOAD utils/marked.min.js before calling marked.parse
		  const htmlTxt = marked.parse(text);
        htmlObj.innerHTML = htmlTxt;
      } catch (error) {
        htmlObj.innerHTML = 'XCP fetch file: ' + error.message;
      }

    }

