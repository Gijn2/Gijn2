package l_collection;

import java.util.ArrayList;
import java.util.Iterator;

public class Ex02_ArrayList02 {
	public static void main(String[] args) {
	
		ArrayList<Student> list = method();
		
		//		// 원래 for 문 
		//		for(int i = 0; i <list.size(); i++) {
		//			Student s = (Student)list.get(i);
		//			System.out.println(s.toString());
		//			
		//		}
		
		// 향상된 for 문 - 배열, List, set 등의 집합 구조에서만 사용가능. + 집합구조가 generics 되어있어야함
		for(Student s :list) {
			System.out.println(s.toString());
		}
		
		// 순서대로 검색만 하는 구조 	    **참고
		// Enumeration  -> Iterator
		
		Iterator it = list.iterator();
		while(it.hasNext()) {
			System.out.println(it.next().toString());
		}
		
	}

	
	
	
	//함수
	static ArrayList<Student> method() {

		ArrayList<Student> list = new ArrayList<Student>();

		list.add(new Student("홍길동",22));
		list.add(new Student("홍길자",23));
		list.add(new Student("홍길쇠",32));

		return list;

	}
}
