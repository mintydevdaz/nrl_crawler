import json
import logging
from collections.abc import Iterable
from pathlib import Path

import chompjs
from niquests import Response
from selectolax.parser import HTMLParser


class File:
    @staticmethod
    def path(target_folder: str) -> str:

        # Establish path to folder inside project
        dir_path = Path().absolute().joinpath(target_folder)
        if dir_path.exists():
            return str(dir_path)

        msg = f"The specified path '{dir_path}' does not exist!"
        raise FileNotFoundError(msg)


class Save:
    @staticmethod
    def to_json(folder_path: str, filename: str, data: Iterable) -> None:
        output_fp: str = f"{folder_path}/{filename}"
        with open(output_fp, "w") as f:
            json.dump(data, f)
            msg = f" > {filename} saved to: {folder_path}."
            print(msg)
            logging.info(msg)


def logger(folder_path: str, filename: str = "app.log"):
    logging.basicConfig(
        filename=f"{folder_path}/{filename}",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s | %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
    )


def parse_html(response: Response) -> HTMLParser:
    return HTMLParser(str(response.text))


def html_node_to_iterable(
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
