package l_collection;

import java.util.*;

public class Ex05_TreeSet {
	public static void main(String[] args) {
		
		TreeSet set = new TreeSet();
		set.add("horse");
		set.add("cat");
		set.add("dog");
		set.add("tiger");
		set.add("elephant");
		set.add("bee");
		set.add("coooowww");
		set.add("fox");
		set.add("dog");
		set.add("man");
		
		System.out.println(set);
		// 자동정렬, 중복처리 안됨
		System.out.println(set.subSet("d", "t"));
		// d 로 시작하는 애들부터 t 앞까지
		System.out.println(set.tailSet("e"));
		// e 로 ㅅㅣ작하는 애들부터
		System.out.println(set.headSet("e"));
		// e 앞까지
		
	}
}
