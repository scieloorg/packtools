<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:template match="front" mode="modal-contrib">
        <!-- sobrescreve article-meta mode="modal-contrib" -->
        <xsl:apply-templates select="article-meta" mode="modal-contrib-div"/>
    </xsl:template>

    <xsl:template match="article-meta | front-stub" mode="modal-contrib">
        <!-- sobrescreve article-meta mode="modal-contrib" -->
        <xsl:apply-templates select="." mode="modal-contrib-div"/>
    </xsl:template>

    <xsl:template match="article-meta | front-stub" mode="modal-contrib-div">
        <div class="modal fade ModalDefault ModalTutors"
            id="ModalTutors"
            tabindex="-1"
            role="dialog"
            aria-modal="true"
            aria-labelledby="ModalTutorsLabel"
            aria-hidden="true">

            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h2 class="h4 modal-title" id="ModalTutorsLabel">
                            <xsl:apply-templates select="." mode="interface">
                                <xsl:with-param name="text">About the authors</xsl:with-param>
                            </xsl:apply-templates>
                        </h2>
                        <button class="btn-close" data-bs-dismiss="modal">
                            <xsl:attribute name="aria-label">
                                <xsl:apply-templates select="." mode="interface">
                                    <xsl:with-param name="text">Close</xsl:with-param>
                                </xsl:apply-templates>
                            </xsl:attribute>
                        </button>
                    </div>
                    <div class="modal-body">
                        <div id="authorCardsContainer"></div>
                    </div>                    
                </div>
            </div>
        </div>
    </xsl:template>

    <xsl:template match="author-notes" mode="modal-contrib-div">
        <xsl:apply-templates select="*" mode="modal-contrib-div"/>
    </xsl:template>

    <xsl:template match="corresp" mode="modal-contrib-div">
        <div class="correspondence mt-3 mb-4 d-none" id="correspondenceSection">
            <div class="section-grid">
                <span class="material-icons-outlined" aria-hidden="true">
                person
                </span>
                <div>
                    <xsl:apply-templates select="*" mode="modal-contrib-div"/>
                </div>
            </div>
        </div>
    </xsl:template>

    <xsl:template match="corresp/*" mode="modal-contrib-div">
        <div class="section-content">
            <span id="correspondenceText"></span>
            <br/>
            <a href="" id="correspondenceEmail">
            </a>
        </div>
    </xsl:template>

    <xsl:template match="corresp/label| corresp/title" mode="modal-contrib-div">
        <p class="section-title mb-1"><xsl:apply-templates/></p>
    </xsl:template>

    <xsl:template match="/" mode="modal-contrib-js">
        <script type="text/javascript">
            <!-- base js -->
            <xsl:apply-templates select="." mode="modal-contrib-js-base"/>

            <!-- affiliation data -->
            <xsl:apply-templates select="." mode="modal-contrib-js-affs"/>
            <!-- authors data -->
            <xsl:apply-templates select="." mode="modal-contrib-js-authors"/>

            <!-- js functions -->
            <xsl:apply-templates select="." mode="modal-contrib-js-function-create-author-button"/>
            <xsl:apply-templates select="." mode="modal-contrib-js-function-append-author-item"/>
            <xsl:apply-templates select="." mode="modal-contrib-js-function-append-summary-item"/>
            <xsl:apply-templates select="." mode="modal-contrib-js-function-render-authors"/>
            <xsl:apply-templates select="." mode="modal-contrib-js-function-build-institution-text"/>
            <xsl:apply-templates select="." mode="modal-contrib-js-function-build-author-card"/>
            <xsl:apply-templates select="." mode="modal-contrib-js-function-open-author-modal"/>
        </script>
    </xsl:template>

    <xsl:template match="/" mode="modal-contrib-js-affs">
        <xsl:choose>
            <xsl:when test=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']//front-stub//contrib">
                <xsl:apply-templates select=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']//front-stub" mode="modal-contrib-js-affiliation-data"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select=".//article-meta" mode="modal-contrib-js-affiliation-data"/>                    
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="/" mode="modal-contrib-js-authors">
        <xsl:choose>
            <xsl:when test=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']//front-stub//aff">
                <xsl:apply-templates select=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']//front-stub" mode="modal-contrib-js-author-data"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select=".//article-meta" mode="modal-contrib-js-author-data"/>                    
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="*" mode="modal-contrib-js-base">
        const MAX_VISIBLE_AUTHORS = 25;
        const ALWAYS_VISIBLE_FIRST = 2;
        const ALWAYS_VISIBLE_LAST = 1;

        const authorList = document.getElementById("authorList");

        const authorModalElement = document.getElementById("ModalTutors");
        const authorCardsContainer = document.getElementById("authorCardsContainer");
        const correspondenceSection = document.getElementById("correspondenceSection");
        const correspondenceText = document.getElementById("correspondenceText");
        const correspondenceEmail = document.getElementById("correspondenceEmail");

        const authorModal = authorModalElement
        ? new bootstrap.Modal(authorModalElement)
        : null;

        let expanded = false;

    </xsl:template>

    <xsl:template match="*" mode="modal-contrib-js-affiliation-data">
        const affiliationMap = {<xsl:apply-templates select=".//aff" mode="modal-contrib-js-affiliation-map-affiliation-text"/>
        };
    </xsl:template>

    <xsl:template match="aff" mode="modal-contrib-js-affiliation-map-affiliation-text"><xsl:text>
            </xsl:text>&quot;<xsl:value-of select="@id"/>&quot;: &quot;<xsl:apply-templates select="institution[@content-type='original']" /><xsl:if test="not(institution[@content-type='original'])"><xsl:apply-templates select=".//*" mode="modal-contrib-js-affiliation-map-affiliation-text-base"/></xsl:if>&quot;<xsl:if test="position() != last()">,</xsl:if>
    </xsl:template>

    <xsl:template match="aff//*[@content-type!='original']" mode="modal-contrib-js-affiliation-map-affiliation-text-base"><xsl:value-of select="."/><xsl:if test="position() != last()">, </xsl:if></xsl:template>

    <xsl:template match="contrib" mode="modal-contrib-js-corresponding">
        <xsl:choose>
            <xsl:when test="xref[@ref-type='corresp']">true</xsl:when>
            <xsl:otherwise>false</xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="contrib" mode="modal-contrib-js-affiliation">[<xsl:for-each select="xref[@ref-type='aff']">&quot;<xsl:value-of select="@rid"/>&quot;<xsl:if test="position() != last()">, </xsl:if></xsl:for-each>]</xsl:template>

    <xsl:template match="xref[@ref-type='corresp']" mode="modal-contrib-js-email">
        <xsl:variable name="rid"><xsl:value-of select="@rid"/></xsl:variable>
        <xsl:apply-templates select="../../..//corresp[@id=$rid]/email"/>
    </xsl:template>

    <xsl:template match="contrib" mode="modal-contrib-js-roles">
        <xsl:for-each select="role">
            <xsl:value-of select="."/>
            <xsl:if test="position() != last()"> · </xsl:if>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="article-meta|front-stub" mode="modal-contrib-js-author-data">
        const authors = [
            <xsl:for-each select=".//contrib[@contrib-type='author']">
                {
                    name: &quot;<xsl:apply-templates select="name|collab" mode="modal-contrib-js-author"/>&quot;,
                    affiliations: <xsl:apply-templates select="." mode="modal-contrib-js-affiliation"/>,
                    orcid: &quot;<xsl:value-of select="contrib-id[@contrib-id-type='orcid']"/>&quot;,
                    email: &quot;<xsl:apply-templates select="xref[@ref-type='corresp']" mode="modal-contrib-js-email"/>&quot;,
                    corresponding: <xsl:apply-templates select="." mode="modal-contrib-js-corresponding"/>,
                    roles: &quot;<xsl:apply-templates select="." mode="modal-contrib-js-roles"/>&quot;
                }<xsl:if test="position() != last()">,</xsl:if>
            </xsl:for-each>
        ];
    </xsl:template>

    <xsl:template match="name" mode="modal-contrib-js-author">
        <xsl:value-of select="given-names"/><xsl:text> </xsl:text><xsl:value-of select="surname"/><xsl:if test="string-length(@suffix) > 0"><xsl:text>, </xsl:text><xsl:value-of select="@suffix"/></xsl:if>
    </xsl:template>

    <xsl:template match="collab" mode="modal-contrib-js-author">
        <xsl:value-of select="."/>
    </xsl:template>

    <xsl:template match="*" mode="modal-contrib-js-function-create-author-button">
        function createAuthorButton(author, index) {
            const button = document.createElement("button");

            button.type = "button";
            button.className = "btn-link px-0";
            button.setAttribute("data-author-index", index);
            button.setAttribute("aria-label", `Abrir detalhes de ${author.name}`);

            if (author.corresponding || author.email) {
                const icon = document.createElement("span");

                icon.className = "material-icons-outlined me-1 fs-6";
                icon.setAttribute("aria-hidden", "true");
                icon.textContent = "mail";

                button.appendChild(icon);
            }

            const name = document.createElement("span");
            name.textContent = author.name;

            button.appendChild(name);

            button.addEventListener("click", () => {
                openAuthorModal(index);
            });

            return button;
        }
    </xsl:template>
    
    <xsl:template match="*" mode="modal-contrib-js-function-append-author-item">
        function appendAuthorItem(author, index, isLastVisibleItem) {
            const li = document.createElement("li");

            li.appendChild(createAuthorButton(author, index));

            if (!isLastVisibleItem) {
                const separator = document.createElement("span");
                separator.className = "author-separator";
                separator.setAttribute("aria-hidden", "true");
                separator.textContent = ",";

                li.appendChild(separator);
            }

            authorList.appendChild(li);
        }
    </xsl:template>


    <xsl:template match="*" mode="modal-contrib-js-function-append-summary-item">
        function appendSummaryItem(hiddenCount, isLastItem = false) {
            const li = document.createElement("li");

            const button = document.createElement("button");
            button.type = "button";
            button.className = "btn btn-secondary btn-sm outlineFadeLink ms-0";

            if (expanded) {
                button.textContent = "Ocultar autores";
                button.setAttribute("aria-label", "Ocultar autores intermediários");
                button.setAttribute("aria-expanded", "true");
            } else {
                button.textContent = `+ ${hiddenCount} autores`;
                button.setAttribute("aria-label", `Mostrar os ${hiddenCount} autores ocultos`);
                button.setAttribute("aria-expanded", "false");
            }

            button.addEventListener("click", () => {
                expanded = !expanded;
                renderAuthors();
            });

            li.appendChild(button);

            if (!isLastItem) {
                const separator = document.createElement("span");
                separator.className = "author-separator";
                separator.setAttribute("aria-hidden", "true");
                separator.textContent = ",";

                li.appendChild(separator);
            }

            authorList.appendChild(li);
        }
    </xsl:template>
    
    <xsl:template match="*" mode="modal-contrib-js-function-render-authors">
        <xsl:text>
        function renderAuthors() {
            if (!authorList) return;

            authorList.innerHTML = "";

            const total = authors.length;
            const hiddenCount = total - (ALWAYS_VISIBLE_FIRST + ALWAYS_VISIBLE_LAST);
            const canCollapse = total > MAX_VISIBLE_AUTHORS &amp;&amp; hiddenCount > 0;

            if (!canCollapse) {
                authors.forEach((author, index) => {
                appendAuthorItem(author, index, index === total - 1);
                });

                return;
            }

            if (expanded) {
                authors.forEach((author, index) => {
                appendAuthorItem(author, index, index === total - 1);
                });

                appendSummaryItem(hiddenCount, true);
                return;
            }

            const firstAuthors = authors.slice(0, ALWAYS_VISIBLE_FIRST);
            const lastAuthors = authors.slice(total - ALWAYS_VISIBLE_LAST);

            firstAuthors.forEach((author, index) => {
                appendAuthorItem(author, index, false);
            });

            appendSummaryItem(hiddenCount, false);

            lastAuthors.forEach((author, idx) => {
                const realIndex = total - ALWAYS_VISIBLE_LAST + idx;
                appendAuthorItem(author, realIndex, true);
            });
        }
        </xsl:text>
    </xsl:template>
    
    <xsl:template match="*" mode="modal-contrib-js-function-build-institution-text">
        function buildInstitutionText(author) {
            return author.affiliations
                .map(code => affiliationMap[code] || `Afiliação ${code}`)
                .join(" ");
        }
    </xsl:template>

    <xsl:template match="*" mode="modal-contrib-js-function-build-author-card">
        function buildAuthorCard(author) {
            const card = document.createElement("div");
            card.className = "author-card";

            const nameRow = document.createElement("div");
            nameRow.className = "author-grid-row";

            const personIcon = document.createElement("span");
            personIcon.className = "material-icons-outlined";
            personIcon.setAttribute("aria-hidden", "true");
            personIcon.textContent = "person";

            const nameWrapper = document.createElement("div");
            nameWrapper.className = "author-name";

            const nameText = document.createElement("span");
            nameText.className = "author-name-text";
            nameText.textContent = author.name;

            nameWrapper.appendChild(nameText);
            nameRow.appendChild(personIcon);
            nameRow.appendChild(nameWrapper);

            card.appendChild(nameRow);

            const roles = document.createElement("div");
            roles.className = "author-roles author-subrow mb-2";
            roles.textContent = author.roles || "Sem funções informadas.";

            card.appendChild(roles);

            const institutionRow = document.createElement("div");
            institutionRow.className = "author-grid-row author-subrow mb-2";

            const schoolIcon = document.createElement("span");
            schoolIcon.className = "material-icons-outlined";
            schoolIcon.setAttribute("aria-hidden", "true");
            schoolIcon.textContent = "school";

            const institution = document.createElement("div");
            institution.className = "author-institution";

            const institutionText = document.createElement("span");
            institutionText.className = "author-inst-text";
            institutionText.textContent = buildInstitutionText(author);

            institution.appendChild(institutionText);
            institutionRow.appendChild(schoolIcon);
            institutionRow.appendChild(institution);

            card.appendChild(institutionRow);

            if (author.orcid) {
                const orcidWrap = document.createElement("div");
                orcidWrap.className = "orcid-button-wrap ms-4";

                const orcidLink = document.createElement("a");
                orcidLink.target = "_blank";
                orcidLink.rel = "noopener noreferrer";
                orcidLink.className = "btn btn-secondary orcid-button";
                orcidLink.href = `https://orcid.org/${author.orcid}`;
                orcidLink.textContent = author.orcid;
                orcidLink.setAttribute(
                "aria-label",
                `Acessar perfil ORCID ${author.orcid}. Abre em nova aba.`
                );

                orcidWrap.appendChild(orcidLink);
                card.appendChild(orcidWrap);
            }

            return card;
        }
    </xsl:template>

    <xsl:template match="*" mode="modal-contrib-js-function-open-author-modal">
        function openAuthorModal(index) {
            if (!authorModal || !authorCardsContainer) return;

            const author = authors[index];

            if (!author) return;

            authorCardsContainer.innerHTML = "";
            authorCardsContainer.appendChild(buildAuthorCard(author));

            if (correspondenceSection){
                if (author.email) {
                    correspondenceSection.classList.remove("d-none");
                    correspondenceText.textContent = `${author.name}. E-mail: `;
                    correspondenceEmail.href = `mailto:${author.email}`;
                    correspondenceEmail.textContent = author.email;
                } else {
                    correspondenceSection.classList.add("d-none");
                    correspondenceText.textContent = "";
                    correspondenceEmail.removeAttribute("href");
                    correspondenceEmail.textContent = "";
                }
            }
            
            authorModal.show();
        }

        renderAuthors();
    </xsl:template>
    
</xsl:stylesheet>