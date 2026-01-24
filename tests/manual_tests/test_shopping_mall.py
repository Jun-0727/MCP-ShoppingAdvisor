"""
쇼핑몰 유틸리티 모듈 수동 테스트.

직접 실행하여 쇼핑몰 URL 생성 및 정보 조회 기능을 테스트합니다.
"""

import sys
from pathlib import Path

# 경로 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from shopping_advisor.utils.shopping_mall import (
    generate_shopping_mall_url,
    get_mall_all,
    get_mall_detail,
    get_mall_description,
    get_mall_pros,
    get_mall_cons,
    get_mall_best_for
)


def test_generate_shopping_mall_url():
    """제품 검색 링크 생성 테스트"""
    print("=" * 60)
    print("제품 검색 링크 생성 테스트")
    print("=" * 60)
    
    mall = input("쇼핑몰 이름을 입력하세요. (예: 쿠팡): ").strip() or "쿠팡"
    product = input("제품명을 입력하세요. (예: 아이폰 17): ").strip() or "아이폰 17"
    
    print(f"\n🔍 {mall}에서 '{product}' 검색 URL 생성 중...\n")
    
    url = generate_shopping_mall_url(mall, product)
    
    if url:
        print(f"✅ 성공!")
        print(f"{mall}에서 {product} 검색 링크: {url}")
    else:
        print(f"❌ 실패")


def test_get_mall_all():
    """쇼핑몰 목록 조회 테스트"""
    print("=" * 60)
    print("쇼핑몰 목록 조회 테스트")
    print("=" * 60)

    malls = get_mall_all()
    
    for i, mall in enumerate(malls, 1):
        print(f"{i:2d}. {mall:15s}")


def test_get_mall_detail():
    """쇼핑몰 상세 정보 조회 테스트"""
    print("=" * 60)
    print("쇼핑몰 상세 정보 조회 테스트")
    print("=" * 60)
    
    mall = input("쇼핑몰 이름 (예: 쿠팡): ").strip() or "쿠팡"
    
    info = get_mall_detail(mall)
    
    if info:
        print(f"\n✅ {mall} 정보:")
        print(f"   이름: {info['name']}")
        print(f"   설명: {get_mall_description(mall)}")
        print(f"   장점: {get_mall_pros(mall)}")
        print(f"   단점: {get_mall_cons(mall)}")
        print(f"   추천: {get_mall_best_for(mall)}")
    else:
        print(f"\n❌ '{mall}' 쇼핑몰을 찾을 수 없습니다.")


def main():
    """메인 메뉴"""
    while True:
        print("\n" + "=" * 60)
        print("쇼핑몰 유틸리티 모듈 테스트 메뉴")
        print("=" * 60)
        print("1. 제품 검색 링크 생성 테스트")
        print("2. 쇼핑몰 목록 조회 테스트")
        print("3. 쇼핑몰 상세 정보 조회")
        print("4. 종료")
        print("=" * 60)
        
        choice = input("\n선택 (1-4): ").strip()
        
        if choice == "1":
            test_generate_shopping_mall_url()
        elif choice == "2":
            test_get_mall_all()
        elif choice == "3":
            test_get_mall_detail()
        elif choice == "4":
            print("\n👋 종료합니다.")
            break
        else:
            print("\n⚠️  잘못된 선택입니다.")


if __name__ == "__main__":
    print("\n🚀 쇼핑몰 유틸리티 모듈 수동 테스트 시작\n")
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 사용자에 의해 종료되었습니다.")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()