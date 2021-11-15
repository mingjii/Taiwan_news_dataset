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
    url = r'https://star.ettoday.net/news/9444'
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
            國民黨主席馬英九表示,面對嚴峻的經濟情勢,台灣需要的是一個能再次將台灣帶出經濟衰退
            的政黨,國民黨甫執政就遇到幾十年來罕見的經濟衰退,比民進黨碰到的情況壞很多,但國民黨
            的執政表現比民進黨好很多,因為國民黨是真正有能力、有智慧,真正能幫台灣解決問題的
            政黨,希望明年1月14日,政黨票投國民黨,立委票投選區的國民黨立委,總統票支持
            馬英九吳敦義,讓台灣繼續向前行,台灣一定贏。 國民黨26日晚間在台中市豐原體育場舉辦
            建黨117週年黨慶晚會,現場湧入近3萬名支持群眾,一起歡慶國民黨117歲生日,短短的
            進場路程,在鄉親們的簇擁下,馬英九花了10多分鐘才走到台上,現場氣氛熱烈high翻天
            。 馬英九表示,國民黨執政不只重視經濟成長,也重視所得分配,努力照顧弱勢,實施
            勞保年金、國民年金,提高貧窮線,讓受惠人從26萬增加到86萬,2次提高勞工基本工資,實施
            奢侈稅,遏止短期房地產投資。 馬英九指出,上週國民黨提出不分區立委名單,婦女排第一名
            的是兒福聯盟執行長王育敏小姐,她很驚訝兒童沒有選票而國民黨願意提她為不分區立委
            ,她很高興有這個機會能擴大為兒童服務,馬主席強調,國民黨照顧的人不一定有選票
            ,「選票雖然重要,但弱勢照顧更重要」。 而排女性第2名的「罕病天使」楊玉欣小姐,她建議
            有些社福津貼18年都沒調整了,是否可以一次調足,再從調整後的基礎上,每四年一次依照
            物價指數來調整。馬主席說,他同意楊玉欣的建議,因為照顧弱勢不應該為德不足,要讓
            弱勢同胞感受到政府的照顧,因此決定將8種社福津貼一次調足,調整幅度是16%-33%
            ,也將老農津貼配合8種社福津貼的調整,將幅度從5.27%增加到16.7%,維持過去慣例的
            1000元。 馬英九強調,老農津貼調整1000元是過去的慣例,並不是學民進黨的,因為國民黨
            的版本設有排富條款,是民進黨沒有的,國民黨有弱勢照顧,民進黨沒有,馬主席指出,民進黨
            不會照顧沒有選票的人,但國民黨一定照顧弱勢。 馬英九談到上週大雨造成農產品損傷,表示
            在勘災之後認為現行的農業天然災害救助辦法不盡合理,因此做了調整,調高5-6成,以符合
            比例原則,國民黨用對的方式照顧農民,讓農民能真正得到補助照顧。 馬英九抨擊民進黨
            最近發放的造謠水果月曆,農民說台中紅柿一斤實際應該是41元,但民進黨卻硬將不能賣
            需再加工的次級品價格拿來說全部的紅柿一斤只有2元,嚴重傷害農民。馬主席譴責指出
            ,民進黨為了選舉犧牲農民的行為是不道德的,台灣人沒有這種不道德的傳統,「台灣人是
            正直、善良的,不做這種卑下的事情」,「任何一個有格調的政黨都不應該做這樣的事情」
            。 國民黨執政也改善兩岸關係,讓兩岸沒有戰爭,只有和平與繁榮,去年和中國大陸簽訂
            ECFA,對台中地區帶來很大幫助,工業方面台中地區機械工業成長了46%,自行車和
            汽車零組件成長了42%,農業方面造福了文心蘭、茶葉和香蕉,茶葉成長了一半以上,馬主席
            強調,他愛台灣,他推動兩岸關係永遠都為了台灣利益,台灣是他的家園也是他的國家
            ,他一定會確保中華民國主權獨立與完整,確保台灣的安全與尊嚴。 馬英九說,政府拼經濟
            讓台灣走出金融風暴,但未來幾個月因為歐債和美債的問題,又會有嚴峻的情勢出現,主計處
            預估今年的經濟成長還有4.51%,但明年會降到4.19%,尤其是明年總統選舉的第一季情況
            很差,正因為如此,台灣更需要能將經濟帶上正軌的政府。 他說,民進黨不只用不入流的做法
            打擊農民,還鋪天蓋地的進行抹黑,結果那個黑他們又說是好人,讓人感到莫名其妙,也不會
            放心讓他們執政,國民黨的不分區立委名單媒體民調獲得民眾45%的滿意,而民進黨不分區
            很多人都有案在身,卻還大肆抹黑,這樣的政黨是沒有希望的。
            '''
        ),
    )
    assert parsed_news.category == '政治'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1322463120
    assert parsed_news.reporter is None
    assert parsed_news.title == '馬英九:國民黨是能再次將台灣帶出經濟衰退的政黨'
    assert parsed_news.url_pattern == '9444'
