package e_method;

public class Ex02_반환2 {
public static void main(String[] args) {
	
	int [] data = add();
	// 함수 안의 a, b 를 합산 후 출력
	
	int sum = data[0] + data[1];
	System.out.println(sum);
}

static int[] add() {
	int a= 10, b= 20;
	int [] data = {a,b}; // 함수 내 data 라는 가상 배열변수 안에 두 개의 인덱스로 저장
	
	return data; // 리턴할 수 있는 가상 변수는 한 개
	
}

}
