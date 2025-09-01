
async function qlReadServerFile(url_md) {
	// Configure marked for cleaner output
    marked.setOptions({
      gfm: true,
      breaks: true,
      smartLists: true,
      smartypants: true
    });
	
      try {
        const response = await fetch(url_md); 
		// LOAD the ql_read_md.js, which contains this function (qlReadServerFile), after markdownOut is defined
		const htmlObj  = document.getElementById('markdownOut')

        if (!response.ok) throw new Error(`HTTP XCP: ${response.status}`);
        let md_text = await response.text();
        // Normalize line endings and trim leading spaces
        md_text = md_text.replace(/\r\n|\r/g, '\n').replace(/^\s+/gm, '');
		  // LOAD utils/marked.min.js before calling marked.parse
		  const htmlTxt = marked.parse(md_text);
        htmlObj.innerHTML = htmlTxt;
      } catch (error) {
        htmlObj.innerHTML = 'XCP fetch file: ' + error.message;
      }

    }




