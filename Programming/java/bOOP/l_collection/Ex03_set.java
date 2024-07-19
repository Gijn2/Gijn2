package l_collection;

import java.util.HashSet;

public class Ex03_set {
	public static void main(String[] args) {
		HashSet set = new HashSet();		//set 의 가장 대표적인 명령어 HashSet
		set.add("horse");
		set.add("ant");
		set.add("zebra");
		set.add("mouse");
		set.add("dog");
		set.add("tiger");
		set.add("dog");
		set.add("rabbit");
		
		System.out.println(set);
		// 순서가 뒤죽박죽, 중복처리도 안됨. 사용 예시, 로또
	}
}
