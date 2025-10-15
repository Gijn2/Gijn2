package z_recursive;

//재기호출
public class AsumTestRecursive {
public static void main(String[] args) {
int sum = 0;
sum = sumFunc(5);
System.out.println(sum);
}
static int sumFunc(int i) {
	if( i ==1) {
		return 1;
	}
	return i+ sumFunc(i-1); // 재기호출: 함수 자신을 계속 불러도 된다.
	
	
}
}
