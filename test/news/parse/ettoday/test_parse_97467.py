import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.ettoday


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='東森')
    url = r'https://star.ettoday.net/news/97467'
    response = news.crawlers.util.request_url.get(url=url)

    raw_news = news.crawlers.db.schema.RawNews(
        company_id=company_id,
        raw_xml=news.crawlers.util.normalize.compress_raw_xml(
            raw_xml=response.text,
        ),
        url_pattern=news.crawlers.util.normalize.compress_url(
            company_id=company_id,
            url=url,
        )
    )

    parsed_news = news.parse.ettoday.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            寶靈老師為天秤座抽到的塔羅牌是:聖杯侍衛 運勢指數4 愛情指數4 一切都有人替自己
            準備好的感覺,心態上非常充裕滿足,建議你拿回自己的決定權與行動力,使自己更有效率。
            '''
        ),
    )
    assert parsed_news.category == '運勢'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1346643420
    assert parsed_news.reporter is None
    assert parsed_news.title == '9/3天秤座運勢'
    assert parsed_news.url_pattern == '97467'
