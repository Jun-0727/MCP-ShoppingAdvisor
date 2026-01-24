"""
Formatter 수동 테스트 스크립트.

직접 실행하여 마크다운 변환 결과를 확인합니다.
"""

import sys
from pathlib import Path

# 프로젝트 루트 경로 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from shopping_advisor.utils.formatter import MarkdownFormat


def test_product_info():
    """제품 정보 마크다운 변환 테스트"""
    print("=" * 60)
    print("제품 정보 마크다운 변환 테스트")
    print("=" * 60)
    
    sample_data = {
        "features": [
            "40W 스테레오 사운드",
            "블루투스 5.0 지원",
            "빈티지 디자인"
        ],
        "pros": [
            "풍부한 중저음",
            "인테리어 효과 우수",
            "견고한 빌드 퀄리티"
        ],
        "cons": [
            "무거운 무게 (5.5kg)",
            "높은 가격대",
            "휴대성 부족"
        ],
        "purchase_notes": [
            "정품 여부 확인 필수",
            "보증 기간 확인",
            "전압 호환성 체크"
        ]
    }
    
    result = MarkdownFormat.product_info(sample_data)
    
    print("\n📤 마크다운 변환 결과:")
    print("-" * 40)
    print(result)
    print("-" * 40)


def test_shopping_guide():
    """쇼핑 가이드 마크다운 변환 테스트"""
    print("=" * 60)
    print("쇼핑 가이드 마크다운 변환 테스트")
    print("=" * 60)
    
    sample_data = {
        "product_info": {
            "features": ["프리미엄 사운드", "무선 연결"],
            "pros": ["음질 우수"],
            "cons": ["가격 높음"],
            "purchase_notes": ["정품 확인"]
        },
        "mall_info": {
            "recommend_malls": [
                {
                    "mall_name": "쿠팡",
                    "reason": "로켓배송으로 빠른 수령 가능",
                    "url": "https://www.coupang.com"
                },
                {
                    "mall_name": "네이버 쇼핑",
                    "reason": "가격 비교에 유리",
                    "url": "https://shopping.naver.com"
                }
            ]
        }
    }
    
    result = MarkdownFormat.shopping_guide(sample_data)
    
    print("\n📤 마크다운 변환 결과:")
    print("-" * 40)
    print(result)
    print("-" * 40)


def test_comparison_data():
    """제품 비교 마크다운 변환 테스트"""
    print("=" * 60)
    print("제품 비교 마크다운 변환 테스트")
    print("=" * 60)
    
    sample_data = {
        "products": ["아이폰 16", "갤럭시 S24"],
        "comparison_table": {
            "디스플레이": {
                "아이폰 16": "6.1인치 Super Retina XDR",
                "갤럭시 S24": "6.2인치 Dynamic AMOLED 2X"
            },
            "카메라": {
                "아이폰 16": "48MP 메인 + 12MP 울트라와이드",
                "갤럭시 S24": "50MP 메인 + 12MP 울트라와이드 + 10MP 망원"
            },
            "배터리": {
                "아이폰 16": "3,561mAh",
                "갤럭시 S24": "4,000mAh"
            }
        },
        "overall_summary": "사진 촬영이 중요하다면 갤럭시 S24, 생태계 연동이 중요하다면 아이폰 16을 추천합니다."
    }
    
    result = MarkdownFormat.comparison_data(sample_data)
    
    print("\n📤 마크다운 변환 결과:")
    print("-" * 40)
    print(result)
    print("-" * 40)


def main():
    """메인 메뉴"""
    while True:
        print("\n" + "=" * 60)
        print("Formatter 테스트 메뉴")
        print("=" * 60)
        print("1. 제품 정보 마크다운 변환")
        print("2. 쇼핑 가이드 마크다운 변환")
        print("3. 제품 비교 마크다운 변환")
        print("4. 종료")
        print("=" * 60)
        
        choice = input("\n선택 (1-9): ")
        
        if choice == "1":
            test_product_info()
        elif choice == "2":
            test_shopping_guide()
        elif choice == "3":
            test_comparison_data()
        elif choice == "4":
            print("\n👋 종료합니다.")
            break
        else:
            print("\n⚠️ 잘못된 선택입니다.")


if __name__ == "__main__":
    print("\n🚀 Formatter 수동 테스트 시작\n")
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 사용자에 의해 종료되었습니다.")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()