import sys

import nrl_crawler.src.fetch as fetch
from env import CMD_MSG, ENV
from nrl_crawler.src.tools import File, logger


def main() -> None:

    n: int = len(sys.argv)
    if n == 1 or n >= 3:
        print(CMD_MSG)
        sys.exit(1)

    if sys.argv[1] not in {"ladder", "players", "team_stats"}:
        print(CMD_MSG)
        sys.exit(1)

    dir_path: str = File.path("data")
    logger(dir_path, "app.log")
    keyword: str = sys.argv[1]

    match keyword:

        case "ladder":
            fetch.ladder(dir_path, ENV[keyword])

        case "players":
            fetch.players(dir_path, ENV[keyword])

        case "team_stats":
            fetch.team_stats(dir_path, ENV[keyword])


if __name__ == "__main__":
    main()
