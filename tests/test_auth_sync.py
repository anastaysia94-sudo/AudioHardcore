from backend.app.auth import hash_password, verify_password, issue_token, verify_token
from core.sync import Change, merge_change

def test_password_token_roundtrip():
    encoded=hash_password('secret')
    assert verify_password('secret',encoded)
    assert not verify_password('wrong',encoded)
    token=issue_token('u1','test-secret',ttl_seconds=10)
    assert verify_token(token,'test-secret')=='u1'
    assert verify_token(token,'wrong') is None

def test_merge_policies():
    local=Change('track','1','rating',4,'2026-01-01T00:00:00+00:00','a')
    remote=Change('track','1','rating',5,'2026-01-02T00:00:00+00:00','b')
    assert merge_change(local,remote).winner.value==5
    assert merge_change(local,remote,user_preference='local').winner.value==4
