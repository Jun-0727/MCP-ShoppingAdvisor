from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class SimpleMemoryCache:
    """메모리 전용 캐시 (재시작 시 초기화됨)"""
    
    def __init__(self, max_size: int = 1000):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self.max_size = max_size
    
    def get(self, product_name: str) -> Optional[Dict[str, Any]]:
        """캐시 조회"""
        key = product_name.lower()
        if key in self._cache:
            logger.debug(f"캐시 히트: {product_name}")
            return self._cache[key]
        return None
    
    def set(self, product_name: str, data: Dict[str, Any]):
        """캐시 저장"""
        key = product_name.lower()
        
        # 캐시 교체 알고리즘 - LRU
        if len(self._cache) >= self.max_size:
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
            logger.debug(f"캐시 용량 초과, 삭제: {oldest_key}")
        
        self._cache[key] = data
        logger.debug(f"캐시 저장: {product_name}")
    
    def clear(self):
        """전체 캐시 삭제"""
        self._cache.clear()
        logger.info("전체 캐시 초기화")
    
    def get_stats(self) -> Dict[str, Any]:
        """캐시 통계"""
        return {
            "total_products": len(self._cache),
            "max_size": self.max_size
        }

# 전역 인스턴스
cache_manager = SimpleMemoryCache(max_size=1000)