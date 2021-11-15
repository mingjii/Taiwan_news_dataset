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
    url = r'https://star.ettoday.net/news/9156'
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
            新北市100學年度學生舞蹈比賽,11月26日起至12月2日於板橋體育館及新北市藝文中心
            辦理個人及團體甲乙丙組比賽,包括古典、民俗、現代及兒童舞蹈等類型。本次賽程預計個人
            及團體共196支隊伍參賽,優勝隊伍將代表本市參加全國學生舞蹈比賽。 今日首先登場的是
            團體甲組賽程,共計16隊參賽。團體甲組每隊最多參加學生達75人,可說是舞蹈比賽中最具
            氣勢的組別,來自新北市各區高中職、國中小的舞林高手,匯聚在板橋體育館大展才能
            。比賽首先由金山國小以水芙蓉舞爭妍的古典舞蹈揭開大會正式比賽的序曲。 值得一提的是
            ,參賽隊伍之一的瑞亭國小,每年都從瑞芳不畏路遠辛勞熱情前往參加,從不缺席,巾扇舞
            已成為該校的特色及註冊商標,小朋友手執羽扇,翩然起舞如仙童,彷彿身置古典仙境
            ;南強工商則是首度參加本市學生舞蹈比賽,由表演藝術科同學擔綱演出,將現代語彙融入
            古典舞碼,銀色旗語訴說著因時空錯置讓相愛男女無法相遇的悲傷;最後壓軸的是安和國小
            的小朋友,他們藉由記憶中的學生椅,以童趣的方式表現「上學趣」的種種趣味。 以 「茶香
            .茶鄉」舞碼得到西區優等,並代表新北市參加全國學生舞蹈比賽的裕民國小,由校長
            張恒南親自帶隊,他說,「學校的舞團是以課後班社團的形式來組成,這次演出結合
            鄉土語文領域客語組的同學參與演唱『客家四季』並配上手語演出,提供給學生多元學習
            的機會。」 指導老師許見平則表示,這次演出動作融入了客家採茶、選茶、曬茶的優雅動作
            ,也表現出客家人樂觀、辛勤及迎接豐收的喜悅。5年9班黃昱祺表示,「比賽好緊張,但可以
            看到很多精彩的演出,收獲很大。」3年1班的陳采羚則說,「練習時好辛苦喔!尤其是後軟翻
            的動作,腰酸背痛的,現在得獎了,很開心。」 本次學生舞蹈比賽在各隊高水準的演出下
            ,競爭特別激烈,另在11/30、12/1、12/2於藝文中心仍有個人及團體乙、丙組的比賽
            ,歡迎市民踴躍前往欣賞,並為所有參賽的選手們加油打氣。
            '''
        ),
    )
    assert parsed_news.category == '地方'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1322293800
    assert parsed_news.reporter is None
    assert parsed_news.title == '舞林高手大集合 新北市學生舞蹈比賽登場'
    assert parsed_news.url_pattern == '9156'
