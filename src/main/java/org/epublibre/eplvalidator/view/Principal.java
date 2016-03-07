package org.epublibre.eplvalidator.view;

import java.awt.BorderLayout;
import java.awt.FlowLayout;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.border.CompoundBorder;
import javax.swing.border.BevelBorder;
import org.epublibre.eplvalidator.core.filechooser.EPLFileFinder;

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
	private EPLFileFinder btnSearch;
	private JButton btnCopyClipboard;
	
	public Principal(){
		initialize();
	}
	
	private void initialize(){
		this.setContentPane(getContentPanel());
	}
	
	private JPanel getContentPanel(){
		if(contentPanel == null){
			contentPanel = new JPanel();
			contentPanel.setBorder(new CompoundBorder(new BevelBorder(BevelBorder.RAISED), new BevelBorder(BevelBorder.LOWERED)));
			contentPanel.setLayout(new BorderLayout());
			contentPanel.add(getNorthPanel(), BorderLayout.NORTH);
			contentPanel.add(getScrollPane(), BorderLayout.CENTER);
			contentPanel.add(getSouthPanel(), BorderLayout.SOUTH);
		}
		return contentPanel;
	}
	
	private JPanel getNorthPanel(){
		if(northPanel == null){
			northPanel = new JPanel();
			northPanel.setBorder(new BevelBorder(BevelBorder.RAISED));
			northPanel.setLayout(new BorderLayout());
			northPanel.add(getBtnSearch(), BorderLayout.CENTER);
		}
		return northPanel;
	}
	
	private JPanel getSouthPanel(){
		if(southPanel == null){
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
	
	private JScrollPane getScrollPane(){
		if(scrollPane == null){
			scrollPane = new JScrollPane();
			scrollPane.setBorder(new BevelBorder(BevelBorder.RAISED));
			scrollPane.setViewportView(getTextArea());
		}
		return scrollPane;
	}
	
	public JTextArea getTextArea(){
		if(textArea == null){
			textArea = new JTextArea();
			textArea.setEditable(false);
		}
		return textArea;
	}
	
	public JButton getBtnValidate(){
		if(btnValidate == null){
			btnValidate = new JButton("Validar");
		}
		return btnValidate;
	}
	
	public EPLFileFinder getBtnSearch(){
		if(btnSearch == null){
			btnSearch = new EPLFileFinder();
		}
		return btnSearch;
	}

	private JButton getBtnCopyClipboard() {
		if (btnCopyClipboard == null) {
			btnCopyClipboard = new JButton("Copiar a portapapeles");
		}
		return btnCopyClipboard;
	}
}
