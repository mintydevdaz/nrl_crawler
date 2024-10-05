from typing import Literal

import chompjs
from niquests import Response
from selectolax.parser import HTMLParser, Node

from nrl_crawler.src.models import PlayerModel
from nrl_crawler.src.web import request


# ! Fix output / type hints of profile
class Player:
    def __init__(self, tree: HTMLParser) -> None:
        self.profile = self._get_profile(tree, "script[type='application/ld+json']")
        self.tables = self._get_tables(tree)

    def _html_node_to_iterable(
        self,
        tree: HTMLParser,
        query: str,
        attr: str | None = None,
    ) -> list | dict | None:

        if not (node := tree.css_first(query)):
            return None

        raw_text: str | None = node.attributes.get(attr) if attr else node.text()

        if not raw_text:
            return None

        try:
            data: list | dict = chompjs.parse_js_object(raw_text)
        except ValueError:
            return None
        else:
            return data

    def _sanitise(self, data: dict):
        player = PlayerModel(
            name=data.get("name", ""),
            family_name=data.get("familyName", ""),
            given_name=data.get("givenName", ""),
            url=data.get("url"),
            birth_date=data.get("birthDate", ""),
            birth_place=data.get("birthPlace", "").get("address", ""),
            height=data.get("height", 0.0).get("value", 0.0),
            weight=data.get("weight", 0.0).get("value", 0.0),
            role=data.get("jobTitle", ""),
        )
        return player.model_dump(by_alias=True)

    def _get_profile(self, tree: HTMLParser, query: str) -> dict | None:
        data = self._html_node_to_iterable(tree, query)
        return self._sanitise(data) if data else None

    def _get_tables(self, tree: HTMLParser) -> dict:
        if not (tables := tree.css("table")):
            return {}

        if len(tables) == 1:
            t1 = Table(tables[-1], "careerOverall")
            return {t1.table_name: t1.output()}

        elif len(tables) == 2:
            t1 = Table(tables[-1], "careerOverall")
            t2 = Table(tables[-2], "careerSeason")
            return {t1.table_name: t1.output(), t2.table_name: t2.output()}

        else:
            t1 = Table(tables[-1], "careerOverall")
            t2 = Table(tables[-2], "careerSeason")
            t3 = Table(tables[-3], "currentSeason")
            return {
                t1.table_name: t1.output(),
                t2.table_name: t2.output(),
                t3.table_name: t3.output(),
            }

    def output(self):
        return {"profile": self.profile, "stats": self.tables}


class Table:
    def __init__(
        self,
        tree: HTMLParser,
        name: Literal["currentSeason", "careerSeason", "careerOverall"],
    ) -> None:
        self.table_name = name
        self._column_titles = self._get_titles(tree)
        self._column_values = self._get_values(tree)

    def _nodes(self, tree: HTMLParser, query: str) -> list[Node] | list:
        return tree.css(query)

    def _text_filter(self, values: list[str]) -> list[str]:
        output = []
        for v in values:

            if v in ["LLost", "WWon", "DDrawn"]:
                new_val = v[1:]
                output.append(new_val)

            else:
                output.append(v)

        return output

    def _get_titles(self, tree: HTMLParser) -> list | None:

        # Find table headers
        if not (headers := self._nodes(tree, "thead > tr")):
            return None

        # Second header row - contains all column titles
        row = headers[-1]

        # Find titles
        if not (titles := self._nodes(row, "th.table__cell.table__th")):
            return None

        # Unpack title strings
        values = [v.text(strip=True).replace("\xa0", " ") for v in titles if v.text()]

        if self.table_name in ["careerSeason", "careerOverall"]:

            # Insert Extra Title
            values.insert(0, "Team")

        else:
            # Insert Extra Title
            values.insert(2, "Outcome")

        return values

    def _get_values(self, tree: HTMLParser) -> list[list] | None:

        # Find all rows
        if not (rows := self._nodes(tree, "tbody > tr")):
            return None

        output = []
        if self.table_name in ["careerSeason", "careerOverall"]:

            for row in rows:

                cells = self._nodes(row, "td.table__cell.table-tbody__td")
                values = [c.text(strip=True) for c in cells if c.text()]

                # Omit empty string
                values = values[1:]

                output.append(values)

        elif self.table_name == "currentSeason":

            for row in rows:

                cells = self._nodes(row, "td")
                values = [c.text(strip=True) for c in cells if c.text(strip=True) != ""]
                clean_values = self._text_filter(values)
                output.append(clean_values)

        return output

    def output(self) -> list[list] | list:
        if not self._column_titles or not self._column_values:
            return []

        try:
            data = [self._column_titles, *self._column_values]
        except Exception:
            return []
        else:
            return data


def _build_team_urls(ids: list[int], comp_id: int) -> list[str]:
    return [
        f"https://www.nrl.com/players//data?competition={comp_id}&team={i}" for i in ids
    ]


def _unpack_team_lists(responses: list[Response]) -> list[dict]:

    # Pre-validated responses
    data = [response.json() for response in responses]

    teams: list[dict] = []
    for d in data:

        try:
            team: list[dict] = d["profileGroups"][0]["profiles"]
        except (KeyError, IndexError):
            #! Log Error
            continue
        else:
            teams.extend(team)

    return teams


def get_nrl_team_webpages(
    team_ids: list[int],
    comp_id: int,
    headers: dict[str, str] | None,
) -> list[Response] | None:
    urls = _build_team_urls(team_ids, comp_id)
    return request(urls, headers, "Team Sites")


def get_player_webpages(
    responses: list[Response],
    headers: dict[str, str] | None,
    base_url: str = "https://www.nrl.com",
):
    teams = _unpack_team_lists(responses)
    hrefs = list(map(lambda x: x["url"], teams))
    urls = list(map(lambda href: f"{base_url}{href}", hrefs))
    return request(urls, headers, "Player Sites")
