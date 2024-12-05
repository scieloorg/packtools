import unittest

from packtools.sps.utils.xml_utils import get_xml_tree
from packtools.sps.validation.article_lang import ArticleLangValidation


class ArticleLangTest(unittest.TestCase):
    def test_validate_article_lang_without_title(self):
        self.maxDiff = None
        xml_str = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" dtd-version="1.1" 
            specific-use="sps-1.9" xml:lang="pt">
            <front>
                <article-meta>
                    <abstract><p>Resumo em português</p></abstract>
                    <kwd-group xml:lang="pt">
                        <kwd>Palavra chave 1</kwd>
                        <kwd>Palavra chave 2</kwd>
                    </kwd-group>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)

        obtained = list(ArticleLangValidation(xml_tree).validate_article_lang())

        expected = [
            {
                'title': 'title element lang attribute',
                'parent': None,
                'parent_article_type': None,
                'parent_id': None,
                'parent_lang': 'pt',
                'item': 'title',
                'sub_item': None,
                'validation_type': 'match',
                'response': 'ERROR',
                'expected_value': 'title in pt',
                'got_value': None,
                'message': 'Got None, expected title in pt',
                'advice': 'Provide title in the pt language',
                'data': None
            }
        ]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_sub_article_lang_without_title(self):
        self.maxDiff = None
        xml_str = """
        <article  xml:lang="pt">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Título em português</article-title>
                    </title-group>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="TRen" xml:lang="en">
                <front-stub>
                    <abstract xml:lang="en">
                        Abstract in english
                    </abstract>
                    <kwd-group xml:lang="en">
                        <kwd>Keyword 1</kwd>
                        <kwd>Keyword 2</kwd>
                    </kwd-group>
                </front-stub>
            </sub-article>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)

        obtained = list(ArticleLangValidation(xml_tree).validate_article_lang())

        expected = [
            {
                'title': 'title element lang attribute',
                'parent': None,
                'parent_article_type': None,
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'title',
                'sub_item': None,
                'validation_type': 'match',
                'response': 'ERROR',
                'expected_value': 'title in en',
                'got_value': None,
                'message': 'Got None, expected title in en',
                'advice': 'Provide title in the en language',
                'data': None
            }
        ]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_article_lang_without_abstract(self):
        self.maxDiff = None
        xml_str = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" dtd-version="1.1"
            specific-use="sps-1.9" xml:lang="pt">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Título em português</article-title>
                    </title-group>
                    <kwd-group xml:lang="pt">
                        <kwd>Palavra chave 1</kwd>
                        <kwd>Palavra chave 2</kwd>
                    </kwd-group>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)

        obtained = list(ArticleLangValidation(xml_tree).validate_article_lang())

        expected = [
            {
                'title': 'abstract element lang attribute',
                'parent': None,
                'parent_article_type': None,
                'parent_id': None,
                'parent_lang': 'pt',
                'item': 'abstract',
                'sub_item': None,
                'validation_type': 'match',
                'response': 'ERROR',
                'expected_value': 'abstract in pt',
                'got_value': None,
                'message': 'Got None, expected abstract in pt',
                'advice': 'Provide abstract in the pt language',
                'data': None
            }
        ]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_sub_article_lang_without_abstract(self):
        self.maxDiff = None
        xml_str = """
        <article  xml:lang="pt">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Título em português</article-title>
                    </title-group>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="TRen" xml:lang="en">
                <front-stub>
                    <title-group>
                        <article-title xml:lang="en">Title in english</article-title>
                    </title-group>
                    <kwd-group xml:lang="en">
                        <kwd>Keyword 1</kwd>
                        <kwd>Keyword 2</kwd>
                    </kwd-group>
                </front-stub>
            </sub-article>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)

        obtained = list(ArticleLangValidation(xml_tree).validate_article_lang())

        expected = [
            {
                'title': 'abstract element lang attribute',
                'parent': None,
                'parent_article_type': None,
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'abstract',
                'sub_item': None,
                'validation_type': 'match',
                'response': 'ERROR',
                'expected_value': 'abstract in en',
                'got_value': None,
                'message': 'Got None, expected abstract in en',
                'advice': 'Provide abstract in the en language',
                'data': None
            }
        ]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_article_lang_without_kwd_group(self):
        self.maxDiff = None
        xml_str = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" dtd-version="1.1"
            specific-use="sps-1.9" xml:lang="pt">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Título em português</article-title>
                    </title-group>
                    <abstract><p>Resumo em português</p></abstract>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)

        obtained = list(ArticleLangValidation(xml_tree).validate_article_lang())

        expected = [
            {
                'title': 'kwd-group element lang attribute',
                'parent': None,
                'parent_article_type': None,
                'parent_id': None,
                'parent_lang': 'pt',
                'item': 'kwd-group',
                'sub_item': None,
                'validation_type': 'match',
                'response': 'ERROR',
                'expected_value': 'kwd-group in pt',
                'got_value': None,
                'message': 'Got None, expected kwd-group in pt',
                'advice': 'Provide kwd-group in the pt language',
                'data': None
            }
        ]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_sub_article_lang_without_kwd_group(self):
        self.maxDiff = None
        xml_str = """
        <article  xml:lang="pt">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Título em português</article-title>
                    </title-group>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="TRen" xml:lang="en">
                <front-stub>
                    <title-group>
                        <article-title xml:lang="en">Title in english</article-title>
                    </title-group>
                    <abstract xml:lang="en">
                        Abstract in english
                    </abstract>
                </front-stub>
            </sub-article>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)

        obtained = list(ArticleLangValidation(xml_tree).validate_article_lang())

        expected = [
            {
                'title': 'kwd-group element lang attribute',
                'parent': None,
                'parent_article_type': None,
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'kwd-group',
                'sub_item': None,
                'validation_type': 'match',
                'response': 'ERROR',
                'expected_value': 'kwd-group in en',
                'got_value': None,
                'message': 'Got None, expected kwd-group in en',
                'advice': 'Provide kwd-group in the en language',
                'data': None
            }
        ]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_article_lang_with_title_only(self):
        self.maxDiff = None
        xml_str = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" dtd-version="1.1"
            specific-use="sps-1.9" xml:lang="pt">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Título em português</article-title>
                        <trans-title-group xml:lang="en">
                            <trans-title>Title in english</trans-title>
                        </trans-title-group>
                    </title-group>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)

        obtained = ArticleLangValidation(xml_tree).validate_article_lang()

        self.assertEqual(list(obtained), [])

    def test_validate_sub_article_lang_with_title_only(self):
        self.maxDiff = None
        xml_str = """
        <article  xml:lang="pt">
            <front>

            </front>
            <sub-article article-type="translation" id="TRen" xml:lang="en">
                <front-stub>
                    <title-group>
                        <article-title xml:lang="en">Title in english</article-title>
                    </title-group>
                </front-stub>
            </sub-article>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)

        obtained = list(ArticleLangValidation(xml_tree).validate_article_lang())

        expected = [
            {
                'title': 'title element lang attribute',
                'parent': None,
                'parent_article_type': None,
                'parent_id': None,
                'parent_lang': 'pt',
                'item': 'title',
                'sub_item': None,
                'validation_type': 'match',
                'response': 'ERROR',
                'expected_value': 'title in pt',
                'got_value': None,
                'message': 'Got None, expected title in pt',
                'advice': 'Provide title in the pt language',
                'data': None
            }
        ]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_issue_712(self):
        self.maxDiff = None
        xml_str = """
        <article article-type="editorial" dtd-version="1.1" specific-use="sps-1.9" xml:lang="es" xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink">
        <front>
        <journal-meta>
        <journal-id journal-id-type="publisher-id">cys</journal-id>
        <journal-title-group>
        <journal-title>Ciencia y Sociedad</journal-title>
        <abbrev-journal-title abbrev-type="publisher">cys</abbrev-journal-title>
        </journal-title-group>
        <issn pub-type="ppub">0378-7680</issn>
        <issn pub-type="epub">2613-8751</issn>
        <publisher>
        <publisher-name>Instituto Tecnol&#x00F3;gico de Santo Domingo (INTEC)</publisher-name>
        </publisher>
        </journal-meta>
        <article-meta>
        <article-id pub-id-type="publisher-id">cys.2023.v48i4.3014</article-id>
        <article-id pub-id-type="doi">10.22206/cys.2023.v48i4.3014</article-id>
        <article-categories>
        <subj-group subj-group-type="heading">
        <subject>Editorial</subject>
        </subj-group>
        </article-categories>
        <title-group>
        <article-title><italic>SECUELAS, SERVICIOS P&#x00DA;BLICOS E IM&#x00C1;GENES. TRES TEMAS PARA UN CIERRE</italic></article-title>
        </title-group>
        <contrib-group>
        <contrib contrib-type="author" corresp="yes">
        <name>
        <surname>Ulloa Hung</surname>
        <given-names>Jorge</given-names>
        <prefix>Dr.</prefix>
        </name>
        <xref ref-type="aff" rid="aff1"/>
        <role>Profesor Investigador</role>
        </contrib>
        <aff id="aff1">
        <institution content-type="original">Profesor Investigador Instituto Tecnol&#x00F3;gico de Santo Domingo (INTEC) Director de Ciencia y Sociedad</institution>
        <institution content-type="orgname">Instituto Tecnol&#x00F3;gico de Santo Domingo (INTEC)</institution>
            <institution content-type="orgdiv1">Profesor Investigador</institution>
        <institution content-type="orgdiv1">Director de Ciencia y Sociedad</institution>
        <country country="DO">República Dominicana</country>
        <email>jorge.ulloa@intec.edu.do</email>
        P&#x00E1;gina web: <ext-link ext-link-type="uri" xlink:href="https://www.intec.edu.do">https://www.intec.edu.do</ext-link>
        </aff>
        </contrib-group>
        <pub-date publication-format="electronic" date-type="pub">
        <day>29</day>
        <month>12</month>
        <year>2023</year>
        </pub-date>
        <volume>48</volume>
        <issue>4</issue>
        <fpage>1</fpage>
        <lpage>4</lpage>
        <permissions>
        <copyright-statement>&#x00A9; Ciencia y Sociedad, 2023</copyright-statement>
        <copyright-year>2023</copyright-year>
        <license license-type="open-access" xlink:href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.es" xml:lang="es">
        <license-p>Esta obra est&#x00E1; bajo una licencia internacional Creative Commons Atribuci&#x00F3;n-NoComercial-CompartirIgual 4.0. CC BY-NC-SA</license-p>
        </license>
        </permissions>
        </article-meta>
        </front>
        <body>
        <p>En este n&#x00FA;mero de cierre del 2023 <italic>Ciencia y Sociedad</italic> centra su atenci&#x00F3;n en tres aspectos esenciales, las secuelas de la pandemia del COVID 19, la percepci&#x00F3;n sobre servicios p&#x00FA;blicos esenciales como el transporte y los servicios de salud, y finalmente el tema de la imagen. Este &#x00FA;ltimo presente a trav&#x00E9;s del an&#x00E1;lisis iconogr&#x00E1;fico de una de las especies animales caribe&#x00F1;as vinculada a momentos precolombinos y vigente dentro del universo de representaci&#x00F3;n de lo americano desplegado a partir de 1492.</p>
        <p>Las secuelas de la pandemia de COVID se enfocan en dos elementos centrales, el consumo de drogas y los riesgos de ruptura o separaci&#x00F3;n sentimental. El primero, es abordado a partir de un estudio con alcance descriptivo-transversal sobre el impacto generado por la pandemia en la salud mental de jov&#x00E9;nes estudiantes en diversas universidades de la regi&#x00F3;n del Caribe colombiano. Esta colaboraci&#x00F3;n, que constituye la apertura de la secci&#x00F3;n <italic>Articulo originales</italic>, intenta describir y comparar aspectos como la frecuencia, lugares, y circunstancias asociadas al consumo de drogas, antes y durante la pandemia dentro de la poblaci&#x00F3;n objeto de estudio.</p>
        <p>Sus resultados esenciales no solo revelan la existencia de drogas legales e ilegales en los entornos universitarios de la regi&#x00F3;n estudiada, sino tambi&#x00E9;n su aumento sustancial debido a los cambios en la forma de vida provocados por la situaci&#x00F3;n global de salud vinculada a la dispersi&#x00F3;n del COVID 19. Por otro lado, evidencian la necesidad de implementar programas de prevenci&#x00F3;n y promoci&#x00F3;n de salud mental espec&#x00ED;ficamente enfocados en la poblaci&#x00F3;n juvenil universitaria de la regi&#x00F3;n objeto de estudio, y en general de todo el territorio colombiano. Aspecto que entronca con la propuesta de considerar esta l&#x00ED;nea de investigaci&#x00F3;n prospectiva como una constante para comprender a fondo situaciones que generen trastornos psicol&#x00F3;gicos en estudiantes universitarios, y establecer estrategias de atenci&#x00F3;n integral sobre su salud emocional y mental m&#x00E1;s all&#x00E1; de las circunstancias espec&#x00ED;ficas experimentadas durante la pandemia.</p>
        <p>La segunda colaboraci&#x00F3;n en este n&#x00FA;mero de <italic>Ciencia y Sociedad</italic> centrada en las secuelas de la pandemia de COVID 19 tiene como objetivo identificar variables que puedan predecir de manera m&#x00E1;s eficiente el riesgo de ruptura o separaci&#x00F3;n sentimental en las parejas. El estudio maneja como escenario el contexto social dominicano e intenta probar una hip&#x00F3;tesis donde la angustia psicol&#x00F3;gica, la percepcion de equidad, el apoyo de la pareja y la satisfacci&#x00F3;n se consideran factores o variables esenciales en el riesgo percibido de separaci&#x00F3;n.</p>
        <p>Esta investigaci&#x00F3;n desarrollada desde un enfoque cuantitativo muestra entre sus resultados m&#x00E1;s relevantes la identificaci&#x00F3;n de estas cuatro variables que afectan significativamente el riesgo de separaci&#x00F3;n entre los sujetos estudiados. Adem&#x00E1;s, en comparaci&#x00F3;n con otras investigaciones que han evaluado el riesgo de separaci&#x00F3;n de pareja muestra que a pesar de existir una asociacion entre las variables estudiadas no todas tienen el mismo peso dentro de los predictores significativos de riesgo . En ese caso las dificultades en una relaci&#x00F3;n antes de establecerse la cohabitaci&#x00F3;n forzosa creada por la pandemia constituye un elemento central considerado. En general el modelo desarrollado por esta investigaci&#x00F3;n combina un &#x00E9;nfasis en aspectos como la satisfacci&#x00F3;n conyugal, la percepcion del riesgo de separaci&#x00F3;n, el tipo de convivencia, y la cantidad de tiempo de calidad en las parejas antes de la pandemia, como predictores esenciales para pensar en la disoluci&#x00F3;n de una relaci&#x00F3;n a partir del detonante de las condiciones sociales at&#x00ED;picas impuesta por esa situacion sanitaria. Aspecto que por otro lado tributa a una discusi&#x00F3;n del rol del g&#x00E9;nero en este fen&#x00F3;meno, sobre todo al considerar que la mayor&#x00ED;a de la muestra vinculada al estudio estuvo compuesta por mujeres.</p>
        <p>La percepci&#x00F3;n sobre los servicios p&#x00FA;blicos como tema en esta edici&#x00F3;n de <italic>Ciencia y Sociedad</italic> tiene como escenario los espacios sociales de Ecuador y M&#x00E9;xico. A trav&#x00E9;s de un estudio de caso que eval&#x00FA;a los servicios de transporte p&#x00FA;blico en la ciudad de Cuenca -Ecuador, la primera de estas contribuciones realiza una medici&#x00F3;n que busca aportar a los procesos de movilizaci&#x00F3;n de la poblaci&#x00F3;n, as&#x00ED; como contribuir a mejorar las condiciones sociales, econ&#x00F3;micas y ambientales vinculadas a ese fen&#x00F3;meno. Desde un enfoque de investigaci&#x00F3;n mixto que incluye entrevistas semiestructuradas y cuestionarios aplicados a una muestra no probabilista de diferentes actores dentro del sistema de transporte p&#x00FA;blico, el estudio arroja aspectos esenciales caracterizadores de ese servicio. Un aspecto valioso de sus resultados es que fomentan una perspectiva diagn&#x00F3;stica que puede ser una de las bases fundamentales para un programa que garantice la movilidad eficiente, equitativa y sostenible en esta ciudad. Aspecto que como bien se&#x00F1;alan los autores de la colaboraci&#x00F3;n es imprescindible para su desarrollo econ&#x00F3;mico, su cohesi&#x00F3;n y movilidad social adem&#x00E1;s de la protecci&#x00F3;n de su ambiente. En esencia para la mejor calidad de vida y creaci&#x00F3;n de oportunidades a nivel individual y comunitario.</p>
        <p>El ausentismo y la satisfacci&#x00F3;n laboral en un hospital de segundo nivel de atenci&#x00F3;n en M&#x00E9;xico constituye el tema de la segunda colaboraci&#x00F3;n relacionada con los servicios p&#x00FA;blicos en este n&#x00FA;mero de <italic>Ciencia y Sociedad</italic>. Su objetivo central es determinar la relaci&#x00F3;n entre ambas variables dentro del personal vinculado a servicios de enfermer&#x00ED;a en una instituci&#x00F3;n de esa naturaleza localizada en San Luis Potos&#x00ED;. Con alcance descriptivo- correlacional y a partir de un enfoque cuantitativo esta investigaci&#x00F3;n indaga sobre las principales razones que generan ausentismo y sus v&#x00ED;nculos con los &#x00ED;ndices de satisfacci&#x00F3;n laboral. Un aspecto que resaltar dentro de esta colaboraci&#x00F3;n, al igual que en el caso anterior, es su sentido diagn&#x00F3;stico y predictivo, as&#x00ED; como su aliciente o fundamento para implementar estrategias de mejora de los servicios de salud considerando la autopercepci&#x00F3;n de sus proveedores. Estrategias que a partir de los resultados obtenidos apuntan hacia factores como ambiente f&#x00ED;sico, pol&#x00ED;ticas salariales y cultura laboral. Aspectos remarcables no solo para el caso estudiado, sino tambi&#x00E9;n para otros servicios de salud en espacios de Am&#x00E9;rica Latina.</p>
        <p>Finalmente, dentro de la secci&#x00F3;n <italic>Art&#x00ED;culos originales</italic> de esta entrega el estudio de las im&#x00E1;genes se materializa a trav&#x00E9;s del an&#x00E1;lisis est&#x00E9;tico de las variantes iconogr&#x00E1;ficas y el simbolismo de la llamada zarig&#x00FC;eya com&#x00FA;n de orejas negras (<italic>Didelphis marsupialis</italic> Linnaeus 1758). Especie animal presente en adornos cer&#x00E1;micos de origen ind&#x00ED;gena localizados en las Antillas Menores y Venezuela, as&#x00ED; como dentro del corpus de impresos, descripciones e ilustraciones creados por artistas europeos. La manera en que cronistas y artistas usaron un esquema anal&#x00F3;gico comparativo para crear un nuevo concepto y mostrar algo desconocido es el aspecto central en el an&#x00E1;lisis de este art&#x00ED;culo.</p>
        <p>A trav&#x00E9;s de un recorrido hist&#x00F3;rico cr&#x00ED;tico, que incluye diversos autores y formas de representaci&#x00F3;n de este animal, la colaboraci&#x00F3;n tiene la capacidad de definir y caracterizar diversas tendencias en cuanto a sus interpretaciones y significados. Estas tendencias no solo son propias de diferentes momentos y se vinculan a los avances en el estudio emp&#x00ED;rico y anat&#x00F3;mico de la especie, sino que al mismo tiempo se relacionan con visiones más cercanas y objetivas o m&#x00E1;s alejadas y remotas sobre el universo americano y caribe&#x00F1;o.</p>
        <p>La acostumbrada secci&#x00F3;n de <italic>Rese&#x00F1;as y revisiones de libros</italic> en esta entrega final del 2023 de <italic>Ciencia y Sociedad</italic> incluye las rese&#x00F1;as de dos obras recientemente publicadas en el espacio editorial y acad&#x00E9;mico dominicano, <italic>Miradas Desencadenantes. Construcci&#x00F3;n de conocimientos para la igualdad</italic> y <italic>Sociedades ind&#x00ED;genas en la isla de Santo Domingo: una mirada desde las colecciones arqueol&#x00F3;gicas del Centro Le&#x00F3;n</italic>.</p>
        <p>La primera de estas obras fue publicada en marzo del 2023 por el Centro de Estudios de G&#x00E9;nero de INTEC y constituye el volumen n&#x00FA;mero 6 de la serie &#x201C;Miradas Desencadenantes&#x201D; que tradicionalmente agrupa art&#x00ED;culos presentados en el marco de las Conferencias Dominicanas de Estudios de G&#x00E9;nero organizadas por esa instituci&#x00F3;n. Los art&#x00ED;culos compilados en ese volumen incluyen una diversidad de tem&#x00E1;ticas, vivencias y experiencias que como bien anuncia la autora de la rese&#x00F1;a tienen especial relevancia al plasmar de manera critica distintas facetas de la estratificaci&#x00F3;n de g&#x00E9;nero que viven las mujeres en la Rep&#x00FA;blica Dominicana. Aspecto que convierte el volumen en una herramienta pedag&#x00F3;gica y de construcci&#x00F3;n de pensamiento cr&#x00ED;tico desde la perspectiva de g&#x00E9;nero y a su vez en un desaf&#x00ED;o para convertir los temas fundamentales abordados a trav&#x00E9;s de este en parte del debate p&#x00FA;blico.</p>
        <p><italic>Sociedades ind&#x00ED;genas en la isla de Santo Domingo: una mirada desde las colecciones arqueol&#x00F3;gicas del Centro Le&#x00F3;n</italic> constituye la segunda obra rese&#x00F1;ada en esta edici&#x00F3;n de <italic>Ciencia y Sociedad e</italic> ilustra sobre una obra que tiene la capacidad de cruzar las fronteras y romper con los clich&#x00E9;s tradicionales en la representaci&#x00F3;n de estas culturas. En ella, la tradicional exotizaci&#x00F3;n a trav&#x00E9;s de objetos extraordinarios o &#x00FA;nicos y el aislamiento de esta parte del pasado seden lugar a una representaci&#x00F3;n m&#x00E1;s compleja y al reconocimiento de una persistencia cultural a trav&#x00E9;s del legado que alcanza diversas esferas de la vida social del dominicano.</p>
        <p>Esta obra cuya conformaci&#x00F3;n es resultado del proyecto Investigaci&#x00F3;n colaborativa y capacitaci&#x00F3;n basada en intercambios en gesti&#x00F3;n de colecciones, ejecutado por el Centro Cultural Eduardo Le&#x00F3;n y financiado por el Fondo de Embajadores de los Estados Unidos para la Preservaci&#x00F3;n de la Cultura, constituye adem&#x00E1;s un rescate y valorizaci&#x00F3;n cient&#x00ED;fica de testimonios y evidencias arqueol&#x00F3;gicas cuyos or&#x00ED;genes o formas de registro est&#x00E1;n marcados por el uso de pr&#x00E1;cticas poco controladas o el mero inter&#x00E9;s coleccionista. En esencia, se trata de una obra que intenta otorgar vida y reconocimiento no solo a esos artefactos a trav&#x00E9;s de su estudio cient&#x00ED;fico y exposici&#x00F3;n, sino tambi&#x00E9;n a una parte relevante de la historia y la cultura dominicana muchas veces reducida a an&#x00E9;cdota de inicio o expresi&#x00F3;n est&#x00E9;tica de unas culturas cuya diversidad y trascendencia merece ser mejor estudiada.</p>
        </body>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)

        obtained = list(ArticleLangValidation(xml_tree).validate_article_lang())

        self.assertEqual(len(obtained), 0)


if __name__ == '__main__':
    unittest.main()
