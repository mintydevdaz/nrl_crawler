# NRL Crawler

A web crawler tailored to extract data from https://www.nrl.com/.

## Why?
I've created (and destroyed) numerous rough scripts to lift data from the NRL's website but decided there should be a more permanent solution made publicly available.

Also, other NRL-scraping repos used headless browsers (e.g. Selenium) which I feel is overkill for this use case. The NRL website has some exposed endpoints and where these are closed off, traversing the DOM is simple enough.

## Usage
Download from the command line. Arg options: **players, ladders, team_stats**.
```bash
python main.py arg
```
Output is automatically saved (in JSON) to **~/nrl_crawler/nrl_crawler/data**. Modify **env.py** in the root folder to alter the output.

### Players
- Extracts data from all player's profiles for a specified competition.
- Includes basic info (defined in json schema) and statistics located in table elements. Inclusive of current season (by round), career by season, and career overall.
- Table stats are designed to be dropped directly into a Pandas DataFrame.
- Not all players have stats available due to misadventure during the season (or not being selected to play).

### Ladder
- Gets ladder standings from [here](https://www.nrl.com/ladder/).

### Team Stats
- Gets stats grouped by team from [here](https://www.nrl.com/stats/).

## Notes

- The expectation is that users will want to scrape player data for the **Men's Premiership** only. The downside is that:
    
    - the men's competition has over 500 regiestered players each season which is, in effect, 500+ requests.
    - the web request object currently has limited functionality (e.g. unable to rotate headers and/or proxies, unable to throttle / backoff request speed etc).
    - it's possible that the server will block you while scraping.

- The crawler will break if the NRL decides to change the website layout.

## NRL Internal IDs
### Competition
<table>
<thead>
<tr>
<th align="center">ID</th>
<th align="left">Type</th>
</tr>
</thead>
<tbody>
<tr>
<th align="center">111</td>
<th align="left">Premiership (Men)</td>
</tr>
<tr>
<th align="center">161</td>
<th align="left">Premiership (Women)</td>
</tr>
<tr>
<th align="center">116</td>
<th align="left">State of Origin (Men)</td>
</tr>
<tr>
<th align="center">156</td>
<th align="left">State of Origin (Women)</td>
</tr>
<tr>
<th align="center">113</td>
<th align="left">NSW Cup</td>
</tr>
<tr>
<th align="center">114</td>
<th align="left">QLD Cup</td>
</tr>
<tr>
<th align="center">131</td>
<th align="left">Rugby League World Cup (Men)</td>
</tr>
<tr>
<th align="center">157</td>
<th align="left">Rugby League World Cup (Women)</td>
</tr>
</tbody>
</table>

### Statistics
<table>
<thead>
<tr>
<th align="center">ID</th>
<th align="left">Type</th>
</tr>
</thead>
<tbody>
<tr>
<th align="center">3</td>
<th align="left">Tackles</td>
</tr>
<tr>
<th align="center">4</td>
<th align="left">Missed Tackles</td>
</tr>
<tr>
<th align="center">9</td>
<th align="left">Possession %</td>
</tr>
<tr>
<th align="center">28</td>
<th align="left">Offloads</td>
</tr>
<tr>
<th align="center">29</td>
<th align="left">Tackle Breaks</td>
</tr>
<tr>
<th align="center">30</td>
<th align="left">Linebreaks</td>
</tr>
<tr>
<th align="center">31</td>
<th align="left">Line Break Assists</td>
</tr>
<tr>
<th align="center">32</td>
<th align="left">Total Kick Metres</td>
</tr>
<tr>
<th align="center">33</td>
<th align="left">Total Kicks</td>
</tr>
<tr>
<th align="center">35</td>
<th align="left">Try Assists</td>
</tr>
<tr>
<th align="center">37</td>
<th align="left">Errors</td>
</tr>
<tr>
<th align="center">38</td>
<th align="left">Tries</td>
</tr>
<tr>
<th align="center">69</td>
<th align="left">Field Goals</td>
</tr>
<tr>
<th align="center">76</td>
<th align="left">Points</td>
</tr>
<tr>
<th align="center">78</td>
<th align="left">Kick Return Metres</td>
</tr>
<tr>
<th align="center">81</td>
<th align="left">Dummy Half Runs</td>
</tr>
<tr>
<th align="center">82</td>
<th align="left">40/20 Kicks</td>
</tr>
<tr>
<th align="center">1000000</td>
<th align="left">Charge Downs</td>
</tr>
<tr>
<th align="center">1000002</td>
<th align="left">Decoy Runs</td>
</tr>
<tr>
<th align="center">1000003</td>
<th align="left">Ineffective Tackles</td>
</tr>
<tr>
<th align="center">1000004</td>
<th align="left">Intercepts</td>
</tr>
<tr>
<th align="center">1000015</td>
<th align="left">Supports</td>
</tr>
<tr>
<th align="center">1000025</td>
<th align="left">Line Engaged</td>
</tr>
<tr>
<th align="center">1000026</td>
<th align="left">Penalties Conceded</td>
</tr>
<tr>
<th align="center">1000028</td>
<th align="left">All Receipts</td>
</tr>
<tr>
<th align="center">1000034</td>
<th align="left">Goals</td>
</tr>
<tr>
<th align="center">1000037</td>
<th align="left">All Run Metres</td>
</tr>
<tr>
<th align="center">1000038</td>
<th align="left">All Runs</td>
</tr>
<tr>
<th align="center">1000079</td>
<th align="left">Handling Errors</td>
</tr>
<tr>
<th align="center">1000112</td>
<th align="left">Post Contact Metres</td>
</tr>
<tr>
<th align="center">1000209</td>
<th align="left">Conversion %</td>
</tr>
<tr>
<th align="center">1000210</td>
<th align="left">Set Completion %</td>
</tr>
<tr>
<th align="center">1000415</td>
<th align="left">Short Dropouts</td>
</tr>
</tbody>
</table>