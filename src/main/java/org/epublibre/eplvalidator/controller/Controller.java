package org.epublibre.eplvalidator.controller;

import java.awt.Toolkit;
import java.awt.datatransfer.Clipboard;
import java.awt.datatransfer.StringSelection;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JFileChooser;
import javax.swing.filechooser.FileNameExtensionFilter;

import org.epublibre.eplvalidator.view.Principal;

public class Controller implements ActionListener {

	private Principal principal;

	public Controller(Principal principal) {
		this.principal = principal;
	}

	public void actionPerformed(ActionEvent e) {

		if (e.getSource().equals(principal.getBtnCopyClipboard())) {
			StringSelection result = new StringSelection(principal.getTextArea().getText());
			Clipboard clipboard = Toolkit.getDefaultToolkit().getSystemClipboard();
			clipboard.setContents(result, null);
		}

		if (e.getSource().equals(principal.getBtnSearch())) {
			JFileChooser fileChooser = new JFileChooser();
			fileChooser.setFileSelectionMode(JFileChooser.FILES_ONLY);
			fileChooser.setFileFilter(new FileNameExtensionFilter("*.epub", "epub"));
			fileChooser.setDialogTitle("Seleccione el epub a validar");
			int selection = fileChooser.showDialog(fileChooser, "Seleccionar");
			if (selection == JFileChooser.APPROVE_OPTION)
				principal.getTxtSearch().setText(fileChooser.getSelectedFile().getAbsolutePath());
			fileChooser = null;
		}

	}

}
