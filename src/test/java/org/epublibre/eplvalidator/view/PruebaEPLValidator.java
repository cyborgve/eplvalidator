package org.epublibre.eplvalidator.view;

import java.awt.EventQueue;

import javax.swing.WindowConstants;

public class PruebaEPLValidator {
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {

			@Override
			public void run() {
				Principal thisClass = new Principal();
				thisClass.setTitle("EPLValidator");
				thisClass.setSize(600, 900);
				thisClass.setLocationRelativeTo(null);
				thisClass.setVisible(true);
				thisClass.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
			}
		});
	}

}
