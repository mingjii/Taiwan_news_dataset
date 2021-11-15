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
    url = r'https://star.ettoday.net/news/8680'
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
            屏東一名許姓婦人因為向一名刑大偵查佐討債40萬元,屢次催討不成,就跑到縣警局刑警大隊
            對面,爬到路燈上脫衣叫罵,要逼這名偵查佐出面,由於這個地點剛好位在百貨公司前,吸引
            大批民眾圍觀,最後由警消將這名婦人緊緊抓住,才用雲梯車將她送下來。 這名曾是屏東市
            大戲院千金的許姓女子23日下午2時許,只穿著黑色內衣跟褲子,光著腳丫,霸占百貨公司前
            路燈燈桿,消防人員對她喊話,「妳先下來啊!先下來,我請他跟妳講,好不好?這樣可以嗎?」
            警方試圖勸導無效。 「不要,拿大聲公給我!」情緒激動的她,根本不理會底下消防人員喊話
            ,甚至還不斷大力晃動高壓電線示威,就怕她一時情緒失控會不小心掉下來,底下圍觀的人群
            看了心驚膽跳。許姓女子還激動地說,「不要啦!你們警察吃案啦!你們警察沒有用啦!」 據
            指出,鄭姓偵查佐欠許姓女子60萬元,還了20萬元,卻未拿回本票,許女不承認,23日下午到
            刑警大隊找鄭姓偵查佐討錢不成,火大爬到警局前的燈桿,大聲叫欠錢的警察出來下跪
            ,邊罵邊脫掉外套,露出黑色內衣。許女見鄭警不為所動,情緒更加激動,大聲叫罵並猛力
            搖燈桿。 由於過程中只聽得清楚許姓女子大罵警察吃案,還說要找記者,彷彿是有冤屈要
            申訴,消防隊員用雲梯車載著一名記者跟女子的妹妹緩緩接近她,說要跟她溝通,但
            說時遲那時快,消防隊員一瞬間就把女子抱住,但大力抵抗的女子哪會乖乖就範,不但用腳勾住
            燈桿,還瘋狂對著消防人員亂咬,好不容易把人給拉到平地,女子的情緒還是無法平復
            。 原本大批媒體把麥克風堵在女子面前,想讓女子說清楚為什麼爬上燈桿上鬧事,卻被
            消防單位攔阻堅持要先送醫治療,讓家屬跟媒體都不滿而破口大罵,許女的妹妹大罵警方動作
            「太粗暴了」,事後屏東縣警局才召開記者會說明原委,刑大隊長林英仁指出,「根據許姓女子
            的需求說,跟我們刑大一個偵查佐有個40萬元的債務糾紛。」 警方表示,這名現年45歲的
            許姓女子疑似因為跟刑警大隊一名鄭姓偵查佐有40萬元的債務糾紛,而許姓女子就是因為催討
            不成,氣不過才發狠跑到刑警大隊前鬧事,希望用激烈的行動逼對方還錢。
            '''
        ),
    )
    assert parsed_news.category == '地方'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1322105280
    assert parsed_news.reporter is None
    assert parsed_news.title == '千金女爬電線桿 叫罵刑警還錢40萬'
    assert parsed_news.url_pattern == '8680'
