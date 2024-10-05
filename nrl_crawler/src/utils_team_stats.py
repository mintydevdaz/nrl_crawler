from niquests import Response
from niquests.exceptions import JSONDecodeError

from nrl_crawler.src.web import request


def _build_urls(comp_id: int, year: int, stat_ids: list[int]):
    return [
        f"https://www.nrl.com/stats/teams//data?competition={comp_id}&season={year}&stat={i}"
        for i in stat_ids
    ]


def get_team_webpages(
    comp_id: int,
    year: int,
    stat_ids: list[int],
    headers: dict[str, str] | None,
):
    urls = _build_urls(comp_id, year, stat_ids)
    return request(urls, headers, terminal_desc="Team Stats")


def extract_total_stats(responses: list[Response]) -> list[dict] | None:
    try:
        data = [r.json()["totalStats"] for r in responses]
    except (JSONDecodeError, KeyError):
        return None
    else:
        return data


def parse_stats(data: list[dict]) -> list[dict]:

    output = []
    for stat in data:

        title: str = stat["title"]
        teams = list(
            map(
                lambda x: {
                    "team": x["teamNickName"],
                    "value": x["value"],
                    "played": x["played"],
                },
                stat["leaders"],
            )
        )
        output.append({"stat": title, "leaders": teams})
    
    return output
