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
    url = r'https://star.ettoday.net/news/9279'
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
            27日上午近11時,一名男子從北醫附設醫院研究大樓墜下,消防局派員到場救護時,男子已無
            呼吸心跳,頭骨破裂當場死亡,警方封鎖現場,正進一步調查因。 台北市消防局指出,11時7分
            左右接到報案,在台北市吳興街附近有一名年約25歲的男子,從台北醫學大學附設醫院研究
            大樓墜樓身亡,救護人員抵時時發現,男子已無生命跡象。警方封鎖現場,正進一步了解實際
            案發原因。
            '''
        ),
    )
    assert parsed_news.category == '社會'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1322367480
    assert parsed_news.reporter is None
    assert parsed_news.title == '北醫大樓1男墜樓 頭骨破裂當場死亡'
    assert parsed_news.url_pattern == '9279'
