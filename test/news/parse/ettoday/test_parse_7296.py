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
    url = r'https://star.ettoday.net/news/7296'
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
            一隻可憐的狗狗被賊人猛刺21刀,還把牠丟到隔壁的院子裡,打算任牠孤獨的死去。然而這隻
            生命力極強的狗狗「丹普西」,卻奇蹟一般的活了下來! 事情的緣起是有數名賊人持刀闖
            空門,企圖洗劫狗狗主人的房子。這隻個性溫順、忠心守護家園的斯塔福郡鬥牛梗,慘遭竊賊
            毒手,身上被刺了20多刀,傷及多處內臟。 住在英國多塞特郡的狗主人克萊兒說,她的19歲
            女兒蘿倫晚上回到家時,發現屋子裡被翻箱倒櫃,地上 血跡斑斑, 鄰居聽到騷動聲後,好心
            的跑過來幫尋找這隻6歲的狗狗,最終發現牠身滿身血污的被人丟到隔壁的院子裡。 警方把
            丹普西火速送到醫院救治,接受了三個小時的救命手術後,丹普西令人難以置信的活了下來
            。負責救治牠的獸醫說,這是他看顧過「最悲慘的傷者」,卻有超乎尋常的生命力。
            '''
        ),
    )
    assert parsed_news.category == '寵物'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1321424760
    assert parsed_news.reporter is None
    assert parsed_news.title == '好強的狗命 狗狗被竊賊狂刺21刀 奇蹟存活!'
    assert parsed_news.url_pattern == '7296'
