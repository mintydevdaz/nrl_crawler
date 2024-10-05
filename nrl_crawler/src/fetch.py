import sys

from nrl_crawler.src.teams import TEAMS
from nrl_crawler.src.tools import Save, parse_html
from nrl_crawler.src.utils_ladder import get_competition_ladder, positions
from nrl_crawler.src.utils_players import (
    Player,
    get_nrl_team_webpages,
    get_player_webpages,
)
from nrl_crawler.src.utils_team_stats import (
    extract_total_stats,
    get_team_webpages,
    parse_stats,
)


def ladder(dir_path: str, env: dict):

    HEADERS: None = None
    COMP_ID: int = env["comp_id"]
    YEAR: int = env["year"]
    ROUND_NUM: int = env["round"]

    raw_data = get_competition_ladder(COMP_ID, ROUND_NUM, YEAR, HEADERS)

    if not raw_data:
        sys.exit(1)

    clean_data = positions(raw_data)
    output_data = {"year": YEAR, "round": ROUND_NUM, "ladder": clean_data}
    Save.to_json(dir_path, "ladderClean.json", output_data)


def players(dir_path: str, env: dict):

    HEADERS: None = None
    COMP_ID: int = env["comp_id"]
    TEAM_IDS: list[int] = list(map(lambda x: x["team_id"], TEAMS[COMP_ID]))

    team_responses = get_nrl_team_webpages(TEAM_IDS, COMP_ID, HEADERS)

    if not team_responses:
        sys.exit(1)

    player_responses = get_player_webpages(team_responses, HEADERS)

    if not player_responses:
        sys.exit(1)

    # Parse Data on a per player basis
    trees = list(map(parse_html, player_responses))
    player_data = [Player(tree) for tree in trees]
    clean_data = [player.output() for player in player_data]

    Save.to_json(dir_path, "playerClean.json", clean_data)


def team_stats(dir_path: str, env: dict):

    HEADERS: None = None
    YEAR: int = env["year"]
    COMP_ID: int = env["comp_id"]
    STAT_IDS: list[int] = env["stat_ids"]

    responses = get_team_webpages(COMP_ID, YEAR, STAT_IDS, HEADERS)

    if not responses:
        sys.exit(1)

    raw_data = extract_total_stats(responses)
    clean_data = parse_stats(raw_data)
    Save.to_json(dir_path, "statsTeamClean.json", clean_data)
