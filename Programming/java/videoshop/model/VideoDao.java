package videoshop.model;

import java.util.ArrayList;

import javax.swing.JOptionPane;

import videoshop.model.vo.Video;

public interface VideoDao {
	public void insertVideo(Video vo, int count) throws Exception;
	
	public void modifyVideo(Video vo)throws Exception;
	
	public void deleteVideo(Video vo)throws Exception;
	
	public ArrayList selectVideos(int idx, String keyword) throws Exception;
	
	public Video searchByPk(int videoNum) throws Exception;
}
