package b_operator;

public class Ex04_shift {
public static void main(String[] args) {

	// shift 연산자는 각각 비트의 값을 이동하는 연산자 ** 솔직히 쓸 일 없다고 하심
	// ex. 0010
	// 		ㄴ 오른쪽으로 쉬프트 = 0001, 왼쪽으로 쉬프트 0100
	
	
	int a = 4;			// 0100
	int b = a << 2;		// 1000, 오른쪽 쉬프트
	int c = a >> 1;		// 0010, 왼쪽  쉬프트
	
	System.out.println(a+", "+b+", "+c);
	
	int d = a >>> 1;
	System.out.println(d); // 옮긴 친구 무조건 양수 만들기?
}
}
