import kuzu
import pytest

from NowDotAI.storage import NowDotAIKuzuGraphStore


class GraphStoreFixtures:
    @pytest.fixture
    def kuzu_graph_store(self, tmpdir):
        db_path = tmpdir / "test_db"
        db = kuzu.Database(str(db_path))

        graph_store = NowDotAIKuzuGraphStore(db)
        return graph_store

    @pytest.fixture
    def graph_store(self, request, kuzu_graph_store):
        graph_stores = {
            "kuzu": kuzu_graph_store,
        }
        return graph_stores.get(request.param)
