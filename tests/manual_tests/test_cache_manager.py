"""
캐시 매니저 수동 테스트 스크립트.

직접 실행하여 SimpleMemoryCache 및 ProductCacheManager 동작을 확인합니다.
"""

import sys
import os
import json
import tempfile
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

# 프로젝트 루트 경로 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from shopping_advisor.utils.cache_manager import (
    MemoryCacheManager, 
    DBCacheManager, 
    ProductCacheManager
)


SAMPLE_PRODUCT = {
    "name": "아이폰 16",
    "data" : {
        "features": [
            "특징1",
            "특징2"
        ],
        "pros": [
            "장점1",
            "장점2"
        ],
        "cons": [
            "단점1",
            "단점2"
        ],
        "purchase_notes": [
            "구매 전 확인사항1"
        ]
    }
}


# ──────────────────────────────────────────
# MemoryCache 테스트
# ──────────────────────────────────────────
memeory_cache = MemoryCacheManager(max_cache_size=10)

def test_memory_cache_set():
    """[SimpleMemoryCache] 제품 저장 테스트"""
    print("=" * 60)
    print("제품 저장 테스트")
    print("=" * 60)
    
    product = input("제품명을 입력하세요 (예: 마샬 스피커): ")    
    
    if memeory_cache.set(product, SAMPLE_PRODUCT):
        print(f"\n✅ '{product}' 제품 저장 완료")
    else:
        print(f"\n❌ '{product}' 제품 저장 실패")

def test_memory_cache_get():
    """[SimpleMemoryCache] 제품 조회 테스트"""
    print("=" * 60)
    print("제품 조회 테스트")
    print("=" * 60)
    
    product = input("제품명을 입력하세요 (예: 마샬 스피커): ")    
    
    result = memeory_cache.get(product)
    
    if result:
        print("\n✅ 제품 조회 성공!")
        print("\n" + json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("\n❌ 제품 조회 실패")

def test_memory_cache_delete():
    """[SimpleMemoryCache] 제품 삭제 테스트"""
    print("=" * 60)
    print("제품 삭제 테스트")
    print("=" * 60)
    
    product = input("제품명을 입력하세요 (예: 마샬 스피커): ")    
    
    if memeory_cache.delete(product):
        print(f"\n✅ '{product}' 제품 삭제 완료")
    else:
        print(f"\n❌ '{product}' 제품 삭제 실패")   

def test_memory_cache_clear():
    """전체 초기화"""
    print("=" * 60)
    print("[SimpleMemoryCache] 전체 초기화 테스트")
    print("=" * 60)

    if memeory_cache.clear():
        if memeory_cache.size == 0:
            print("\n✅ 전체 캐시 초기화 완료")
    else:
        print("\n❌ 전체 캐시 초기화 실패")
        
def test_memory_cache_lru_algorithm():
    """LRU 교체 알고리즘 — 용량 초과 시 가장 오래된 항목 제거"""
    print("=" * 60)
    print("[MemoryCache] LRU 교체 알고리즘")
    print("=" * 60)

    memeory_cache = MemoryCacheManager(max_cache_size=3)

    memeory_cache.set("상품A", {"id": "A"})
    memeory_cache.set("상품B", {"id": "B"})
    memeory_cache.set("상품C", {"id": "C"})

    # 상품A를 조회해 최근 사용으로 갱신
    memeory_cache.get("상품A")

    # 새 항목 추가 → 가장 오래된 상품B가 제거되어야 함
    memeory_cache.set("상품D", {"id": "D"})

    assert memeory_cache.get("상품B") is None, "상품B가 제거되어야 합니다"
    assert memeory_cache.get("상품A") is not None, "상품A는 최근 사용됐으므로 유지되어야 합니다"
    assert memeory_cache.get("상품C") is not None, "상품C는 유지되어야 합니다"
    assert memeory_cache.get("상품D") is not None, "상품D는 새로 추가됐으므로 있어야 합니다"
    print("✅ LRU 교체 정상 동작 (상품B 제거, 나머지 유지)")


_tmp_db_dir = tempfile.TemporaryDirectory()
db = DBCacheManager(db_path=str(Path(_tmp_db_dir.name) / "test_cache.db"))

def test_db_cache_get():
    """[DBCacheManager] 제품 조회 테스트"""
    print("=" * 60)
    print("제품 조회 테스트")
    print("=" * 60)
    
    product = input("제품명을 입력하세요 (예: 마샬 스피커): ")    
    
    result = db.get(product)
    
    if result:
        print("\n✅ 제품 조회 성공!")
        print("\n" + json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("\n❌ 제품 조회 실패")

def test_db_cache_set():
    """[DBCacheManager] 제품 저장 테스트"""
    print("=" * 60)
    print("[DBCacheManager] 제품 저장 테스트")
    print("=" * 60)
    
    product = input("제품명을 입력하세요 (예: 마샬 스피커): ")    
    
    if db.set(product, SAMPLE_PRODUCT):
        print(f"\n✅ '{product}' 제품 저장 완료")
    else:
        print(f"\n❌ '{product}' 제품 저장 실패")

def test_db_cache_delete():
    """[DBCacheManager] 제품 삭제 테스트"""
    print("=" * 60)
    print("[DBCacheManager] 제품 삭제 테스트")
    print("=" * 60)
    
    product = input("제품명을 입력하세요 (예: 마샬 스피커): ")    

    if db.delete(product):
        print(f"\n✅ '{product}' 제품 삭제 완료")
    else:
        print(f"\n❌ '{product}' 제품 삭제 실패")

def test_db_cache_clear():
    """[DBCacheManager] 전체 초기화 테스트"""
    print("=" * 60)
    print("[DBCacheManager] 전체 초기화 테스트")
    print("=" * 60)

    if db.clear():
        print("\n✅ 전체 캐시 초기화 완료")
    else:
        print("\n❌ 전체 캐시 초기화 실패")

def test_db_cache_delete_expired():
    """[DBCacheManager] 만료된 캐시 삭제 테스트"""
    print("=" * 60)
    print("만료된 캐시 삭제 테스트")
    print("=" * 60)

    if db.delete_expired():
        print("\n✅ 만료된 캐시 삭제 완료")
    else:
        print("\n❌ 만료된 캐시 삭제 실패")

def test_db_cache_stats():
    """DBCacheManager] 캐시 통계 조회 테스트"""
    print("=" * 60)
    print("캐시 통계 조회 테스트")
    print("=" * 60)


    stats = db.get_stats()

    if stats:
        print("\n✅ 캐시 통계 조회 성공!")
        print("\n" + json.dumps(stats, ensure_ascii=False, indent=2))
    else:
        print("\n❌ 캐시 통계 조회 실패")


# ──────────────────────────────────────────
# ProductCacheManager 자동 테스트
# ──────────────────────────────────────────
 
def _make_manager(tmp_dir: str, cache_days: int = 30) -> ProductCacheManager:
    """테스트용 임시 DB를 사용하는 매니저 생성"""
    os.environ["CACHE_DB_PATH"] = str(Path(tmp_dir) / "test_cache.db")
    os.environ["CACHE_EXPIRE_DAYS"] = str(cache_days)
    return ProductCacheManager(cache_days=1, max_cache_size=5)
 
def test_cache_set():
    """set — 메모리 + DB 동시 저장 확인"""
    print("=" * 60)
    print("[ProductCacheManager] set 테스트")
    print("=" * 60)
 
    with tempfile.TemporaryDirectory() as tmp:
        manager = _make_manager(tmp)
 
        assert manager.get("아이폰 16") is None, "초기 조회는 None이어야 합니다"
 
        result = manager.set("아이폰 16", SAMPLE_PRODUCT)
        assert result is True, "set은 True를 반환해야 합니다"
 
        # 메모리 캐시 확인
        assert manager._memory.get("아이폰 16") is not None, "메모리 캐시에 저장되어야 합니다"
 
        # DB 캐시 확인
        assert manager._db.get("아이폰 16") is not None, "DB 캐시에 저장되어야 합니다"
 
        print("✅ 메모리 + DB 동시 저장 확인")
 
 
def test_cache_get():
    """get — 메모리 히트 → DB 히트 → write-back 확인"""
    print("=" * 60)
    print("[ProductCacheManager] get 테스트")
    print("=" * 60)
 
    with tempfile.TemporaryDirectory() as tmp:
        manager = _make_manager(tmp)
        manager.set("갤럭시 S24", SAMPLE_PRODUCT)
 
        # 1차: 메모리 캐시 히트
        result = manager.get("갤럭시 S24")
        assert result == SAMPLE_PRODUCT, "메모리 캐시 조회 결과가 달라서는 안 됩니다"
        print("✅ 메모리 캐시 히트 확인")
 
        # 2차: 메모리 비운 뒤 DB에서 복구
        manager._memory.clear()
        assert manager._memory.get("갤럭시 S24") is None, "메모리 캐시가 비워져야 합니다"
 
        result = manager.get("갤럭시 S24")
        assert result == SAMPLE_PRODUCT, "DB에서 복구된 데이터가 달라서는 안 됩니다"
        print("✅ DB 캐시 히트 확인")
 
        # write-back 확인
        assert manager._memory.get("갤럭시 S24") is not None, "write-back 후 메모리에 없습니다"
        print("✅ write-back으로 메모리 재적재 확인")
 
 
def test_cache_delete():
    """delete — 메모리 + DB 양쪽 제거 확인"""
    print("=" * 60)
    print("[ProductCacheManager] delete 테스트")
    print("=" * 60)
 
    with tempfile.TemporaryDirectory() as tmp:
        manager = _make_manager(tmp)
        manager.set("아이폰 16", SAMPLE_PRODUCT)
 
        result = manager.delete("아이폰 16")
        assert result is True, "delete는 True를 반환해야 합니다"
        assert manager.get("아이폰 16") is None,          "삭제 후 조회 시 None이어야 합니다"
        assert manager._memory.get("아이폰 16") is None,  "메모리 캐시도 삭제되어야 합니다"
        assert manager._db.get("아이폰 16") is None,      "DB 캐시도 삭제되어야 합니다"
        print("✅ 메모리 + DB 동시 삭제 확인")
 
 
def test_cache_clear():
    """clear — 메모리 + DB 전체 초기화 확인"""
    print("=" * 60)
    print("[ProductCacheManager] clear 테스트")
    print("=" * 60)
 
    with tempfile.TemporaryDirectory() as tmp:
        manager = _make_manager(tmp)
        manager.set("상품A", {"id": "A"})
        manager.set("상품B", {"id": "B"})
 
        result = manager.clear()
        assert result is True, "clear는 True를 반환해야 합니다"
 
        stats = manager.get_cache_stats()
        assert stats["total_products"] == 0,   "전체 삭제 후 DB가 비어야 합니다"
        assert manager._memory.size == 0,      "전체 삭제 후 메모리 캐시도 비어야 합니다"
        print("✅ 메모리 + DB 전체 초기화 확인")
 
 
def test_cache_expiry():
    """만료된 캐시 — 조회 시 None 반환 확인"""
    print("=" * 60)
    print("[ProductCacheManager] 캐시 만료 처리 테스트")
    print("=" * 60)
 
    with tempfile.TemporaryDirectory() as tmp:
        manager = _make_manager(tmp, cache_days=0)
        manager.set("구형제품", SAMPLE_PRODUCT)
 
        # DB의 created_at을 과거로 강제 조작
        past = (datetime.now() - timedelta(days=1)).isoformat()
        with sqlite3.connect(manager.db_path) as conn:
            conn.execute(
                "UPDATE product_cache SET created_at = ? WHERE product_name = ?",
                (past, "구형제품")
            )
            conn.commit()
 
        # 메모리 비워서 DB 경로 강제
        manager._memory.clear()
 
        result = manager.get("구형제품")
        assert result is None, "만료된 캐시는 None을 반환해야 합니다"
        print("✅ 만료된 캐시 None 반환 확인")
 
 
def test_cache_stats():
    """get_cache_stats — 통계 정보 확인"""
    print("=" * 60)
    print("[ProductCacheManager] get_cache_stats 테스트")
    print("=" * 60)
 
    with tempfile.TemporaryDirectory() as tmp:
        manager = _make_manager(tmp)
        manager.set("상품1", {"data": "a" * 100})
        manager.set("상품2", {"data": "b" * 200})
 
        stats = manager.get_cache_stats()
        assert stats["total_products"] == 2,   "저장한 항목 수와 통계가 다릅니다"
        assert stats["total_size_bytes"] > 0,  "크기가 0보다 커야 합니다"
        assert stats["memory_cache_size"] == 2, "메모리 캐시 크기가 다릅니다"
 
        print(f"✅ 통계 정상 조회:")
        print(f"   - 총 상품 수       : {stats['total_products']}")
        print(f"   - 총 크기          : {stats['total_size_bytes']} bytes ({stats['total_size_mb']} MB)")
        print(f"   - 메모리 캐시      : {stats['memory_cache_size']} / {stats['memory_cache_max']}")
 
 
# ──────────────────────────────────────────
# 메뉴
# ──────────────────────────────────────────
 
def _run_auto_tests():
    """ProductCacheManager 자동 테스트 일괄 실행"""
    auto_tests = [
        ("set — 메모리 + DB 동시 저장",      test_cache_set),
        ("get — 메모리/DB 히트 + write-back", test_cache_get),
        ("delete — 메모리 + DB 동시 삭제",    test_cache_delete),
        ("clear — 전체 초기화",               test_cache_clear),
        ("캐시 만료 처리",                    test_cache_expiry),
        ("get_cache_stats — 통계 조회",       test_cache_stats),
    ]
 
    passed, failed = 0, 0
    for name, fn in auto_tests:
        try:
            fn()
            passed += 1
        except Exception as e:
            print(f"❌ FAILED [{name}]: {e}")
            failed += 1
 
    print("\n" + "=" * 60)
    print(f"결과: {passed}개 통과 / {failed}개 실패 (총 {len(auto_tests)}개)")
    print("=" * 60)
 
 
def main():
    """메인 메뉴"""
    while True:
        print("\n" + "=" * 60)
        print("캐시 매니저 테스트 메뉴")
        print("=" * 60)
        print("──── MemoryCacheManager ────")
        print("1.  저장 테스트")
        print("2.  조회 테스트")
        print("3.  삭제 테스트")
        print("4.  전체 초기화 테스트")
        print("5.  데이터 교체(LRU) 테스트")
        print("──── DBCacheManager ────")
        print("6.  저장 테스트")
        print("7.  조회 테스트")
        print("8.  삭제 테스트")
        print("9.  전체 초기화 테스트")
        print("10. 만료 데이터 삭제 테스트")
        print("11. 통계 조회 테스트")
        print("──── ProductCacheManager (자동) ────")
        print("12. 전체 자동 테스트 실행")
        print("=" * 60)
        print("0.  종료")
        print("=" * 60)
 
        choice = input("\n선택: ").strip()
 
        if   choice == "1":  test_memory_cache_set()
        elif choice == "2":  test_memory_cache_get()
        elif choice == "3":  test_memory_cache_delete()
        elif choice == "4":  test_memory_cache_clear()
        elif choice == "5":  test_memory_cache_lru_algorithm()
        elif choice == "6":  test_db_cache_set()
        elif choice == "7":  test_db_cache_get()
        elif choice == "8":  test_db_cache_delete()
        elif choice == "9":  test_db_cache_clear()
        elif choice == "10": test_db_cache_delete_expired()
        elif choice == "11": test_db_cache_stats()
        elif choice == "12": _run_auto_tests()
        elif choice == "0":
            print("\n👋 종료합니다.")
            break
        else:
            print("\n⚠️  잘못된 선택입니다.")
 
 
if __name__ == "__main__":
    print("\n캐시 매니저 수동 테스트 시작\n")
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 사용자에 의해 종료되었습니다.")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
 