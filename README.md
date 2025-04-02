This repository is an attempt at leveling up both my data engineering skills and my pokemon go experience.

Features it will have:
  1-Quick evaluation of all pokemons in their potential for raids.
  2-Evaluation of possible evolutions.
  3-Evaluation of possible attack sets.
  4-A collection tracker to be able to hunt for Pokemons missing from a pokedex.
    4.1-accounting for pokemons in other places such as pokemon home, mainline games, let's go pikachu/let's go Eevee, Mario kart, or the legends games.
  5-Evaluation by size, making sure you keep the best possible pokemon for those showcases.
  6-Accounting for costumes, shinies and any other thing that might make it special to the user.
  7-Ability to asign roles to certain pokemon based on evaluations.
    7.1-User defined roles.
  8-Quick recomendations for evolutions an training.
    8.1-Ability to lock down a pokemon for certain leagues.
    8.2-Ability to determine which pokemon can participate in hat leagues after evolving.
    8.3-Estimations of the amount of work needed to evolve/power up a pokemon to certain level.
    8.4-Noifications if a new pokemon has the potential to replace/surpass a pokemon on their role.
  9-Simulation of raids and specific battles to find the best team for the encounter.

How it works and why, given the insane amount of data it would need to balance and update just to check for 9300 potential pokemons in the pokemon go app alone, and because it is good practice, I will try to use a mix beteen relational databases and data processing to find the best pokemon each time. I chose PostgresSQL as my RDBMS and Python for this project.

Currently using the PSYCOPG2 and Pandas modules, will update as they're needed in the project.
shoutout to pokeapi for the best pokedex ever know to man.
