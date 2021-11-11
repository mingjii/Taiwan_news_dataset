import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.epochtimes


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='大紀元')
    url = r'https://www.epochtimes.com/b5/13/12/12/n4032207.htm'
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

    parsed_news = news.parse.epochtimes.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            二零一三年十二月九日(週一),也是國際人權日的前一天,來自
            不同國家因信仰自由、維護民主和人權遭受迫害的近二十多個團體的代表在加拿大首都渥
            太華舉辦了圓桌會議。法輪大法學會主席李迅應邀與會併發言,從深度、廣度和嚴重程度等
            方面講述了在中國法輪功長達十四年遭受迫害的真相。 加拿大多元文化事務部長提姆•厄
            普(Tim Uppal)、綠黨領袖伊麗莎白•梅(Elizabeth May)、新民主黨議員韋恩•馬斯通
            (Wayne Marston)的助手、參議員阮大海(Hon. Thanh Hai Ngo)、保守黨國會議員、
            國會人權委員會成員大衛•斯維特(David Sweet)等政要傾聽了代表們的發言。 在中國
            曾遭受迫害的九名法輪功學員到場。法輪功學員何立志還講述了自身受迫害的故事。 不同的
            辦公室:「六一零」推行迫害 加宗教自由辦公室推廣信仰自由 「中共在一九九九年成立了
            六一零辦公室,對法輪功長達十四年的系統迫害開始了,這個辦公室遍及政府,從中央到省、
            市甚至基層各個層面。每個層面的『六一零』辦公室對法輪功的迫害都擁有絕對的權力,而
            沒有任何法律依據。六一零辦公室甚至遍及司法、軍隊、媒體、警察等各領域並延伸到
            海外。」加拿大法輪大法學會主席李迅在當天的發言中說。 李迅接著說,對法輪功的迫害
            遍及中國的每個角落。談到迫害的慘烈程度,他說,「這星球上從未有過的邪惡」——活摘
            法輪功學員器官大量存在;已經證實,超過三千七百名法輪功學員被迫害致死,實際的數字
            遠遠超過這個數據。據聯合國相關報告稱,酷刑在中國被系統廣泛的濫用,百分之六十六的
            酷刑案例是針對法輪功學員的。 於今年二月十九日成立的旨在全球推廣宗教及信仰自由的
            加拿大「宗教自由辦公室」,與中共各級「六一零」辦公室形成了鮮明對照。厄普部長在當天
            的發言中鼓勵受迫害的團體到加拿大政府申訴。他說:對於加拿大政府而言,人權和宗教自由
            非常重要,人們能夠不受歧視和迫害的實踐他們的信仰是非常重要的。這就是為甚麼我們的
            政府成立了宗教自由辦公室。他鼓勵受迫害團體與信仰自由辦公室互動,並瞭解宗教自由
            辦公室在做甚麼。 何立志談迫害:每一秒鐘都遭受精神和肉體奴役 何立志曾是中國建設部
            執業資格註冊中心高級工程師,獲得過十多項國家及部級獎勵。他曾因堅持真善忍信仰被中共
            非法判刑三年半。 何立志先生講述了他在中國遭受的迫害。他說:迫害幾乎奪走了我的生命,
            在遭受非法監禁和巨大折磨的三年半中,我每一天、每一秒鐘都在遭受奴役,不僅僅是肉體上
            的,而且是精神上的。他們使用一切手段,強迫我放棄良知和信仰。冬天被扒光衣服,一盆
            一盆地澆涼水,導致我發高燒兩個月,而沒有任何醫療措施...... 何立志說,所有的迫害
            都是非法的。因為給親朋好友發信講法輪功真相,何立志被國安綁架,在被非法關押在拘留所
            期間,建設部黨委一名宣傳部長和官方檢察官對他說,「如果你寫個聲明,說你在拘留所沒有
            看到法輪功遭受任何酷刑,你馬上就能回單位上班。」何立志沒有答應,緊接著,他就被起訴
            和非法判刑。 家人為何立志找到的第一個律師因為之前為其他法輪功學員做無罪辯護後來被
            吊銷了執照,無法繼續為他做辯護。第二任律師曾對他說,如果為法輪功學員做無罪辯護,他
            將失去工作。在對何立志非法判刑三年半後,法官曾對何立志說:「雖然我是法官,但是你的
            刑期開庭前上面就已經定了。你為甚麼找律師?這不是和政府對著幹嗎?逼著給你
            判刑。」 傾聽真相影響決策 加政府鼓勵受迫害群體申訴 厄普部長鼓勵受迫害的人們說出
            他們的遭遇,因為加拿大政府對此瞭解得越多,越會決定政府的政策。他說,「作為多元文化
            部長,傾聽加拿大人(的遭遇)和關注非常重要。這些關注可能存在於廣泛的領域,今天的關注
            是人權和信仰自由,人們因為他們的信仰,在不同的國家和地區遭遇迫害。我真的很想傾聽
            他們的(遭遇),瞭解正在發生甚麼,因為我們知道得越多,就越會影響我們的決策。」 聯邦
            參議員阮大海說:「這個會議是一個讓加拿大政府及國會議員們增加瞭解的機會,我們還應該
            要求加拿大政府為了這些人的安危而進行干預。」 加拿大國會議員大衛•斯維特非常關注
            中共活體摘取法輪功學員器官的真相,他表示,國會人權委員會正在準備對中共活摘法輪功
            學員器官的指控做進一步的調查。 斯維議員說:「大衛•麥塔斯和大衛•喬高已經針對活摘
            器官的證據和後果發表了兩次報告,所以我們要查明真相,對此我們會對更多證人舉行
            聽證。」 宗教自由辦公室大使:對法輪功等信仰的迫害不能接受 據加拿大媒體
            《卡爾加里先驅報》、《蒙特利爾公報》等報導,宗教自由辦公室大使安德魯•伯納德
            (Andrew Bennett)表示,他對中國政府對少數信仰團體令人震驚的迫害深感困擾,對於
            法輪功修煉者以及佛教徒、新疆穆斯林和基督徒的不能令人接受的迫害非常關注。 「在致力
            於中國信仰自由的工作中,我知道,對所有的迫害,我們將有機會,向前邁進並大聲疾呼,」
            他說,「法輪功修煉者已經形成國際運動,反對中共政權的迫害。」
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1386777600
    assert parsed_news.reporter is None
    assert parsed_news.title == '國際人權日 加拿大部長關注在中國的信仰迫害'
    assert parsed_news.url_pattern == '13-12-12-4032207'