package e_tabpane.model;

import java.sql.Connection;

public class ModelA {

	DBDriver dbd;

	public ModelA() throws Exception{
	
		// dbd = new DBDriver();
		dbd = DBDriver.getInstance();
	}
}

