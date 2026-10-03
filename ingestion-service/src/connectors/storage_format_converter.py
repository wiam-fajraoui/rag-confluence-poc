import html

from bs4 import BeautifulSoup, NavigableString, Tag


# Les espaces de noms utilisés par le Storage Format Confluence
# (préfixes "ac:" et "ri:") ne sont pas déclarés dans le fragment
# retourné par l'API. On les déclare nous-mêmes en enveloppant le
# fragment dans une racine, pour permettre un parsing XML correct
# (notamment pour que les sections CDATA des blocs de code soient
# lues correctement).
_NAMESPACE_WRAPPER = (
    '<root '
    'xmlns:ac="http://www.atlassian.com/schema/confluence/4/ac/" '
    'xmlns:ri="http://www.atlassian.com/schema/confluence/4/ri/">'
    "{content}"
    "</root>"
)

# Macros Confluence qui n'apportent pas de contenu documentaire
# utile (recherche, filtres d'espace, widgets d'administration) :
# elles sont ignorées plutôt que converties.
_IGNORED_MACROS = {
    "panel",
    "livesearch",
    "info",
    "listlabels",
    "recently-updated",
}


class StorageFormatConverter:
    """
    Convertit le contenu d'une page Confluence au format Storage
    (XHTML + macros propriétaires) en Markdown, avec les mêmes
    conventions que le corpus local (docs/*.md) : '#'/'##' pour les
    titres, '---' pour les séparateurs, '- ' pour les listes, blocs
    ```language pour le code.

    Objectif : produire un Markdown suffisamment proche du corpus
    local pour que chunker.py fonctionne sans aucune modification.
    """

    def convert(self, storage_html: str) -> str:

        # L'API Confluence renvoie les caractères accentués sous forme
        # d'entités HTML nommées (ex. "&eacute;" pour "é"), pas en
        # UTF-8 direct. Le parseur XML utilisé plus bas ne connaît que
        # les 5 entités XML standard (&lt; &gt; &amp; &quot; &apos;) et
        # supprime silencieusement toute entité HTML5 qu'il ne
        # reconnaît pas -- d'où la perte des accents si on ne décode
        # pas ces entités avant le parsing.
        # Limite connue : si un bloc de code (CDATA) contenait
        # lui-même une séquence ressemblant à une entité HTML, elle
        # serait aussi décodée par erreur. Non rencontré sur ce
        # corpus, mais à garder en tête.
        storage_html = html.unescape(storage_html)

        wrapped = _NAMESPACE_WRAPPER.format(content=storage_html)

        # On encode explicitement en UTF-8 avant de parser, plutôt que
        # de laisser le parseur XML deviner l'encodage à partir d'une
        # chaîne Python. Sans cela, certains environnements (observé
        # sur Windows) peuvent perdre les caractères accentués lors du
        # parsing, alors que le même code fonctionne correctement sur
        # d'autres systèmes (observé sous Linux). Passer des bytes
        # UTF-8 explicites lève toute ambiguïté.
        soup = BeautifulSoup(wrapped.encode("utf-8"), "xml")

        root = soup.find("root")

        lines = []

        for element in root.contents:
            converted = self._convert_element(element)
            if converted is not None:
                lines.append(converted)

        return "\n\n".join(line for line in lines if line.strip())

    def _convert_element(self, element):

        if isinstance(element, NavigableString):
            text = str(element).strip()
            return text if text else None

        if not isinstance(element, Tag):
            return None

        name = element.name

        if name in ("h1", "h2", "h3", "h4"):
            level = int(name[1])
            return ("#" * level) + " " + element.get_text().strip()

        if name == "hr":
            return "---"

        if name == "p":
            text = element.get_text().strip()
            return text if text else None

        if name in ("ul", "ol"):
            return self._convert_list(element, ordered=(name == "ol"))

        if name == "structured-macro":
            return self._convert_macro(element)

        # Élément non reconnu : on tente d'extraire le texte brut
        # plutôt que de perdre l'information silencieusement.
        text = element.get_text().strip()
        return text if text else None

    def _convert_list(self, list_element, ordered: bool) -> str:

        items = []

        for index, li in enumerate(
            list_element.find_all("li", recursive=False), start=1
        ):
            text = li.get_text().strip()
            if not text:
                continue
            prefix = f"{index}. " if ordered else "- "
            items.append(prefix + text)

        return "\n".join(items)

    def _convert_macro(self, macro_element):

        macro_name = macro_element.get("ac:name")

        if macro_name == "code":
            return self._convert_code_macro(macro_element)

        if macro_name in _IGNORED_MACROS:
            return None

        # Macro inconnue : on récupère le texte du corps enrichi si
        # présent, plutôt que de perdre l'information silencieusement.
        rich_body = macro_element.find("rich-text-body")
        if rich_body:
            text = rich_body.get_text().strip()
            return text if text else None

        return None

    def _convert_code_macro(self, macro_element) -> str:

        language = ""
        for param in macro_element.find_all("parameter"):
            if param.get("ac:name") == "language":
                language = param.get_text().strip()
                break

        body = macro_element.find("plain-text-body")
        code = body.get_text() if body else ""

        return f"```{language}\n{code.strip()}\n```"