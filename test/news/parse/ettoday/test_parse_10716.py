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
    url = r'https://star.ettoday.net/news/10716'
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
            我不懂電磁波。或者說,我沒有比一般民眾懂更多。 大鳴大放,先講先贏。台灣媒體一向
            這樣。但林瑞雄丟出「電磁波說」,媒體突然有了「難言之隱」。媒體都在等。等什麼?
            一等林瑞雄更多的發言,不敢「遽下結論」。再等,如果大家心中的疑問真被「証實」,該
            如何處理這個棘手的「政治問題」。對媒體來說,要說實話,突然有點難。 像
            桑塔格(Susan Songtag)說的:疾病,是社會的集體隱喻。副總統候選人的精神狀態
            ,這有高度政治性,主流媒體「不敢為天下先」,外弛內張,這可以理解。距離投票日不到40天
            ,尤其是這個周末(10日)將舉行的電視辯論,對林瑞雄的關注,將被放大到不成比例。簡單講
            ,媒體將會用精神病學角度謹慎審視林瑞雄的一言一行。 部份媒體已經用旁敲側擊方式,處理
            這種關注。甚至用「人格分裂」字眼直接詢問林瑞雄。確實,不少精神醫學方面的專業人士
            暗示,只要一提到「電磁波攻擊」,十之八九都「bingo」。更使得媒體離開了「林瑞雄拋出
            的問題」,直接處理「林瑞雄本身的問題」。 不是在林瑞雄丟出「電磁波說」才開始
            。9月20日,林瑞雄成為宋楚瑜副手,之後,神隱,將近兩個月。檯面下,這個疑問,從沒停止
            ,越滾越大。比他的雙重國籍問題,更大。林瑞雄也把「電磁波攻擊」的起點回溯到9月20日
            當天下午,使得整個事件,很難單純從他的語意去判斷真偽。 我認識林瑞雄。20年前,我訪問
            過他。為了檳榔流行病學問題。確實是個老頑童。即使這幾天,政媒圈子裡,林瑞雄的
            「問題」檯面化,我總是半開玩笑為他辯,說他的言行,在親民黨裡不算瘋狂。很冷。 過去
            ,面對陳水扁狂人式的言行,我曾多次呼籲,正副總統候選人登記時,都應檢附健康檢查報告
            。身體除外,精神的,也要。但是,當候選人真的被懷疑可能有精神疾病時,我反而保留。在
            個人隱私和公共法益之間,模糊空間非常大,談論風險也非常大。我只能說,宋楚瑜丟給選民
            一個難題。尤其是近一成的支持者。而這個難題,也成了親民黨的尷尬。畢竟宣稱自己會
            當選,畢竟有潛在近百萬選票的支持,畢竟副手是「備位元首」,法定民主儲君。世界各國的
            憲政制度都一樣,無「法」「廢儲」。終究只能政治處理。 林瑞雄對國安單位
            「電磁波攻擊」的指控已經具體而密集。國安單位沈默。 但是,沈默不是辦法。這徒然
            招議,彷彿先入為主,把林瑞雄當瘋子。國安單位早晚要有回應,拿捏分寸,難度極高
            。 我不懂電磁波。但我知道,林瑞雄「質疑」的問題,以及林瑞雄「被質疑」的問題
            ,都很難有標準答案。這場選舉,選民的智慧空前重要。雖然,把這種難題交給選民,也很殘忍。
            '''
        ),
    )
    assert parsed_news.category == '雲論'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1323051300
    assert parsed_news.reporter == '唐湘龍'
    assert parsed_news.title == '林瑞雄質疑與被質疑的「問題」'
    assert parsed_news.url_pattern == '10716'
