from app.cache import MemoryCache
from app.payments import PaymentService
from app.predictor import FrequencyPredictor


def test_cache_tracks_hits_misses_and_expired_entries():
    cache = MemoryCache()
    assert cache.get("missing") is None
    cache.set("k", {"v": 1})
    assert cache.get("k") == {"v": 1}
    snapshot = cache.snapshot()
    assert snapshot["hits"] == 1
    assert snapshot["misses"] == 1
    assert snapshot["hit_rate"] == 0.5


def test_frequency_predictor_recommends_most_accessed_keys():
    predictor = FrequencyPredictor()
    for key in ["a", "b", "a", "c", "a", "b"]:
        predictor.record(key)
    assert predictor.recommend(2) == ["a", "b"]


def test_payment_idempotency_and_approval_state():
    service = PaymentService()
    first = service.create("idem-1", 12.5, "usd", "vendor-1")
    duplicate = service.create("idem-1", 12.5, "USD", "vendor-1")
    assert first.payment_id == duplicate.payment_id
    assert service.approve(first.payment_id).status == "approved"
