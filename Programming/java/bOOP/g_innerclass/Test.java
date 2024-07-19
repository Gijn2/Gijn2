package g_innerclass;

class Outer{

	static class Inner{
		static void najababa() {
			System.out.println("나 잡아봐");
		}
	}
}
//간단한거 testing 할 경우, class 를 따로 만들어 사용가능 *비추*
//outer 안 inner 클래스도 클래스를 따로 만들어준다.
public class Test {
	public static void main(String[] args) {

		//1. 일반
		//		Outer out = new Outer();
		//		Outer.Inner in = out.new Inner();
		//		in.najababa();

		//2. inner 에 static 이 잡혀있는 경우
		//		Outer.Inner in = new Outer.Inner();
		//		in.najababa();

		//3 najababa 도 static 이 잡혀있는 경우
		Outer.Inner.najababa();
	}
}
