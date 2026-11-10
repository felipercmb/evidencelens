# Proveniência e limites de licença

## Incluído

Código da demo, testes, gerador sintético e documentação do projeto, desenvolvidos com assistência de IA. O gerador produz exemplos fictícios de funcionamento de estabelecimentos. Não há dados de usuários ou artigos científicos incorporados. A licença MIT cobre este código/documentação original.

## Utilizado somente na pesquisa local; não distribuído

- SNLI e MultiNLI: benchmarks de inferência textual. Seus componentes possuem termos próprios; não inferir autorização de redistribuição a partir da licença do código. Fontes: https://nlp.stanford.edu/projects/snli/ e https://cims.nyu.edu/~sbowman/multinli/ .
- ANLI: https://github.com/facebookresearch/anli , CC BY-NC 4.0. Pesos derivados dessa adaptação permanecem separados e não comerciais. Nenhum dado ou peso ANLI está neste pacote.
- Modelo original `cross-encoder/nli-deberta-v3-small`: cartão declara Apache 2.0, revisão usada `fa2804872c3b4bd748f38c0185cc85775361e735`. Fonte: https://huggingface.co/cross-encoder/nli-deberta-v3-small . Não distribuído, nem executado pela demo pública. Licença do modelo não elimina requisitos de dados ou outros direitos.
- SciFact: https://github.com/allenai/scifact . Anotações sob CC BY 4.0; corpus sob ODC-By, com direitos subjacentes dos abstracts. Não distribuído.
- Belebele: https://github.com/facebookresearch/belebele , CC BY-SA 4.0 para o conjunto utilizado. Não distribuído.
- Novos abstracts obtidos de artigos PLOS via Europe PMC: https://europepmc.org/ . Licença CC BY 4.0 verificada em cada XML. Foram usados para diagnóstico local; não são redistribuídos neste pacote. Reservas de dez documentos cada, de 2025, 2024 e 2023, com títulos/textos exatos verificados contra as fontes anteriores.

Relatos agregados não são uma relicença de dados, modelos ou artigos. Não há liberação comercial de todos os componentes experimentais por meio deste repositório.
