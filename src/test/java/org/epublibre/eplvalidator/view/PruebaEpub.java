package org.epublibre.eplvalidator.view;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;

import nl.siegmann.epublib.domain.Book;
import nl.siegmann.epublib.epub.EpubReader;

public class PruebaEpub {
	public static void main(String[] args) throws FileNotFoundException, IOException {
		File file = new File("libro.epub");
		Book book = new EpubReader().readEpub(new FileInputStream(file));

		System.out.println(book.getMetadata().getDescriptions());
	}

}
