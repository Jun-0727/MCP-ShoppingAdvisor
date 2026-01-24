import sys
import json
import asyncio
from pathlib import Path

# 경로 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from shopping_advisor.utils.tool import (
    get_product,
    create_shopping_guide,
    compare_products
)


async def test_get_product():
    """제품 상세 조회 테스트"""
    print("=" * 60)
    print("제품 상세 조회 테스트")
    print("=" * 60)
    
    product = input("제품명을 입력하세요 (예: 마샬 스피커): ").strip() or "마샬 스피커"
    
    print(f"\n🔍 '{product}'에 대한 정보 조회 중...\n")
    
    result = await get_product(product)

    if result:
        print("✅ 성공!")
        print("\n" + json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("❌ 실패")


async def test_create_shopping_guide():
    """쇼핑 가이드 생성 테스트"""
    print("=" * 60)
    print("쇼핑 가이드 생성 테스트")
    print("=" * 60)
    
    product = input("제품명을 입력하세요 (예: 마샬 스피커): ").strip() or "마샬 스피커"
    
    print(f"\n🔍 '{product}'에 대한 쇼핑 가이드 생성 중...\n")
    
    guide = await create_shopping_guide(product)
    
    if guide:
        print("✅ 성공!")
        print("\n" + json.dumps(guide, ensure_ascii=False, indent=2))
    else:
        print("❌ 실패")


async def test_comapre_products():
    """제품 비교 테스트"""
    print("=" * 60)
    print("제품 비교 테스트")
    print("=" * 60)
    
    product_list = list(split(",") for split in input("비교할 제품명을 쉼표(,)로 구분하여 입력하세요 (예: 아이폰16, 갤럭시24)"))

    print(f"\n🔍 '{product_list}' 제품 비교중...\n")
    
    guide = await compare_products(product_list)
    
    if guide:
        print("✅ 성공!")
        print("\n" + json.dumps(guide, ensure_ascii=False, indent=2))
    else:
        print("❌ 실패")


async def main():
    """메인 메뉴"""
    while True:
        print("\n" + "=" * 60)
        print("테스트 메뉴")
        print("=" * 60)
        print("1. 제품 정보 조회 테스트")
        print("2. 쇼핑 가이드 생성 테스트")
        print("3. 제품 비교 테스트")
        print("4. 종료")
        print("=" * 60)
        
        choice = input("\n선택 (1-4): ")
        
        if choice == "1":
            await test_get_product()
        elif choice == "2":
            await test_create_shopping_guide()
        elif choice == "3":
            await test_comapre_products()
        elif choice == "4":
            print("\n👋 종료합니다.")
            break
        else:
            print("\n⚠️  잘못된 선택입니다.")


if __name__ == "__main__":
    print("\n🚀 GPT-4 API 수동 테스트 시작\n")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 사용자에 의해 종료되었습니다.")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()