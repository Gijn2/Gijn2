package b_캡슐화;

public class CalculatorExpr {

	private int num1;
	private int num2;
	

	
	// --------------------------------------
	
	 int getGetAddition() {
		return num1 +num2;
	}
	
	 int getGetSubtraction() {
		int getSubtraction = num1 - num2;
		return getSubtraction;
	}
	
	 int getGetMultiplication() {
		int getMultiplication = num1*num2;
		return getMultiplication;
	}
	
	 double getGetDivision() {
		double getDivision = num1/num2;
		return getDivision;
	}
	 
	 //----------------------------------
	
	public int getNum1() {
		return num1;
	}
	public void setNum1(int num1) {
		this.num1 = num1;
	}
	public int getNum2() {
		return num2;
	}
	public void setNum2(int num2) {
		this.num2 = num2;
	}
	
	//----------------------------------
	
	
}
