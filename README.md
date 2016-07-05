# Persea

## Personal search engine project  
  
In current search engines, user are consumers of information but have no practical mechanism to generate and add information into the search engine.  This is despite the fact that often times information that a user might generate would be amongst the most relevant to them.   This project is a first step closing that gap.

For this project, I decided to use a dump of [stackoverflow](http://stackoverflow.com) for the core search engine.  I find myself searching the same question on stackoverflow over and over again (usually something of the form: "how do I do X in python" or "how do I do X in pandas") and for each search, I typically spend 10 minutes going through the different question/answers until I find one that provides the answer I want with a code example I can use.  I wanted to have a way to save away that distilled result and have a seamless way to recover that result next time I do a search for the same or a similar question.

Persea is a web app that allows the user to search and browse the stackoverflow database and add entries to a personal database that is searched in conjunction with the search of the stackoverflow database.  Currently the search engine is still in an early beta stage.

Here's a screenshot of Persea:
![alt text](https://github.com/knpatel401/Persea/images/persea.png "Persea Screenshot")

Here's a block diagram of Persea:
![alt text](https://github.com/knpatel401/Persea/images/block_diagram.png "Persea block diagram")

