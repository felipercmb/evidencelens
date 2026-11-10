# Resumo da pesquisa local

Este documento descreve experimentos realizados fora da demo pública. Não inclui datasets, pesos, textos dos artigos, predições individuais ou scripts dependentes do ambiente local. Logo, estes números não são reproduzíveis integralmente apenas com este repositório. São resultados reportados com limitações, não certificações.

## Evolução relevante

- Adaptação documental inicial: reserva interna de 82 pares, macro-F1 0,410 → 0,535 e acertos 36 → 49. Porém, recall de insuficiência caiu de 24/32 para 18/32. Nenhum limiar satisfez a regra de calibração; nenhuma decisão automática foi liberada.
- Janelas conservadoras: diagnóstico construído por IA, 30 alegações sobre dez abstracts novos ao projeto. Janelas acertaram 24/30 contra 18/30 do abstract completo com a mesma penalização. As dez insuficiências foram reconhecidas, mas houve seis erros. Não demonstra segurança.
- Insuficiências mais sutis: outra reserva, 40 alegações sobre dez outros abstracts. Janelas acertaram 31/40 e reconheceram 18/20 insuficientes. Houve extrapolação indevida de infância para idade adulta e de experimento em animais para resultado clínico humano. Modelos permaneceram congelados.
- Contexto e escopo: terceira reserva documental, 40 alegações, dez documentos distintos. Baseline e candidatos acertaram 33/40. Baseline: 19/20 insuficientes, 8/10 contradições, 6/10 suportes. Candidatos: 20/20 insuficientes, 6/10 contradições, 7/10 suportes. Melhorar uma classe custou erros em outra.

Não comparar 24/30, 31/40 e 33/40 como uma curva de ganho: são desafios diferentes, com proporções de classes e documentos distintos.

## Última rodada

A seleção feita na calibração manteve o baseline; não foi trocada após a avaliação. Alertas de escopo marcaram 16/40 casos: 12 insuficientes, três contradições e um suporte legítimo. Alertas não corrigem o rótulo nem reduzem automaticamente a carga de revisão. Todos os 40 casos continuaram exigindo revisão. Não houve promoção do candidato.

Os casos foram construídos e revisados por IA antes das previsões. Isso não é anotação humana, avaliação independente por especialistas ou amostra de respostas naturais. As referências são relativas aos abstracts, não à verdade médica ou científica. Documentos não duplicados exatamente ainda podem conter semelhanças semânticas ou ter aparecido no pré-treino.

## Metodologia e limitações

Seleção, parâmetros e modelos foram congelados antes do acesso às novas reservas. Ajustes de redação sugeridos por uma segunda revisão por IA ocorreram antes das previsões, com versões preservadas localmente. Os testes já consultados não voltaram a ser apresentados como independentes na rodada seguinte.

O trabalho investigou janelas, definições de siglas, contexto, agregação e alertas de população/causalidade. O mecanismo de cláusulas não foi ativado nos pares de treino/calibração usados; não há evidência de que ele tenha aprendido relações sujeito/propriedade. Uma inversão desse tipo continuou errada na última reserva.

A busca ocorreu em corpora de apenas dez documentos por reserva. Os documentos são abstracts em inglês, principalmente científicos, de um único editor. Não validam português, documentos longos, busca em grande escala ou distribuição real de erros.

Na última rodada, a execução de contexto levou aproximadamente 7,7 segundos contra 1,9 segundo do baseline no equipamento local, sem contar todas as etapas de preparação. Esses números não são benchmark universal de latência.

## Testes

Na cópia local completa, 19 testes da aplicação e 87 do pipeline de pesquisa passaram. O pacote público contém os 19 testes da demo; não contém os 87 testes de pesquisa nem seus insumos. Testes de software não validam precisão ou segurança do modelo.

## Decisão

Manter revisão obrigatória e separar experimento de produto. Mais dados bem adjudicados e avaliação humana em documentos e respostas novos são prioritários antes de qualquer alegação de uso real. Não existe garantia de melhoria percentual futura.
