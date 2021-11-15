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
    url = r'https://star.ettoday.net/news/92931'
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
            這是一個最好的時代,這是智慧的時代,從電腦進入平板及觸控手機的世代,在時間如短跑
            選手般迅速趨前,一回神已經是觸控世界的天下。我們都需要一個好用外觀時尚的觸控筆
            讓我們在平板上盡情投入、在使用的時候展現手上的無限魅力,剛好最近入手了一系列美呆了
            的觸控筆,必須立即告訴大家這款觸控筆有多迷人! 潔白款式觸控筆,包裝設計充滿質感
            ,霧面貼面,正面可直接看到筆完整的樣子,肆意選擇自己喜歡的顏色吧!兼具實用與外觀的
            晶鑽水晶兩用觸控筆,是原子筆,也是觸控筆,為了搭配水晶,筆桿與筆頭皆為淡淡珠光閃耀
            ,可以看到筆頭部分為同色系的圓頭設計,摸起來柔軟,適用於所有電容式觸控面版3C電子
            產品。 這款觸控筆最重要的地方在於筆桿裡的晶鑽水晶,當光線投射在水晶上,折射出閃爍
            的光芒,書寫時筆桿跟著搖擺,晶瑩剔透的水晶如同舞會中迷人的首飾,一閃一閃絕對
            最吸引人。一共有五個顏色,潔白款的水晶清透誘人,帶有鑽石的高貴特質,切割折射的光彩
            叫人難以將目光移開。 幻夢粉紅的女孩色彩,如同做一個浪漫沉醉的美夢,隨著每一次的
            呼吸,只有越來越迷戀及痴狂;優雅淡藍的中性氣質,是知性人喜歡的愜意藍天,色澤輕淡卻
            帶有深沉的幽靜,如同站在地中海,悠藍風情不過如此;與潔白款相同擁有純淨的水晶,筆桿
            為沉穩洗鍊的黑色,高階主管喜愛的顏色,低調個性飄然展現,品味無限釋放;紫迷心醉,紫色
            總是帶有神秘風貌,成熟的美感在手間綻放,喜歡尼泊爾、瑪雅等神秘國度的人,一定對此款
            一見傾心。 最令人意外的,此款觸控筆竟然是甜蜜的對筆!有長款(長14CM,直徑1CM)及
            短款(長12CM,直徑0.8CM)的分別,材質為矽鋁銅合金。戀人之間,也能書寫屬於兩人的
            親密文字。(偶而暫停使用簡訊吧!) 書寫起來十分流暢滑順,筆桿大小適中,握筆順手
            ,以食指輕觸筆夾的地方,筆頭的觸控功能將會顯現,無論滑過、點選都能輕鬆操作
            。 我們被多樣化的選擇沖昏了頭,但能充滿真切情意的商品卻十分缺乏,實用、美觀是我們
            迫切需要的。在七夕前夕,不妨挑選一組觸控筆,提示另一半應該要開始撰寫一封真摯流露的
            卡片,讓感情更加升溫吧!
            '''
        ),
    )
    assert parsed_news.category == '民生消費'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1345806180
    assert parsed_news.reporter is None
    assert parsed_news.title == '手上的璀璨魅力 水晶兩用觸控筆'
    assert parsed_news.url_pattern == '92931'
