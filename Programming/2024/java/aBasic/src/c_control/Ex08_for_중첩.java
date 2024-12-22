package c_control;

public class Ex08_for_중첩 {
	public static void main(String[] args) {

		//힘드네요
		System.out.print("*");

		for(int a1 = 1; a1 <=4; a1++) {
			System.out.println("");
			for(int a = 1;a<=5;a++) {
				System.out.print("*");
			}
		}
		
		//------------비교용--------------------------

		for(int a2 = 0; a2 <=4; a2++) {
			System.out.println("");
			for(int a3 = 1;a3<=a2+1;a3++) {
				System.out.print("*");
			}
		}
		
		//--------------정신나갈거같아--------------------
		for(int a2 = 0; a2 <=4; a2++) {
			System.out.println("");
			for(int a3 = 1;a3<=5-a2;a3++) {
				System.out.print("*");
			}
		}











	}
}
