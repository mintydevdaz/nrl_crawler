import logging
from niquests.exceptions import JSONDecodeError

from nrl_crawler.src.models import Ladder, Stats
from nrl_crawler.src.web import request


def get_competition_ladder(
    comp_id: int,
    round_num: int,
    year: int,
    headers: dict[str, str] | None,
) -> list[dict] | None:

    url = f"https://www.nrl.com/ladder//data?competition={comp_id}&round={round_num}&season={year}"
    response = request(urls=[url], headers=headers, terminal_desc="Ladder")

    if not response:
        return None

    try:
        data = response[0].json()
        positions = data["positions"]

    except (JSONDecodeError, KeyError) as e:
        logging.error(f"Unable to unpack JSON for url '{url}': {e}.")
        return None

    else:
        return positions


def positions(data: list[dict]) -> list[dict]:

    result = []
    for team in data:
        
        try:
            name: str = team.get("teamNickname", "Error fetching name")
            stats: dict = team["stats"]
            ladder = Ladder(name=name, stats=Stats(**stats))

        except Exception as exc:
            logging.error(f"Unable to parse ladder data: {exc}")
            continue
            
        else:
            result.append(ladder.model_dump(by_alias=True))

    return result
