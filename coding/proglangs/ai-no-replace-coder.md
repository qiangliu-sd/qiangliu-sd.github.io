# Will software developers be replaced by LLM-AI?
    Not yet, my experiments with Gemini CLI and Copilot show!

Across the board, software developers are concerned about the rapid advancement of LLM-based AI. And rightfully so, but somewhat superficially.

Nowadays, I use **Gemini CLI** and **Copilot** a lot. For example, I asked Gemini CLI to write Python methods with the following prompt:

> write Python functions with the following features: 
A GUI with a button; clicking button will open a file dialog, ask to choose a docx file, and convert it into html; save html to a place with a name chosen by the user;
Treat http links as href;
Handle bold and/or italic correctly;
handle images and tables;
handle footnotes with bidirectional links;
name argument with pattern lowercase_lowercase;
name local variable with pattern lowercaseUppercase

Gemini did it quickly, using **pypandoc**. Asked to download pypandoc, Gemini did. Asked to run the script, Gemini told me to install **pandoc**. Asked to install pandoc, Gemini said it could not.

Then I asked Gemini to rewrite the script without using pandoc. Gemini obliged and used **mammoth** instead. And it works!

The other day, Copilot wrote the function to turn my Windows PC into a web server for me. Based on this code, I created the App for [Turn your Windows into a HTTP server](https://github.com/qiangliu-sd/folder-sharing-via-web).

For specific short one-function coding requests, I find that Gemini CLI and Copilot do an excellent job if you provide the **right** prompts.

Unfortunately or fortunately, though, **both Gemini and Copilot fail when the task is complex, new, or not widely used**.

When I tried to learn PyScript for HTML, I asked Copilot to
> write a simple page with one button. When the button is clicked, PyScript will take two inputs and combine them into a single message displayed on the page.

Copilot failed to provide a working example after almost **ten** tries.

Eventually, I made it to work on my own after searching online without finding any examples. So I put this simple [PyScript in HTML](https://github.com/qiangliu-sd/web) on GitHub.

When I used it to check weather, Gemini offered me an HTML with real-time data via Gemini API with Google Search and JavaScript. After **seven iterations with 14 tries** without success, I gave up on Gemini. Gemini confessed as follows, and I quote Gemini here directly:

> You are absolutely right to be frustrated. My sincere apologies for the continued failures. The issue isn't on your end or even with the code itself, but with the **fundamental limitations of using a large language model** like the Gemini API for a task that requires perfectly structured data.

> The core problem is this: even when we ask the Gemini model to provide a precise JSON or text format, it is **not an exact data extraction tool**. It's a creative and conversational tool, and it can sometimes fail to follow strict formatting rules, which causes the application to crash.

That is quite frank and eloquent, I have to say! 

Incidentally, [my weather AI agent](https://github.com/qiangliu-sd/ai-agent-LangGraph), with about 40 lines of code, works great.

In conclusion, **software developers will not be replaced by LLM-AI**, at least not yet. On the other hand, used correctly, **LLM-AI can be an excellent assistant to developers**.