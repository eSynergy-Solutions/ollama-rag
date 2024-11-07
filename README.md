<strong>TO DO</strong>

<ul>
<li>Identify relevant links to feed to llm - Monday EOD</li>
<li>Scrape the HTML from them and then clean the HTML</li>
<li>Feed the text to vector DB - blocked (datastax)</li>
<li>Connect the vector to the LLM - blocked</li>
<li>Build the UI with DEFRA feel - HTML already downloaded</li>
<li>Connect UI and Backend (LLM)</li>
</ul>

<strong>Possible Improvements</strong>

<ul>
<li>Short-term memory for the model</li>
<li>The model is loosely grounded on the links. For example: feed it a url and ask it the capital of France. Ideally, it shouldn't answer (not sure about this one)</li>
<li>The RAGApplication object (rag_app.py) doesn't initialise unless a url is provided on initialisation. Need to change that (contradicts the previous point)</li>
<li>Ability to handle certain kinds of documents (currently limited to urls)</li>
<li>Refine the recursiveURLSearch.py file</li>
<li></li>
<li></li>
<li></li>
<li></li>
</ul>
