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
    url = r'https://star.ettoday.net/news/2517'
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
            民國38年的金門,當時《三角堡》曾是重要的戰地之一,光陰芢苒,今日的金門,已轉為小三通
            具有觀光指標的地點,甚至要重新賦予三角堡意義。《金門生存遊戲協會》自10月10日至
            10月23日舉辦兩階段活動,預計數百位玩家共襄盛舉,一般民眾也可以參與機槍射擊體驗
            。 從建國百年10月10日起,一直到10月23日,金門三角堡舉行第一階段的射擊體驗活動
            ,一般民眾可以免費使用現場供應的BB槍,射擊碉堡外的十面相當擬真的人型立靶,拍照留念
            。 第二階段於10月22日,上午九點半展開活動,近四百名兩岸三地的生存遊戲玩家,分別模擬
            打仗,全天將有三場精采攻防,民眾可登上三角堡,觀賞兩隊刺激作戰。 擁有10生存遊戲經驗
            的資深玩家鄒志偉表示,三角堡與台灣生存遊戲最大不同處在於,本身場地從前就是戰場
            ,而非主辦單位另外找場地,因此玩起來特別有fu,雖然BB槍不像漆彈,打到會有顏色顯示
            ,不過也因此,玩法採榮譽制分勝負,玩的是本身的「榮譽心」,更有意思! 鄒志偉特別提醒說
            ,生存遊戲雖然拿的是BB槍,但是威力也不容小覷,玩家千萬不要耍帥不戴護目鏡、配備
            ,眼睛、手部都是要額外注意保護的部位,玩得安全,才能真正玩得盡興!
            '''
        ),
    )
    assert parsed_news.category == '旅遊'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1319162400
    assert parsed_news.reporter == '黃彥綺'
    assert parsed_news.title == '三角堡大型戰場 生存遊戲超刺激'
    assert parsed_news.url_pattern == '2517'
