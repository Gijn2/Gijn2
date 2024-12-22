package l_collection;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;

public class Ex04_LottoSet {
	public static void main(String[] args) {

		HashSet lottos = new HashSet();

		while(lottos.size() <6) {
			int num = (int)(Math.random()*45) + 1;
			lottos.add(num);
		}
		
		// System.out.println(lottos);
		ArrayList list = new ArrayList(lottos);
		Collections.sort(list);
		System.out.println(list);
	}
}