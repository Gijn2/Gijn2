package i_inherit3;

public class Main {
	public static void main(String[] args) {
		Item[] result = method();
		//output() 호출해서 여기 출력
		for(int i =0; i <result.length; i++) {
			result[i].output();
			// 
			// result 값을 돌리면 여러값이 나오는 이유: overriding
		}
	}

	static Item[] method() {
		// void에서 값을 return 해야하므로 배열함수로 변경
		Book b = new Book("가","나","다","라");
		Dvd d = new Dvd();
		Cd c = new Cd();
		//여기서 모든 값을 다 가져오고 싶을 때, 배열함수에 넣어서 값을 가져와라
		
		Item[]i = new Item[3];
		i[0] = b;
		i[1] = d;
		i[2] = c;
		
		return i;
	}
	
}
