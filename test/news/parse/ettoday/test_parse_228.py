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
    url = r'https://star.ettoday.net/news/228'
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
            千呼萬喚始出來的iphone新機型終於亮相,但可能卻另所有蘋果迷大失所望。10月4日蘋果
            新任執行長提姆庫克(Tim Cook)帶著蘋果所推出的新機型亮相,但是卻不是所有蘋果迷期望
            的iPhone 5,只是一台看起來似乎和iPhone 4幾乎一樣,但規格卻號稱有大翻幅新的
            iPhone 4S。更令人失望的的是iPhone 4S還沒中文化。 根據《蘋果日報》報導,蘋果
            新公布推出的新機iPhone 4S有所謂「聲控助理」的新功能,可以聽懂英文、法文和德文
            ,並且還號稱可以回答使用者有關天氣或餐飲等相關問題。但對中文世界的消費者來說
            ,iPhone 4S聽不懂中文令人大失所望,在中國上海就有蘋果迷在大街上舉牌抗議
            ,「No中文?!真心失望」。 即使iPhone 4S有多種西方語言,但iPhone 4S的語音服務
            還是不盡完美,有美國媒體記者用iPhone 4S查詢飛機航班時,卻得到「抱歉無法協助」的
            答案。 蘋果的新機發表,不但讓蘋果迷大為傷心,也讓蘋果概念股在失望性賣壓盡出下,股價
            大幅下滑,而其他蘋果的競爭對手,則鬆了一口氣。非蘋果陣營手機股全面大漲,5日雖然台股
            大盤震盪翻黑,但是包括宏達電、華寶、毅嘉、美律、華冠等股價都拉高,宏達電更是一舉
            奪回股王寶座。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1317825720
    assert parsed_news.reporter is None
    assert parsed_news.title == 'iPhone4S聲控不懂中文 華人蘋果迷:失望'
    assert parsed_news.url_pattern == '228'
