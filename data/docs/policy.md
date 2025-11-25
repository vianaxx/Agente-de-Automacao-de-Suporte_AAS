# Política de Suporte de Nível 1

## Serviço Relatórios Financeiros (report-svc)

1.  **Portas de Comunicação:** Usa a porta 8080 para comunicação interna.
2.  **Erros Comuns:** O erro "Connection Refused na porta 8080" geralmente indica que o serviço travou.
3.  **Ação Padrão:** Em caso de erro de conexão ou serviço travado, a **ação padrão obrigatória é reiniciar o serviço 'report-svc'**.

## Serviço Auth-Gateway (auth-gateway)

1.  **Portas de Comunicação:** Usa a porta 443.
2.  **Ação Padrão:** É um serviço crítico. **NUNCA reinicie o 'Auth-Gateway'** sem autorização de um Engenheiro N2.