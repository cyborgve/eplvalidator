package org.epublibre.eplvalidator.view;

import java.util.Arrays;
import java.util.function.Function;

import org.epublibre.eplvalidator.model.Constants;
import org.epublibre.eplvalidator.model.ErrorType;

public class PruebaConstantes {
	public static void main(String[] args) {
		Arrays.asList(Constants.LISTA_ERRORES).stream().map((Function<String, ErrorType>) s -> {
			ErrorType errorType = new ErrorType(s.split(":")[0], s.split(":")[1], s.split(":")[2]);
			return errorType;
		}).forEach(System.out::println);
	}

}
