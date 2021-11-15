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
    url = r'https://star.ettoday.net/news/94529'
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
            發言時間 101/08/28 16:24:06 發言人 廖雲煥 發言人職稱 特助 發言人
            電話 03-5992646-240 主旨 : 本公司國內第三次無擔保轉換公司債到期還本暨終止
            上櫃事宜 符合條款第49款 事實發生日101/08/28 說明 1.事實發生日
            :101/08/28 2.公司名稱:奇力新電子股份有限公司 3.與公司關係(請輸入本公司或
            聯屬公司):本公司 4.相互持股比例:不適用 5.發生緣由:本公司國內第三次無擔保轉換
            公司債自民國96年10月02日開始發行至 101年10月02日到期,擬依本債券發行及轉換辦法
            辦理買回事宜,並終止上櫃買賣。 6.因應措施:債券到期時依債券面額以現金一次償還
            。 7.其他應敘明事項: 奇力新電子股份有限公司國內第三次無擔保轉換公司債將於101年
            10月02日到期,依其 發行及轉換辦法第9條規定,該轉換公司債自101年09月23日至101年
            10月02日停止轉換, 並於到期日之次一營業日(101年10月03日)終止上櫃買賣。正因
            除息作業,奇力新電子股 份有限公司國內第三次無擔保轉換公司債自101年09月04日至
            101年09月30日停止轉換, 債券持有人如擬申請轉換,最遲應於101年09月03日前向往來
            證券商辦理轉換事宜。 以上資料均由各公司依發言當時所屬市場別之規定申報後,由本系統
            對外公佈,資料如有虛偽不實,均由該公司負責.
            '''
        ),
    )
    assert parsed_news.category == '財經'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1346142240
    assert parsed_news.reporter is None
    assert parsed_news.title == '奇力新 本公司國內第三次無擔保轉換公司債到期還本暨終止上櫃事宜'
    assert parsed_news.url_pattern == '94529'
