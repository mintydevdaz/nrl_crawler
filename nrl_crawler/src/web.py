import logging

from niquests import Response, Session
from niquests.exceptions import ReadTimeout, RequestException
from tqdm import tqdm


def request(
    urls: list[str],
    headers: dict[str, str] | None = None,
    terminal_desc: str = "Fetch",
) -> list[Response] | None:

    errors = 0
    output = []

    with Session() as s:

        for url in tqdm(urls, desc=terminal_desc, ncols=75):

            try:
                response = s.get(url, headers=headers)

            except (ReadTimeout, RequestException) as exc:
                errors += 1
                msg = f"Error fetching response for url '{url}': {exc}."
                logging.error(msg)

            else:
                if response.ok:
                    output.append(response)
                else:
                    errors += 1
                    msg = f"Response not saved for url '{url}'. Status Code: {response.status_code}."
                    logging.error(msg)

    msg = f" > Final Summary | URLS: {len(urls)} | Response: {len(output)} | Errors: {errors}"
    logging.info(msg)
    return output or None
