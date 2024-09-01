import pathlib
import uuid
from typing import Optional, Union

import appdirs
import requests


def get_cache_dir() -> pathlib.Path:
    """Get the cache directory and create it if it does not exist"""
    cache_dir = pathlib.Path(appdirs.user_cache_dir('ssnolib'))
    if not cache_dir.exists():
        cache_dir.mkdir(parents=True)
    return cache_dir


def download_file(url,
                  dest_filename: Optional[Union[str, pathlib.Path]] = None,
                  known_hash: Optional[str] = None,
                  exist_ok: bool = False,
                  **kwargs) -> pathlib.Path:
    """Download a file from a URL and check its hash
    
    Parameter
    ---------
    url: str
        The URL of the file to download
    dest_filename: str or pathlib.Path
        The destination filename
    known_hash: str
        The expected hash of the file
    exist_ok: bool
        Whether to return an existing file. Otherwise, it is overwritten.
    **kwargs
        Additional keyword arguments passed to requests.get()
    
    Returns
    -------
    pathlib.Path
        The path to the downloaded file
    """
    if dest_filename is None:
        dest_filename = get_cache_dir() / uuid.uuid4().hex
    response = requests.get(url, stream=True, **kwargs)
    response.raise_for_status()
    if response.status_code == 200:
        content = response.content

        # Calculate the hash of the downloaded content
        if known_hash:
            import hashlib
            calculated_hash = hashlib.sha256(content).hexdigest()
            if not calculated_hash == known_hash:
                raise ValueError('File does not match the expected has')

        # Save the content to a file
        dest_filename = pathlib.Path(dest_filename)
        dest_parent = dest_filename.parent
        if not dest_parent.exists():
            dest_parent.mkdir(parents=True)

        if dest_filename.exists() and exist_ok:
            return dest_filename

        dest_filename.unlink(missing_ok=True)

        with open(dest_filename, "wb") as f:
            f.write(content)

        return dest_filename
    raise RuntimeError(f'Failed to download the file from {url}')
