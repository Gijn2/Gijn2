package d_constructure3;


public class GradeExpr {
	//멤버변수
	int[] jumsu;

	//생성자
	GradeExpr(int[]jumsu){
		this.jumsu = jumsu;
	}

	double getAverage(){
		double avg = (double)getTotal()/jumsu.length;
		return avg;
	}

	int getTotal() {
		int total = 0;
		for(int i =0;i <jumsu.length; i++) {
			total += jumsu[i];
		}
		return total;
	}

	int getGoodScore() {
		int goodScore = jumsu[0];
		for(int i =0; i <jumsu.length; i++) {
			if(goodScore<jumsu[i]) {
				goodScore = jumsu[i];
			}
		}
		return goodScore;
	}

	int getBadScore() {
		int badScore = jumsu[0];
		for(int i =0; i <jumsu.length; i++) {
			if(badScore>jumsu[i]) {
				badScore = jumsu[i];	
			}
		}
		return badScore;

	}
}
