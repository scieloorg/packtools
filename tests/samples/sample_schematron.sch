<schema xmlns="http://purl.oclc.org/dsdl/schematron">
  <pattern id="rsp_nlm_title">
    <title>Make sure RSP's nlm title is correct</title>

    <rule context="/article/front/journal-meta/journal-id[@journal-id-type='nlm-ta']">
      <assert test="text() = 'Rev Saude Publica'">
          Element 'journal-id': Invalid NLM title.
      </assert>
    </rule>
  </pattern>
</schema>

