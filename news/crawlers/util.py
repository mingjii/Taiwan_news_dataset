import random
import time

from requests import Response

# Times (in seconds) to sleep for each request. Set to 0 if the website is not
# blocking us. Note that LTN, SET, ftv, storm, TVBS use cloudfront services.
# Note that LTN, ftv and SET will ban us.
BEFORE_BANNED_SLEEP_SECS = {
    'chinatimes': 0.0,
    'cna': 0.0,
    'epochtimes': 0.0,
    'ettoday': 0.0,
    'ftv': 0.0,
    'ltn': 60.0,
    'ntdtv': 0.0,
    'setn': 60.0,
    # Storm response bad request with status 200.
    'storm': 1.0,
    'tvbs': 0.0,
    'udn': 0.0,
}
# Times (in seconds) to sleep when crawler get banned. Set to 0 if the website
# is not blocking us. Note that LTN, SET, storm, TVBS use cloudfront
# services. Note that LTN and SET will ban us.
# ChinaTimes, epochtimes, ettoday, ntdtv are set to 0 since it does not banned
# bad request.
# FTV is set to 0 since it host on cloudflare but for each missing page it will
# first response a 200 then redirect to 404.
# storm is set to 0 since it host on cloudfront but for each missing page it
# response 200 instead of 404.
# TVBS is set to 0 since we use API without bad request.
AFTER_BANNED_SLEEP_SECS = {
    'chinatimes': 0.0,
    'cna': 0.0,
    'epochtimes': 0.0,
    'ettoday': 0.0,
    'ftv': 0.0,
    'ltn': 86400.0,
    'ntdtv': 0.0,
    'setn': 86400.0,
    'storm': 0.0,
    'tvbs': 0.0,
    'udn': 86400.0,
}
REQUEST_TIMEOUT = 60


def after_banned_sleep(company: str) -> None:
    secs = AFTER_BANNED_SLEEP_SECS[company]
    if secs != 0.0:
        rand_secs = random.gauss(mu=1, sigma=2)
        # Avoid negative random.
        while rand_secs < 0:
            rand_secs = random.gauss(mu=1, sigma=2)
        secs += rand_secs
        time.sleep(secs)


def before_banned_sleep(company: str) -> None:
    secs = BEFORE_BANNED_SLEEP_SECS[company]
    if secs != 0.0:
        rand_secs = random.gauss(mu=1, sigma=2)
        # Avoid negative random.
        while rand_secs < 0:
            rand_secs = random.gauss(mu=1, sigma=2)
        secs += rand_secs
        time.sleep(secs)


def check_status_code(company: str, response: Response) -> None:
    # Got banned.
    if response.status_code == 403:
        after_banned_sleep(company=company)
        raise Exception('Got banned.')

    # Missing news or no news.
    # ETtoday use 410 instead of 404.
    if response.status_code in [404, 410]:
        before_banned_sleep(company=company)
        raise Exception('News not found.')

    # To many crawler at the same time.
    if response.status_code == 429:
        before_banned_sleep(company=company)
        raise Exception('Too many request.')

    # Something weird happend.
    if response.status_code != 200:
        before_banned_sleep(company=company)
        raise Exception(f'{response.url} is weird.')

    # Do nothing when status code 200.
    return
