package org.epublibre.eplvalidator.view;

import java.awt.BorderLayout;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;

public class Principal extends JFrame {

	/**
	 * 
	 */
	private static final long serialVersionUID = 5165690525717569551L;
	private JPanel contentPanel;
	private JScrollPane scrollPane;
	private JTextArea textArea;
	private JButton btnValidate;
	
	public Principal(){
		initialize();
	}
	
	private void initialize(){
		this.setContentPane(getContentPanel());
	}
	
	private JPanel getContentPanel(){
		if(contentPanel == null){
			contentPanel = new JPanel();
			contentPanel.setLayout(new BorderLayout());
			contentPanel.add(getScrollPane(), BorderLayout.CENTER);
			contentPanel.add(getBtnValidate(), BorderLayout.SOUTH);
		}
		return contentPanel;
	}
	
	private JScrollPane getScrollPane(){
		if(scrollPane == null){
			scrollPane = new JScrollPane();
			scrollPane.setViewportView(getTextArea());
		}
		return scrollPane;
	}
	
	private JTextArea getTextArea(){
		if(textArea == null){
			textArea = new JTextArea();
		}
		return textArea;
	}
	
	private JButton getBtnValidate(){
		if(btnValidate == null){
			btnValidate = new JButton("Validar");
		}
		return btnValidate;
	}

}
