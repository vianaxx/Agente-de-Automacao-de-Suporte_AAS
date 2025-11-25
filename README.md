## Agente de Automação de Suporte (ASS)

**Status:** Em Desenvolvimento 🚧

O objetivo é construir um agente de IA que possa diagnosticar problemas em sistemas simulados e tomar decisões sobre como resolvê-los (como reiniciar um serviço), usando o Ollama Cloud como o cérebro (LLM).


### Objetivo Principal

* **Diagnóstico Inteligente:** Analisar dados de *logs*, métricas e estados de sistemas simulados.
* **Tomada de Decisão:** Determinar a **melhor ação** para resolver o problema (e.g., reiniciar um componente, escalar para um humano, executar um *script*).
* **Ação Autônoma:** Integrar-se com sistemas de execução para implementar as soluções propostas.

### Arquitetura do Sistema

O ASS é construído sobre módulos que trabalham em conjunto para formar um ciclo completo de diagnóstico e ação.

| Módulo | Função | Status |
| :--- | :--- | :--- |
| **Coleta de Dados** | Ingestão e normalização de dados (logs, métricas, alertas) dos sistemas simulados. | ❌ Pendente |
| **Módulo RAG** | Aumenta o contexto do LLM com documentação e manuais de diagnóstico especializados. | ✅ **Desenvolvido** |
| **Motor de Raciocínio (LLM)** | Utiliza o Ollama Cloud para analisar o problema e propor uma solução. | ⏳ Em Integração |
| **Módulo de Ação** | Executa o comando de solução determinado pelo LLM (e.g., `restart service X`). | ❌ Pendente |

---

### Próximos Passos (Roadmap)

1.  **Integração do Ollama Cloud:** Estabelecer a comunicação com o *endpoint* do Ollama e criar os *prompts* iniciais para diagnóstico.
2.  **Desenvolvimento do Módulo de Coleta de Dados:** Criar a interface para ingestão de dados de *logs* de erro simulados.
3.  **Desenvolvimento do Módulo de Ação:** Implementar um mecanismo seguro para traduzir a decisão do LLM em um comando executável (e.g., um *wrapper* seguro para APIs de gerenciamento de serviço).
4.  **Testes em Ambiente Simulado (MVP):** Validar o ciclo completo do ASS em um cenário de falha controlada.
