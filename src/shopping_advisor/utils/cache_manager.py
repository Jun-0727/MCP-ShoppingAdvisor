import os
import json
import logging
import sqlite3
from collections import OrderedDict
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from pathlib import Path
from dotenv import load_dotenv


logger = logging.getLogger(__name__)

load_dotenv()

# ──────────────────────────────────────────
# 1계층: 메모리 LRU 캐시
# ──────────────────────────────────────────

class MemoryCacheManager:
    """1차 메모리 캐시(LRU)"""
    
    def __init__(self, max_cache_size: int = 1000):
        self._cache: OrderedDict[str, Dict[str, Any]] = OrderedDict()
        self.max_cache_size = max_cache_size
    
    def _normalize_key(self, product_name: str) -> str:
        """제품명을 캐시 키로 변환 (공백 제거 및 소문자 변환)"""
        return product_name.replace(" ", "").lower()
    
    def get(self, product_name: str) -> Optional[Dict[str, Any]]:
        """캐시 조회"""
        key = self._normalize_key(product_name)
        
        if key in self._cache:
            self._cache.move_to_end(key)
            logger.debug(f"메모리 캐시 히트: {product_name}")
            return self._cache[key]
        
        return None
    
    def set(self, product_name: str, data: Dict[str, Any]) -> bool:
        """캐시 저장"""
        try:
            key = self._normalize_key(product_name)
            
            if len(self._cache) >= self.max_cache_size:
                oldest_key, _ = self._cache.popitem(last=False)
                logger.debug(f"캐시 용량 초과, 캐시 삭제: {oldest_key}")
            
            self._cache[key] = data
            logger.debug(f"메모리 캐시 저장: {product_name}")
            return True
        
        except Exception as e:
            logger.error(f"메모리 캐시 저장 실패: {product_name}, 오류: {e}")
            return False
    
    def delete(self, product_name: str) -> bool:
        """캐시 삭제"""
        try:
            key = self._normalize_key(product_name)
            self._cache.pop(key, None)
            logger.debug(f"메모리 캐시 삭제: {product_name}")
            return True

        except Exception as e:
            logger.error(f"메모리 캐시 삭제 실패: {product_name}, 오류: {e}")
            return False

    def clear(self):
        """전체 캐시 초기화"""
        try:
            self._cache.clear()
            logger.info("메모리 캐시 초기화")
            return True
        
        except Exception as e:
            logger.error(f"전체 캐시 초기화 실패, 오류 : {e}")
            return False    
    
    @property
    def size(self) -> int:
        return len(self._cache)

 
# ──────────────────────────────────────────
# 2계층: SQLite 캐시
# ──────────────────────────────────────────

class DBCacheManager:
    """2차 DB(SQLite) 캐시"""
 
    def __init__(self, db_path: str, cache_days: int = 30):
        self.db_path = db_path
        self.cache_days = cache_days
        self._init_database()
 
    def _init_database(self):
        """테이블 생성"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS product_cache (
                        id           INTEGER PRIMARY KEY AUTOINCREMENT,
                        product_name TEXT UNIQUE NOT NULL,
                        product_data TEXT NOT NULL,
                        created_at   TEXT NOT NULL,
                        accessed_at  TEXT NOT NULL
                    )
                """)
                conn.commit()
            logger.info(f"DB 캐시 초기화 완료: {self.db_path}")
        
        except Exception as e:
            logger.error(f"DB 초기화 실패: {e}", exc_info=True)
            raise
 
    def _normalize(self, product_name: str) -> str:
        """공백 제거 및 소문자 변환"""
        return product_name.replace(" ", "").lower()

    def get(self, product_name: str) -> Optional[Dict[str, Any]]:
        """캐시 조회 — 만료 시 자동 삭제 후 None 반환"""
        key = self._normalize(product_name)
 
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "SELECT product_data, created_at FROM product_cache WHERE product_name = ?",
                    (key,)
                )
                row = cursor.fetchone()
 
                if not row:
                    return None
 
                product_data, created_at = row
 
                # 데이터 유효성 만료 확인
                if datetime.now() - datetime.fromisoformat(created_at) > timedelta(days=self.cache_days):
                    logger.info(f"DB 캐시 만료: {product_name}")
                    self.delete(product_name)
                    return None
 
                # 접근 시간 갱신
                conn.execute(
                    "UPDATE product_cache SET accessed_at = ? WHERE product_name = ?",
                    (datetime.now().isoformat(), key)
                )
                conn.commit()
 
                logger.debug(f"DB 캐시 히트: {product_name}")
                return json.loads(product_data)
 
        except Exception as e:
            logger.error(f"DB 캐시 조회 실패: {product_name}", exc_info=True)
            return None
 
    def set(self, product_name: str, data: Dict[str, Any]) -> bool:
        """캐시 저장"""
        key = self._normalize(product_name)
 
        try:
            now = datetime.now().isoformat()
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO product_cache
                        (product_name, product_data, created_at, accessed_at)
                    VALUES (?, ?, ?, ?)
                    """,
                    (key, json.dumps(data, ensure_ascii=False), now, now)
                )
                conn.commit()
            logger.debug(f"DB 캐시 저장: {key}")
            return True
 
        except Exception as e:
            logger.error(f"DB 캐시 저장 실패: {product_name}", exc_info=True)
            return False

    def delete(self, product_name: str) -> bool:
        """캐시 삭제"""
        key = self._normalize(product_name)
 
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "DELETE FROM product_cache WHERE product_name = ?",
                    (key,)
                )
                conn.commit()
            logger.debug(f"DB 캐시 삭제: {key}")
            return True
 
        except Exception as e:
            logger.error(f"DB 캐시 삭제 실패: {product_name}", exc_info=True)
            return False
 
    def delete_expired(self) -> bool:
        """만료된 항목 삭제"""
        try:
            expiry_date = (datetime.now() - timedelta(days=self.cache_days)).isoformat()
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "DELETE FROM product_cache WHERE created_at < ?",
                    (expiry_date,)
                )
                conn.commit()
            logger.info(f"만료 캐시 {cursor.rowcount}개 삭제")
            return True
 
        except Exception as e:
            logger.error("만료 캐시 삭제 실패", exc_info=True)
            return False
         
    def clear(self) -> bool:
        """전체 삭제"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("DELETE FROM product_cache")
                conn.commit()
            logger.info("DB 캐시 전체 초기화")
            return True
 
        except Exception as e:
            logger.error("DB 캐시 전체 초기화 실패", exc_info=True)
            return False
 
    def get_stats(self) -> Dict[str, Any]:
        """캐시 통계"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "SELECT COUNT(*), SUM(LENGTH(product_data)) FROM product_cache"
                )
                count, total_size = cursor.fetchone()
            return {
                "total_products": count or 0,
                "total_size_bytes": total_size or 0,
                "total_size_mb": round((total_size or 0) / 1024 / 1024, 2),
            }
        except Exception as e:
            logger.error("DB 캐시 통계 조회 실패", exc_info=True)
            return {}


class ProductCacheManager:
    """제품 정보 캐시 매니저 (SQLite + LRU 메모리 캐시)"""
    
    def __init__(self, cache_days: Optional[int] = None, max_cache_size: Optional[int] = None):
        db_path = self._resolve_db_path()
        
        # 명시한 경우 그대로, 아니면 환경변수, 그것도 없으면 기본값
        cache_days = cache_days if cache_days is not None else int(os.getenv("CACHE_EXPIRE_DAYS", "30"))
        max_cache_size = max_cache_size if max_cache_size is not None else int(os.getenv("MEMORY_CACHE_SIZE", "1000"))

        self._memory = MemoryCacheManager(max_cache_size=max_cache_size)
        self._db = DBCacheManager(db_path=db_path, cache_days=cache_days)

    def _resolve_db_path(self) -> str:
        """환경 변수에서 DB 경로 결정"""
        db_path_env = os.getenv("CACHE_DB_PATH", "data/product_cache.db")
        
        if not os.path.isabs(db_path_env):
            project_root = Path(__file__).parent.parent.parent.parent
            db_path = project_root / db_path_env
        else:
            db_path = Path(db_path_env)
 
        db_path.parent.mkdir(parents=True, exist_ok=True)
        return str(db_path)
    
    # ──────────────────────────────────────────
    # 공개 API
    # ──────────────────────────────────────────
 
    def get(self, product_name: str) -> Optional[Dict[str, Any]]:
        """제품 정보 조회"""

        # 1차: 메모리
        data = self._memory.get(product_name)
        if data:
            logger.info(f"메모리 캐시 히트: {product_name}")
            return data
 
        # 2차: DB
        data = self._db.get(product_name)
        if data:
            logger.info(f"DB 캐시 히트 → 메모리 write-back: {product_name}")
            self._memory.set(product_name, data)
            return data
    
        return None
    
    def set(self, product_name: str, data: Dict[str, Any]) -> bool:
        """메모리 + DB 동시 저장"""
        memory_ok = self._memory.set(product_name, data)
        db_ok = self._db.set(product_name, data)
 
        if memory_ok and db_ok:
            logger.info(f"캐시 저장 완료: {product_name}")
        else:
            logger.warning(f"캐시 저장 부분 실패 (memory={memory_ok}, db={db_ok}): {product_name}")
 
        return memory_ok and db_ok
 
    def delete(self, product_name: str) -> bool:
        """메모리 + DB 동시 삭제"""
        memory_ok = self._memory.delete(product_name)
        db_ok = self._db.delete(product_name)
        logger.info(f"캐시 삭제 완료: {product_name}")
        return memory_ok and db_ok
 
    def clear(self) -> bool:
        """메모리 + DB 전체 초기화"""
        memory_ok = self._memory.clear()
        db_ok = self._db.clear()
        logger.info("전체 캐시 초기화 완료")
        return memory_ok and db_ok
 
    def clear_old_cache(self) -> bool:
        """만료된 DB 캐시 정리 (메모리는 LRU로 자동 관리)"""
        return self._db.delete_expired()
 
    def get_cache_stats(self) -> Dict[str, Any]:
        """통합 캐시 통계"""
        db_stats = self._db.get_stats()
        return {
            **db_stats,
            "memory_cache_size": self._memory.size,
            "memory_cache_max": self._memory.max_cache_size,
        }
 
    # 내부 접근용 (테스트 호환)
    @property
    def _memory_cache(self) -> MemoryCacheManager:
        return self._memory
 
    @property
    def db_path(self) -> str:
        return self._db.db_path
 
 
# 전역 인스턴스
cache_manager = ProductCacheManager()