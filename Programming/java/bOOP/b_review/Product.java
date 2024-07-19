package b_review;

public class Product {
	
private int productNo;
private String productName;
private int stock;

//--------
public void setProductNo(int productNo) {
	this.productNo = productNo;
}
public void setProductName(String productName) {
	this.productName = productName;
}
public void setStock(int stock) {
	this.stock = stock;
}

//--------

public int income(int a) {
	stock += a;
	return stock;
}

public int sale(int b) {
	stock -= b;
return stock-0;	
}

public void output() {
	System.out.println("품번: "+productNo+", 품명: "+productName+", 재고: "+stock);
}

}
