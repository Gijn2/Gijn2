package videoshop.model;

import java.util.ArrayList;

public interface RentDao {

	public void RentVideo(String tel, int vNum) throws Exception;

	public void ReturnVideo(String tel,int vNum)throws Exception;
	
	public ArrayList selectNoReturn()throws Exception;


}
