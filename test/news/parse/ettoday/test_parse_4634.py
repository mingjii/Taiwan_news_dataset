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
    url = r'https://star.ettoday.net/news/4634'
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
            貧富懸殊持續擴大。根據物質不滅定律,窮人愈來愈多,也意味著有錢的人更有錢。英國著名
            奢華設計公司 Stuart Hughes最近推出一款名為「黃金歷史版」
            ( Gold History Edition)的iPad2,外殼由24K黃金 、鑽石和暴龍化石打造,售價高達
            500萬英鎊(約2億4000萬台幣 )。 它重約3公斤。外殼背板是24K純金。光是背板的金蘋果
            商標,就有53顆12.5克拉的鑽石,跟正面的 Home 鍵加起來共有 65 顆。正面的面板四周
            是一種名為斑彩螺石(Ammolite)的寶石 ( 這種寶石本身是菊石的殼留下來的化石)
            。不止如此,裡面還滲了暴龍的化石! 真不愧是「黃金歷史版」。因為這些化石真的有夠
            古早的! 這款貴重的iPad只生產兩台。嫌貴?有一台已經賣出去了!
            '''
        ),
    )
    assert parsed_news.category == '新奇'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1320207960
    assert parsed_news.reporter is None
    assert parsed_news.title == '黃金鑽石+暴龍化石打造 最貴的iPad2要價兩億!'
    assert parsed_news.url_pattern == '4634'
