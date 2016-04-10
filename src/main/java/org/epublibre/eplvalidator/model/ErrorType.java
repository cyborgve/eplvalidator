package org.epublibre.eplvalidator.model;

import java.io.Serializable;
import java.util.Arrays;
import java.util.List;
import java.util.function.Function;
import java.util.stream.Collectors;

public class ErrorType implements Serializable, Constants {

	/**
	 * 
	 */
	private static final long serialVersionUID = -7065490164514621848L;
	private String code;
	private String name;
	private String description;

	public ErrorType(String code, String name, String description) {
		this.code = code;
		this.name = name;
		this.description = description;
	}

	public ErrorType() {
		this(null, null, null);
	}

	public String getCode() {
		return code;
	}

	public void setCode(String code) {
		this.code = code;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getDescription() {
		return description;
	}

	public void setDescription(String description) {
		this.description = description;
	}

	public String toString() {
		return code + "," + name + "," + description;
	}

	public List<ErrorType> Errors() {
		List<ErrorType> result = Arrays.asList(Constants.LISTA_ERRORES).stream()
				.map((Function<String, ErrorType>) s -> {
					ErrorType errorType = new ErrorType();
					errorType.setCode(s.split(":")[0]);
					errorType.setName(s.split(":")[1]);
					errorType.setDescription(s.split(":")[2]);
					return errorType;
				}).collect(Collectors.toList());
		return result;
	}
}
