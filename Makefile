clean:
	@python setup.py clean
	@rm -f dist/*

build:
	@python setup.py sdist
	@cd dist; ls *.tar.gz | xargs python -m pip wheel --no-deps -w .

upload:
	@twine upload dist/*


#########
## i18n #
#########

# IMPORTANTE: Seguir os seguintes passos para atualização dos .pot e po:
#
# 1. make make_message (Varre todos os arquivo [.html, .py, .txt, ...] buscando por tags de tradução)
# 2. make update_catalog (Atualizar todos os com .po a apartir do .pot)
# 6. make compile_messages para gerar os arquivo .mo
# 7. realize a atualização no repositório de códigos.

# Faz um scan em toda a packtools/webapp buscando strings traduzíveis e o resultado fica em packtools/webapp/translations/messages.pot
make_messages:
	pybabel extract -F packtools/webapp/config/babel.cfg -k lazy_gettext -k __ -o packtools/webapp/translations/messages.pot .

# cria o catalogo para o idioma definido pela variável LANG, a partir das strings: packtools/webapp/translations/messages.pot
# executar: $ LANG=en make create_catalog
create_catalog:
	pybabel init -i packtools/webapp/translations/messages.pot -d packtools/webapp/translations -l $(LANG)

# atualiza os catalogos, a partir das strings: packtools/webapp/translations/messages.pot
update_catalog:
	pybabel update -i packtools/webapp/translations/messages.pot -d packtools/webapp/translations

# compila as traduções dos .po em arquivos .mo prontos para serem utilizados.
compile_messages:
	pybabel compile -d packtools/webapp/translations

build_i18n:
	@make make_messages && make update_catalog && make compile_messages



.PHONY: clean build upload
