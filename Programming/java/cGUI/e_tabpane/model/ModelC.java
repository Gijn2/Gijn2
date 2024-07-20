package e_tabpane.model;

import java.sql.Connection;

public class ModelC {
	
	DBDriver dbd;
	
	public ModelC() throws Exception{


		// dbd = new DBDriver();
		dbd = DBDriver.getInstance();
	
	}
}

