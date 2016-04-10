package org.epublibre.eplvalidator.model;

public interface Constants {

	public static final String VERSION_BASE = "1.2";
	public static final boolean CORREGIR_AUTOMATICO = true;
	public static final String[] LISTA_ERRORES = {
			// OPF (METADATOS)
			"1:ERROR 01:Archivo content.opf con errores ('Your OPF file was broken'). Es necesario recrear el aporte",
			"2:ERROR 02:Metadatos faltantes: %s", "3:ERROR 03:Metadatos vac�os: %s",
			"4:ERROR 04:Metadatos repetidos: %s",
			"5:ERROR 05:Descripci�n en metadatos (%s) coincide con ePub base. Debe cambiarse en cada aporte",
			"6:ERROR 06:Idioma en metadatos (%s) no es uno de los aceptados actualmente",
			"7:ERROR 07:Editorial (%s) incorrecta. Debe ser ePubLibre (respetando las may�sculas)",
			// TOC
			"8:ERROR 08:T�tulo interno difiere entre content.opf y toc. Debe regenerarse esta antes de guardar el aporte",
			// BOOK-ID
			"9:ERROR 09:BookId (%s) coincide con ePub base. Debe cambiarse en cada aporte", "10:ERROR 10:BookId vac�o",
			"11:ERROR 11:BookId debe ser de tipo UUID", "12:ERROR 12:Formato incorrecto de BookId (%s)",
			"13:ERROR 13:BookId difiere entre content.opf y toc. Debe regenerarse esta antes de guardar el aporte",
			// CSS
			"14:ERROR 14:Archivo 'style.css' renombrado o no encontrado",
			"15:ERROR 15:Encontrado m�s de un archivo CSS",
			"16:ERROR 16:Primera secci�n de la CSS ('ESTILOS GLOBALES Y DE SECCIONES FIJAS') no es la aprobada del ePub base",
			// G�NEROS
			"17:ERROR 17:G�nero faltante o err�neo", "18:ERROR 18:Subg�nero faltante o err�neo",
			"19:ERROR 19:G�neros o subg�neros repetidos: %s", "20:ERROR 20:Uso de tipo innecesario (%s)",
			"21:ERROR 21:Uso de g�nero o subg�nero no aprobado (%s)", "22:ERROR 22:Uso de g�neros de %s en libro de %s",
			"23:ERROR 23:Uso de subg�neros de %s en libro de %s",
			"24:ERROR 24:Uso simult�neo de g�neros de Ficci�n y No ficci�n",
			// T�TULO
			"25:ERROR 25:T�tulo en %s (%s) coincide con ePub base. Debe cambiarse en cada aporte",
			"26:ERROR 26:T�tulo no encontrado en %s", "27:ERROR 27:T�tulo %s (%s) difiere de %s (%s)",
			// AUTOR / TRADUCTOR / COLABORADORES
			"28:ERROR 28:%s en %s (%s) coincide con ePub base. Debe cambiarse en cada aporte",
			"29:ERROR 29:Autor no encontrado en %s", "30:ERROR 30:Autor en %s (%s) difiere de %s (%s)",
			"31:ERROR 31:Traductor encontrado en %s (%s) pero faltante en %s",
			"32:ERROR 32:Traductor en metadatos (%s) difiere de p�gina info (%s)",
			"33:ERROR 33:File-as [Ordenar como] de %s (%s) coincide con ePub base. Debe cambiarse en cada aporte",
			"34:ERROR 34:File-as [Ordenar como] faltante para %s (%s)",
			"35:ERROR 35:File-as [Ordenar como] de %s (%s) parece incorrecto al compararlo con metadatos (%s)",
			"36:ERROR 36:File-as [Ordenar como] de %s incorrecto. Falta coma de separaci�n",
			"37:ERROR 37:La notaci�n aprobada para varios %ses es 'AA. VV.'. Debe corregirse en %s",
			"38:ERROR 38:%s en metadatos (%s) a�adido con rol de %s",
			// TAMA�OS E IM�GENES
			"39:ERROR 39:Tama�o de archivo interno (%s) excede l�mite de 300 Kb",
			"40:ERROR 40:Tama�o de imagen de cubierta %s incorrecto. Debe ser 600 x 900 px",
			"41:ERROR 41:Error al procesar imagen (%s). Debe revisarse", "42:ERROR 42:Imagen faltante (%s)",
			"43:ERROR 43:Imagen (%s) parece coincidir con ePub base. Debe cambiarse en cada aporte",
			"44:ERROR 44:Imagen (%s) no es la aprobada del ePub base",
			"45:ERROR 45:Ancho de imagen %s (%s px) sobrepasa l�mite permitido (600)",
			"46:ERROR 46:Alto de imagen %s (%s px) sobrepasa l�mite recomendado (400)",
			"47:ERROR 47:Probable imagen de autor (%s) encontrada sin %sdicha p�gina",
			"48:ERROR 48:Imagen guardada como jpeg progresivo (%s). Debe ser s�lo optimizado (de preferencia) o l�nea de base",
			// SAGA/SERIE
			"49:ERROR 49:Entrada 'calibre:series%s' vac�a en content.opf",
			"50:ERROR 50:Saga/serie encontrada en %s (%s) pero faltante en %s",
			"51:ERROR 51:Saga/serie en metadatos (%s) difiere de p�gina t�tulo (%s)",
			"52:ERROR 52:N�mero de volumen encontrado en %s (%s) pero faltante en %s",
			"53:ERROR 53:N�mero de volumen en metadatos (%s) difiere de p�gina t�tulo (%s)",
			// N�MERO DE REVISI�N
			"54:ERROR 54:N�mero de revisi�n no encontrado en %s",
			"55:ERROR 55:N�mero de revisi�n en p�gina t�tulo (%s) difiere de nombre de archivo (%s)",
			"56:ERROR 56:N�mero de revisi�n con dos decimales en %s. Debe aumentarse d�gito principal (excepto en candidaturas)",
			// FECHAS
			"57:ERROR 57:Fecha de publicaci�n original en metadatos (%s) coincide con ePub base. Debe cambiarse en cada aporte",
			"58:ERROR 58:Fecha de publicaci�n original en %s (%s) es posterior al a�o actual",
			"59:ERROR 59:Fecha de publicaci�n original faltante en %s",
			"60:ERROR 60:Fecha de publicaci�n original en metadatos (%s) difiere de p�gina info (%s)",
			"61:ERROR 61:Fecha de modificaci�n en %s (%s) coincide con ePub base. Debe cambiarse en cada aporte",
			"62:ERROR 62:Fecha de modificaci�n no encontrada en %s",
			"63:ERROR 63:Fecha de modificaci�n en metadatos (%s) difiere de p�gina t�tulo (%s)",
			// ALIAS DE EDITOR
			"64:ERROR 64:Alias de editor no encontrado en %s",
			"65:ERROR 65:Alias de editor en p�gina t�tulo (%s) difiere de p�gina info (%s)",
			// NOMBRES DE ARCHIVO
			"66:ERROR 66:Caracteres no permitidos en nombre de archivo%s",
			"67:ERROR 67:Identificador �nico [ePL-ID] faltante en nombre de archivo",
			"68:ERROR 68:Idioma en nombre de archivo [%s] no es uno de los aceptados actualmente",
			"69:ERROR 69:Idioma [ES] innecesario en nombre de archivo",
			"70:ERROR 70:Idioma encontrado en metadatos (%s) pero faltante en nombre de archivo",
			"71:ERROR 71:Idioma en metadatos (%s) difiere de nombre de archivo [%s]",
			"72:ERROR 72:Formato de nombre de archivo incorrecto. Es recomendable generarlo desde la ficha web",
			// FUENTES
			"73:ERROR 73:Aporte con fuentes incrustadas sin archivo 'com.apple.ibooks.display.xml'",
			"74:ERROR 74:Archivo 'com.apple.ibooks.display.xml' es obligatorio a partir del ePub base r1.1",
			// ORDEN DE SECCIONES
			"75:ERROR 75:Orden de las cuatro primeras secciones fijas (%s) parece incorrecto",
			"76:ERROR 76:Orden de las secciones autor (%s) y notas (%s) parece incorrecto",
			// CONCEPTOS
			"77:ERROR 77:Concepto err�neo (Imagen de portada) para %s",
			"78:ERROR 78:Concepto faltante (Imagen de portada) para %s",
			"79:ERROR 79:Concepto no permitido (%s) para p�gina %s",
			"80:ERROR 80:Concepto faltante (Portada) para p�gina %s",
			// C�DIGO Y ARCHIVOS BASURA
			"81:ERROR 81:Texto sin modificar en %s (%s)",
			"82:ERROR 82:Signo de puntuaci�n innecesario en %s final de l�nea %s (%s)",
			"83:ERROR 83:Jerarqu�a de partes o cap�tulos debe comenzar en <h1>",
			"84:ERROR 84:Jerarqu�a de secci�n fija debe ser <h1> (%s)",
			"85:ERROR 85:C�digo modificado en secci�n fija (%s). Comparar con ePub base",
			"86:ERROR 86:C�digo del ePub base anterior en %s%s (%s)",
			"87:ERROR 87:C�digo err�neo o no permitido en %s%s (%s)",
			"88:ERROR 88:C�digo de notas no est�ndar en %s l�nea %s (%s)",
			"89:ERROR 89:C�digo no permitido en <head> de %s a partir de l�nea %s (%s)",
			"90:ERROR 90:Car�cter err�neo en lugar de raya en %s (dec:%s). Reemplazarlo con Informes de Sigil",
			"91:ERROR 91:Car�cter err�neo o combinado en %s (dec:%s). Reemplazarlo con Informes de Sigil",
			"92:ERROR 92:Error al procesar archivo %s. Debe revisarse",
			"93:ERROR 93:Entrada no permitida en content.opf (%s)",
			"94:ERROR 94:Entrada incompleta en content.opf (%s)", "95:ERROR 95:Entrada innecesaria en content.opf (%s)",
			"96:ERROR 96:Archivo referido en content.opf pero no encontrado (%s) (posible error en caracteres)",
			"97:ERROR 97:Archivo encontrado pero no referido en content.opf (%s)",
			"98:ERROR 98:Archivo innecesario (%s)", };

	public static final String[] LISTA_AVISOS = { "1 : - C�digo innecesario en %s l�nea %s (%s)",
			"2 : - Espacios innecesarios en nombre de archivo", "3 : - Doble extensi�n .epub en nombre de archivo",
			"4 : - Alias de editor no personalizado en nombre de archivo (%s)",
			"5 : - S�lo debe usarse la palabra '%s' si es parte del nombre original (encontrada en %s)",
			"6 : - El aporte usa una versi�n anterior del ePub base. Se recomienda actualizar a la %s",
			"7 : - Cambiado al menos un nombre de im�genes fijas %s", };

	public static final String[] UUID_EPUBBASE = { "urn:uuid:125147a0-df57-4660-b1bc-cd5ad2eb2617",
			"urn:uuid:00000000-0000-0000-0000-000000000000" };

	public static final String[] TIPO = { "Ficci�n", "No ficci�n", "ficci�n", "ficcion", "no ficci�n", "no ficcion",
			"no-ficci�n", "no-ficcion", "noficci�n", "noficcion" };

	public static final String[] GENEROS_FICCION = { "Guion", "Novela", "Poes�a", "Relato", "Teatro" };

	public static final String[] GENEROS_NO_FICCION = { "Cr�nica", "Divulgaci�n", "Ensayo", "Referencia" };

	public static final String[] SUBGENEROS_FICCION = { "Aventuras", "B�lico", "Ciencia ficci�n", "Did�ctico", "Drama",
			"Er�tico", "Fant�stico", "Filos�fico", "Hist�rico", "Humor", "Infantil", "Interactivo", "Intriga",
			"Juvenil", "Policial", "Psicol�gico", "Realista", "Rom�ntico", "S�tira", "Terror", "Otros" };

	public static final String[] SUBGENEROS_NO_FICCION = { "Arte", "Autoayuda", "Ciencias exactas",
			"Ciencias naturales", "Ciencias sociales", "Comunicaci�n", "Cr�tica y teor�a literaria",
			"Deportes y juegos", "Diccionarios y enciclopedias", "Espiritualidad", "Filosof�a", "Historia", "Hogar",
			"Humor", "Idiomas", "Manuales y cursos", "Memorias", "Padres e hijos", "Psicolog�a", "Salud y bienestar",
			"Sexualidad", "Tecnolog�a", "Viajes", "Otros" };

	public static final String[] IDIOMAS = { "es:Espa�ol", "ca:Catal�n", "de:Alem�n", "en:Ingl�s", "eo:Esperanto",
			"eu:Euskera/Vasco", "fr:Franc�s", "gl:Gallego", "it:Italiano", "pt:Portugu�s", "sv:Sueco", "zh:Chino" };

	public static final String AUT = "autor";
	public static final String MET = "metadata";
	public static final String MATAD = "metadatos";
	public static final String PSINO = "p�gina sinopsis";
	public static final String PTITU = "p�gina t�tulo";
	public static final String PINFO = "p�gina info";
	public static final String NARCH = "nombre de archivo";
	public static final String PERROR = " (posible error de c�digo)";
	public static final String CAUTO = "  --- corregido autom�ticamente";
	public static final String IMPOS = "\nIMPOSIBLE CONTINUAR CON ESTE APORTE";
	public static final String GRAVE = "\nES OBLIGATORIO RECREAR ESTE APORTE";

}
