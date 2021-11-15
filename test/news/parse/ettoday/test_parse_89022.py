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
    url = r'https://star.ettoday.net/news/89022'
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
            台灣的醫療人才濟濟,醫療水準也不輸給歐美等先進國家,近來,就有兩例醫療個案,因表現
            良好,並且在國家地理頻道拍攝的紀錄片中,嘎上一腳,成為另類的台灣之光。 這兩例醫療
            個案分別是林口長庚醫院教授江東和成功為馬來西亞幼童做臍帶血移植,治癒重度
            海洋性貧血症,中研院新科院士魏福全為埃及外科醫師成功完成趾對指關節移植重建手術
            ,而且很特別的是,都發生在桃園縣內。 行政院衛生署與國家地理頻道合作,拍攝報導台灣
            國際醫療專業與產業紀錄片,4個醫療案例中,林口長庚醫院有2個,包括江東和的臍帶血移植
            及魏福金的趾對指關節移植重建顯微手術,估計全球超過1億以上觀眾收視,見證台灣奇蹟和
            醫療水平。 這兩例醫療案例,台灣都已經利用相關技術治癒那些有相同病症的人,尤其是
            指關節移植重建顯微手術,台灣的技術更是領先全球,更可以稱的上是台灣的驕傲。
            '''
        ),
    )
    assert parsed_news.category == '生活'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1345365000
    assert parsed_news.reporter == '李義輝'
    assert parsed_news.title == '醫療案例榮登國家地理頻道'
    assert parsed_news.url_pattern == '89022'
