# -*- coding: utf-8 -*-
import json

def s(id_, nom, bloc, ambit, tram_base=None, star=False):
    return {
        "id": id_, "nom": nom, "bloc": bloc, "ambit": ambit,
        "tram_base": tram_base, "font_star": star,
        "estat": "pendent",
        "resum": None, "competencia": None,
        "normativa_mare": [],
        "checklist": [],
        "data_actualitzacio": None
    }

def item(pregunta, llei_nom, explicacio, llindar_label,
         article="", pob_min=None, pob_min_strict=True, pob_max=None, pob_max_strict=True):
    return {
        "pregunta": pregunta,
        "llei_nom": llei_nom, "article": article,
        "explicacio": explicacio, "llindar_label": llindar_label,
        "pob_min": pob_min, "pob_min_strict": pob_min_strict,
        "pob_max": pob_max, "pob_max_strict": pob_max_strict,
    }

serveis = []

# --- SERVEIS DE PRESTACIÓ OBLIGATÒRIA ---
serveis += [
    s("enllumenat-public", "Enllumenat públic", "obligatori", "Urbanisme, via pública i medi ambient"),
    s("cementiri", "Cementiri", "obligatori", "Urbanisme, via pública i medi ambient"),
    s("recollida-residus", "Recollida de residus", "obligatori", "Urbanisme, via pública i medi ambient"),
    s("neteja-viaria", "Neteja viària", "obligatori", "Urbanisme, via pública i medi ambient"),
    s("abastament-aigua", "Abastament domiciliari d'aigua potable", "obligatori", "Urbanisme, via pública i medi ambient"),
    s("clavegueram", "Clavegueram / evacuació d'aigües residuals", "obligatori", "Urbanisme, via pública i medi ambient"),
    s("acces-nuclis", "Accés als nuclis de població", "obligatori", "Urbanisme, via pública i medi ambient"),
    s("pavimentacio-vies", "Pavimentació i conservació de les vies públiques", "obligatori", "Urbanisme, via pública i medi ambient"),
    s("control-aliments", "Control d'aliments i begudes", "obligatori", "Salut", star=True),
]
serveis += [
    s("parc-public", "Parc públic", "obligatori", "Urbanisme, via pública i medi ambient", tram_base=5000),
    s("biblioteca-publica", "Biblioteca pública", "obligatori", "Cultura", tram_base=5000),
    s("tractament-residus", "Tractament de residus", "obligatori", "Urbanisme, via pública i medi ambient", tram_base=5000),
    s("mercat", "Mercat", "obligatori", "Comerç, ocupació i promoció econòmica", tram_base=5000, star=True),
]
serveis += [
    s("proteccio-civil", "Protecció civil", "obligatori", "Seguretat i protecció", tram_base=20000),
    s("serveis-socials-avaluacio", "Serveis socials: avaluació, informació i atenció immediata en situacions de risc d'exclusió", "obligatori", "Serveis socials", tram_base=20000),
    s("prevencio-incendis", "Prevenció i extinció d'incendis", "obligatori", "Seguretat i protecció", tram_base=20000),
    s("installacions-esportives", "Instal·lacions esportives d'ús públic", "obligatori", "Esports i lleure", tram_base=20000),
]
serveis += [
    s("lectura-publica-descentralitzada", "Servei de lectura pública descentralitzat", "obligatori", "Cultura", tram_base=30000, star=True),
]
serveis += [
    s("transport-collectiu-urba", "Transport col·lectiu urbà de viatgers", "obligatori", "Mobilitat i transport", tram_base=50000),
    s("medi-ambient-urba", "Medi ambient urbà / Protecció del medi", "obligatori", "Urbanisme, via pública i medi ambient", tram_base=50000),
    s("transport-adaptat", "Transport adaptat", "obligatori", "Mobilitat i transport", tram_base=50000, star=True),
]

# --- SERVEIS I RESPONSABILITATS D'INTERÈS MUNICIPAL ---
im = [
    ("casal-gent-gran", "Casal de gent gran", "Serveis socials"),
    ("centres-dia-residencies", "Centres de dia i residències", "Serveis socials"),
    ("mediacio-ciutadana", "Mediació ciutadana", "Serveis socials"),
    ("sad", "Servei d'Ajuda a Domicili", "Serveis socials"),
    ("teleassistencia", "Teleassistència", "Serveis socials"),
    ("centres-ensenyament", "Centres d'ensenyaments i formació", "Educació i joventut"),
    ("espai-jove", "Espai jove", "Educació i joventut"),
    ("punt-informacio-juvenil", "Punt d'informació juvenil", "Educació i joventut"),
    ("informacio-orientacio-dona", "Informació i orientació de la dona", "Serveis socials"),
    ("piscina-municipal", "Piscina municipal", "Esports i lleure"),
    ("museu", "Museu", "Cultura"),
    ("arts-esceniques", "Promoció de les arts escèniques", "Cultura"),
    ("mobilitat", "Mobilitat (sostenible, escolar, col·lectius, interurbà)", "Mobilitat i transport"),
    ("atencio-ciutadana", "Atenció ciutadana", "Organització interna i transparència"),
    ("omic", "OMIC", "Comerç, ocupació i promoció econòmica"),
    ("suport-empresa", "Suport a l'empresa", "Comerç, ocupació i promoció econòmica"),
    ("mercat-treball", "Mercat de treball (orientació, inserció i formació ocupacional)", "Comerç, ocupació i promoció econòmica"),
    ("fires", "Fires", "Comerç, ocupació i promoció econòmica"),
    ("comerc", "Comerç", "Comerç, ocupació i promoció econòmica"),
    ("turisme", "Turisme", "Comerç, ocupació i promoció econòmica"),
    ("oficina-local-habitatge", "Oficina local d'habitatge", "Habitatge"),
    ("policia-vigilancia-local", "Policia / vigilància local", "Seguretat i protecció"),
    ("promocio-salut", "Promoció de la salut", "Salut"),
    ("proteccio-salut", "Protecció de la salut", "Salut"),
    ("transparencia", "Obligacions en matèria de transparència", "Organització interna i transparència"),
    ("fhn", "Funcionaris d'habilitació nacional", "Organització interna i transparència"),
    ("recursos-humans", "Recursos humans", "Organització interna i transparència"),
]
for id_, nom, ambit in im:
    serveis.append(s(id_, nom, "interes_municipal", ambit))

# --- FITXES VALIDADES ---
LLEI_LBRL = "Llei 7/1985, de 2 d'abril, reguladora de les bases del règim local"
DECRET_MORTUORIA = "Decret 297/1997, de 25 de novembre, pel qual s'aprova el Reglament de policia sanitària mortuòria de Catalunya"
LLEI_FUNERARIS = "Llei 2/1997, de 3 d'abril, sobre serveis funeraris"
LLEI_BIBLIOTECARI = "Llei 4/1993, de 18 de març, del sistema bibliotecari de Catalunya"
DECRET_LEG_2003 = "Decret legislatiu 2/2003, de 28 d'abril, pel qual s'aprova el Text refós de la Llei municipal i de règim local de Catalunya"
MAPA_LECTURA = "Mapa de la Lectura Pública de Catalunya"

for it in serveis:
    if it["id"] == "cementiri":
        it.update({
            "estat": "validat",
            "resum": "Cal garantir un servei de cementiri, propi o compartit amb altres municipis, que compleixi les condicions sanitàries i funcionals mínimes.",
            "competencia": "propia",
            "data_actualitzacio": "2026-07-01",
            "normativa_mare": [LLEI_LBRL, DECRET_LEG_2003],
            "checklist": [
                item("El municipi garanteix el servei de cementiri, propi o associat?",
                     LLEI_LBRL,
                     "El cementiri és un servei mínim obligatori que han de prestar tots els municipis, individualment o associats.",
                     "Tots els municipis", article="art. 26.1.a"),
                item("El cementiri disposa dels elements mínims exigibles (sepultures suficients, dipòsit de cadàvers, ossera general, instal·lacions d'aigua, serveis higiènics i llibre-registre d'inhumacions i exhumacions)?",
                     DECRET_MORTUORIA,
                     "El cementiri ha de disposar, com a mínim, de sepultures suficients, dipòsit de cadàvers, ossera general, instal·lacions d'aigua, serveis higiènics i llibre-registre d'inhumacions i exhumacions.",
                     "Tots els municipis", article="art. 46"),
                item("Està garantit l'accés als serveis funeraris al municipi?",
                     LLEI_FUNERARIS,
                     "Els serveis funeraris són un servei essencial d'interès general que l'ajuntament ha de garantir a tota la col·lectivitat local.",
                     "Tots els municipis", article="art. 1"),
                item("Se sap qui presta els serveis funeraris i sota quin règim d'autorització?",
                     LLEI_FUNERARIS,
                     "Els serveis funeraris poden ser prestats per l'Administració, empreses públiques o empreses privades, sempre sotmesos a control, policia i autorització.",
                     "Tots els municipis", article="art. 1"),
            ],
        })
    if it["id"] == "biblioteca-publica":
        it.update({
            "estat": "validat",
            "resum": "Cal garantir l'accés de la ciutadania a la lectura pública, amb biblioteca pròpia o amb el suport d'altres administracions.",
            "competencia": "propia",
            "data_actualitzacio": "2026-07-01",
            "normativa_mare": [LLEI_LBRL, DECRET_LEG_2003],
            "checklist": [
                item("El municipi coordina i promou la lectura pública al seu terme municipal?",
                     LLEI_BIBLIOTECARI,
                     "La llei atribueix a tots els municipis la funció de coordinar i promoure la lectura pública, més enllà de si disposen o no d'una biblioteca pròpia.",
                     "Tots els municipis"),
                item("Si disposa d'una biblioteca de titularitat municipal, està creada, regulada, organitzada i gestionada d'acord amb la llei, el reglament i el Mapa de la Lectura Pública?",
                     LLEI_BIBLIOTECARI,
                     "Els municipis han de crear, regular, organitzar i gestionar les biblioteques de titularitat municipal d'acord amb la llei, el reglament i el Mapa de la Lectura Pública.",
                     "Tots els municipis"),
                item("Quin suport comarcal rep el municipi per a la prestació del servei de lectura pública?",
                     LLEI_BIBLIOTECARI,
                     "Els municipis de menys de 5.000 habitants han de rebre el suport de la comarca respectiva en la prestació del servei de lectura pública.",
                     "Menys de 5.000 hab.", pob_max=5000, pob_max_strict=True),
                item("El municipi està atès per un servei de biblioteca filial, d'acord amb el Mapa de la Lectura Pública?",
                     MAPA_LECTURA,
                     "El Mapa de la Lectura Pública preveu que els municipis d'aquesta franja siguin atesos per un servei de biblioteca filial.",
                     "Entre 3.000 i 5.000 hab.", pob_min=3000, pob_min_strict=False, pob_max=5000, pob_max_strict=True),
                item("El servei es presta mitjançant biblioteca municipal pròpia o mitjançant una altra biblioteca del Sistema de Lectura Pública amb conveni?",
                     LLEI_BIBLIOTECARI,
                     "Els municipis de 5.000 habitants o més han de prestar el servei de biblioteca local, amb biblioteca pròpia o mitjançant conveni amb una altra biblioteca del Sistema de Lectura Pública.",
                     "5.000 hab. o més", pob_min=5000, pob_min_strict=False),
                item("El servei de lectura pública es presta de manera descentralitzada, d'acord amb el Mapa de la Lectura Pública?",
                     DECRET_LEG_2003,
                     "Els municipis de més de 30.000 habitants han de prestar el servei de lectura pública de manera descentralitzada, d'acord amb el Mapa de la Lectura Pública.",
                     "Més de 30.000 hab.", article="art. 66.3", pob_min=30000, pob_min_strict=True),
            ],
        })

with open("serveis.json", "w", encoding="utf-8") as f:
    json.dump(serveis, f, ensure_ascii=False)

print(len(serveis), "serveis generats")
print(sum(1 for x in serveis if x["bloc"] == "obligatori"), "obligatoris")
print(sum(1 for x in serveis if x["bloc"] == "interes_municipal"), "interès municipal")
print(sum(1 for x in serveis if x["estat"] == "validat"), "validats")
