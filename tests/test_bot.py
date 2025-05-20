def test_decision():
    from updater import get_decision
    assert "or" in get_decision("acheter gold").lower()
    assert "bitcoin" in get_decision("revendre BTC").lower()
    assert "aucune" in get_decision("je sais pas").lower()