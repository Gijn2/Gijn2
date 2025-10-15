package a_datatype;

public class Ex04_char {
public static void main(String[] args) {
	
	char ch = 'A'; // 2 byte
	
	int i = 'A';   // 4 byte
	
	 System.out.println("문자는"+ i);
	// '문자는65'로 찍힌다 -> 고로 캐스팅처리
	 System.out.println((char)i);
	
	/**
	 1. 자바 언어 이전의 문자체제는 아스키코드 (ascii-code) 자바는 unicode
	 [asci-code] -- 1byte(2^8개 문자표현가능)
	 	영어 숫자 특수기호 등만 표현
	 
	 'A' = 0100(대문자) 0001(1번 = A) => 2^6 + 2^0 = 65 **위에 65가 찍힌 이유
	 'E' = 0100 0101 = 2^6 + 2^2 +2^0 = 69
	 
	 'a' = 0110(소문자) 0001(첫 영단어) => 이진법 계산은.. 64 32 1 = 97 
	 'b' = 0110 0010 => (생략)64 32 2 = 98
	 
	 
	 [uni-code] -- 2Byte(2^16만큼의 문자표현)
	 asci-code에 더불어 일본어, 한국어 등 일부 다른 외국어들도 포함
	 - 표현 '/u0000'
	 
	 2. cmd 자바 
	 
	 */
	 
	 
}
}
