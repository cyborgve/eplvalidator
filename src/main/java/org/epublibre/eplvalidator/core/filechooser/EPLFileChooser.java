package org.epublibre.eplvalidator.core.filechooser;

import javax.swing.JFileChooser;

class EPLFileChooser extends JFileChooser {

	/**
	 * 
	 */
	private static final long serialVersionUID = -3825086425629348314L;
	
	public EPLFileChooser(){
		this.setFileSelectionMode(JFileChooser.FILES_ONLY);
		this.setFileFilter(new EPLFileChooserFilter());
	}

}
