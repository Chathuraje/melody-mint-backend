from app.api.v1.libraries.music_identifier.libraries.libs.generate_fingerprint import (
    fingerprint,
)
from app.utils import config
from itertools import zip_longest
import math
import pandas as pd
from app.utils import logging
from config.database import get_collection

logger = logging.getLogger()


async def find_matches(channel, sampling_rate=config.DEFAULT_SAMPLING_RATE):
    """Matches audio fingerprints.

    Fingerprints of an audio channel is matched against the stored fingerprints in the database.

    Args:
        channel:
            An audio channel. Array of bytes.
        sampling_rate:
            Number of samples per second taken to construct a discrete signal.
        args:
            Either 'localhost' to connect to localhost server or 'remote'

    Yields:
        song_id: Song id of matched fingerprint.
    """

    hashes = fingerprint(channel, sampling_rate)
    mapper = {}

    for hash_val, offset in hashes:
        mapper[hash_val.upper()] = offset

    values = mapper.keys()

    if values is None:
        logger.info("no values")
    else:
        counter = 0
        logger.info(f"Taking step length of {config.MATCH_STEP_LENGTH}")

        song_fingerprints = await get_collection("song_fingerprints")
        for split_values in grouper(values, config.MATCH_STEP_LENGTH):
            counter += 1

            fingerprint_data = list(await song_fingerprints.find().to_list(length=None))
            fingerprint_df = pd.DataFrame(fingerprint_data)

            matched_data = fingerprint_df[
                fingerprint_df["hash"].str.upper().isin(split_values)
            ]

            matches_found = len(matched_data)
            if matches_found > 0:

                logger.info(
                    f"Found {matches_found} hash matches at step {counter}/{math.ceil(len(values)/config.MATCH_STEP_LENGTH)}"
                )
            else:
                logger.info(
                    f"No hash matches found at step {counter}/{math.ceil(len(values)/config.MATCH_STEP_LENGTH)}"
                )

            for index, row in matched_data.iterrows():
                yield row["song_id"]


def grouper(iterable, n, fill_value=None):
    """Generates iterator.

    Generates iterables of fingerprints.

    Args:
        iterable:
            List of objects to generate iterator.
        n:
            Number of iterables
        fill_value:
            A value placed in case of missing value from the iterable

    Returns:
        iterator: Aggregated elements of each iterable
    """

    args = [iter(iterable)] * n
    return (filter(None, values) for values in zip_longest(fillvalue=fill_value, *args))
