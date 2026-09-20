\# AI Research Agent



An AI-powered research agent that searches the web and provides brief answers with source links.



\## Features



\- Web search

\- AI-generated brief answers

\- Multiple questions

\- Source links

\- Dark-themed frontend

\- Flask backend

\- Groq API integration



\## Technologies



\- Python

\- Flask

\- Groq API

\- DuckDuckGo Search

\- HTML

\- CSS



\## Project Structure



```text

ai-research-agent/

│

├── app.py

├── README.md

├── .gitignore

└── templates/

&#x20;   └── index.html

````



\## Installation



Install the required packages:



```bash

pip install flask openai ddgs

```



\## API Key



Set your Groq API key as an environment variable.



Windows CMD:



```cmd

set GROQ\_API\_KEY=your\_groq\_api\_key

```



\## Run



```cmd

python app.py

```



Then open:



```text

http://127.0.0.1:5000/

```



\## Security



Never upload your Groq API key to GitHub.



````



Save and close Notepad.



\---



\# Part 7 — Upload your project to GitHub



Now we connect your computer folder to the repository you created in the GitHub app.



First check whether Git is installed:



```cmd

git --version

````



If you get something like:



```text

git version 2.x.x

```



you're ready.



Then:



```cmd

git init

```



Then:



```cmd

git add .

```



Then:



```cmd

git commit -m "Initial AI research agent"

```



Then:



```cmd

git branch -M main

```



\---



\# Part 8 — Connect to your GitHub repository



Open your repository in the GitHub app.



Tap \*\*Code\*\* or the repository's clone option and copy the \*\*HTTPS URL\*\*.



It will look approximately like:



```text

https://github.com/YOUR\_USERNAME/ai-research-agent.git

```



Then in CMD:



```cmd

git remote add origin YOUR\_REPOSITORY\_URL

```



For example:



```cmd

git remote add origin https://github.com/yourusername/ai-research-agent.git

```



Then:



```cmd

git push -u origin main

```



Git may ask you to authenticate with GitHub.



\---



\# Part 9 — Check your GitHub app



Go back to the GitHub app and open:



\*\*Your profile → Repositories → ai-research-agent\*\*



You should see:



```text

📄 app.py

📄 README.md

📄 .gitignore

📁 templates

```



Open `templates` and you should see:



```text

📄 index.html

```



That's your complete project repository.



\### One thing I strongly recommend



Before you run `git push`, run:



```cmd

git status

```



and:



```cmd

git diff --cached

```



If you see your actual `gsk\_...` Groq key anywhere, \*\*stop\*\* and don't push it.



If you want, I can next walk you through \*\*the GitHub app screen-by-screen first\*\*, then we'll do the CMD upload together.



