package org.epublibre.eplvalidator.main;

import java.awt.EventQueue;

import javax.swing.UIManager;
import javax.swing.UnsupportedLookAndFeelException;
import javax.swing.WindowConstants;

import org.epublibre.eplvalidator.view.Principal;

public class EPLValidator {
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {

			@Override
			public void run() {
				try {
					UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
				} catch (ClassNotFoundException | InstantiationException | IllegalAccessException
						| UnsupportedLookAndFeelException e) {
					e.printStackTrace();
				}
				Principal thisClass = new Principal();
				thisClass.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
				thisClass.setSize(640, 480);
				thisClass.setLocationRelativeTo(null);
				thisClass.setTitle("EPL Validator 0.0.1 - ePubLibre.org");
				thisClass.setVisible(true);
			}
		});
	}

}
