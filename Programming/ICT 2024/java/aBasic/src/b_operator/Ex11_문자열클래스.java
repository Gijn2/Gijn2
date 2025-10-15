package b_operator;

public class Ex11_문자열클래스 {

	public static void main(String[] args) {
		/*
		 자바에서 문자열을 처리하는 클래스
		 - String, StringBuffer, StringBuilder
		 	- String 특권
		 	  ㄴ new ~ 생략가능
		 	  ㄴ + 연산가능 = 계속 문자를 연결가능
		 	- StringBuffer
		 	- StringBuilder
		 	  ㄴ Buffer와 거의 동일하지만 접근속도에 따른 구별이 있다.
		 	  ex. '가'와 '나'가 동시에 접근하려하면 먼저 접근한 '가' 외의 '나'는 접근불가
		 	  #OSI7계층
		 	  
		 	  String과 그 외의 차이점
		 	  메모리로 접근해버려
		 	  ex. String의 경우, '1'을 저장할 때, 1번 메모리공간에 '1'을 저장. 후에
		 	  		'1+1은?'로 내용을 추가할 경우, 1번 메모리 공간을 비우고 2번 메모리 공간에 '1+1은?'저장
		 	  
		 	  
		 	  
		 	  
		 	  
		 	  글자(내용)의 변화가 심화면 StringBuffer/Builder
		 	  글자(내용)의 변화가 적으면 String
		 	  ㄴString을 계속 쓰면 생기는 새로운 메모리 공간 외에 안쓰는공간은 자동수거된다.(쓰레기컬렉터가 이씀)
		 	  ㄴ 쓰레기(Garbage): 사용중이지 않은 메모리공간을 칭하는 말 // 가비지컬렉터랑 가비지 알아두자
		 	  
		 */

		/**
		String a = "홍길동";
		System.out.println(a);
		
		String a1 = "홍길동2";
		
		StringBuilder b = new StringBuilder("김길동");
		System.out.println(b);
		
		// StringBuilder b2 = "김길동2";
		// 에러나옴. 유일하게 String만 생략이가능. Builder,Buffer는 앞에 new String~(""); 쳐줘야댐.

		
		String a2 = "홍길동3";
		a2 += "힘내"; // s3 = s3 + "힘내" 			// String 특권
		
		b.append("힘내");							// String 외의 문자 연결방법
		*/
		
		
		
		
	}

}
