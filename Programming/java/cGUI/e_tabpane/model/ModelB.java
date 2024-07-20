package e_tabpane.model;

import java.sql.Connection;

public class ModelB {

	DBDriver dbd;

	public ModelB() throws Exception{

		// dbd = new DBDriver();
		dbd = DBDriver.getInstance();
		
	}
}

