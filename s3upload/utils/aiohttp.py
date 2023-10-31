from aiohttp import ClientResponse


def get_filename_from_response(response: ClientResponse) -> str | None:
    if "content-disposition" in response.headers:
        header: str = response.headers["content-disposition"]
        raw_filename = header.split("filename=")[-1]
        filename = raw_filename.replace('"', "")
        if not filename.endswith(".zip"):
            # In case when format was not found in URL
            filename = f"{filename}.zip"
        return filename
    return None
