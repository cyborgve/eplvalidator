package org.epublibre.eplvalidator.view;

import java.awt.BorderLayout;
import java.awt.FlowLayout;
import java.net.URL;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.border.BevelBorder;
import javax.swing.border.CompoundBorder;

import org.epublibre.eplvalidator.controller.Controller;

public class Principal extends JFrame {

	/**
	 * 
	 */
	private static final long serialVersionUID = 5165690525717569551L;
	private JPanel contentPanel;
	private JPanel southPanel;
	private JPanel northPanel;
	private JScrollPane scrollPane;
	private JTextArea textArea;
	private JButton btnValidate;
	private JTextField txtSearch;
	private JButton btnSearch;
	private JButton btnCopyClipboard;
	private Controller controller;

	public Principal() {
		controller = new Controller(this);
		initialize();
	}

	private void initialize() {
		this.setContentPane(getContentPanel());
	}

	private JPanel getContentPanel() {
		if (contentPanel == null) {
			contentPanel = new JPanel();
			contentPanel.setBorder(
					new CompoundBorder(new BevelBorder(BevelBorder.RAISED), new BevelBorder(BevelBorder.LOWERED)));
			contentPanel.setLayout(new BorderLayout());
			contentPanel.add(getNorthPanel(), BorderLayout.NORTH);
			contentPanel.add(getScrollPane(), BorderLayout.CENTER);
			contentPanel.add(getSouthPanel(), BorderLayout.SOUTH);
		}
		return contentPanel;
	}

	private JPanel getNorthPanel() {
		if (northPanel == null) {
			northPanel = new JPanel(new BorderLayout());
			northPanel.setBorder(new BevelBorder(BevelBorder.RAISED));
			northPanel.add(getTxtSearch(), BorderLayout.CENTER);
			northPanel.add(getBtnSearch(), BorderLayout.EAST);
		}
		return northPanel;
	}

	private JPanel getSouthPanel() {
		if (southPanel == null) {
			southPanel = new JPanel();
			southPanel.setBorder(new BevelBorder(BevelBorder.RAISED));
			FlowLayout layout = new FlowLayout();
			layout.setAlignment(FlowLayout.RIGHT);
			southPanel.setLayout(layout);
			southPanel.add(getBtnCopyClipboard());
			southPanel.add(getBtnValidate());
		}
		return southPanel;
	}

	private JScrollPane getScrollPane() {
		if (scrollPane == null) {
			scrollPane = new JScrollPane();
			scrollPane.setBorder(new BevelBorder(BevelBorder.RAISED));
			scrollPane.setViewportView(getTextArea());
		}
		return scrollPane;
	}

	public JTextArea getTextArea() {
		if (textArea == null) {
			textArea = new JTextArea();
			textArea.setEditable(false);
		}
		return textArea;
	}

	public JTextField getTxtSearch() {
		if (txtSearch == null) {
			txtSearch = new JTextField();
		}
		return txtSearch;
	}

	public JButton getBtnSearch() {
		if (btnSearch == null) {
			URL iconUrl = this.getClass().getResource("/org/epublibre/eplvalidator/images/find16.png");
			ImageIcon icon = new ImageIcon(iconUrl);
			btnSearch = new JButton(icon);
			btnSearch.addActionListener(controller);
		}
		return btnSearch;
	}

	public JButton getBtnValidate() {
		if (btnValidate == null) {
			btnValidate = new JButton("Validar");
		}
		return btnValidate;
	}

	public JButton getBtnCopyClipboard() {
		if (btnCopyClipboard == null) {
			btnCopyClipboard = new JButton("Copiar a portapapeles");
		}
		return btnCopyClipboard;
	}
}
