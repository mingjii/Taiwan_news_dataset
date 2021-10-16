import test.news.crawlers.conftest
from typing import Final, List

import news.crawlers.db.read
import news.crawlers.db.schema
import news.crawlers.ltn


def test_save_news_to_db(
    db_name: Final[str],
    response_200: Final[test.news.crawlers.conftest.MockResponse],
    cleanup_db_file: Final,
    monkeypatch: Final,
) -> None:
    r"""Save crawling news to database with correct format."""

    def mock_get_news_list(**kwargs) -> List[news.crawlers.db.schema.RawNews]:
        return [
            news.crawlers.db.schema.RawNews(
                idx=0,
                company_id=news.crawlers.ltn.COMPANY_ID,
                raw_xml='abc',
                url_pattern='123',
            ),
            news.crawlers.db.schema.RawNews(
                idx=0,
                company_id=news.crawlers.ltn.COMPANY_ID,
                raw_xml='def',
                url_pattern='456',
            ),
        ]

    monkeypatch.setattr(
        news.crawlers.ltn,
        'get_news_list',
        mock_get_news_list,
    )

    news.crawlers.ltn.main(db_name=db_name)

    all_records = news.crawlers.db.read.read_all_records(db_name=db_name)
    assert len(all_records)

    for record in all_records:
        assert isinstance(record, news.crawlers.db.schema.RawNews)
        assert isinstance(record.idx, int)
        assert record.company_id == news.crawlers.ltn.COMPANY_ID
        assert isinstance(record.raw_xml, str)
        assert isinstance(record.url_pattern, str)
