# discordurldatabase
collect URLs shared in a discord server into a single database

I started this project as a small effort for the Boot.dev project assignement. Beause we focused 500+ lessons on python i wanted to attack this challenge in that language. 
## What is this
I have a discord with a bunch of IRL friends that has been going for 8 years, i wanted a way to capture the informaiton we have shared over the years and get some analytics on who is active, who havnt we heard from in awhile etc. 



## Things I Learned
1. I believe this could have been factored as classes but im not 100% sure how that is supposed to look.
2. This started out monolthic and i broke it out into components. I was particluarly happy with the ability to add more commands in a single file and not have to worry about other parts of the codes being impacted. 
3. When designing how i wanted this to function i ran into a few issues, there were a lot of things that i would consider to be Dev Ops more related issues which are good to encounter and resolve. 
    - Postgres self hosted and setup
    - UTF encoding! Lol this was a fun error of how to solve with the least amount of code. 
    - Librarys and documentation, discord library has a lot of gotchas that you will trial and error through like having to await to send a message and the decorator use for command designation. 
4. Github has some enhanced features when a dev pushes a commit with a sensitive token in it. This lead me down a rabbit hole of learning all about rebase the hard way. I came out of it better for this error and lessong in opsec. 
5. Speaking of rebase, i spent a ton of time setting up SSH for verified commits on github and fixing the unverified commits. Do not want to have to do this on a more active repo but i am in a better spot if i do encounter it in the future. 
6. Permission handling
    - Discord bots have a ton of setup and permissioning just to get added to a server, this makes it difficult to add a scraping bot using the Discord API, it is still possible to scrape servers with playwright or something through the web ui. 
    - Once the bot was in server there was still some handling to take place where the bot may not have access to the channel and that needs to be handled gracefully. 
7. Environment variables, use them and learn to love them. Being able to have specific configurations for a project. I still dont know how to save these important secrets if a computer was lost, there are ways to hash and encrypt this data but i still feel that there is something too human that may impact. Wil be looking for a selfhosted solution for secrets vault like i have for passwords. 

## Whats next?
For me this itch has been scratched, i dont plan to put more time into this. 
I may figure out how to make this into a docker container and set it up to always keep the data updated and preservered but not a priority. 

This can be extended with new commands easily as well as expanded to support multiple servers quite easily. 

    Add Guild Information to Database and CSV Logging:

    Include the guild_id when logging URLs to the database and CSV file.
    Ensure that guild-specific data is fetched and processed correctly.
    Update Data Extraction and Logging:

    Modify extract_and_log_urls to include the guild ID.
    Update the database schema to store the guild ID.
    Update Command Handlers and Event Listeners:

    Ensure commands and event listeners are aware of the guild context.


