package l_collection;

/* 스택과 큐
 * 
 * - 스택(LIFO): 라스트 인 퍼스트 아웃
 * - 큐 (FIFO): 퍼스트 인 퍼스트 아웃
 * 
 */

import java.util.Stack;

public class Ex09_StackQueue {
	public static void main(String[] args) {

		Stack stack = new Stack();
		stack.push("A");
		stack.push("B");
		stack.push("C");
		while(!stack.empty()) {
			System.out.println(stack.pop());
		}
	}
}
