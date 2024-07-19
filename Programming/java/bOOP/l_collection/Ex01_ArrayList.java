package l_collection;

import java.util.ArrayList;
import java.util.Collections;

public class Ex01_ArrayList {
	public static void main(String[] args) {
		
		
		ArrayList<String> list = new ArrayList<String>(4);
		list.add("rabbit");
		list.add("tiger");
		list.add("lion");
		list.add("goat");
		list.add("fox");
		list.add("zebra");
		
		System.out.println(list);
		
		list.set(3, "dog");
		System.out.println(list);
		
		list.remove(0);
		System.out.println(list);
		
		Collections.sort(list);
		System.out.println(list);
	}
}
