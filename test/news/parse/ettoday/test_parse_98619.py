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
    url = r'https://star.ettoday.net/news/98619'
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
            浮腳筋不只有久站才會引起,長時間久坐也容易出現,尤其部分女性更注重自己是否能擁有
            一雙美腿,但到底要怎麼才能預防浮腳筋呢?其實,睡覺前用枕頭墊高兩腿,且超過心臟的高度
            ,可有效幫助腿部靜脈血液回流。 嘉義基督教醫院心血管外科醫師甘宗本表示,其實只要
            掌握幾個小撇步,且養成習慣,就能有效預防浮腳筋。首先可透過睡覺前,用枕頭墊高兩腿
            ,且超過心臟的高度,有效幫助腿部靜脈血液回流。 甘宗本進一步說明,民眾應建立起良好的
            運動習慣,包過健走、騎腳踏車、游泳等,都有助於減少靜脈血液蓄積,降低靜脈壓力。另外
            ,盡量避免穿著有鬆緊帶的襪子,容易造成腿部靜脈無法正常回流,且隨時記得讓腿部保持
            活動性,不管是久坐或久站的人,至少10分鐘就屈曲足踝關節10次。 甘宗本說,比較適合是
            穿著彈性襪,可以促使靜脈血液推擠回心臟,建議民眾也應避免處於高溫環境,包括泡湯或
            泡熱水澡等,都有可能因太熱使得浮腳筋加劇。 靜脈曲張其實俗稱就是浮腳筋,是因下肢
            淺層靜脈系統的血管,因病變形成不正常的擴大,通常女性的機率比男性高,尤其會隨著年齡
            增長而使症狀加劇,嚴重可能會造成腫痛、腫脹甚至皮膚潰爛等問題出現,民眾絕不能忽略
            嚴重性。
            '''
        ),
    )
    assert parsed_news.category == '生活'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1347175500
    assert parsed_news.reporter == '林怡亭'
    assert parsed_news.title == '防腿部暴青筋 抬腿高過心臟改善好'
    assert parsed_news.url_pattern == '98619'
