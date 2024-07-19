package j_final;


	abstract class Parent{
		   abstract  int  getNumber( );
		}
		public class Testing extends Parent {
		private  int  number = 100;
		int  getNumber() {   return  number;  }
		}
		// 오답: getNumber 의 private 뿐 아니라 Child class - public 을 바꿔줘야한다.
		// 물려받은 getNumber가 추상적이므로 private는 변경해줘야함.//
		
		// 5 **2번안되고 1번도 안됨
		
		// 3 ,내 자식 패키지만 사용가능한..
		
		// 1 ,역시 final 이야 믿고 있었어
		
		// 2 ,복붙
		
		// 2 ** 3번도 된다.
		
		// 2 ** super도 제일 위에 와야함 -> 3 ,(순서)super -> this -> ...
		
		/* 8번: 추상 함수가 있을 경우, 클래스는 무조건 추상 클래스 이어야하지만 추상클래스라고 추상 함수가 있을 필요는 없다.
		 * 	   추상 클래스는 객체 생성을 할 수가 없다.
		 */
		

