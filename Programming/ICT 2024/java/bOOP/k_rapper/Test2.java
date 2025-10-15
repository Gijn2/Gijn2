package k_rapper;

import java.util.ArrayList;

public class Test2 {
	public static void main(String[] args) {
		ArrayList list = method();
		for(int i =0; i <list.size(); i++) {
			System.out.println(list.get(i));
		}
	}

	static ArrayList method() {
		String name	  = "홀길동";
		int    age	  = 30;
		double height = 180.99;

		ArrayList list = new ArrayList(2); // Object[] 이면서 크기가 자동 증가됨
		list.add(name);
		list.add(age);
		list.add(height);
		
		//List:
		
		return list;
		
	}
}
