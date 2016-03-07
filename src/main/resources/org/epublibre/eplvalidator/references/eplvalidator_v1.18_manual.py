#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
ePLValidator (Python 2.6/3.x)

@autor: betatron
Creado el 16 mayo 2013

@actualizador: jugaor
Modificado noviembre 2015

Ver changelog para listado de pruebas implementadas y pendientes
'''


from __future__ import unicode_literals, division, absolute_import, print_function
import fnmatch
import os
import re
import shutil
import stat
import string
import struct
import sys
import uuid
import zipfile
from datetime import datetime, date
from xml.dom.minidom import parse


# comprueba versión de Python
if sys.version_info[0] < 3:
	from io import open
	from urllib import unquote
	reload(sys)
	sys.setdefaultencoding('utf-8')
	input = raw_input
	range = xrange
	texto = unicode
	try:
		from Tkinter import Tk
		import tkFileDialog
	except ImportError:
		pass	# sigue ejecutándolo sin tkinter
	def fdialog():
		return tkFileDialog.Open(multiple=True).show()
else:
	from urllib.parse import unquote
	texto = str
	try:
		from tkinter import Tk, filedialog
	except ImportError:
		pass
	def fdialog():
		return filedialog.askopenfilename(multiple=True)


# constantes globales
vversion = '1.18'
version_base = '1.2'
corregir_errores = False


# errores
listaerrores = {
# OPF (METADATOS)
	 1 : "ERROR 01: Archivo content.opf con errores ('Your OPF file was broken'). Es necesario recrear el aporte",
	 2 : "ERROR 02: Metadatos faltantes: %s",
	 3 : "ERROR 03: Metadatos vacíos: %s",
	 4 : "ERROR 04: Metadatos repetidos: %s",
	 5 : "ERROR 05: Descripción en metadatos (%s) coincide con ePub base. Debe cambiarse en cada aporte",
	 6 : "ERROR 06: Idioma en metadatos (%s) no es uno de los aceptados actualmente",
	 7 : "ERROR 07: Editorial (%s) incorrecta. Debe ser ePubLibre (respetando las mayúsculas)",
# TOC
	 8 : "ERROR 08: Título interno difiere entre content.opf y toc. Debe regenerarse esta antes de guardar el aporte",
# BOOK-ID
	 9 : "ERROR 09: BookId (%s) coincide con ePub base. Debe cambiarse en cada aporte",
	10 : "ERROR 10: BookId vacío",
	11 : "ERROR 11: BookId debe ser de tipo UUID",
	12 : "ERROR 12: Formato incorrecto de BookId (%s)",
	13 : "ERROR 13: BookId difiere entre content.opf y toc. Debe regenerarse esta antes de guardar el aporte",
# CSS
	14 : "ERROR 14: Archivo 'style.css' renombrado o no encontrado",
	15 : "ERROR 15: Encontrado más de un archivo CSS",
	16 : "ERROR 16: Primera sección de la CSS ('ESTILOS GLOBALES Y DE SECCIONES FIJAS') no es la aprobada del ePub base",
# GÉNEROS
	17 : "ERROR 17: Género faltante o erróneo",
	18 : "ERROR 18: Subgénero faltante o erróneo",
	19 : "ERROR 19: Géneros o subgéneros repetidos: %s",
	20 : "ERROR 20: Uso de tipo innecesario (%s)",
	21 : "ERROR 21: Uso de género o subgénero no aprobado (%s)",
	22 : "ERROR 22: Uso de géneros de %s en libro de %s",
	23 : "ERROR 23: Uso de subgéneros de %s en libro de %s",
	24 : "ERROR 24: Uso simultáneo de géneros de Ficción y No ficción",
# TÍTULO
	25 : "ERROR 25: Título en %s (%s) coincide con ePub base. Debe cambiarse en cada aporte",
	26 : "ERROR 26: Título no encontrado en %s",
	27 : "ERROR 27: Título %s (%s) difiere de %s (%s)",
# AUTOR / TRADUCTOR / COLABORADORES
	28 : "ERROR 28: %s en %s (%s) coincide con ePub base. Debe cambiarse en cada aporte",
	29 : "ERROR 29: Autor no encontrado en %s",
	30 : "ERROR 30: Autor en %s (%s) difiere de %s (%s)",
	31 : "ERROR 31: Traductor encontrado en %s (%s) pero faltante en %s",
	32 : "ERROR 32: Traductor en metadatos (%s) difiere de página info (%s)",
	33 : "ERROR 33: File-as [Ordenar como] de %s (%s) coincide con ePub base. Debe cambiarse en cada aporte",
	34 : "ERROR 34: File-as [Ordenar como] faltante para %s (%s)",
	35 : "ERROR 35: File-as [Ordenar como] de %s (%s) parece incorrecto al compararlo con metadatos (%s)",
	36 : "ERROR 36: File-as [Ordenar como] de %s incorrecto. Falta coma de separación",
	37 : "ERROR 37: La notación aprobada para varios %ses es 'AA. VV.'. Debe corregirse en %s",
	38 : "ERROR 38: %s en metadatos (%s) añadido con rol de %s",
# TAMAÑOS E IMÁGENES
	39 : "ERROR 39: Tamaño de archivo interno (%s) excede límite de 300 Kb",
	40 : "ERROR 40: Tamaño de imagen de cubierta %s incorrecto. Debe ser 600 x 900 px",
	41 : "ERROR 41: Error al procesar imagen (%s). Debe revisarse",
	42 : "ERROR 42: Imagen faltante (%s)",
	43 : "ERROR 43: Imagen (%s) parece coincidir con ePub base. Debe cambiarse en cada aporte",
	44 : "ERROR 44: Imagen (%s) no es la aprobada del ePub base",
	45 : "ERROR 45: Ancho de imagen %s (%s px) sobrepasa límite permitido (600)",
	46 : "ERROR 46: Alto de imagen %s (%s px) sobrepasa límite recomendado (400)",
	47 : "ERROR 47: Probable imagen de autor (%s) encontrada sin %sdicha página",
	48 : "ERROR 48: Imagen guardada como jpeg progresivo (%s). Debe ser sólo optimizado (de preferencia) o línea de base",
# SAGA/SERIE
	49 : "ERROR 49: Entrada 'calibre:series%s' vacía en content.opf",
	50 : "ERROR 50: Saga/serie encontrada en %s (%s) pero faltante en %s",
	51 : "ERROR 51: Saga/serie en metadatos (%s) difiere de página título (%s)",
	52 : "ERROR 52: Número de volumen encontrado en %s (%s) pero faltante en %s",
	53 : "ERROR 53: Número de volumen en metadatos (%s) difiere de página título (%s)",
# NÚMERO DE REVISIÓN
	54 : "ERROR 54: Número de revisión no encontrado en %s",
	55 : "ERROR 55: Número de revisión en página título (%s) difiere de nombre de archivo (%s)",
	56 : "ERROR 56: Número de revisión con dos decimales en %s. Debe aumentarse dígito principal (excepto en candidaturas)",
# FECHAS
	57 : "ERROR 57: Fecha de publicación original en metadatos (%s) coincide con ePub base. Debe cambiarse en cada aporte",
	58 : "ERROR 58: Fecha de publicación original en %s (%s) es posterior al año actual",
	59 : "ERROR 59: Fecha de publicación original faltante en %s",
	60 : "ERROR 60: Fecha de publicación original en metadatos (%s) difiere de página info (%s)",
	61 : "ERROR 61: Fecha de modificación en %s (%s) coincide con ePub base. Debe cambiarse en cada aporte",
	62 : "ERROR 62: Fecha de modificación no encontrada en %s",
	63 : "ERROR 63: Fecha de modificación en metadatos (%s) difiere de página título (%s)",
# ALIAS DE EDITOR
	64 : "ERROR 64: Alias de editor no encontrado en %s",
	65 : "ERROR 65: Alias de editor en página título (%s) difiere de página info (%s)",
# NOMBRES DE ARCHIVO
	66 : "ERROR 66: Caracteres no permitidos en nombre de archivo%s",
	67 : "ERROR 67: Identificador único [ePL-ID] faltante en nombre de archivo",
	68 : "ERROR 68: Idioma en nombre de archivo [%s] no es uno de los aceptados actualmente",
	69 : "ERROR 69: Idioma [ES] innecesario en nombre de archivo",
	70 : "ERROR 70: Idioma encontrado en metadatos (%s) pero faltante en nombre de archivo",
	71 : "ERROR 71: Idioma en metadatos (%s) difiere de nombre de archivo [%s]",
	72 : "ERROR 72: Formato de nombre de archivo incorrecto. Es recomendable generarlo desde la ficha web",
# FUENTES
	73 : "ERROR 73: Aporte con fuentes incrustadas sin archivo 'com.apple.ibooks.display.xml'",
	74 : "ERROR 74: Archivo 'com.apple.ibooks.display.xml' es obligatorio a partir del ePub base r1.1",
# ORDEN DE SECCIONES
	75 : "ERROR 75: Orden de las cuatro primeras secciones fijas (%s) parece incorrecto",
	76 : "ERROR 76: Orden de las secciones autor (%s) y notas (%s) parece incorrecto",
# CONCEPTOS
	77 : "ERROR 77: Concepto erróneo (Imagen de portada) para %s",
	78 : "ERROR 78: Concepto faltante (Imagen de portada) para %s",
	79 : "ERROR 79: Concepto no permitido (%s) para página %s",
	80 : "ERROR 80: Concepto faltante (Portada) para página %s",
# CÓDIGO Y ARCHIVOS BASURA
	81 : "ERROR 81: Texto sin modificar en %s (%s)",
	82 : "ERROR 82: Signo de puntuación innecesario en %s final de línea %s (%s)",
	83 : "ERROR 83: Jerarquía de partes o capítulos debe comenzar en <h1>",
	84 : "ERROR 84: Jerarquía de sección fija debe ser <h1> (%s)",
	85 : "ERROR 85: Código modificado en sección fija (%s). Comparar con ePub base",
	86 : "ERROR 86: Código del ePub base anterior en %s%s (%s)",
	87 : "ERROR 87: Código erróneo o no permitido en %s%s (%s)",
	88 : "ERROR 88: Código de notas no estándar en %s línea %s (%s)",
	89 : "ERROR 89: Código no permitido en <head> de %s a partir de línea %s (%s)",
	90 : "ERROR 90: Carácter erróneo en lugar de raya en %s (dec:%s). Reemplazarlo con Informes de Sigil",
	91 : "ERROR 91: Carácter erróneo o combinado en %s (dec:%s). Reemplazarlo con Informes de Sigil",
	92 : "ERROR 92: Error al procesar archivo %s. Debe revisarse",
	93 : "ERROR 93: Entrada no permitida en content.opf (%s)",
	94 : "ERROR 94: Entrada incompleta en content.opf (%s)",
	95 : "ERROR 95: Entrada innecesaria en content.opf (%s)",
	96 : "ERROR 96: Archivo referido en content.opf pero no encontrado (%s) (posible error en caracteres)",
	97 : "ERROR 97: Archivo encontrado pero no referido en content.opf (%s)",
	98 : "ERROR 98: Archivo innecesario (%s)",
	}


listaavisos = {
	 1 : "- Código innecesario en %s línea %s (%s)",
	 2 : "- Espacios innecesarios en nombre de archivo",
	 3 : "- Doble extensión .epub en nombre de archivo",
	 4 : "- Alias de editor no personalizado en nombre de archivo (%s)",
	 5 : "- Sólo debe usarse la palabra '%s' si es parte del nombre original (encontrada en %s)",
	 6 : "- El aporte usa una versión anterior del ePub base. Se recomienda actualizar a la %s",
	 #7 : "- Cambiado al menos un nombre de imágenes fijas %s",
	 }


uuid_epubbase = ['urn:uuid:125147a0-df57-4660-b1bc-cd5ad2eb2617', 'urn:uuid:00000000-0000-0000-0000-000000000000']

# géneros y subgéneros:
tipo = ['Ficción', 'No ficción', 'ficción', 'ficcion', 'no ficción', 'no ficcion', 'no-ficción', 'no-ficcion', 'noficción', 'noficcion']

generos_ficcion = ['Guion', 'Novela', 'Poesía', 'Relato', 'Teatro']

generos_no_ficcion = ['Crónica', 'Divulgación', 'Ensayo', 'Referencia']

subgeneros_ficcion = ['Aventuras', 'Bélico', 'Ciencia ficción', 'Didáctico',
					 'Drama', 'Erótico', 'Fantástico', 'Filosófico',
					 'Histórico', 'Humor', 'Infantil', 'Interactivo', 'Intriga',
					 'Juvenil', 'Policial', 'Psicológico', 'Realista',
					 'Romántico', 'Sátira', 'Terror', 'Otros']

subgeneros_no_ficcion = ['Arte', 'Autoayuda', 'Ciencias exactas', 'Ciencias naturales',
						 'Ciencias sociales', 'Comunicación', 'Crítica y teoría literaria', 'Deportes y juegos',
						 'Diccionarios y enciclopedias', 'Espiritualidad', 'Filosofía', 'Historia',
						 'Hogar', 'Humor', 'Idiomas', 'Manuales y cursos', 'Memorias',
						 'Padres e hijos', 'Psicología', 'Salud y bienestar', 'Sexualidad',
						 'Tecnología', 'Viajes', 'Otros' ]

generos = generos_ficcion + generos_no_ficcion	# todos los géneros

generos_y_subgeneros_ficcion = generos_ficcion + subgeneros_ficcion	# todos los géneros y subgéneros de Ficción

generos_y_subgeneros_no_ficcion = generos_no_ficcion + subgeneros_no_ficcion	# todos los géneros y subgéneros de No ficción

# todos los géneros y subgéneros EXCLUSIVOS de Ficción
excl_generos_y_subgeneros_ficcion = [e for e in generos_y_subgeneros_ficcion if e not in generos_y_subgeneros_no_ficcion]

# todos los géneros y subgéneros EXCLUSIVOS de No Ficción
excl_generos_y_subgeneros_no_ficcion = [e for e in generos_y_subgeneros_no_ficcion if e not in generos_y_subgeneros_ficcion]

subgeneros = list(set(subgeneros_ficcion + subgeneros_no_ficcion))	# subgéneros sin repetición

# idiomas aceptados a la fecha
idiomas = {'es':'Español', 'ca':'Catalán', 'de':'Alemán', 'en':'Inglés', 'eo':'Esperanto', 'eu':'Euskera/Vasco', 'fr':'Francés', 'gl':'Gallego', 'it':'Italiano', 'pt':'Portugués', 'sv':'Sueco', 'zh':'Chino'}

# cadenas multilingües
aa_vv_M = re.compile(r'(?i)\b(a+\b[.,\s]*v+\b[.,]*|v+\b[.,\s]*a+\b[.,]*|autores\s+varios|varios\s+autores)')
conec_M = re.compile(r'(\s+&amp;|\s+and|\s+avec|\s+con|\s+med|\s+och|\s+i|\s+y|\s+eta|\s+et?|\s+[—–-]+|,)\s')
dedic_h = re.compile(r'(?i)(x?\d+-|)dedi[ck]a(ce|t[io]|zioa)')
autor_h = re.compile(r'(?i)(x?\d+-|)(aut(h?o|eu)r|(schriftstel+|verfas+)er|idazlea|forfat+are)')
cubrt_M = '(Cubi?erta|Coberta|Buchtitel|Cover|Kovrilo|Azala|Couverture|Copertina|Capa|Omslag)'
autor_M = '(?:Aut(?:h?o|eu)r|Schriftsteller|Verfasser|A\u016Dtoro|Idazlea|Författare)'
notas_M = '(?i)(x?\d+-|)(notas|(end|foot|)note[nrs]|piednoto|oharrak)'
editr_M = r'<p class="salto10">(?:Editor[ae]?s?\s+di[gx]itale?s?|Digital(?:herausgeber|\s+[Ee]ditors?|\s+[Uu]tgivare)|Di.ita\s+[Rr]edaktisto|Argitaratzaile\s+[Dd]igitala|Éditeur\s+[Nn]umérique(?:&nbsp;|)|Editora?\s+de\s+[Dd]igital):\s+([^<]+?)(?i)(,\s+.*|(\s+para\s+|\s*)\(?\[?www\.epublibre\.org\)?\]?|)</p>'
tradc_M = r'<p\b[^>]*>(?:Tradu(?:c+ió|ctor|ction|ko|ção|zione)|Translat(?:ion|or)|(?:Euskara|Itzul)tzailea|Översättning).*?:\s+(.+?)</p>'
orden_M = ['cubierta, sinopsis, titulo, info', 'coberta, sinopsi, titol, info', 'buchtitel, inhalt, titel, info', 'buchtitel, synopsis, titel, info', 'cover, blurb, title, info', 'cover, synopsis, title, info', 'kovrilo, sinopsis, titolo, info', 'azala, laburpena, izenburua, info', 'couverture, sinopsis, titre, info', 'cuberta, sinopse, titulo, info', 'copertina, trama, titolo, info', 'capa, sinopse, titulo, info', 'omslag, beskrivning, rubrik, info', 'omslag, synopsis, rubrik, info', '1-cubierta, 2-sinopsis, 3-titulo, 4-info']
mal_titu = ['título', 'titulo', 'títol', 'titol', 'titel', 'title', 'titolo', 'izenburua', 'titre', 'rubrik']
mal_autor = ['autor', 'schriftsteller', 'verfasser', 'author', 'a\u016Dtoro', 'idazlea', 'auteur', 'autore', 'författare', 'traductor', 'übersetzer', 'translator', 'tradukisto', 'itzultzaileak', 'traducteur', 'tradutor', 'traduttore', 'översättare', 'apellidos, nombres', 'apellidos nombres', 'nombres apellidos', 'nombres, apellidos']
mala_saga = r'\b([Ss]aga\b|[Ss][eéè]rie\b|[Nn][uú]m(ero|)\b|[Nn]um+b?er\b|[Nn][.\s]*[°ºª]|[Tt]omo?\b|[Vv]ol([uú]me?n?|)\b)'

# otras:
caracteres_permitidos = string.ascii_letters + string.digits + ' _-[]().,&'	# lista de caracteres permitidos en nombres de archivo
caracteres_internos = string.ascii_letters + string.digits + '_-.'	# lista de caracteres permitidos en nombres de archivos internos
arch_basura = ['calibre_bookmarks.txt', 'iTunesMetadata.plist', '.DS_Store']
meta_dc = {'aut':'autor', 'modification':'modificación', 'publication':'publicación', 'title':'título', 'description':'descripción', 'language':'idioma', 'publisher':'editorial', 'subject':'materia', 'identifier':'identificador UUID'}
colaborador = {'adp':'adaptador', 'ann':'anotador', 'aui':'introductor', 'aut':'autor', 'col':'recolector', 'com':'compilador', 'cov':'diseñador', 'drt':'director', 'dsr':'diseñador', 'edt':'editor', 'ill':'ilustrador', 'red':'redactor', 'trl':'traductor'}
fechas_base = ['2012-12-12', '2013-04-23', '2014-04-23']
img_size = [[8395, 8400, 6601], [6664], [18642]]	# tamaños base [[cover r1.0, r1.1, r1.2], [EPL_logo], [ex_libris]]
mal_alias = ['mi alias', 'alias', 'mi nick', 'nick', 'el editor', 'editor', 'el usuario', 'usuario']

# varios:
aut = 'autor'
met = 'metadata'
metad = 'metadatos'
psino = 'página sinopsis'
ptitu = 'página título'
pinfo = 'página info'
narch = 'nombre de archivo'
perror = ' (posible error de código)'
cauto = '  --- corregido automáticamente'
impos = '\nIMPOSIBLE CONTINUAR CON ESTE APORTE'
grave = '\nES OBLIGATORIO RECREAR ESTE APORTE'


# funciones auxiliares
def busca(pat, arch, *args):
	with open(os.path.join(o_text, arch), 'r', encoding='utf-8') as f:
		m = (re.search(pat, line) for line in f)
		if args:
			return next(([match.group(1), match.group(args[0])] for match in m if match), ['', ''])
		else:
			return next((match.group(1) for match in m if match), '')


def recurs(pats, arch, msj1, msj2):
	with open(os.path.join(o_text, arch), 'r', encoding='utf-8') as f:
		for line in f:
			for pat in pats:
				for m in re.finditer(pat, line):
					lista_errores.append(listaerrores[81] % (msj1, m.group(0) + msj2))


def modif():
	global epub_modificado
	lista_errores.append(cauto)
	epub_modificado = True


def prettify(xml):
	xml = xml.toprettyxml(indent='  ', newl='\n')
	# minimiza diferencias entre versiones y plataformas
	xml = re.sub(r'((?<=>)(\n\s*)(?=[^<\s]))|(?<=[^>\s])(\n\s*)(?=<)', '', xml)
	xml = re.sub(r'(?s)<\?\s*xml version=[^>]*>', r'<?xml version="1.0" encoding="utf-8"?>\n', xml)
	xml = re.sub('(?s)<package[^>]*>', '<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="BookId" version="2.0">', xml)
	xml = re.sub('(?s)<!DOCTYPE[^>]*>.*?<ncx[^>]*>', r'<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"\n "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">\n<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">', xml)
	xml = re.sub('<meta [^>]*content="%s"[^>]*>' % cover_id, '<meta name="cover" content="%s" />' % cover_id, xml)	# evita bug Nook
	xml = re.sub(r'\n\s*\n', r'\n', xml)
	xml = re.sub(r'\n\s*\n', r'\n', xml)
	xml = re.sub(r'<\s+', '<', xml)
	xml = re.sub(r'\s+>', '>', xml)
	xml = re.sub(r'\s*/\s*>', ' />', xml)
	return xml


def locate(pat, root=os.curdir):
	for path, dirs, files in os.walk(os.path.abspath(root)):
		# devuelve archivos que coinciden con cierto patrón
		for filename in fnmatch.filter(files, pat):
			yield os.path.join(path, filename)


def recursive_zip(zipf, directory, folder=None):
	nodes = os.listdir(directory)
	# comprime archivos
	for item in nodes:
		if os.path.isfile(os.path.join(directory, item)) and item not in arch_basura:
			zipf.write(os.path.join(directory, item), os.path.join(folder, item), zipfile.ZIP_DEFLATED)
		elif os.path.isdir(os.path.join(directory, item)):
			recursive_zip(zipf, os.path.join(directory, item), os.path.join(folder, item))


def romano(rom):
	val = {'I':1, 'V':5, 'X':10, 'L':50, 'C':100, 'D':500, 'M':1000}
	total = 0
	try:
		while rom:
			if len(rom) == 1 or val[rom[0]] >= val[rom[1]]:
				total += val[rom[0]]
				rom = rom[1:]
			else:
				total += val[rom[1]] - val[rom[0]]
				rom = rom[2:]
	except:
		total = 0
	finally:
		return texto(total)


def imprime(txt):
	for e in txt:
		e = e.replace('&amp;', '&')
		try:
			print(e)
		except UnicodeEncodeError:
			e = re.sub('[“”]', '{"}', e)
			e = re.sub('[‘’]', "{'}", e)
			e = re.sub('[—–\u2212\u2012\u2015\u203E]', '{-}', e)	# emdash, endash, minus, figure dash, horizontal bar, overline
			e = e.replace('•', '{·}')
			e = e.replace('…', '{...}')
			e = ''.join(c if 31 < ord(c) < 127 or 160 < ord(c) < 256 else '{*}' for c in e)
			print(e)


def limpia(txt):
	if txt:
		txt = re.sub('</?[^/>]+>', '', txt)	# toda etiqueta, menos <br/> o <hr/>
		txt = re.sub(r'\s*&nbsp;\s*|  +', ' ', txt)
		return txt.strip()
	return ''


def normaliza(txt):
	if txt:
		return ''.join(c for c in txt if c in caracteres_permitidos)
	return ''


def roles(rol):
	if rol in colaborador:
		return colaborador[rol]
	return 'colaborador'


def file_as_to_autor(autor):
	if autor:
		if not autor.count(' '):
			return autor

		#autor = re.sub(r'(?i) y (colaboradores|otr[ao]s)\b', r' & \1', autor)
		autores = autor.split(' & ')
		autor_inv = ''
		for a in autores:
			if autor_inv:
				autor_inv += ' & '
			a_sort = a.split(', ')
			if aa_vv_M.search(a) or len(a_sort) < 2:
				autor_inv += a
			else:
				autor_inv += a_sort[1] + ' ' + a_sort[0]

		return autor_inv
	return ''


def vvaa(autor):
	if autor:
		if aa_vv_M.search(autor) and 'AA. VV.' not in autor:
			return True
	return False


# obtención de datos básicos
def get_file_name(title_id, node):
	for n in lManifest[0].childNodes:
		if n.nodeName == 'item' and n.getAttribute('id') == title_id:
			return(os.path.basename(n.getAttribute('href')))
	# si no se encuentra, se le ha cambiado el nombre. Se ubica por posición
	title_id = lSpine[node].getAttribute('idref')
	for n in lManifest[0].childNodes:
		if n.nodeName == 'item' and n.getAttribute('id') == title_id:
			return(os.path.basename(n.getAttribute('href')))


def get_jpg_size(jpeg):
	jpeg.read(2)
	b = jpeg.read(1)
	try:
		while (b and ord(b) != 0xDA):
			while (ord(b) != 0xFF): b = jpeg.read(1)
			while (ord(b) == 0xFF): b = jpeg.read(1)
			if ord(b) >= 0xC0 and ord(b) <= 0xC3:
				jpeg.read(3)
				h, w = struct.unpack(str('>HH'), jpeg.read(4))	# no usar 'texto' (P2.6)
				break
			else:
				jpeg.read(int(struct.unpack(str('>H'), jpeg.read(2))[0])-2)	# no usar 'texto' (P2.6)
			b = jpeg.read(1)
		try:
			width = int(w)
			height = int(h)
			return (width, height)
		except NameError:
			return None
	except struct.error:
		return None
	except ValueError:
		return None


# funciones para comprobaciones en los epubs
def validar_broken_opf():
	if re.search(r'(?i)Your\s*OPF\s*file\s*was\s*broken', txt_opf):
		lista_errores.append(listaerrores[1])

def validar_metadatos():
	global meta_idioma	# código de dos letras en min, se usará en validar_formato_nombre_archivo
	elem = xml_opf.getElementsByTagName(met)
	meta_obligatorios = meta_dc.keys()	# aut, modification, publication no se detectan tal cual
	[meta_actuales, meta_vacios, visto] = [[], [], set()]

	for n in elem[0].childNodes:
		nname = n.nodeName.replace('dc:', '')
		nvalue = n.firstChild.nodeValue if n.firstChild else ''

		if nname in meta_obligatorios:
			if not nvalue:
				meta_vacios.append(meta_dc[nname])
			else:
				meta_actuales.append(meta_dc[nname])

		elif nname == 'creator':	# no se comprueba rol 'aut', se hará en 'validar_autor'
			if not nvalue:
				meta_vacios.append(aut)
			else:
				meta_actuales.append(aut)

		elif nname == 'contributor':
			rol = roles(n.getAttribute('opf:role'))
			if not nvalue:
				meta_vacios.append(rol)
			else:
				meta_actuales.append(rol)

		elif nname == 'date':
			fecha = n.getAttribute('opf:event')
			if fecha in ['modification', 'publication']:
				if not nvalue:
					meta_vacios.append(meta_dc[fecha])
				else:
					meta_actuales.append(meta_dc[fecha])

		if nname == 'description' and nvalue == 'Sinopsis':	# sinopsis del ePub base sin cambiar
			lista_errores.append(listaerrores[5] % nvalue)

		if nname == 'language':
			if nvalue in idiomas.keys():
				meta_idioma = nvalue
			else:
				lista_errores.append(listaerrores[6] % nvalue)

		if nname == 'publisher' and nvalue != 'ePubLibre':
			lista_errores.append(listaerrores[7] % nvalue)

	meta_obligatorios = meta_dc.values()
	meta_faltantes = sorted(set(meta_obligatorios) - set(meta_actuales))
	meta_repetidos = sorted(set([x for x in meta_actuales if (x in visto or visto.add(x))]))
	if meta_faltantes:
		lista_errores.append(listaerrores[2] % ', '.join(meta_faltantes))
	if meta_vacios:
		lista_errores.append(listaerrores[3] % ', '.join(meta_vacios.sort()))
	if meta_repetidos:
		lista_errores.append(listaerrores[4] % ', '.join(meta_repetidos))
	lista_errores.sort()


def validar_bookid():
	n = xml_opf.getElementsByTagName('dc:identifier')
	bookid = n[0].firstChild.nodeValue if n[0].firstChild else ''

	# comprueba si BookId es de tipo UUID
	if n[0].getAttribute('opf:scheme').upper() != 'UUID':
		lista_errores.append(listaerrores[11])
	# comprueba si es igual al del ePub base
	elif bookid in uuid_epubbase:
		lista_errores.append(listaerrores[9] % bookid.replace('urn:uuid:', ''))
		nuevoBookId(n[0])
	# comprueba si está relleno
	elif not bookid:
		lista_errores.append(listaerrores[10])
	else:
		# comprueba formato correcto del UUID
		uuid4hex_pat = 'urn:uuid:[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}'
		if not re.search(uuid4hex_pat, bookid):
			lista_errores.append(listaerrores[12] % bookid)
			nuevoBookId(n[0])

		# comprueba que esté igual en la TOC
		nodes_ncx = xml_ncx.getElementsByTagName('meta')
		for nn in nodes_ncx:
			if nn.getAttribute('name') == 'dtb:uid':
				if nn.getAttribute('content') != n[0].firstChild.nodeValue:
					lista_errores.append(listaerrores[13])	# no se autocorrige, regenerar la TOC evita errores adicionales


def nuevoBookId(bnode):
	if corregir_errores:
		newId = uuid.uuid4()	# genera nuevo uuid aleatorio
		bnode.firstChild.nodeValue = 'urn:uuid:' + texto(newId)

		n = xml_ncx.getElementsByTagName('meta')
		for e in n:
			if e.getAttribute('name') == 'dtb:uid':
				e.setAttribute('content', 'urn:uuid:' + texto(newId))

		with open(toc_file, 'w', encoding='utf-8') as f:
			f.write(prettify(xml_ncx))	# guarda toc.ncx

		modif()


def validar_toc():
	tit_opf = tit_ncx = ''
	try:
		tit_opf = xml_opf.getElementsByTagName('dc:title')[0].firstChild.nodeValue
		# en una TOC bien formada, docTitle siempre tiene el primer elemento <text>
		tit_ncx = xml_ncx.getElementsByTagName('text')[0].firstChild.nodeValue
	except:
		pass	# por si falla cualquiera de los dos anteriores
	if tit_opf != tit_ncx:
		lista_errores.append(listaerrores[8])


def validar_css():
	if not os.path.isfile(stylecss) or not re.search('"Styles/style.css"', txt_opf):
		lista_errores.append(listaerrores[14])
		return

	files = locate('*.css', tempdir)
	if sum(1 for _ in files) > 1:
		lista_errores.append(listaerrores[15])

	if version_epub == '1.0':
		pat = r'/\*\s*[Ee][Pp][Uu][Bb] base r1\.0 e[Pp]ub[Ll]ibre\s*\*/\s*/\*\s*-+\s*ESTILOS\s*GLOBALES\s*Y\s*DE\s*SECCIONES\s*FIJAS\s*\(NO\s*MODIFICABLES\)\s*-+\s*\*/\s*body\s*\{\s*margin\s*:\s*1em\s*;\s*\}\s*p\s*\{\s*margin\s*:\s*0\s*;\s*text-align\s*:\s*justify\s*;\s*text-indent\s*:\s*1\.5em\s*;\s*line-height\s*:\s*1\.3em\s*;\s*\}\s*a\s*\{\s*font-style\s*:\s*normal\s*;\s*font-weight\s*:\s*normal\s*;\s*text-decoration\s*:\s*none\s*;\s*\}\s*sup\s*,\s*sub\s*\{\s*font-size\s*:\s*0\.75em\s*;\s*line-height\s*:\s*normal\s*;\s*\}\s*/\*\s*-+\s*CUBIERTA\s*-+\s*\*/\s*\.cubierta\s*\{\s*margin\s*:\s*0\s*;\s*padding\s*:\s*0\s*;\s*border\s*:\s*0\s*;\s*font-size\s*:\s*0\s*;\s*text-align\s*:\s*center\s*;\s*text-indent\s*:\s*0\s*;\s*\}\s*\.cubierta\s*img\s*\{\s*height\s*:\s*100%\s*;\s*max-height\s*:\s*100%\s*;\s*\}\s*/\*\s*-+\s*SINOPSIS\s*-+\s*\*/\s*\.sinopsis\s*,\s*\.sinopsis\s*p\s*,\s*\.sinopsis\s*em\s*,\s*\.sinopsis\s*strong\s*,\s*\.sinopsis\s*span\s*\{\s*margin-top\s*:\s*0\.5em\s*;\s*text-indent\s*:\s*0\s*;\s*font-family\s*:\s*sans-serif\s*;\s*\}\s*/\*\s*-+\s*TITULO\s*-+\s*\*/\s*\.tlogo\s*,\s*\.tautor\s*,\s*\.ttitulo\s*,\s*\.tsubtitulo\s*,\s*\.trevision\s*,\s*\.tfirma\s*\{\s*text-align\s*:\s*center\s*;\s*text-indent\s*:\s*0\s*;\s*adobe-hyphenate\s*:\s*none\s*;\s*hyphenate\s*:\s*none\s*;\s*hyphens\s*:\s*none\s*;\s*-moz-hyphens\s*:\s*none\s*;\s*-webkit-hyphens\s*:\s*none\s*;\s*\}\s*\.tlogo\s*span\s*\{\s*margin\s*:\s*3em\s*0\s*2\.5em\s*;\s*padding\s*:\s*0\s*;\s*border\s*:\s*0\s*;\s*display\s*:\s*inline-block\s*;\s*width\s*:\s*8em\s*;\s*\}\s*\.tautor\s*\{\s*margin-bottom\s*:\s*0\.5em\s*;\s*font-size\s*:\s*1\.2em\s*;\s*color\s*:\s*#595959\s*;\s*\}\s*\.ttitulo\s*\{\s*margin\s*:\s*0\s*;\s*font-size\s*:\s*1\.8em\s*;\s*\}\s*\.tsubtitulo\s*\{\s*margin\s*:\s*0\.3em\s*0\s*0\s*;\s*\}\s*\.trevision\s*\{\s*margin\s*:\s*2\.5em\s*0\s*0\s*;\s*font-size\s*:\s*0\.8em\s*;\s*color\s*:\s*#595959\s*;\s*\}\s*\.tfirma\s*,\s*\.tfirma\s*strong\s*,\s*\.tfirma\s*code\s*\{\s*font-size\s*:\s*0\.8em\s*;\s*\}\s*\.tfecha\s*\{\s*color\s*:\s*#595959\s*;\s*\}\s*/\*\s*-+\s*INFO\s*-+\s*\*/\s*\.info\s*\{\s*margin\s*:\s*3\.5em\s*1\.5em\s*;\s*font-size\s*:\s*0\.8em\s*;\s*width\s*:\s*90%\s*;\s*\}\s*\.info\s*p\s*\{\s*text-align\s*:\s*left\s*;\s*text-indent\s*:\s*0\s*;\s*\}\s*/\*\s*-+\s*DEDICATORIA\s*-+\s*\*/\s*\.dedicatoria\s*\{[^}]+?\}\s*\.dedicatoria\s*p\s*\{[^}]+?\}\s*/\*\s*-+\s*AUTOR\s*-+\s*\*/\s*\.autorimg\s*\{\s*margin\s*:\s*1\.5em\s*;\s*padding\s*:\s*0\s*;\s*border\s*:\s*0\s*;\s*text-align\s*:\s*center\s*;\s*text-indent\s*:\s*0\s*;\s*display\s*:\s*block\s*;\s*height\s*:\s*40%\s*;\s*\}\s*/\*\s*-+\s*NOTAS\s*-+\s*\*/\s*\.nota\s*\{\s*padding-top\s*:\s*10%\s*;\s*text-indent\s*:\s*0\s*;\s*page-break-before\s*:\s*always\s*;\s*\}\s*\.nota\s*p\s*\{\s*text-indent\s*:\s*0\s*;\s*\}'
	elif version_epub == '1.1':
		pat = r'/\*\s*ePub\s*base\s*r1\.1\s*ePubLibre\s*\*/\s*/\*\s*-+\s*ESTILOS\s*GLOBALES\s*Y\s*DE\s*SECCIONES\s*FIJAS\s*\(NO\s*MODIFICABLES\)\s*-+\s*\*/\s*body\s*\{\s*margin\s*:\s*1em\s*;\s*padding\s*:\s*0\s*;\s*border\s*:\s*0\s*;\s*\}\s*p\s*\{\s*margin\s*:\s*0\s*;\s*text-align\s*:\s*justify\s*;\s*text-indent\s*:\s*1\.5em\s*;\s*line-height\s*:\s*1\.3em\s*;\s*\}\s*a\s*,\s*\.normal\s*\{\s*font-style\s*:\s*normal\s*;\s*font-weight\s*:\s*normal\s*;\s*text-decoration\s*:\s*none\s*;\s*\}\s*sup\s*,\s*sub\s*\{\s*font-size\s*:\s*0\.75em\s*;\s*line-height\s*:\s*normal\s*;\s*\}\s*\.cubierta\s*\{\s*margin\s*:\s*0\s*;\s*padding\s*:\s*0\s*;\s*border\s*:\s*0\s*;\s*font-size\s*:\s*0\s*;\s*text-align\s*:\s*center\s*;\s*text-indent\s*:\s*0\s*;\s*page-break-before\s*:\s*always\s*;\s*page-break-after\s*:\s*always\s*;\s*\}\s*\.cubierta\s*img\s*\{\s*height\s*:\s*100%\s*;\s*max-height\s*:\s*100%\s*;\s*\}\s*\.tlogo\s*,\s*\.tautor\s*,\s*\.ttitulo\s*,\s*\.tsubtitulo\s*,\s*\.trevision\s*,\s*\.tfirma\s*\{\s*margin\s*:\s*0\s*0\.25em\s*;\s*text-align\s*:\s*center\s*;\s*text-indent\s*:\s*0\s*;\s*font-family\s*:\s*sans-serif\s*;\s*font-weight\s*:\s*bold\s*;\s*adobe-hyphenate\s*:\s*none\s*;\s*hyphenate\s*:\s*none\s*;\s*hyphens\s*:\s*none\s*;\s*-moz-hyphens\s*:\s*none\s*;\s*-webkit-hyphens\s*:\s*none\s*;\s*\}\s*\.tlogo\s*span\s*\{\s*margin\s*:\s*3em\s*0\s*2\.5em\s*;\s*display\s*:\s*inline-block\s*;\s*width\s*:\s*8em\s*;\s*\}\s*\.tautor\s*\{\s*margin-bottom\s*:\s*0\.5em\s*;\s*font-size\s*:\s*1\.2em\s*;\s*font-weight\s*:\s*normal\s*;\s*color\s*:\s*#595959\s*;\s*\}\s*\.ttitulo\s*\{\s*(margin-bottom\s*:\s*0.15em\s*;\s*|)padding\s*:\s*0\s*;\s*border\s*:\s*0\s*;\s*font-size\s*:\s*1\.8em\s*;\s*font-style\s*:\s*normal\s*;\s*text-decoration\s*:\s*none\s*;\s*color\s*:\s*black\s*;\s*visibility\s*:\s*visible\s*;\s*\}\s*(\.tsubtitulo\s*\{\s*margin-top\s*:\s*0\.3em\s*;\s*\}|)\s*\.trevision\s*\{\s*margin-top\s*:\s*2\.5em\s*;\s*font-size\s*:\s*0\.8em\s*;\s*color\s*:\s*#595959\s*;\s*\}\s*\.tfirma\s*\{\s*margin-top\s*:\s*0\.25em\s*;\s*font-size\s*:\s*0\.65em\s*;\s*\}\s*\.tfecha\s*\{\s*font-family\s*:\s*sans-serif\s*;\s*font-weight\s*:\s*normal\s*;\s*color\s*:\s*#595959\s*;\s*\}\s*\.sinopsis\s*,\s*\.sinopsis\s*p\s*,\s*\.autor\s*,\s*\.autor\s*p\s*,\s*\.nota\s*p\s*\{\s*margin-top\s*:\s*0\.5em\s*;\s*text-indent\s*:\s*0\s*;\s*\}\s*\.sinopsis\s*p\s*,\s*\.sinopsis\s*em\s*,\s*\.sinopsis\s*strong\s*,\s*\.sinopsis\s*big\s*,\s*\.sinopsis\s*small\s*,\s*\.sinopsis\s*span\s*\{\s*font-family\s*:\s*sans-serif\s*;\s*\}\s*\.info\s*\{\s*margin\s*:\s*3\.5em\s*1\.5em\s*2\.5em\s*;\s*font-size\s*:\s*0\.8em\s*;\s*width\s*:\s*90%\s*;\s*\}\s*\.info\s*p\s*\{\s*text-align\s*:\s*left\s*;\s*text-indent\s*:\s*0\s*;\s*\}\s*\.vineta\s*\{\s*padding\s*:\s*1em\s*0\s*;\s*text-align\s*:\s*center\s*;\s*display\s*:\s*block\s*;\s*\}\s*\.nota\s*\{\s*padding-top\s*:\s*9%\s*;\s*page-break-before\s*:\s*always\s*;\s*\}'
	else:
		pat = r'/\*\s*ePub\s*base\s*r1\.2\s*ePubLibre\s*\*/\s*/\*\s*-+\s*ESTILOS\s*GLOBALES\s*Y\s*DE\s*SECCIONES\s*FIJAS\s*\(NO\s*MODIFICABLES\)\s*-+\s*\*/\s*body\s*\{\s*margin\s*:\s*1em\s*;\s*padding\s*:\s*0\s*;\s*border\s*:\s*0\s*;\s*\}\s*p\s*\{\s*margin\s*:\s*0\s*;\s*text-align\s*:\s*justify\s*;\s*text-indent\s*:\s*1\.5em\s*;\s*line-height\s*:\s*1\.25em\s*;\s*\}\s*a\s*,\s*\.normal\s*\{\s*font-style\s*:\s*normal\s*;\s*font-weight\s*:\s*normal\s*;\s*text-decoration\s*:\s*none\s*;\s*\}\s*sup\s*,\s*sub\s*\{\s*font-size\s*:\s*0\.75em\s*;\s*line-height\s*:\s*normal\s*;\s*\}\s*\.cubierta\s*\{\s*margin\s*:\s*0\s*;\s*padding\s*:\s*0\s*;\s*border\s*:\s*0\s*;\s*font-size\s*:\s*0\s*;\s*text-align\s*:\s*center\s*;\s*text-indent\s*:\s*0\s*;\s*page-break-before\s*:\s*always\s*;\s*page-break-after\s*:\s*always\s*;\s*\}\s*\.cubierta\s*img\s*\{\s*height\s*:\s*100%\s*;\s*max-height\s*:\s*100%\s*;\s*\}\s*\.tlogo\s*,\s*\.tautor\s*,\s*\.ttitulo\s*,\s*\.tsubtitulo\s*,\s*\.trevision\s*,\s*\.tfirma\s*\{\s*margin\s*:\s*0\s*0\.25em\s*;\s*text-align\s*:\s*center\s*;\s*text-indent\s*:\s*0\s*;\s*font-family\s*:\s*sans-serif\s*;\s*font-weight\s*:\s*bold\s*;\s*adobe-hyphenate\s*:\s*none\s*;\s*hyphenate\s*:\s*none\s*;\s*hyphens\s*:\s*none\s*;\s*-moz-hyphens\s*:\s*none\s*;\s*-webkit-hyphens\s*:\s*none\s*;\s*\}\s*\.tlogo\s*span\s*\{\s*margin\s*:\s*3em\s*0\s*2\.5em\s*;\s*display\s*:\s*inline-block\s*;\s*width\s*:\s*8em\s*;\s*\}\s*\.tautor\s*\{\s*margin-bottom\s*:\s*0\.5em\s*;\s*font-size\s*:\s*1\.2em\s*;\s*font-weight\s*:\s*normal\s*;\s*color\s*:\s*#595959\s*;\s*\}\s*\.ttitulo\s*\{\s*(margin-bottom\s*:\s*0.15em\s*;\s*|)padding\s*:\s*0\s*;\s*border\s*:\s*0\s*;\s*font-size\s*:\s*1\.8em\s*;\s*font-style\s*:\s*normal\s*;\s*text-decoration\s*:\s*none\s*;\s*color\s*:\s*black\s*;\s*visibility\s*:\s*visible\s*;\s*\}\s*(\.tsubtitulo\s*\{\s*margin-top\s*:\s*0\.3em\s*;\s*\}|)\s*\.trevision\s*\{\s*margin-top\s*:\s*2\.5em\s*;\s*font-size\s*:\s*0\.8em\s*;\s*color\s*:\s*#595959\s*;\s*\}\s*\.tfirma\s*\{\s*margin-top\s*:\s*0\.25em\s*;\s*font-size\s*:\s*0\.65em\s*;\s*\}\s*\.tfecha\s*\{\s*font-family\s*:\s*sans-serif\s*;\s*font-weight\s*:\s*normal\s*;\s*color\s*:\s*#595959\s*;\s*\}\s*\.sinopsis\s*,\s*\.sinopsis\s*p\s*,\s*\.autor\s*,\s*\.autor\s*p\s*,\s*\.nota\s*p\s*\{\s*margin-top\s*:\s*0\.5em\s*;\s*text-indent\s*:\s*0\s*;\s*\}\s*\.sinopsis\s*p\s*,\s*\.sinopsis\s*em\s*,\s*\.sinopsis\s*strong\s*,\s*\.sinopsis\s*big\s*,\s*\.sinopsis\s*small\s*,\s*\.sinopsis\s*span\s*\{\s*font-family\s*:\s*sans-serif\s*;\s*\}\s*\.info\s*\{\s*margin\s*:\s*3\.5em\s*1\.5em\s*2\.5em\s*;\s*font-size\s*:\s*0\.8em\s*;\s*width\s*:\s*90%\s*;\s*\}\s*\.info\s*p\s*\{\s*text-align\s*:\s*left\s*;\s*text-indent\s*:\s*0\s*;\s*\}\s*\.vineta\s*\{\s*padding\s*:\s*1em\s*0\s*;\s*text-align\s*:\s*center\s*; text-indent\s*:\s*0\s*;\s*display\s*:\s*block\s*;\s*\}\s*\.nota\s*\{\s*padding-top\s*:\s*9%\s*;\s*page-break-before\s*:\s*always\s*;\s*\}'

	with open(stylecss, 'r', encoding='utf-8') as f:
		txt = f.read()

	if not re.search(pat, txt):
		lista_errores.append(listaerrores[16])
	if not re.search(r'(?<!\.sinopsis)(?<!\.tlogo| \.sans|\.serif| \.mono) span[{\s]', txt):
		inneces.append(r'(<span>)(?!<img alt="[^"]*" src="\.\./Images/%s")' % img_base[1])	# excluye <span> vacíos pero válidos (para validar_errores_codigo)


def validar_generos_y_subgeneros():
	[etiquetas, visto] = [[], set()]
	elem = xml_opf.getElementsByTagName('dc:subject')
	for n in elem:
		if n.firstChild:
			etiquetas.extend(n.firstChild.nodeValue.split(', '))
	# comprueba que hay al menos un género
	if not set(etiquetas).intersection(generos):
		lista_errores.append(listaerrores[17])
	# comprueba que hay al menos un subgénero
	if not set(etiquetas).intersection(subgeneros):
		lista_errores.append(listaerrores[18])
	# comprueba repeticiones
	etiq_repetidas = sorted(set([x for x in etiquetas if (x in visto or visto.add(x))]))
	if etiq_repetidas:
		lista_errores.append(listaerrores[19] % ', '.join(etiq_repetidas))
	for etiq in etiquetas:
		# comprueba si se ha añadido Tipo
		if etiq.lower() in tipo:
			lista_errores.append(listaerrores[20] % etiq)
		# comprueba si una etiqueta no aparece en ninguna de las listas
		elif etiq not in (generos + subgeneros):
			lista_errores.append(listaerrores[21] % etiq)
	etiquetas = set(etiquetas)
	# si es un género de Ficción, comprueba que no haya géneros y subgéneros de No ficción
	if etiquetas.intersection(generos_ficcion):
		if etiquetas.intersection(generos_no_ficcion):
			lista_errores.append(listaerrores[22] % (tipo[0], tipo[1]))
		if etiquetas.intersection([item for item in subgeneros_no_ficcion if item not in subgeneros_ficcion]):
			lista_errores.append(listaerrores[23] % (tipo[0], tipo[1]))
	# si es un género de No ficción, comprueba que no haya asignados géneros y subgéneros de Ficción
	if etiquetas.intersection(generos_no_ficcion):
		if etiquetas.intersection(generos_ficcion):
			lista_errores.append(listaerrores[22] % (tipo[1], tipo[0]))
		if etiquetas.intersection([item for item in subgeneros_ficcion if item not in subgeneros_no_ficcion]):
			lista_errores.append(listaerrores[23] % (tipo[1], tipo[0]))
	# comprueba que no haya géneros mezclados de Ficción y No ficción
	if etiquetas.intersection(excl_generos_y_subgeneros_ficcion) and etiquetas.intersection(excl_generos_y_subgeneros_no_ficcion):
		lista_errores.append(listaerrores[24])


def validar_titulo():
	titulo_metadata = title_title = titulo_title = titulov_title = ''

	elem = xml_opf.getElementsByTagName('dc:title')
	if elem:
		titulo_metadata = elem[0].firstChild.nodeValue if elem[0].firstChild else ''

	if version_epub == '1.0':
		pat = r'(?s)<(h\d) class="ttitulo"[^>]*?( title="[^"]+"|)[^>]*><strong class="sans">(.+?)</strong></\1>(?:<p class="ttitulo"><strong class="sans">(\W*[A-ZÀ-Þ].+?)</strong></p>|<p class="tsubtitulo"><strong class="sans">(\W*[a-zß-ÿ].+?)</strong></p>|)'
	else:
		pat = r'(?s)<(h\d) class="ttitulo"[^>]*?( title="[^"]+"|)[^>]*>(.+?)</\1>(?:<p class="ttitulo">(\W*[A-ZÀ-Þ].+?)</p>|<p class="tsubtitulo">(\W*[a-zß-ÿ].+?)</p>|)'

	with open(os.path.join(o_text, title_file), 'r', encoding='utf-8') as f:
		txt = f.read()
		txt = re.sub(r'(<h\d\b[^>]*?) id="[^"]*"', r'\1', txt)
		txt = re.sub(r'(?s)\s*<!--.+?-->\s*', '', txt)
		txt = re.sub(r'\s*<br\s*/\s*>\s*', '<br />', txt)
		txt = re.sub(r'>\s*<', '><', txt)

	for m in re.finditer(pat, txt):
		if m.group(3):	# título simple
			titulo_title = limpia(m.group(3).replace('&amp;', '&'))
		if m.group(2):	# uso de "title"
			title_title = re.sub(' title=|"', '', m.group(2))
			if m.group(4):	# dos ttitulos
				if re.search(r'[^.]\. \W*[A-ZÀ-Þ\d]', titulo_metadata):
					titulov_title = titulo_title.rstrip('.') + '. ' + m.group(4)
				else:
					titulov_title = titulo_title + ' ' + m.group(4)
			elif m.group(5):	# ttitulo y subtítulo
				titulov_title = titulo_title + ' ' + m.group(5)
			else:
				titulov_title = titulo_title
			titulov_title = limpia(titulov_title.replace('&amp;', '&'))
		elif re.search(r'[^.]\. \W*[A-ZÀ-Þ\d]', titulo_metadata):	# metadatos con punto: más de un título
			titulov_title = re.sub(r'\.?<br />(?=\W*[A-ZÀ-Þ\d])', '. ', titulo_title)
		else:
			titulov_title = re.sub('<br />', ' ', titulo_title)	# título corrido con <br/>

	# no comprueba titulo_metadata faltante, ya se hizo en 'validar_metadatos'
	if titulo_metadata.lower() in mal_titu:
		lista_errores.append(listaerrores[25] % (metad, titulo_metadata))
	if not titulov_title:
		lista_errores.append(listaerrores[26] % ptitu + perror)
	elif titulov_title.lower() in mal_titu:
		lista_errores.append(listaerrores[25] % (ptitu, titulov_title))
	elif title_title and title_title != titulov_title:
		lista_errores.append(listaerrores[27] % ('real ["title"]', title_title, 'título visible', titulov_title))
	elif titulo_metadata and titulo_metadata != titulov_title:
		lista_errores.append(listaerrores[27] % ('en metadatos', titulo_metadata, ptitu, titulov_title))


def validar_autor():
	autor_metadata = ''

	elem = xml_opf.getElementsByTagName('dc:creator')
	if elem and elem[0].getAttribute('opf:role') == 'aut':
		autor_metadata = elem[0].firstChild.nodeValue if elem[0].firstChild else ''

	if version_epub == '1.0':
		pat = r'<p class="tautor">\s*<code class="sans">(.+)</code>\s*</p>'
	else:
		pat = '<p class="tautor">(.+)</p>'

	autor_title = busca(pat, title_file)
	autor_info = busca(r'<p>([^\d:]+),(.*?\b\d{3,4}\b|\s*(a(ñ|nh?y?)o|fecha) de (1\.ª |)publicaci[oó]n).*</p>', info_file)	# non-greedy, para usar primer año

	# no cambiado y autor_fileas se comprobarán en 'validar_colaboradores'
	if not autor_metadata:
		lista_errores.append(listaerrores[29] % metad + perror)
	if not autor_title:
		lista_errores.append(listaerrores[29] % ptitu + perror)
	elif autor_title.lower() in mal_autor:
		lista_errores.append(listaerrores[28] % ('Autor', ptitu, autor_title))
	if not autor_info:
		lista_errores.append(listaerrores[29] % pinfo + perror)
	elif autor_info.lower() in mal_autor:
		lista_errores.append(listaerrores[28] % ('Autor', pinfo, autor_info))

	autor_title_l = limpia(autor_title)
	autor_title_c = conec_M.sub(' & ', autor_title_l)
	autor_info_l = limpia(autor_info)
	autor_info_c = conec_M.sub(' & ', autor_info_l)

	if autor_metadata.lower() not in mal_autor + ['']:
		autor_metadata_c = conec_M.sub(' & ', autor_metadata)
		if autor_title and autor_metadata_c != autor_title_c:
			lista_errores.append(listaerrores[30] % (metad, autor_metadata, ptitu, autor_title_l))
		if autor_info and autor_metadata_c != autor_info_c:
			lista_errores.append(listaerrores[30] % (metad, autor_metadata, pinfo, autor_info_l))
	if autor_title and autor_info and autor_title_c != autor_info_c:
		lista_errores.append(listaerrores[30] % (ptitu, autor_title, pinfo, autor_info_l))

	if vvaa(autor_title):
		lista_errores.append(listaerrores[37] % (aut, ptitu))
	if vvaa(autor_info):
		lista_errores.append(listaerrores[37] % (aut, pinfo))

	m = re.search('([^][]+) +- +', epub)
	if m and vvaa(m.group(1)):
		lista_errores.append(listaerrores[37] % (aut, narch))


def validar_traductor():
	traductor_metadata = ''

	elem = xml_opf.getElementsByTagName(met)
	for n in elem[0].childNodes:
		if n.nodeName == 'dc:contributor' and n.getAttribute('opf:role') == 'trl':
			traductor_metadata = n.firstChild.nodeValue if n.firstChild else ''

	traductor_info = busca(tradc_M, info_file)
	traductor_info = re.sub(r'[.,;’(-]*?\s*\b\d{3,4}\b.*$', '', traductor_info)
	traductor_info_l = limpia(traductor_info)
	traductor_info_c = conec_M.sub(' & ', traductor_info_l)

	# no cambiado se comprobará en 'validar_colaboradores'
	if traductor_metadata.lower() not in mal_autor + ['']:
		traductor_metadata_c = conec_M.sub(' & ', traductor_metadata)
		if not traductor_info:
			lista_errores.append(listaerrores[31] % (metad, traductor_metadata, pinfo + perror))
		elif traductor_metadata_c != traductor_info_c:
			lista_errores.append(listaerrores[32] % (traductor_metadata, traductor_info_l))

	if traductor_info:
		if traductor_info.lower() in mal_autor:
			lista_errores.append(listaerrores[28] % ('Traductor', pinfo, traductor_info_l))
		elif not traductor_metadata:
			lista_errores.append(listaerrores[31] % (pinfo, traductor_info_l, metad))
		if vvaa(traductor_info):
			lista_errores.append(listaerrores[37] % ('traductor', pinfo))


def validar_colaboradores():
	colab_metadata = colab_rol = colab_fileas = ''

	elem = xml_opf.getElementsByTagName(met)
	for n in elem[0].childNodes:
		if n.nodeName in ['dc:creator', 'dc:contributor']:
			if n.firstChild:
				colab_metadata = n.firstChild.nodeValue
				colab_metadata_c = conec_M.sub(' & ', colab_metadata)
				colab_rol = roles(n.getAttribute('opf:role'))
				colab_fileas = n.getAttribute('opf:file-as')

				if colab_metadata.lower() in mal_autor:
					lista_errores.append(listaerrores[28] % (colab_rol.capitalize(), metad, colab_metadata))
				if vvaa(colab_metadata):
					lista_errores.append(listaerrores[37] % (colab_rol, metad))

				if colab_fileas:
					colab_fileas_inv_c = conec_M.sub(' & ', file_as_to_autor(colab_fileas))
					if colab_fileas.lower() in mal_autor:
						lista_errores.append(listaerrores[33] % (colab_rol, colab_fileas))
					elif colab_fileas_inv_c != colab_metadata_c:
						lista_errores.append(listaerrores[35] % (colab_rol, colab_fileas, colab_metadata))
					if vvaa(colab_fileas):
						lista_errores.append(listaerrores[37] % (colab_rol, 'File-as [Ordenar como] (se copia igual)'))
					elif colab_fileas.lower() not in mal_autor + ['aa. vv.'] and colab_fileas.count(' ') and not colab_fileas.count(','):
						lista_errores.append(listaerrores[36] % colab_rol)
				else:
					lista_errores.append(listaerrores[34] % (colab_rol, colab_metadata))

				if n.nodeName == 'dc:creator' and colab_rol != aut:
					lista_errores.append(listaerrores[38] % (colab_rol.capitalize(), colab_metadata, aut))

				if n.nodeName == 'dc:contributor' and colab_rol == aut:
					lista_errores.append(listaerrores[38] % (colab_rol.capitalize(), colab_metadata, 'colaborador'))


def validar_file_size():
	for f in locate('*.*', tempdir):
		if os.path.getsize(f) >= 307200:
			extension = os.path.splitext(f)[1]
			# omite archivos de fuentes, pues pueden ocupar más de 300 kb
			if extension.lower() not in ['.ttf', '.otf']:
				lista_errores.append(listaerrores[39] % os.path.basename(f))


def validar_imgs_base():
	for e in range(3):
		img = os.path.join(o_images, img_base[e])
		if not os.path.isfile(img):
			lista_errores.append(listaerrores[42] % img_base[e])
		elif e:
			if os.path.getsize(img) not in img_size[e]:
				lista_errores.append(listaerrores[44] % img_base[e])
		else:
			if os.path.getsize(img) in img_size[e]:
				lista_errores.append(listaerrores[43] % img_base[e])
			else:
				with open(img, 'rb') as f:
					cover_size = get_jpg_size(f)
				if not cover_size:
					lista_errores.append(listaerrores[41] % img_base[e])
				elif cover_size != (600, 900):
					lista_errores.append(listaerrores[40] % texto(cover_size))


def validar_img_autor():
	[autores, autor_img] = [0, []]
	pat = r'(?i)<(div|p) class="(?:autorimg|vineta)">\s*<img alt="[^"]*" height="\d+%" src="\.\./Images/([^.]+\.(?:jpe?g|png|gif))"\s*/\s*>\s*</\1>'

	for autor_file in lChapters:
		if autor_h.match(autor_file):
			autores += 1
			m = busca(pat, autor_file, 2)
			if m[1]:
				autor_img.append(m[1])

	for img in autor_img:
		img_file = os.path.join(o_images, img)
		if not os.path.isfile(img_file):
			lista_errores.append(listaerrores[42] % img)
			continue
		elif os.path.getsize(img_file) in [21044, 8990, 20289]:	# r1.0, r1.1, pruebas r1.1
			lista_errores.append(listaerrores[43] % img)
			continue

		with open(img_file, 'rb') as f:
			autor_size = get_jpg_size(f)
			if not autor_size:
				lista_errores.append(listaerrores[41] % img)
			elif autor_size[0] > 600:
				lista_errores.append(listaerrores[45] % (img, autor_size[0]))
			elif autor_size[1] > 450:
				lista_errores.append(listaerrores[46] % (img, autor_size[1]))

	probimg = ', '.join(os.path.basename(m) for m in locate('autor*.*', o_images))
	if probimg and not autores:
		lista_errores.append(listaerrores[47] % (probimg, ''))
	elif probimg and not autor_img:
		lista_errores.append(listaerrores[47] % (probimg, 'código correcto en '))


def validar_jpeg_progresivo():
	for f in locate('*.jp*g', tempdir):
		try:
			with open(f, 'rb') as jpeg:
				b = jpeg.read(2)	# lee los dos primeros bytes
				if b == b'\xFF\xD8':	# SOI (marca de comienzo de archivo)
					while b:
						b = jpeg.read(1)
						if b == b'\xFF':	# MARKER
							b = jpeg.read(1)
							if b in [b'\xC2', b'\xC6', b'\xCA', b'\xCE']:	# indicadores de progresividad
								lista_errores.append(listaerrores[48] % os.path.basename(f))
								break
							elif b in [b'\xC0', b'\xC1', b'\xC3', b'\xC5', b'\xC7', b'\xC9', b'\xCB', b'\xCD', b'\xCF']:	# indicadores de no progresividad
								break
							elif b != b'\xDD':	# comprobación adicional para bloques que no contienen tamaño (DRI y RSTn)
								desp_1 = jpeg.read(1)
								desp_2 = jpeg.read(1)
								try:
									desplazam = (ord(desp_1)*256 + ord(desp_2)) - 2
									jpeg.seek(desplazam,1)	# desplazamiento fuera de bloque de tamaño
								except:
									pass
		except IOError:
			lista_errores.append(listaerrores[41] % os.path.basename(f))


def validar_saga():
	elem = xml_opf.getElementsByTagName('meta')
	snodes = [n.getAttribute('content') for n in elem if n.getAttribute('name') == 'calibre:series']
	vnodes = [n.getAttribute('content') for n in elem if n.getAttribute('name') == 'calibre:series_index']

	if '' in snodes:
		snodes.remove('')
		lista_errores.append(listaerrores[49] % '')
	saga_metadata = snodes[0].strip() if snodes else ''

	if '' in vnodes:
		vnodes.remove('')
		lista_errores.append(listaerrores[49] % '_index')
	vol_metadata = vnodes[0].lstrip('0').replace('.00', '').replace('.0', '').strip() if vnodes else ''
	if re.match(r'\b[IVXLC]+\b', vol_metadata):
		vol_metadata = romano(vol_metadata)

	if version_epub == '1.0':
		pat = r'<p class="tsubtitulo">\s*<strong class="sans">(.+?)\W+?((%s\W*?|)(&nbsp;|)([IVXLC]+|\d{1,3}\.\d{1,3}|\d{1,3}))\s*</strong>\s*</p>' % mala_saga
	else:
		pat = r'<p class="tsubtitulo">(.+?)\W+?((%s\W*?|)(&nbsp;|)([IVXLC]+|\d{1,3}\.\d{1,3}|\d{1,3}))\s*</p>' % mala_saga

	m = busca(pat, title_file, 2)
	saga_title = m[0].replace('&amp;', '&').strip()
	vol_title = m[1].lstrip('0').replace('&nbsp;', ' ').strip()
	if re.match(r'\b[IVXLC]+\b', vol_title):
		vol_title = romano(vol_title)

	if saga_metadata and not saga_title:
		lista_errores.append(listaerrores[50] % (metad, saga_metadata, ptitu + perror))
	if saga_title and not saga_metadata:
		lista_errores.append(listaerrores[50] % (ptitu, saga_title, metad))
	if saga_metadata and saga_title and saga_metadata != saga_title:
		lista_errores.append(listaerrores[51] % (saga_metadata, saga_title))

	if vol_metadata and not vol_title:
		lista_errores.append(listaerrores[52] % (metad, vol_metadata, ptitu + perror))
	if vol_title and not vol_metadata:
		lista_errores.append(listaerrores[52] % (ptitu, vol_title, metad))
	if vol_metadata and vol_title and vol_metadata != vol_title:
		lista_errores.append(listaerrores[53] % (vol_metadata, vol_title))

	for m in re.finditer(mala_saga, saga_metadata):
		lista_avisos.append(listaavisos[5] % (m.group(1), metad))
	for m in re.finditer(mala_saga, saga_title):
		lista_avisos.append(listaavisos[5] % (m.group(1), ptitu))
	for m in re.finditer(mala_saga, vol_metadata):
		lista_avisos.append(listaavisos[5] % (m.group(1), metad))
	for m in re.finditer(mala_saga, vol_title):
		lista_avisos.append(listaavisos[5] % (m.group(1), ptitu))


def validar_revision():
	r_narch = r_narch_dec = ''

	if version_epub == '1.0':
		pat = r'<p class="trevision">\s*<strong class="sans">eP[Uu][Bb] r(\d+\.)(\d+)</strong>\s*</p>'
	else:
		pat = r'<p class="trevision">ePub r(\d+\.)(\d+)</p>'

	m = busca(pat, title_file, 2)
	r_title = m[0] + m[1]
	r_title_dec = m[1]

	for m in re.finditer(r'\(r(\d+\.)(\d+)[^)]*\)(\s*\[[^][]+\]|)\s*\.(EPUB|epub)', epub):
		r_narch = m.group(1) + m.group(2)
		r_narch_dec = m.group(2)

	if not r_title:
		lista_errores.append(listaerrores[54] % ptitu + perror)
	if not r_narch:
		lista_errores.append(listaerrores[54] % narch)
	elif r_title and r_title != r_narch:
		lista_errores.append(listaerrores[55] % (r_title, r_narch))

	if len(r_title_dec) > 1:
		lista_errores.append(listaerrores[56] % ptitu)
	if len(r_narch_dec) > 1:
		lista_errores.append(listaerrores[56] % narch)


def validar_anyo_publicacion():
	pub_metadata = anyo_metadata = 0

	elem = xml_opf.getElementsByTagName(met)
	for n in elem[0].childNodes:
		if n.nodeName == 'dc:date' and n.getAttribute('opf:event') == 'publication':
			pub_metadata = n.firstChild.nodeValue if n.firstChild else ''
			anyo_metadata = int(pub_metadata.split('-')[0])

	anyo_info = busca(r'<p>[^\d:]+,.*?\b(\d{3,4})\b.*</p>', info_file)	# non-greedy, para usar primer año
	anyo_info = int(anyo_info) if anyo_info else 0

	if pub_metadata in fechas_base:	# fecha de publicación del ePub base sin cambiar
		lista_errores.append(listaerrores[57] % pub_metadata)
	if int(date.today().year) < anyo_metadata:
		lista_errores.append(listaerrores[58] % (metad, anyo_metadata))
	if int(date.today().year) < anyo_info:
		lista_errores.append(listaerrores[58] % (pinfo, anyo_info))

	# no comprueba anyo_metadata faltante, ya se hizo en 'validar_metadatos'
	if not anyo_info:
		lista_errores.append(listaerrores[59] % pinfo + perror)
	elif anyo_metadata and anyo_metadata != anyo_info:
		lista_errores.append(listaerrores[60] % (anyo_metadata, anyo_info))


def validar_fecha_modificacion():
	mdate_metadata = mdate_title = ''

	elem = xml_opf.getElementsByTagName(met)
	for n in elem[0].childNodes:
		if n.nodeName == 'dc:date' and n.getAttribute('opf:event') == 'modification':
			mdate_metadata = n.firstChild.nodeValue if n.firstChild else ''

	if version_epub == '1.0':
		pat = r'(<p class="tfirma">\s*<strong class="sans">[^<]+</strong>\s*<code class="tfecha sans">)(\d{,2}\.\d{,2}\.\d{2,4})(</code>\s*</p>)'
	else:
		pat = r'(<p class="tfirma">[^<]+<span class="tfecha">)(\d{,2}\.\d{,2}\.\d{2,4})(</span>\s*</p>)'

	m = busca(pat, title_file, 2)
	try:
		mdate_title = texto(datetime.strptime(m[1], '%d.%m.%y').date())
	except:
		try:
			mdate_title = texto(datetime.strptime(m[1], '%d.%m.%Y').date())
		except:
			mdate_title = ''

	# comprueba si la fecha de modificación es la del ePub base (la primera sólo pasa en Sigil antiguo)
	if mdate_metadata in fechas_base:
		lista_errores.append(listaerrores[61] % (metad, mdate_metadata))
	if mdate_title in fechas_base:
		lista_errores.append(listaerrores[61] % (ptitu, mdate_title))

	# no comprueba mdate_metadata faltante, ya se hizo en 'validar_metadatos'
	if not mdate_title:
		lista_errores.append(listaerrores[62] % ptitu + perror)

	# comprueba si las fechas de modificación son diferentes
	elif mdate_metadata and mdate_metadata != mdate_title:
		lista_errores.append(listaerrores[63] % (mdate_metadata, mdate_title))

		if corregir_errores:
			hoy = texto(date.today().strftime('%d.%m.%y'))
			with open(os.path.join(o_text, title_file), 'r', encoding='utf-8') as f:
				txt = f.read()
			txt = re.sub(pat, r'\g<1>' + hoy + '\g<3>', txt)	# cambia fecha a hoy
			with open(os.path.join(o_text, title_file), 'w', encoding='utf-8') as f:	# guarda titulo.xhtml
				f.write(txt)

			elem = xml_opf.getElementsByTagName(met)
			for n in elem[0].childNodes:
				if n.nodeName == 'dc:date' and n.getAttribute('opf:event') == 'modification':
					n.firstChild.nodeValue = date.today()	# cambia fecha a hoy

			modif()


def validar_editor_en_titulo_e_info():
	if version_epub == '1.0':
		pat = r'<p class="tfirma">\s*<strong class="sans">([^<]+)</strong>'
	else:
		pat = r'<p class="tfirma">([^<]+)\s+<span class="tfecha">'

	editor_title = busca(pat, title_file)
	editor_info = busca(editr_M, info_file)

	if not editor_title:
		lista_errores.append(listaerrores[64] % ptitu + perror)
	if not editor_info:
		lista_errores.append(listaerrores[64] % pinfo + perror)
	elif editor_title and editor_title != editor_info:
		lista_errores.append(listaerrores[65] % (editor_title, editor_info))


def validar_nombre_archivo():
	if not all([c in caracteres_permitidos for c in epub]):
		lista_errores.append(listaerrores[66] % '')


def validar_nombre_archivos_internos():
	for f in locate('*.*', tempdir):
		if not all([c in caracteres_internos for c in os.path.basename(f)]):
			lista_errores.append(listaerrores[66] % ' interno (' + os.path.basename(f) + ')')


def validar_formato_nombre_archivo():
	# Apellido, Nombre - Titulo [ePL-ID] (rx.x alias_opcional) [IDIOMA_opcional].epub
	pats = [r'(?i)[^][]+ +- +[^][]+ +\[\d+\] +\(r\d\.\d+[a-z]?( +[^)]+|)\)( *\[[A-Z]{2}\]|) *\.epub']
	# Apellido, Nombre - [saga número] Titulo [ePL-ID] (rx.x alias_opcional) [IDIOMA_opcional].epub
	pats.append(r'(?i)[^][]+ +- +\[[^[]+\] +[^][]+ +\[\d+\] +\(r\d\.\d+[a-z]?( +[^)]+|)\)( *\[[A-Z]{2}\]|) *\.epub')
	# [saga larga] Apellido, Nombre - Titulo [ePL-ID] (rx.x alias_opcional) [IDIOMA_opcional].epub
	pats.append(r'(?i)\[[^[]+\] +[^][]+ +- +[^][]+ +\[\d+\] +\(r\d\.\d+[a-z]?( +[^)]+|)\)( *\[[A-Z]{2}\]|) *\.epub')
	# [saga larga] [subsaga número] Apellido, Nombre - Titulo [ePL-ID] (rx.x alias_opcional) [IDIOMA_opcional].epub
	pats.append(r'(?i)\[[^[]+\] \[[^[]+\] +[^][]+ +- +[^][]+ +\[\d+\] +\(r\d\.\d+[a-z]?( +[^)]+|)\)( *\[[A-Z]{2}\]|) *\.epub')

	# comprueba identificador ePL-ID válido
	if not re.search(r'\[\d+\] +\(r\.?\d', epub) or re.search(r'\[0+\] +\(r\.?\d', epub):
		lista_errores.append(listaerrores[67])

	# comprueba idioma
	m = re.search(r'(?i)\[([A-Z]+)\] *\.epub', epub)
	idioma_narch = m.group(1).lower() if m else ''
	if m and idioma_narch not in idiomas.keys():
		lista_errores.append(listaerrores[68] % m.group(1))	# idioma_narch no aceptado
	# no comprueba meta_idioma, ya se hizo en 'validar_metadatos'
	if meta_idioma == 'es':
		if idioma_narch == 'es':
			lista_errores.append(listaerrores[69])	# idioma_narch innecesario
		elif m:
			lista_errores.append(listaerrores[71] % (idiomas[meta_idioma], m.group(1)))	# meta_idioma 'es', idioma_narch otro
	elif meta_idioma:
		if not m:	# meta_idioma no 'es', idioma_narch no
			lista_errores.append(listaerrores[70] % (idiomas[meta_idioma]))
		elif meta_idioma != idioma_narch:	# meta_idioma no 'es', idioma_narch otro
			lista_errores.append(listaerrores[71] % (idiomas[meta_idioma], m.group(1)))

	# comprueba espacios innecesarios
	if re.search(r'(?i)^ | $|  | \.epub', epub):
		lista_avisos.append(listaavisos[2])

	# comprueba doble extensión .epub
	if re.search(r'(?i)\.epub *\.epub', epub):
		lista_avisos.append(listaavisos[3])

	# comprueba alias
	m = re.search(r'(?i)\(r\.?\d+\.\d+[a-z]? +([^)]+)\)( *\[[A-Z]+\]|) *\.epub', epub)
	if m and m.group(1).lower() in mal_alias:
		lista_avisos.append(listaavisos[4] % m.group(1))

	# comprueba formato
	for pat in pats:
		if re.match(pat, epub):
			return
	lista_errores.append(listaerrores[72])


def validar_fuentes_ibooks():
	txt = '<?xml version="1.0" encoding="utf-8"?>\n<display_options>\n\t<platform name="*">\n\t\t<option name="specified-fonts">true</option>\n\t</platform>\n</display_options>'
	if os.path.isfile(ibooks_f):
		return
	if version_epub == '1.0':
		if not lFonts:
			return
		lista_errores.append(listaerrores[73])
	else:
		lista_errores.append(listaerrores[74])
	if corregir_errores:
		with open(ibooks_f, 'w', encoding='utf-8') as f:
			f.write(txt)
		modif()


def validar_orden_fijas():
	orden = ', '.join(re.sub(r'\.x?html?', '', get_file_name('', e)) for e in range(4))
	if orden.lower() not in orden_M:
		lista_errores.append(listaerrores[75] % orden)


def validar_orden_autor_notas():
	[pos, autor, nota] = [1, 0, 0]
	for n in lSpine:
		idref = n.getAttribute('idref')
		if autor_h.match(idref):
			[autor_file, autor] = [idref, pos]
			pos += 1
		if re.match(notas_M, idref):
			[notas_file, nota] = [idref, pos]
			pos += 1
	if autor and nota and autor > nota:
		lista_errores.append(listaerrores[76] % (autor_file, notas_file))


def validar_semantics():
	cover = 0
	elem = xml_opf.getElementsByTagName(met)
	for n in elem[0].childNodes:
		if n.nodeName == 'meta' and n.getAttribute('name') == 'cover':
			m = n.getAttribute('content')
			if m == cover_id and not cover:
				cover = 1
			else:
				msj = m + (' (repetido)' if m == cover_id else ' (nombre en lugar de id)' if m == img_base[0] else '')
				lista_errores.append(listaerrores[77] % msj)
				if corregir_errores:
					n.parentNode.removeChild(n)
					modif()
	if not cover:
		lista_errores.append(listaerrores[78] % img_base[0])
		if corregir_errores:
			# crea nodo
			x = xml_opf.createElement('meta')
			x.setAttribute('content', cover_id)
			x.setAttribute('name', 'cover')
			# añade nodo
			elem[0].appendChild(x)
			modif()


def validar_conceptos():
	cubierta = 0
	elem = xml_opf.getElementsByTagName('guide')
	if elem:
		for n in elem[0].childNodes:
			if n.nodeName == 'reference':
				htm = os.path.basename(n.getAttribute('href'))
				tipo = n.getAttribute('type')
				if htm == cubierta_file and tipo == 'cover' and not cubierta:
					cubierta = 1
				else:
					lista_errores.append(listaerrores[79] % (tipo + (' repetido' if htm == cubierta_file else ''), htm))
					if corregir_errores:
						if any('cuatro primeras secciones fijas' in item for item in lista_errores):
							lista_errores.append('  --- no corregido (primero resolver orden de secciones fijas)')
							continue
						n.parentNode.removeChild(n)
						modif()
	if not cubierta:
		lista_errores.append(listaerrores[80] % cubierta_file)
		if corregir_errores:
			if any('cuatro primeras secciones fijas' in item for item in lista_errores):
				lista_errores.append('  --- no corregido (primero resolver orden de secciones fijas)')
				return
			if not elem:
				x = xml_opf.createElement('guide')
				xml_opf.childNodes[0].appendChild(x)
				elem = xml_opf.getElementsByTagName('guide')
			x = xml_opf.createElement('reference')
			x.setAttribute('href', 'Text/' + cubierta_file)
			x.setAttribute('title', 'Cover')
			x.setAttribute('type', 'cover')
			elem[0].appendChild(x)
			modif()


def validar_lineas_sinopsis():
	pats = [r'(?i)Yo\s*por\s*bien\s*tengo\s*que\s*cosas\s*tan\s*se(ñ|nh?y?)aladas']
	pats.append(r'(?i)Y\s*a\s*este\s*prop[oó]sito\s*dice\s*Plinio\s*que\s*no\s*hay\s*libro')
	recurs(pats, sinopsis_file, psino, '...')


def validar_lineas_titulo():
	pats = [r'(?i)<p class="tsubtitulo">\s*(<strong class="sans">|)\s*Subt[ií]tulo\s*(</strong>|)\s*</p>']
	pats.append(r'(?i)<p class="tsubtitulo">\s*(<strong class="sans">|)\s*(Saga\s*:\s*Serie|Saga\s*:)\W*Volumen\s*(</strong>|)\s*</p>')
	pats.append(r'(?i)<p class="tfirma">\s*(<strong class="sans">|)\s*Editor[ae]?s?\b')
	recurs(pats, title_file, ptitu, '')


def validar_lineas_info():
	pats = [r'(?i)T[ií]tulo\s+original\s*:\s*((<em>|<i>|)\s*T[ií]tulo\s*(</em>|</i>|)|[—–-]*\s*</p>)']
	pats.append(r'(?i)a(ñ|nh?y?)o\s*de\s*1\.ª\s*publicaci[oó]n\s*en\s*idioma\s*original')
	pats.append(r'(?i)Ilustraciones\s*:\s*(Ilustrador[ae]?s?\b|[—–-]*\s*</p>)')
	pats.append(r'(?i)Dise(ñ|nh?y?)o\s*/\s*Retoque\s*de\s*(cubierta|portada)\s*:\s*(Dise(ñ|nh?y?)ador[ae]?s?\b|[—–-]*\s*</p>)')
	pats.append(r'(?i)Editor\s*digital\s*:\s*(Editor[ae]?s?\b|[—–-]*\s*</p>)')
	recurs(pats, info_file, pinfo, '')


def validar_lineas_dedicatoria():
	for dedica_file in lChapters:
		if dedic_h.match(dedica_file):
			pats = [r'<div class="dedicatoria">(&nbsp;|\s+|)</div>']
			pats.append(r'(?i)<p\b[^>]*>Suspir[oó]\s*entonces\s*m[ií]o\s*Cid,\s*de\s*pesadumbre\s*cargado')
			recurs(pats, dedica_file, dedica_file, '')


def validar_lineas_autor():
	for autor_file in lChapters:
		if autor_h.match(autor_file):
			pats = [r'NOMBRE\s*DEL\s*AUTOR']
			if version_epub != '1.0':
				pats.append(r'(?i)Integer\s*eu\s*leo\s*justo,\s*vel\s*sodales\s*arcu')
			recurs(pats, autor_file, autor_file, '...')


def validar_lineas_notas():
	for notas_file in lChapters:
		if re.match(notas_M, notas_file):
			if version_epub == '1.0':
				pats = [r'(?i)<p>\s*<a id="nota1">\s*</a>\s*<sup>\s*\[1\]\s*</sup>\s*Lorem\s*ipsum\s*dolor\s*sit\s*amet']
				pats.append(r'(?i)<p>\s*<a id="nota2">\s*</a>\s*<sup>\s*\[2\]\s*</sup>\s*Nulla\s*facilisi\.\s*Nulla\s*libero')
			else:
				pats = [r'(?i)<p id="nt1">\s*<sup>\s*\[1\]\s*</sup>\s*Lorem\s*ipsum\s*dolor\s*sit\s*amet']
				pats.append(r'(?i)<p id="nt2">\s*<sup>\s*\[2\]\s*</sup>\s*Nulla\s*facilisi\.\s*Nulla\s*libero')
			recurs(pats, notas_file, notas_file, '...')


def validar_puntos_titulo_info():
	pat = r'((?<!\b([Ll][Ii][Cc]|[Mm][Aa][Gg]|[Mm][Bb][Aa]|[Pp][Hh][Dd]|[Ss][Rr][Ll]))(?<!\b([DJS]r|M[DdGg]|[A-ZÀ-Þ][A-ZÀ-Þ]))(?<!\b[A-ZÀ-Þc])\.|,|;|:)(</\w+>|)</p>'
	with open(os.path.join(o_text, title_file), 'r', encoding='utf-8') as f:
		for i, line in enumerate(f, 1):
			for m in re.finditer(pat, line):
				lista_errores.append(listaerrores[82] % (ptitu, i, m.group(1)))

	pat = r'((?<!Carlos)(?<!\b([Ll][Ii][Cc]|[Mm][Aa][Gg]|[Mm][Bb][Aa]|[Pp][Hh][Dd]|[Ss][Rr][Ll]))(?<!\b([DJS]r|M[DdGg]|[A-ZÀ-Þ][A-ZÀ-Þ]))(?<!\b[A-ZÀ-Þc])\.|,|;|:)(</\w+>|)</p>'
	with open(os.path.join(o_text, info_file), 'r', encoding='utf-8') as f:
		for i, line in enumerate(f, 1):
			for m in re.finditer(pat, line):
				lista_errores.append(listaerrores[82] % (pinfo, i, m.group(1)))


def validar_errores_codigo():
	[aviso_set, error_set] = [set(), set()]
	head_css = [r'(?i)\bCDATA\b']
	head_css.append('<style type="text/css">')
	head_css.append(r'<meta[^>]*?\s*/\s*>')
	no_perm = [r'(<link[^"]*\bhref="\.\./Styles/(?!style\b)[^.]*\.css")']
	no_perm.append(r'(<body class="[^"]*\bsalto\w*\b[^"]*">)')
#	no_perm.append(r'(?i)(<(div|blockquote)\b(?! class="[^"]*\b(clear|ima?g))[^>]*>(&nbsp;|\s)*</\2>)')	# excepción con clases de imágenes
	no_perm.append(r'(</(h\d|p|li|td|d[dt]|div)>\s*(?!<!--|-->)\S.*$)')
	no_perm.append(r'(<[su]\b[^>]*>)')
	no_perm.append(r'\s(?!alt\b)(\b\w+="\s*")')
	no_perm.append(' (style="[^"]+")')
	no_perm.append(r'(?i) (class="[^"]*\b(calibre|mso|sgc)[^"]*")')
	no_perm.append(r'(<a [^>]*?\bhref="[^"]+"[^>]*>\s*<img)')
	no_perm.append(r'(<([ou]l|li) [^>]*?\b(start|value)="[^"]+")')
	no_perm.append(r'(?i)(<br\s*/\s*>\s*<(/h\d|/[a-z]+|br\s*/\s*)>)')
	no_perm.append(r'(\*+\s*NO\s*HAY\s*\*+)')
	no_perm.append(r'(\*+\s*DIVIDIR\s*DE\s*ACUERDO\s*A[^*]*\*+)')
	if version_epub < '1.2':
		no_perm.append('(<blockquote[^>]*>)')
	else:
		no_perm.append(r'(<blockquote [^>]*?\bclass="[^"]*\b(salto\w*|cita|banner|ilustra)\b[^"]*"[^>]*>)')
	malaraya = '[\u2010-\u2012\u2015\u203E\u2500\u2501]'	# hyphen-non-breaking hyphen-figure dash, horizontal bar, overline, box drawings
	malcarac = '[\u0080-\u009F\u0250-\u036F\u1AB0-\u1AFF\u1DC0-\u1DFF\u2000-\u200A\u200C-\u200F\u20D0-\u20FF\uFE20-\uFE2F]'
	# latin-1 supp(invisibles 0080-009F), ipa exts(0250-)spacing modifier letters-comb.diacritical mks(-036F), comb.diacritical mks extended(1AB0-1AFF)
	# comb.diacritical mks supp(1DC0-1DFF), general punctuation(invisibles 2000-200F, menos 200B=zero width space), comb.diacritical mks for symbols(20D0-20FF), comb.half mks(FE20-FE2F)
	inneces.append(r'(?i)(<!-+\s*(Start|End)Fragment\s*-+>)')
	inneces.append(r'<h\d [^>]*?\b(title="([^"]+)")[^>]*>\s*\2\s*</h\d>')
	inneces.append(r'(?i)<(?!abb)[a-z]+ [^>]*?\b(title="[^"]+")(?![^>]*>\s*<(img|sup)\b)')	# excepción de <abbr> (que sí lo requiere) y <sup>/<img> (que algunos editores usan)
	inneces.append(' (type="(?!text/css)[^"]+")')

	if re.search(r'<content src="Text.%s"\s*/\s*>\s*<navPoint' % title_file, txt_ncx):
		lista_errores.append(listaerrores[83])

	for htm in lChapters:
		if not os.path.isfile(os.path.join(o_text, htm)):
			error_set.add(listaerrores[96] % htm)
			continue

		# dentro del bucle para reiniciar listas especiales (evita repetir detecciones)
		[codigo_fijas, no_perm_fijas, obsolet_fijas] = [[], [], []]

		no_perm_notas = ['(<a>.*?</a>)']	# ancla vacía
		if version_epub == '1.0':
			no_perm_notas.append(r'(?i)(<a( id="[^"]+"| href="\.\./\w+/%s[^"]+")>.*?(?<!&lt;)\s*</a>(?!\s*<(a|sup)\b))' % notas_M)	# llamada incompleta
		else:
			no_perm_notas.append(r'(?i)(<a( id="[^"]+"| href="\.\./\w+/%s[^"]+")>.*?(?<!&lt;)\s*</a>(?!\s*<a\b))' % notas_M)	# llamada incompleta
		no_perm_notas.append(r'(<a href="\.\./[^"]+">.*?</a>\s*<a (href="\.\./|id=")[^"]+"[^>]+>)')	# href/id separados
		no_perm_notas.append(r'(<a id="[^"]+">.*?</a>\s*<a (href="\.\./|id=")[^"]+"[^>]+>)')	# id/href separados
		no_perm_notas.append(r'((<sup\b[^>]*>\s*|)<a (href="\.\./[^"]+" id="[^"]+"|id="[^"]+" href="\.\./[^"]+")>[^<]+?</a>(\s*</sup>|))')	# llamada sin sup interno
		no_perm_notas.append(r'(<sup\b[^>]*>(\s+\[[^][]+\]\s+|\s+\[[^][]+\]\s*|\s*\[[^][]+\]\s+|\s*\[\s+[^][]+\s+\]\s*|\s*\[\s+[^][]+\s*\]\s*|\s*\[\s*[^][]+\s+\]\s*)</sup>)')	# <sup> con espacios sobrantes
		no_perm_notas.append(r'(<sup\b[^>]*>([^]]*|[^[]*)</sup>)\s*</a>')	# <sup> vacío o corchetes incorrectos (llamada)

		try:
			if htm in [cubierta_file, sinopsis_file, title_file, info_file] or autor_h.match(htm) or re.match(notas_M, htm):
				if htm == cubierta_file:
					codigo_fijas.append(r'<body class="sinmargen"><h\d class="cubierta" title="%s"><img alt="[^"]*" src="\.\./Images/%s" /></h\d></body>' % (cubrt_M, img_base[0]))
				if htm == title_file:
					codigo_fijas.append(r'<body><p class="tlogo"><span><img alt="[^"]*" src="\.\./Images/%s" width="100%%" /></span></p>' % img_base[1])
				if htm == info_file:
					codigo_fijas.append('<body><div class="info">')
				if version_epub == '1.0':
					if htm == sinopsis_file:
						codigo_fijas.append('<body><p>&nbsp;</p><div class="sinopsis"><p>')
					if htm == info_file:
						codigo_fijas.append(r'<p class="centrado"><img alt="[^"]*" src="\.\./Images/%s" /></p></body>' % img_base[2])
					if autor_h.match(htm):
						codigo_fijas.append(r'<body><(h\d) class="oculto" title="%s\w*">.*?</\1><p class="autorimg"><img alt="[^"]*" height="\d+%%" src="\.\./Images/[^"]+" /></p><p class="asangre">' % autor_M)
				else:
					if htm == sinopsis_file:
						codigo_fijas.append('<body><div class="sinopsis"><p class="salto10">')
						no_perm_fijas.append(r'(<p\b[^>]*>(&nbsp;|\s)*</p>)')
					if htm == title_file:
						obsolet_fijas.append('(<(code|strong) class="(tfecha |)sans">)')
					if htm == info_file:
						codigo_fijas.append(r'<(div|p) class="vineta"><img alt="[^"]*" height="20%%" src="\.\./Images/%s" /></\1></body>' % img_base[2])
					if autor_h.match(htm):
						codigo_fijas.append(r'<body><(h\d) class="oculto" title="%s\w*">.*?</\1><(div|p) class="vineta"><img alt="[^"]*" height="\d+%%" src="\.\./Images/[^"]+" /></\2><div class="autor"><p>' % autor_M)
					obsolet_fijas.append(r'(?i)(<(div|p) class="centrado">\s*<img alt="[^"]*" src="\.\./Images/%s".+?</\2>)' % img_base[2])
					obsolet_fijas.append('(<(div|p) class="autorimg">)')
					if version_epub > '1.1':
						obsolet_fijas.append('(<div class="vineta">)')
					obsolet_fijas.append(r'\bclass="[^"]*\b(asangre)\b')
				no_perm_fijas.append('(?i)(sigil_not_in_toc|sigilNotInTOC|NotInTOC)')
				no_perm_fijas.append(r'(<p class="[^"]*\bsinopsis\b[^"]*">)')

				with open(os.path.join(o_text, htm), 'r', encoding='utf-8') as f:
					txt = f.read()
					# minimiza diferencias entre versiones y plataformas
					txt = re.sub('  +', ' ', txt)
					txt = re.sub(r'(<h\d\b[^>]*?) id="[^"]*"', r'\1', txt)
					txt = re.sub(r'(?s)\s*<!--.+?-->\s*', '', txt)
					txt = re.sub(r'\s*<br\s*/\s*>\s*', '<br />', txt)
					txt = re.sub(r'\s*/\s*>', ' />', txt)
					txt = re.sub(r'<(h\d|p|li|td|d[dt]|div|title)\b([^>]*?) />', r'<\1\2></\1>', txt)
					txt = re.sub(r'>\s*<', '><', txt)

				# jerarquía fijas
				m = re.findall(r'<h\d\b', txt)
				if m and m[0] != '<h1':
					error_set.add(listaerrores[84] % htm)

				# código base
				for pat in codigo_fijas:
					if not re.search(pat, txt):
						error_set.add(listaerrores[85] % htm)

				if autor_h.match(htm):
					no_perm_autor = [r'(<(div|p) class="(autorimg|vineta)">(?!<img ).+?</\2>)']	# línea de foto, sin imagen a continuación
					if version_epub == '1.0':
						no_perm_autor.append('<img alt="[^"]*" (height="(?!100%)[^"]+")')
					else:
						no_perm_autor.append('<img alt="[^"]*" (height="(?!40%)[^"]+")')
					no_perm_autor.append(r'(?i)(?:<div class="[^"]+">|\.(?:jpe?g|png|gif)" /></p>)<p\b[^>]*>(.?(<span class="nosep">|)(<(em|i|strong|b|small)\b[^>]*>.{,75}</\4|<span class="[^"]*(cursiva|negrita|versalita)[^"]*">.{,75}</span)>)')
					for pat in no_perm_autor:
						for m in re.finditer(pat, txt):
							error_set.add(listaerrores[87] % (htm, '', m.group(1).strip()))

				# recomprobación de página 'real' de notas
				if re.search('<div class="nota">', txt):
					if version_epub == '1.0':
						no_perm_notas.append(r'<p\b[^>]*>\s*<a id="[^"]+">\s*</a>\s*(<sup>([^]]*|[^[]*)</sup>)')	# <sup> vacío o corchetes incorrectos (nota)
						no_perm_notas.append(r'<p\b[^>]*>\s*<a id="[^"]+">\s*</a>\s*<sup>\s*\[[^][]+\]\s*(</sup>(?!</p>)\S+)')	# inicio de nota sin espacio
					else:
						no_perm_notas.append(r'<p [^>]*?\bid="[^"]+">\s*(<sup>([^]]*|[^[]*)</sup>)')
						no_perm_notas.append(r'<p [^>]*?\bid="[^"]+">\s*<sup>\s*\[[^][]+\]\s*(</sup>(?!</p>)\S+)')
						obsolet_fijas.append(r'(<p\b[^>]*>\s*<(a|sup) id="[^"]+">)')
					no_perm_notas.append(r'(\S+(?<!<p>)<a href)="../[^"]+">')	# retorno de nota sin espacio
					no_perm_notas.append(r'<a href="\.\./[^"]+">(.*?(?<!&lt;&lt;)</a>)\s*</(h\d|p|li|td|div|blockquote)>')	# retorno de nota sin caracteres aprobados (<<)
					no_perm_notas.append(r'&lt;\s*&lt;\s*(</a>\s*\S+\s*)</(h\d|p|li|td|div|blockquote)>')	# cierre 'sucio' de retorno de nota

			if htm != sinopsis_file:	# en ese caso, ya se incluyó > 1.1 (pecadito: si existen en sinopsis 1.0, no los detectará :O)
				no_perm_fijas.append(r'(<p\b[^>]*>(&nbsp;|\s)*</p>)')	# no <hx> o <li>, pueden necesitarse

			with open(os.path.join(o_text, htm), 'r', encoding='utf-8') as f:
				for i, line in enumerate(f, 1):
					for pat in obsolet_fijas:
						for m in re.finditer(pat, line):
							error_set.add(listaerrores[86] % (htm, ' línea ' + texto(i).zfill(4), m.group(1)))
					for pat in (no_perm_fijas + no_perm):
						for m in re.finditer(pat, line):
							error_set.add(listaerrores[87] % (htm, ' línea ' + texto(i).zfill(4), m.group(1)))
					for pat in no_perm_notas:
						for m in re.finditer(pat, line):
							error_set.add(listaerrores[88] % (htm, texto(i).zfill(4), m.group(1)))
					for pat in head_css:
						for m in re.finditer(pat, line):
							error_set.add(listaerrores[89] % (htm, texto(i).zfill(4), m.group(0)))
					for m in re.finditer(malaraya, line):
						error_set.add(listaerrores[90] % (htm, ord(m.group(0))))
					for m in re.finditer(malcarac, line):
						error_set.add(listaerrores[91] % (htm, ord(m.group(0))))
					for pat in inneces:
						for m in re.finditer(pat, line):
							aviso_set.add(listaavisos[1] % (htm, texto(i).zfill(4), m.group(1)))

		except IOError:
			error_set.add(listaerrores[92] % htm)

	# clases mal definidas
	no_perm_css = [r'[{;]\s*([^:;]+;)']
	no_perm_css.append(r'(?i):\s*(\d+\s+(em\b|mm\b|p[tx]\b|%))')
	# parámetros erróneos
	no_perm_css.append(r'\b(font-family\s*:\s*(?!serif|sans-serif|monospace|inherit|"\w)\w+)\b')
	no_perm_css.append(r'\bfont-family\s*:[^;}]*\b(cursive|fantasy|mono|sans(?!-serif))\b')
	no_perm_css.append(r'\b(font-style\s*:\s*(?!normal|italic|inherit)\w+)\b')
	no_perm_css.append(r'\b(font-weight\s*:\s*(?!normal|bold|inherit)\w+)\b')
	no_perm_css.append(r'\b(text-align\s*:\s*(?!left|right|center|justify|inherit)\w+)\b')
	# código incompatible
	no_perm_css.append(r'\b(background-(image|repeat)\s*:\s*[^;}]*)[;}]')
	no_perm_css.append(r'\b(font-variant\s*:\s*[^;}]*)[;}]')
	no_perm_css.append(r'\b((letter|word)-spacing\s*:\s*[^;}]*)[;}]')
	no_perm_css.append(r'\b(text-transform\s*:\s*[^;}]*)[;}]')
	no_perm_css.append(r'(:(nth-|)(first|last|nth|of)-\w+\b)')
	no_perm_css.append(r'(:(before|after|link|visited|hover|active|focus|lang|selection))\b')
	# ignorado
	inneces_css = [r'[^.\d]0+(em\b|mm\b|p[tx]\b|%)']
	inneces_css.append(r'(?i)(\.0+)(?!\s*ePubLibre)')
	inneces_css.append(r':\s*(00+)(?!\s*%)')
	inneces_css.append(r'\b((font-style|font-weight|font-family|text-align)\s*:\s*inherit)\b')
	inneces_css.append(r'(!important)\b')
	try:
		with open(stylecss, 'r', encoding='utf-8') as f:
			for i, line in enumerate(f, 1):
				for pat in no_perm_css:
					for m in re.finditer(pat, line):
						error_set.add(listaerrores[87] % ('la CSS', ' línea ' + texto(i).zfill(3), m.group(1).strip()))
				for pat in inneces_css:
					for m in re.finditer(pat, line):
						aviso_set.add(listaavisos[1] % ('la CSS', texto(i).zfill(3), m.group(1)))
	except IOError:
		pass

	no_perm_opf = [r'(?i)<\w+ [^>]*?\bname="calibre:(?!series)[^>]*>']
	no_perm_opf.append(r'(?i)<meta [^>]*?\bname="(?!calibre:|cover|Sigil version)[^>]*>')
	no_perm_opf.append(r'<dc:source\b[^>]*>.+?</dc:source>')
	incompletas_opf = [r'<\S+ \S+="">[^<]*</\S+>']
	incompletas_opf.append(r'<dc:\w+ opf:\w+="[^"]*"\s*/\s*>')
	incompletas_opf.append(r'<\S+ (?!name="calibre|opf:file-as)\S+="" (?!name="calibre|opf:file-as)\S+="[^"]*"\s*/\s*>')
	incompletas_opf.append(r'<\S+ (?!name="calibre|opf:file-as)\S+="[^"]*" (?!name="calibre|opf:file-as)\S+=""\s*/\s*>')
	inneces_opf = [r'<dc:date [^>]*?\bopf:event="creation".+?</dc:date>']
	for pat in no_perm_opf:
		for m in re.finditer(pat, txt_opf):
			error_set.add(listaerrores[93] % m.group(0))
	for pat in incompletas_opf:
		for m in re.finditer(pat, txt_opf):
			error_set.add(listaerrores[94] % m.group(0))
	for pat in inneces_opf:
		for m in re.finditer(pat, txt_opf):
			error_set.add(listaerrores[95] % m.group(0))

	lista_avisos.extend(sorted(aviso_set))
	lista_errores.extend(sorted(error_set))


def validar_archivos_basura():
	for f in locate('*.*', os.path.join(tempdir, dir)):
		ff = os.path.basename(f)
		if ff not in arch_basura + ['content.opf'] and not re.search('<item href=".*?' + ff, txt_opf):
			lista_errores.append(listaerrores[97] % ff)

	for file in arch_basura:
		for f in locate(file, tempdir):
			if os.path.isfile(f):
				lista_errores.append(listaerrores[98] % file)
				if corregir_errores:
					modif()



# AQUÍ COMIENZA TODO
tempdir = ''
lista_archivos = []	# lista vacía donde se añadirán los archivos

if len(sys.argv) == 1:
	try:
		# interfaz gráfica para seleccionar archivo
		root = Tk()
		root.withdraw()	# no necesita un GUI completo, así que no abre la ventana principal
		filename = fdialog()	# muestra diálogo y devuelve nombre de archivo seleccionado
		lista_archivos = [file for file in root.tk.splitlist(filename)]	# corrige bug de cuadro de diálogo de apertura de ficheros de Tk
		if lista_archivos:
			(sdir, sfile) = os.path.split(lista_archivos[0])	# extrae directorio para la descompresión de nombre de primer archivo de la lista
			tempdir = os.path.join(sdir, 'tmp_ePV')	# directorio temporal para descomprimir ePub
	except:
		print('\nTu sistema no tiene tkinter. Usa nombre del aporte en la línea de comandos')
		print('IMPOSIBLE CONTINUAR\n\nPresiona INTRO para salir...')
		sys.exit(1)

elif len(sys.argv) >= 2:
	(sdir, sfile) = os.path.split(sys.argv[1])	# extrae la ruta del directorio temporal del primer argumento enviado
	if not sdir:
		sdir = os.curdir
	tempdir = os.path.join(sdir, 'tmp_ePV')	# directorio temporal para descomprimir el ePub
	for arg in sys.argv[1:]:	# revisa toda la lista de argumentos
		if os.path.isdir(arg):	# si el argumento es un directorio, se añaden todos los nombres de los epub que contiene
			for path, dirs, files in os.walk(os.path.abspath(arg)):
				for filename in fnmatch.filter(files, '*.epub'):
					lista_archivos.append(os.path.join(path, filename))
		elif os.path.isfile(arg):	# si el argumento es un archivo, se añade a la lista
			lista_archivos.append(arg)


# borra directorio temporal, por si quedase de una ejecución previa
if os.path.exists(tempdir):
	shutil.rmtree(tempdir, ignore_errors=True)


try:
	lista_archivos.sort(key=str.lower)
except:
	try:
		lista_archivos.sort(key=unicode.lower)
	except:
		pass


# BUCLE PRINCIPAL
# contadores a cero
epubs_correctos = epubs_avisos = epubs_erroneos = 0

print('\nePLValidator v%s manual (Python v%s)' % (vversion, sys.version[:6].strip()))

if any('.epub' in normaliza(item).lower() for item in lista_archivos):
	for filename in lista_archivos:
		epub = os.path.basename(filename)
		if not normaliza(epub).lower().endswith('.epub'):
			continue

		# limpia variables
		cubierta_file = sinopsis_file = title_file = info_file = opf_file = toc_file = xml_opf = xml_ncx = meta_idioma = ''
		[lManifest, lChapters, lFonts, lSpine, lista_errores, lista_avisos, img_base, inneces] = [[], [], [], [], [], [], [], []]	# listas vacías e independientes
		epub_modificado = False
		version_epub = ''	# vacío, para evitar falsos positivos

		print('\n-----------------------------------------------------------')
		print("Comprobando: '%s'" % normaliza(epub).replace('.epub', ''))

		try:
			zipf = zipfile.ZipFile(filename, 'r')
			os.makedirs(tempdir)
			zipf.extractall(tempdir)	# descomprime archivo
			zipf.close()
		except IOError:
			print('\nError al abrir archivo comprimido' + impos)
			continue

		try:
			with open(os.path.join(tempdir, 'META-INF', 'container.xml'), 'rb') as f:	# ruta de content.opf en container.xml
				xmldoc = parse(f)
			elem = xmldoc.getElementsByTagName('rootfile')
			attr = elem[0].getAttribute('full-path')
			dir = os.path.dirname(attr)
			o_text = os.path.join(tempdir, dir, 'Text')
			o_images = os.path.join(tempdir, dir, 'Images')
			stylecss = os.path.join(tempdir, dir, 'Styles', 'style.css')
			ibooks_f = os.path.join(tempdir, 'META-INF', 'com.apple.ibooks.display-options.xml')

			opf_file = os.path.join(tempdir, attr)

			with open(opf_file, 'rb') as f:	# abre content.opf
				xml_opf = parse(f)	# parsea y deja en memoria, ya que la mayoría de comprobaciones lo necesitan
			with open(opf_file, 'r', encoding='utf-8') as f:
				txt_opf = f.read()	# lo almacena en un archivo textual
				txt_opf = unquote(txt_opf)	# cambia entidades html por caracteres

			if not xml_opf.getElementsByTagName(met):
				print("\ncontent.opf defectuoso (sección 'metadata' no encontrada)" + grave)
				continue

			lManifest = xml_opf.getElementsByTagName('manifest')	# obtiene manifiesto y registra capítulos e imágenes
			if not lManifest:
				print("\ncontent.opf defectuoso (sección 'manifest' no encontrada)" + grave)
				continue
			for n in lManifest[0].childNodes:
				if n.nodeName == 'item':
					node_type = n.getAttribute('media-type')
					if node_type == 'application/xhtml+xml':
						lChapters.append(unquote(os.path.basename(n.getAttribute('href'))))	# lista con nombres de capítulos
					elif node_type.endswith(('opentype', 'x-font-ttf', 'x-font-truetype-collection')):
						lFonts.append(unquote(os.path.basename(n.getAttribute('href'))))	# lista con fuentes del ePub

			lSpine = xml_opf.getElementsByTagName('itemref')	# get spine
			if not lSpine:
				print("\ncontent.opf defectuoso (sección 'spine' no encontrada)" + grave)
				continue

			toc_file = os.path.join(tempdir, dir, 'toc.ncx')
			with open(toc_file, 'rb') as f:	# abre toc.ncx
				xml_ncx = parse(f)	# parsea y deja en memoria
			with open(toc_file, 'r', encoding='utf-8') as f:
				txt_ncx = f.read()	# lo almacena en un archivo textual

			if not xml_ncx.getElementsByTagName('meta'):
				print("\ntoc.ncx defectuosa (sección 'meta' no encontrada)" + grave)
				continue

			# secciones fijas
			cubierta_file = get_file_name('cubierta.xhtml', 0)
			sinopsis_file = get_file_name('sinopsis.xhtml', 1)
			title_file = get_file_name('titulo.xhtml', 2)
			info_file = get_file_name('info.xhtml', 3)
			# imágenes fijas
			m = busca(r'(?i)/Images/([^.]+\.jpe?g)"', cubierta_file)
			img_base.append(m if m else 'cover.jpg')
			cover_id = 'cover.jpg'
			for n in lManifest[0].childNodes:
				if n.nodeName == 'item' and os.path.basename(n.getAttribute('href')) == img_base[0]:
					cover_id = n.getAttribute('id')
			m = busca(r'(?i)/Images/([^.]+\.png)"', title_file)
			img_base.append(m if m else 'EPL_logo.png')
			m = busca(r'(?i)/Images/([^.]+\.png)"', info_file)
			img_base.append(m if m else 'ex_libris.png')
			#if img_base != ['cover.jpg', 'EPL_logo.png', 'ex_libris.png']:
				#lista_avisos.append(listaavisos[7] % texto(img_base))


			# aquí irán las comprobaciones, una a una
			version_epub = busca(r'<p\b[^>]*>ePub base r(\d\.\d)(<br\s*/\s*>|)</p>', info_file)
			if not version_epub:
				print('\nePub base no detectado en %s' % pinfo + perror + impos)
				continue
			elif version_epub > version_base:
				print('\nePub base (%s) superior al actual en %s' % (version_epub, pinfo) + impos)
				continue

			validar_broken_opf()
			validar_metadatos()
			validar_bookid()
			validar_toc()
			validar_css()
			validar_generos_y_subgeneros()
			validar_titulo()
			validar_autor()
			validar_traductor()
			validar_colaboradores()
			validar_file_size()
			validar_imgs_base()
			validar_img_autor()
			validar_jpeg_progresivo()
			validar_saga()
			validar_revision()
			validar_anyo_publicacion()
			validar_fecha_modificacion()
			validar_editor_en_titulo_e_info()
			validar_nombre_archivo()
			validar_nombre_archivos_internos()
			validar_formato_nombre_archivo()
			validar_fuentes_ibooks()
			validar_orden_fijas()
			validar_orden_autor_notas()
			validar_semantics()
			validar_conceptos()
			validar_lineas_sinopsis()
			validar_lineas_titulo()
			validar_lineas_info()
			validar_lineas_dedicatoria()
			validar_lineas_autor()
			validar_lineas_notas()
			validar_puntos_titulo_info()
			validar_errores_codigo()
			validar_archivos_basura()

			if version_epub < version_base:
				lista_avisos.append(listaavisos[6] % version_base)	# versión anterior del ePub base

			# corrige errores, genera nuevo ePub
			if epub_modificado:
				try:
					with open(opf_file, 'w', encoding='utf-8') as f:
						f.write(prettify(xml_opf))

					zipf = zipfile.ZipFile(filename, 'w')
					zipf.write(os.path.join(tempdir, 'mimetype'), 'mimetype', zipfile.ZIP_STORED)
					for item in os.listdir(tempdir):
						if os.path.isdir(os.path.join(tempdir, item)):
							recursive_zip(zipf, os.path.join(tempdir, item), item)
					zipf.close()
				except IOError:
					print('\nError al guardar epub corregido' + impos)
					continue
				finally:
					shutil.rmtree(tempdir, ignore_errors=True)

			# imprime los errores
			print('ePub base', version_epub)
			if lista_errores:
				print('')
				#lista_errores = list(set(lista_errores))	# debug (no usar en versión 'auto')
				#lista_errores.sort()	# debug (bis)
				imprime(lista_errores)
				epubs_erroneos += 1
			if lista_avisos:
				print('\nDETALLES:')
				imprime(lista_avisos)
				if not lista_errores:
					epubs_avisos += 1
			if not (lista_errores + lista_avisos):
				print('\nTodo parece OK!')
				epubs_correctos += 1

		except Exception as ex:
			print('\nError en línea {0} ({1})'.format(sys.exc_info()[-1].tb_lineno, ex) + impos)

		finally:
			shutil.rmtree(tempdir, ignore_errors=True)


	# muestra resumen de resultados
	print('\n\nTotal epubs correctos:', epubs_correctos)
	if epubs_avisos:
		print('Total epubs con avisos:', epubs_avisos)
	print('Total epubs con errores:', epubs_erroneos)


else:
	print('\nNada que hacer. Me voy a tomar un café :)')


input ('\nPresiona INTRO para finalizar...')
