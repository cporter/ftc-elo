# FTC ELO

Calculate ELO rankings based on match_data files generated,
presumably, by the FTC scoring system.

## How we're calcuating ELO

* No performance or provisional ratings
* There's a fixed starting rating for all new teams. (Alas: it is
  hard-coded)
* The K factor currently does not change based on how many matches
  you've played. Reasonable, I think, as an entire regional season
  shouldn't go more than 35 matches for any one team.
* Ratings are live-updated after every match.

Alliances gain and lose ELO together based on the mean average of
their current ratings. I'm not convinced that this is best, only that
it was easy. Open to suggestions.

## How to use this "tool"

The driver is currently pretty primitave. There's a script
[tournament.py](tournament.py) that takes a directory argument and an
optional ratings file argument. Run it in a loop with all of your
tournament directories in cronological order. Something like this:

    touch ratings.txt
    for d in $ORDERED_TOURNAMENT_DIRECTORIES
	do
		python tournament.py "$d" ratings.txt > tmp-ratings.txt
		mv tmp-ratings.txt ratings.txt
	done

Maybe you'll want to save off the ratings files between each
tournament. Maybe not. Your call.  The format of the ratings file is:

    TEAM_NUMBER \t ELO \t MATCHES_PLAYED
