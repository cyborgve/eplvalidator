package org.epublibre.eplvalidator.core.filechooser;

import java.io.File;

import javax.swing.filechooser.FileFilter;

class EPLFileChooserFilter extends FileFilter{
	
	

	@Override
	public boolean accept(File f) {
		if(f.isDirectory()) return true;
		if(f.isFile()){
			String fileName = f.getName();
			StringBuilder extention = new StringBuilder();
			for(int i = fileName.length() - 1; '.' != fileName.charAt(i); i--){
				extention.append(fileName.toLowerCase().charAt(i));
			}
			System.out.println(extention.toString());
			if(extention.toString().equalsIgnoreCase("epub"))
				return true;
		}
		return false;
	}

	@Override
	public String getDescription() {
		return "*.epub";
	}

}
