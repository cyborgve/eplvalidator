package org.epublibre.eplvalidator.core.filechooser;

import java.awt.BorderLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.net.URL;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JPanel;
import javax.swing.JTextField;

public class EPLFileFinder extends JPanel {

	/**
	 * 
	 */
	private static final long serialVersionUID = -183632597166426987L;
	private JButton btnSearch;
	private JTextField txtFileName;

	public EPLFileFinder() {
		this.setLayout(new BorderLayout());
		this.add(getTxtFileName(), BorderLayout.CENTER);
		this.add(getBtnSearch(), BorderLayout.EAST);
	}

	private JButton getBtnSearch() {
		if (btnSearch == null) {
			btnSearch = new JButton();
			URL iconUrl = this.getClass().getResource("/org/epublibre/eplvalidator/images/find16.png");
			ImageIcon icon = new ImageIcon(iconUrl);
			btnSearch.setIcon(icon);
			
			btnSearch.addActionListener(new ActionListener() {

				@Override
				public void actionPerformed(ActionEvent ae) {
					EPLFileChooser fileChooser = new EPLFileChooser();
					int selection = fileChooser.showDialog(fileChooser, "Seleccionar");
					if (selection == JFileChooser.APPROVE_OPTION)
						EPLFileFinder.this.getTxtFileName().setText(fileChooser.getSelectedFile().getAbsolutePath());
					fileChooser = null;
				}
			});
		}
		return btnSearch;
	}

	private JTextField getTxtFileName() {
		if (txtFileName == null) {
			txtFileName = new JTextField();
		}
		return txtFileName;
	}

}
